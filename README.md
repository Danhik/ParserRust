# ParserRust
# ParserRust — Steam Market Parser

Парсер торговой площадки Steam для **Rust** (`appid=252490`).

Скрипт собирает **названия предметов и цены**, работает:
- без авторизации (без API-ключей)
- через список прокси
- в несколько потоков
- с повторной обработкой упавших страниц
- с конвертацией всех цен в **USD**

## 🚀 Возможности

- 🔄 Многопоточная загрузка страниц
- 🌐 HTTP / SOCKS5 прокси
- ♻️ Возврат упавших страниц в очередь (429 / 403)
- 🔁 Повторные проходы по списку прокси (`--proxy-passes`)
- ⏱️ Глобальный rate limit (`--global-interval`)
- 🔧 Режимы `--append` и `--repair`
- 🔤 Сортировка: `name`, `price`, `quantity`
- 💱 Конвертация EUR / GBP / CHF → USD
- 📊 Сохранение в Excel (`.xlsx`)
- 🧠 Дедупликация по URL предмета
- 📈 Логи прогресса и verbose-режим

## 📦 Требования

- Python **3.9+**
- Зависимости:
pip install requests beautifulsoup4 lxml openpyxl

## 🌐 Формат прокси

Файл `proxies.txt`, один прокси на строку:
ip:port:user:pass

## ▶️ Примеры запуска

Обычный запуск:
`python steam_market_parser.py --proxies proxies.txt --out rust.xlsx --appid 252490`

С логами и прогрессом:
`python steam_market_parser.py --proxies proxies.txt --out rust.xlsx --appid 252490 --verbose --progress-every 10`

Repair + append:
`python steam_market_parser.py --proxies proxies.txt --out rust.xlsx --append --repair --total-count 5026 --appid 252490`

Несколько проходов по прокси:
`python steam_market_parser.py --proxies proxies.txt --out rust.xlsx --appid 252490 --proxy-passes 3`

Большой запуск:
`python steam_market_parser.py --proxies proxies.txt --out rust.xlsx --append --repair --total-count 5026 --appid 252490 --workers 
6 --global-interval 1.2 --max-req-per-proxy 10 --proxy-passes 10 --progress-every 10 --verbose --task-retries 10`

## 🔁 Проходы по прокси

По умолчанию каждый прокси используется один раз.
Если прокси закончились, воркеры завершают работу.

Параметр:
--proxy-passes N

Позволяет **пройти по списку прокси N раз подряд**.
Это полезно, если прокси мало, но страниц много.

Пример:
`python steam_market_parser.py --proxies proxies.txt --appid 252490 --proxy-passes 5`

## ⚙️ Основные параметры

- `--proxies` — путь к proxies.txt
- `--out` — выходной Excel файл
- `--appid` — Steam appid
- `--workers` — количество потоков
- `--count` — предметов за один запрос
- `--timeout` — таймаут HTTP-запроса (сек)
- `--delay` — задержка между запросами в воркере
- `--global-interval` — глобальный лимит запросов (на все потоки)
- `--max-req-per-proxy` — максимум запросов на один прокси
- `--proxy-passes` — количество проходов по списку прокси
- `--append` — дописывать в существующий файл
- `--repair` — докачивать недостающие страницы
- `--task-retries` — сколько раз возвращать страницу в очередь
- `--sort-column` — поле сортировки (name / price / quantity)
- `--sort-dir` — направление сортировки (asc / desc)
- `--progress-every` — вывод прогресса каждые N секунд
- `--verbose` — подробные логи

# SwapGG Selenium Parser (Rust)

Парсер торговой площадки **swap.gg** для предметов **Rust**  
Работает через **реальный браузер (Selenium)** и забирает данные **из Network (API)** во время скролла.

Парсер:
- открывает страницу trade,
- переключает категорию на **Rust**,
- скроллит список предметов,
- перехватывает ответы API `/api/inventory/site`,
- сохраняет предметы и цены в **Excel (.xlsx)**.

---

## 🚀 Возможности

- 🧭 Работа как реальный пользователь (через браузер)
- 🛡️ Обход Cloudflare (без прямых запросов)
- 📡 Сбор данных напрямую из Network (JSON)
- 🧾 Корректные имена и цены (без HTML-парсинга)
- 📊 Сохранение в Excel
- 🔁 Скролл до конца списка
- 🪵 Подробные логи (`--verbose`)

---

## 📦 Требования

- Python **3.9+**
- Google Chrome (актуальная версия)

### Запуск
``` 
python swapgg_selenium_network_parser.py --out swap_rust.xlsx --verbose
```
### Установка зависимостей

```bash
pip install selenium selenium-wire openpyxl
pip uninstall blinker -y
pip install blinker==1.6.2
```

# SwapGG User Inventory Selenium Parser (Rust)

Парсер личного инвентаря Steam (Rust) на сайте swap.gg.
Работает через реальный браузер (Selenium) и забирает данные из Network (API) после ручной авторизации.

Парсер:

- открывает страницу trade,
- ждёт ручную авторизацию Steam,
- переключает категорию на Rust,
- скроллит левый инвентарь пользователя,
- перехватывает ответы /api/inventory/user,
- сохраняет доступные предметы в Excel (.xlsx).

---
## 🚀 Возможности

- 🧭 Работа как реальный пользователь (через Chrome)

- 🔐 Ручная авторизация Steam (1 раз)

- 🍪 Сохранение сессии через Chrome profile

- 📡 Сбор данных из Network (JSON)

- 🚫 Фильтрация недоступных предметов (conditions)

- 📊 Экспорт в Excel

-   Подробные логи (--verbose)

## 📦 Требования

- Python 3.9+

- Google Chrome (актуальная версия)

## Установка зависимостей
```bash
pip install selenium selenium-wire openpyxl
pip uninstall blinker -y
pip install blinker==1.6.2
```
## ▶️ Первый запуск (обязательно)

Создай отдельную папку для профиля Chrome, например:

```
C:\ChromeProfiles\swapgg_user
```

Запусти скрипт:
```
python swapgg_user_inventory_parser.py --out user_rust.xlsx --verbose --user-data-dir "C:\ChromeProfiles\swapgg_user"
```

Что сделать вручную в открывшемся браузере:

- зайти на swap.gg

- нажать Войти через Steam

- авторизоваться в Steam

- убедиться, что виден твой инвентарь

- вернуться в консоль и подтвердить продолжение

- После этого куки и сессия сохраняются.

🔁 Повторные запуски
```
python swapgg_user_inventory_parser.py --out user_rust.xlsx --verbose --user-data-dir "C:\ChromeProfiles\swapgg_user"
```

Авторизация уже сохранена, входить заново не нужно.

📄 Excel

В файл попадают только доступные для обмена предметы.

# Steam Price Overview Parser (Rust)

Парсер цен с использованием API **priceoverview**.

## 🚀 Возможности
- ⚡ **Высокая скорость** (поддержка 100+ потоков).
- 🔄 **Ротация прокси** и обработка Rate Limit (429).
- ⏯️ **Resume Support**: можно прерывать и продолжать работу, скрипт пропустит уже обработанные предметы.
- 💰 Валюта **USD** по умолчанию.

## ▶️ Запуск

Базовый пример (быстрый, 100 потоков) с интервалом 0.08 секунд:
```bash
python steam_price_overview_parser.py --names names.txt --proxies proxies.txt --out result.xlsx --workers 100 --global-interval 0.08
```

## ⚙️ Параметры
- `--names` — файл с названиями предметов (построчно).
- `--proxies` — список прокси.
- `--out` — выходной файл.
- `--workers` — число потоков (ставим 100, если много прокси).
- `--global-interval` — задержка между запросами (0.05-0.1 для скорости).

---

# Парсеры Skinswap.com

Для сайта Skinswap.com создано два парсера: для сбора общего инвентаря сайта и для парсинга личного инвентаря авторизованного пользователя.

## 1. Парсер сайта Skinswap (`skinswap_parser.py`)

Парсит весь доступный инвентарь на самом сайте (обменник).
Работает **без авторизации** на чистых `requests` с обходом защиты Cloudflare.

**Особенности:**
- ⚡ Многопоточный сбор (`--workers`).
- 🛡️ Автоматический обход Cloudflare с помощью `OPTIONS` preflight запросов.
- 🔄 Поддержка и умная ротация прокси (каждый поток держит прокси до первого бана/ошибки).

**Пример запуска:**
```bash
python skinswap_parser.py --workers 5 --proxies proxies.txt --out skinswap_items.xlsx --verbose
```
*По умолчанию парсит предметы Rust (`--appid 252490`). Для CS:GO добавьте `--appid 730`.*

## 2. Парсер личного инвентаря Skinswap (`skinswap_user_inventory_parser.py`)

Парсит **ваш личный инвентарь**, который видит сайт Skinswap.
Использует **гибридный подход**: Selenium для первичной авторизации + быстрые `requests` для сбора.

**Особенности:**
- 🔐 **Ручная авторизация Steam (только 1-й раз)**: При первом запуске или когда протух токен, скрипт на 5 минут откроет браузер. Как только вы войдете через Steam, скрипт "поймает" токен, сохранит его в `skinswap_session_<имя>.json` и сам закроет браузер.
- ⚡ **Быстрый парсинг**: После авторизации многопоточно и очень быстро скачивает все страницы личного инвентаря.
- 🎯 **Фильтрация `--accepted-only`**: Позволяет сохранять в Excel *только те вещи, которые можно передать сайту*. Структура файла будет такой же, как у парсера сайта (Name, Price, Limit, Count). Если запустить без этого ключа — в Excel попадут вообще все ваши вещи, но добавятся колонки с причиной отказа (Reason) и статусом (Tradable).
- 👥 **Мультиаккаунтность `--user-profile`**: По умолчанию сессия сохраняется в `skinswap_session_default.json`. Если вы собираете данные с нескольких аккаунтов, передайте уникальное имя профиля (например: `--user-profile main`, `--user-profile bot1`).

**Пример запуска (первый запуск с авторизацией или повторный быстрый запуск):**
```bash
# Базовый запуск (Все вещи + причины отказов)
python skinswap_user_inventory_parser.py --workers 3 --verbose

# Запуск для конкретного аккаунта с фильтрацией принимаемых вещей
python skinswap_user_inventory_parser.py --workers 3 --user-profile bot1 --accepted-only --verbose 

# Запуск только для "принимаемых" вещей (строгий формат вывода)
python skinswap_user_inventory_parser.py --workers 3 --accepted-only --verbose
```