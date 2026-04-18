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

## 1. Парсер сайта Skinswap — браузерный (`skinswap_browser_parser.py`) ✅ Рекомендуется

Парсит весь доступный инвентарь сайта через **реальный браузер (Playwright)**.
Cloudflare проходится автоматически. Данные перехватываются из Network (API JSON) во время скролла.

**Особенности:**
- 🧭 Работает как реальный пользователь — Cloudflare не блокирует
- 🛡️ Профиль Chrome сохраняется (`./chrome_profile`) — CF-куки между запусками живут
- 📡 Перехват ответов `api.skinswap.com/api/site/inventory` прямо в браузере
- 🔄 Автоматический скролл инвентаря до конца списка
- 📊 Сохранение в Excel (Name, Price, Overstock Limit, Overstock Count)
- 🪵 Подробные логи (`--verbose`)

**Установка зависимостей:**
```bash
pip install playwright openpyxl
playwright install chromium
```

**Запуск:**
```bash
# Обычный запуск (Rust, ~1600+ предметов)
python skinswap_browser_parser.py --out skinswap_items.xlsx

# С подробными логами
python skinswap_browser_parser.py --out skinswap_items.xlsx --verbose
```

**Параметры:**
- `--out` — выходной файл Excel (по умолчанию `skinswap_items.xlsx`)
- `--scroll-pause` — пауза между скроллами (сек, по умолчанию `1.0`)
- `--stable-rounds` — остановка после N шагов без новых предметов (по умолчанию `5`)
- `--init-wait` — ожидание после загрузки страницы (сек, по умолчанию `3.0`)
- `--user-data-dir` — путь к профилю Chrome (по умолчанию `./chrome_profile`)
- `--headless` — запуск без видимого окна (не рекомендуется)
- `--max-items` — лимит предметов (0 = без лимита)
- `--verbose` — подробные логи

---

## 2. Парсер сайта Skinswap — API (`skinswap_parser.py`) ⚠️ Устарел

> ⚠️ **Внимание:** Этот парсер работает напрямую через `requests` и подвержен блокировкам Cloudflare (402 ошибки). Рекомендуется использовать `skinswap_browser_parser.py`.

Парсит инвентарь через прямые HTTP-запросы к API с обходом Cloudflare через `curl_cffi`.

## 3. Парсер личного инвентаря Skinswap (`skinswap_user_inventory_parser.py`)

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

---

# Парсеры Tradeit.gg

Для сайта Tradeit.gg добавлены два парсера: для общего инвентаря сайта и для парсинга личного инвентаря авторизованного пользователя.

## 1. Парсер сайта Tradeit (`tradeit_parser.py`)

Парсит весь доступный инвентарь сайта через API `tradeit.gg/api/v2/inventory/data` (без авторизации).

**Особенности:**
- ⚡ Многопоточный сбор (`--workers`)
- 🌐 Поддержка прокси + ротация при ошибках (`--proxies`, `--proxy-passes`)
- 🔁 Повторы запросов при сетевых ошибках и rate limit (`--task-retries`)
- 🧠 Сбор до конца инвентаря (остановка только на пустой странице)
- 📊 Экспорт в Excel только нужных колонок: `Name`, `Price (Trade)`

**Примеры запуска:**
```bash
# Базовый запуск (Rust)
python tradeit_parser.py --game-id 252490 --out tradeit_items.xlsx

# Быстрый запуск с прокси и логами
python tradeit_parser.py --workers 10 --proxies proxies.txt --out tradeit_items.xlsx --verbose
```

**Параметры:**
- `--game-id` — ID игры (`252490` Rust, `730` CS:GO)
- `--sort` — сортировка (`Popularity`, `Price`, `PriceReversed`, `Name`)
- `--limit` — размер страницы API (по умолчанию `160`)
- `--workers` — количество потоков
- `--task-retries` — число попыток на страницу
- `--proxies` — файл с прокси
- `--proxy-passes` — количество проходов по списку прокси
- `--timeout` — таймаут запроса (сек)
- `--out` — выходной Excel файл
- `--verbose` — подробные логи

## 2. Парсер личного инвентаря Tradeit (`tradeit_user_inventory_parser.py`)

Парсит **ваш личный инвентарь** на Tradeit через API `tradeit.gg/api/v2/inventory/my/data`.
Использует **гибридный подход**: Selenium/UC для первичной авторизации + `requests` для последующих запусков.

**Особенности:**
- 🔐 **Ручная авторизация Steam (только 1-й раз)**: при первом запуске открывается браузер, после входа сессия сохраняется в `tradeit_session_<имя>.json`
- ⚡ **Быстрые повторные запуски**: если сессия валидна, браузер не запускается
- 👥 **Мультиаккаунтность `--user-profile`**: отдельный файл сессии под каждый аккаунт
- ✅ Автоматическая проверка валидности сессии перед запросом
- 📊 Экспорт в Excel: `Name`, `Price (Trade)`, `In Bot Now`, `Bot Max`

**Требования:**
- Python **3.9+**
- Google Chrome (актуальная версия)
- Зависимости:
```bash
pip install requests openpyxl undetected-chromedriver selenium
```

**Примеры запуска:**
```bash
# Первый запуск (Rust): откроется браузер для входа через Steam
python tradeit_user_inventory_parser.py --game-id 252490 --user-profile main --verbose

# Повторный запуск (сессия уже сохранена)
python tradeit_user_inventory_parser.py --game-id 252490 --user-profile main --out tradeit_user_items.xlsx

# Запуск для CS:GO
python tradeit_user_inventory_parser.py --game-id 730 --user-profile cs --out tradeit_cs_user.xlsx --verbose
```

**Параметры:**
- `--game-id` — ID игры (`252490` Rust, `730` CS:GO)
- `--out` — выходной Excel файл
- `--user-profile` — имя профиля сессии (`tradeit_session_<имя>.json`)
- `--timeout` — таймаут запроса (сек)
- `--task-retries` — количество попыток API-запроса
- `--session-max-age-hours` — максимальный возраст локальной сессии в часах
- `--verbose` — подробные логи
