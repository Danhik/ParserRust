import os
import sys
import time
import argparse
import random
import threading
import queue
import concurrent.futures
from typing import List, Dict, Any, Optional

import requests
from openpyxl import Workbook

# -------------------------------------------------------------
# Configuration & Utils
# -------------------------------------------------------------

def load_proxies(filepath: str) -> List[str]:
    """Загрузка прокси из файла вида ip:port:user:pass"""
    proxies = []
    if not os.path.exists(filepath):
        print(f"Файл {filepath} не найден. Работа без прокси.")
        return proxies

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            proxies.append(line)
    return proxies

def format_proxy(proxy_str: str, scheme: str = "http") -> dict:
    if not proxy_str:
        return {}
    
    parts = proxy_str.split(":")
    if len(parts) == 4:
        ip, port, user, pwd = parts
        url = f"{scheme}://{user}:{pwd}@{ip}:{port}"
    elif len(parts) == 2:
        ip, port = parts
        url = f"{scheme}://{ip}:{port}"
    else:
        url = f"{scheme}://{proxy_str}"

    return {"http": url, "https": url}

def get_random_user_agent() -> str:
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0"

def format_price(cents: int) -> str:
    dollars = cents / 100.0
    return f"{dollars:.2f}".replace(".", ",")

# -------------------------------------------------------------
# Proxy Pool
# -------------------------------------------------------------

class ProxyPool:
    def __init__(self, proxies: List[str], max_passes: int = 1):
        self._proxies = proxies.copy()
        self._max_passes = max_passes
        self._current_pass = 1
        self._index = 0
        self._lock = threading.Lock()

    def acquire_next(self) -> Optional[str]:
        if not self._proxies:
            return None
            
        with self._lock:
            if self._current_pass > self._max_passes:
                return None
            
            p = self._proxies[self._index]
            self._index += 1
            
            if self._index >= len(self._proxies):
                self._index = 0
                self._current_pass += 1
                
            return p

# -------------------------------------------------------------
# API Worker Logic
# -------------------------------------------------------------

def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": get_random_user_agent(),
        "Origin": "https://skinswap.com",
        "Referer": "https://skinswap.com/",
        "Accept": "*/*",
        "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
        "x-requested-with": "SkinSwap v3.1.5",
        "x-user-validate": "f4e6656e8ae4f4efdf2552cbee8a8f70" 
    })
    return session

def worker_task(
    offset: int, 
    limit: int, 
    appid: int, 
    proxy_pool: ProxyPool, 
    proxy_scheme: str, 
    max_retries: int,
    timeout: int,
    verbose: bool
) -> Optional[List[Dict[str, Any]]]:
    
    url = f"https://api.skinswap.com/api/site/inventory?offset={offset}&limit={limit}&appid={appid}&sort=price-desc&priceType=trade&priceMin=0&priceMax=5000000"
    
    session = create_session()
    current_proxy_str = proxy_pool.acquire_next()
    
    for attempt in range(1, max_retries + 1):
        if current_proxy_str is None:
            if verbose: print(f"[Offset {offset}] Прокси закончились (попытка {attempt}).")
            return None
            
        proxy_dict = format_proxy(current_proxy_str, proxy_scheme)
        proxy_log = current_proxy_str.split(":")[0] if current_proxy_str else "Direct"
        
        if verbose:
            print(f"[API] Offset: {offset} | Попытка {attempt}/{max_retries} через {proxy_log}")
            
        try:
            # OPTIONS preflight для Cloudflare
            session.options(url, proxies=proxy_dict, timeout=timeout)
            
            # Основной запрос GET
            resp = session.get(url, proxies=proxy_dict, timeout=timeout)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get("success"):
                    return data.get("data", [])
                else:
                    if verbose: print(f"      [Ошибка] success=false на offset {offset}")
            elif resp.status_code in [403, 429, 503]:
                if verbose: print(f"      [Ban/RateLimit {resp.status_code}] через {proxy_log}. Меняем прокси.")
                # Бан. Меняем прокси, пересоздаем сессию (очистка кук)
                current_proxy_str = proxy_pool.acquire_next()
                session = create_session()
                time.sleep(1)
                continue
            else:
                if verbose: print(f"      [Ошибка] Код {resp.status_code} на offset {offset}")
                
        except requests.exceptions.RequestException as e:
            if verbose: print(f"      [Network Error] {type(e).__name__} через {proxy_log}. Меняем прокси.")
            current_proxy_str = proxy_pool.acquire_next()
            session = create_session()
            time.sleep(1)
            continue
            
        # Не критичная ошибка (напр 500 сервера, не связанная с прокси), пробуем еще раз
        time.sleep(2)
        
    print(f"Не удалось получить данные для offset={offset} после {max_retries} попыток.")
    return None

# -------------------------------------------------------------
# Main Orchestrator
# -------------------------------------------------------------

def _save_workbook_safe(wb: Workbook, path: str, retries: int = 5):
    for i in range(retries):
        try:
            wb.save(path)
            return
        except PermissionError:
            print(f"[Writer] Ошибка доступа к файлу {path} (возможно открыт?). Попытка {i+1}/{retries} через 5 сек...")
            time.sleep(5)
        except Exception as e:
            print(f"[Writer] Ошибка сохранения {path}: {e}")
            return
    print(f"[Writer] Не удалось сохранить {path} после {retries} попыток. Данные могут быть потеряны.")


def save_to_excel(items: List[Dict[str, Any]], out_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Skinswap Items"
    
    headers = ["Name", "Price (Trade)", "Overstock Limit", "Overstock Count"]
    ws.append(headers)
    
    # Чтобы не было дубликатов из-за сдвигов инвентаря
    seen_ids = set()
    saved = 0
    
    for item in items:
        item_id = item.get("id")
        if item_id and item_id in seen_ids:
            continue
        if item_id:
            seen_ids.add(item_id)
            
        name = item.get("name", "Unknown")
        price_cents = item.get("price", {}).get("trade")
        price_str = format_price(price_cents) if price_cents is not None else ""
        
        overstock = item.get("overstock", {})
        limit = overstock.get("limit", "")
        count = overstock.get("count", "")
        
        ws.append([name, price_str, limit, count])
        saved += 1
        
    _save_workbook_safe(wb, out_path)
    print(f"Сохранено {saved} (уникальных) предметов в файл {out_path}.")

def main():
    ap = argparse.ArgumentParser(description="Парсер инвентаря Skinswap (многопоточный, без авторизации).")
    ap.add_argument("--appid", type=int, default=252490, help="ID игры (по умолчанию 252490 - Rust)")
    ap.add_argument("--proxies", default="proxies.txt", help="Путь к файлу с прокси")
    ap.add_argument("--proxy-scheme", default="http", help="Схема прокси (http/socks5)")
    ap.add_argument("--workers", type=int, default=5, help="Количество потоков")
    ap.add_argument("--proxy-passes", type=int, default=10, help="Количество проходов по списку прокси")
    ap.add_argument("--task-retries", type=int, default=5, help="Количество попыток загрузить одну страницу")
    ap.add_argument("--limit", type=int, default=50, help="Количество предметов на страницу (API limit)")
    ap.add_argument("--max-pages", type=int, default=1000, help="Жесткий лимит страниц, чтобы избежать бесконечного цикла, если API багует")
    ap.add_argument("--out", default="skinswap_items.xlsx", help="Имя выходного файла")
    ap.add_argument("--timeout", type=int, default=15, help="Таймаут запросов")
    ap.add_argument("--verbose", action="store_true", help="Включить подробные логи API")

    args = ap.parse_args()

    proxies = load_proxies(args.proxies)
    if not proxies:
        # Добавим заглушку для работы без прокси ("Direct")
        proxies = [""]
        args.proxy_passes = 1 # Без прокси нет смысла в циклах
    else:
        print(f"Загружено {len(proxies)} прокси.")
        
    proxy_pool = ProxyPool(proxies, max_passes=args.proxy_passes)
    
    print(f"Начинаем сбор инвентаря Skinswap [AppID: {args.appid} | Потоков: {args.workers}]...")
    
    results_by_offset = {}
    
    # Skinswap не возвращает totalCount, поэтому мы вынуждены запрашивать страницы до тех пор, пока не получим пустой ответ.
    # Чтобы использовать многопоточность для неизвестного количества страниц, мы будем закидывать задачи пакетами
    # Начнем с первых N потоков.
    
    offset_queue = queue.Queue()
    for i in range(args.workers): # Изначально закидываем по количеству воркеров
        offset_queue.put(i * args.limit)
    
    highest_offset_queued = (args.workers - 1) * args.limit
    
    active_tasks = 0
    pages_processed = 0
    end_reached = False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        
        # Запуск начальных тасок
        while not offset_queue.empty():
            offset = offset_queue.get()
            fut = executor.submit(
                worker_task, 
                offset, args.limit, args.appid, proxy_pool, args.proxy_scheme, args.task_retries, args.timeout, args.verbose
            )
            futures[fut] = offset
            active_tasks += 1
            
        while active_tasks > 0:
            # Ожидаем завершения хотя бы одной задачи
            done, _ = concurrent.futures.wait(futures.keys(), return_when=concurrent.futures.FIRST_COMPLETED)
            
            for fut in done:
                offset = futures.pop(fut)
                active_tasks -= 1
                pages_processed += 1
                
                try:
                    items = fut.result()
                except Exception as e:
                    print(f"Критическая ошибка в потоке offset={offset}: {e}")
                    items = None
                    
                if items is None:
                    # Ошибка после всех попыток
                    pass
                elif len(items) == 0:
                    # Достигли конца
                    end_reached = True
                else:
                    results_by_offset[offset] = items
                    current_total = sum(len(v) for v in results_by_offset.values())
                    print(f"[Прогресс] Страниц проверено: {pages_processed}. Собрано предметов: {current_total}")
                    
                    # Если вернули полную страницу, и конец еще не достигнут, добавляем новые offset в очередь
                    if len(items) >= args.limit and not end_reached and pages_processed < args.max_pages:
                        highest_offset_queued += args.limit
                        
                        new_fut = executor.submit(
                            worker_task, 
                            highest_offset_queued, args.limit, args.appid, proxy_pool, args.proxy_scheme, args.task_retries, args.timeout, args.verbose
                        )
                        futures[new_fut] = highest_offset_queued
                        active_tasks += 1
                        
            # Небольшая пауза главного потока
            time.sleep(0.1)

    all_items = []
    for off in sorted(results_by_offset.keys()):
        all_items.extend(results_by_offset[off])

    print(f"Сбор завершен. Получено {len(all_items)} предметов.")
    if all_items:
        save_to_excel(all_items, args.out)

if __name__ == "__main__":
    main()
