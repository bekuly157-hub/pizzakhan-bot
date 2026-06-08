#!/usr/bin/env python3
"""Пицца Хан — Telegram Bot v2"""

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime, os

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8827374656:AAFbMRgbnic89nWV5we8nNTsHs2icx75D_A")
MANAGER_ID = 8770900575

bot = telebot.TeleBot(TOKEN)

# ── МИНИМАЛЬНЫЕ ЗАПАСЫ ───────────────────────────────────────────────────────
STOCK_MINS = {
    # Курица
    "Курица для донера (кг)":        5,
    "Курица для донера на станции":  3,
    "Курица для пиццы (кг)":         5,
    "Курица для пиццы на станции":   3,
    # Бургер
    "Булочки для бургера (шт)":      40,
    "Котлеты куриные (шт)":          20,
    # Тесто
    "Тесто малое (шт)":              30,
    "Тесто среднее (шт)":            30,
    "Тесто большое (шт)":            25,
    "Тесто малое запас":             50,
    "Тесто среднее запас":           50,
    "Тесто большое запас":           25,
    # Соусы
    "Пицца-соус на станции (л)":     3,
    "Пицца-соус запас (л)":          5,
    # Лаваш
    "Лаваш (шт)":                    100,
    # Сыр
    "Сыр натёртый (кг)":             15,
    "Сыр запас (кг)":                15,
    # Фарш
    "Фарш для пиццы (кг)":           2,
    # Фри
    "Фри картофель (кг)":            10,
}

# ── ЧЕКЛИСТЫ ─────────────────────────────────────────────────────────────────
CASHIER_OPEN = [
    "💵 Проверить деньги от ночной смены — пересчитать и сфотографировать",
    "💵 Зафиксировать сумму в кассе (внесение в программу)",
    "🖨 Включить кассовый аппарат, проверить чековую ленту",
    "☕ Включить кофемашину, проверить холдер — чистый?",
    "🫖 Включить чайник, налить воду",
    "🧊 Проверить ледогенератор — есть лёд?",
    "🧹 Протереть барную стойку",
    "🍯 Сиропы — протёрты, на месте, не липкие",
    "🥫 Налить кетчуп в соусницы, проверить чистоту соусниц",
    "📦 Посчитать упаковку (крафт пакеты мал/ср/бол, фри, донер, стаканы)",
    "🥤 Посчитать все соки по позициям, сравнить с остатком ночи",
    "📺 Включить телевизор",
    "📱 Зарядить рабочий телефон",
    "📱 Включить все агрегаторы (Яндекс, Wolt, Kaspi)",
    "⛔ Спросить кухню — что в стопе? Обновить в агрегаторах",
    "🧺 Проверить посуду — чистая/грязная",
    "🚽 Проверить туалет — чистый, есть бумага",
    "🌡 Проверить холодильники — работают?",
    "👕 Форма надета, внешний вид опрятный",
    "⚠️ Есть замечания к ночной смене? Сфотографировать и отправить менеджеру",
]

CASHIER_CLOSE = [
    "💵 Пересчитать деньги в кассе, сфотографировать",
    "💵 Закрыть кассу в программе, передать по инструкции",
    "🥤 Посчитать все соки — записать остаток в бот",
    "📦 Посчитать упаковку — записать остаток в бот",
    "🛒 Отметить что нужно заказать на завтра",
    "☕ Выключить кофемашину, вымыть холдер",
    "🫖 Выключить чайник",
    "📺 Выключить телевизор",
    "📱 Выключить или поставить агрегаторы в стоп",
    "📱 Зарядить телефон для ночной смены",
    "❄️ Проверить кондиционер (летом выключить или оставить)",
    "🧹 Протереть барную стойку и сиропы",
    "🧺 Вымыть посуду и стаканы",
    "🗑 Вынести мусор",
    "🔑 Передать ключ ночной смене",
    "📝 Рассказать ночной смене что было за день",
    "⚠️ Есть замечания? Сфотографировать и отправить менеджеру",
]

KITCHEN_OPEN = [
    "🔌 Включить печь (эко-режим до первых заказов)",
    "🔌 Включить фритюр, проверить температуру масла",
    "🔌 Включить турбус и освещение",
    "🍕 Тесто готово — малое/среднее/большое (проверить количество)",
    "🍅 Пицца-соус готов (из помидоров)",
    "🧀 Сыр натёртый на станции (мин 15 кг)",
    "🥩 Фарш отмерен порциями 60г для пиццы (мин 2 кг)",
    "🌭 Колбаса нарезана",
    "🍍 Ананас нарезан",
    "🥗 Овощи нарезаны (помидор, перец, грибы, айсберг)",
    "🍗 Курица для донера разморожена и запечена",
    "🍗 Курица нарезана тонко для донера",
    "🐴 Конина сварена и нарезана",
    "🍔 Котлеты куриные готовы (150г × мин 20 шт)",
    "🍞 Булочки для бургера в наличии (мин 40 шт)",
    "🌯 Лаваш в наличии (мин 100 шт)",
    "🧀 Проверить запас сыра! Если меньше 30 кг — срочно сообщить менеджеру",
    "🍟 Фри в наличии (мин 10 кг)",
    "📊 Проверить все остатки и внести в бот",
]

KITCHEN_CLOSE = [
    "🍗 Вытащить курицу на разморозку для утренней смены",
    "🧹 Убрать все станции",
    "🧊 Накрыть и убрать заготовки в холодильник",
    "🛢 Проверить масло фритюра — нужна замена?",
    "🔌 Выключить печь и фритюр",
    "🔌 Выключить всё оборудование",
    "📊 Записать остатки заготовок в бот",
    "⚠️ Передать смене что готово, что нет",
    "🧹 Убрать рабочее место",
]

PREP_AYSHA = [
    "🍗 Промыть курицу (10 кг)",
    "🍗 Замариновать курицу (специи + соус)",
    "🍗 Расфасовать по 1.5–2 кг, убрать в морозилку",
    "🐴 Сварить/потомить конину, заморозить, нарезать",
    "🍔 Приготовить котлеты куриные (150г)",
    "🌿 Замешать чикен-смесь (мука + крахмал + специи)",
    "🍅 Приготовить пицца-соус из помидоров",
    "🥗 Приготовить соус ранч",
    "🥗 Приготовить красный соус для донера",
    "🥗 Приготовить бургер-соус",
    "🌭 Нарезать колбасу",
    "🧀 Нарезать фитексу",
    "📊 Обновить остатки в боте",
]

PREP_LEYLA = [
    "🌾 Проверить запас муки и тесто-смеси",
    "🌾 Замесить тесто (по расписанию — каждый день или через день)",
    "🍕 Скатать шары — малые (мин 50 шт)",
    "🍕 Скатать шары — средние (мин 50 шт)",
    "🍕 Скатать шары — большие (мин 25 шт)",
    "❄️ Убрать запас в холодильник",
    "📊 Обновить количество теста в боте",
    "⚠️ Если муки мало — сразу сообщить менеджеру",
]

ACCOUNTANT = [
    "📥 Внести все приходы от поставщиков во Frontpad",
    "📊 Проверить движение сырья в Frontpad",
    "📊 Сверить остатки в Frontpad с фактическими",
    "⚠️ Если есть расхождения — сообщить менеджеру",
    "📝 Проверить накладные от поставщиков",
    "💰 Внести прочие расходы если есть",
]

DELIVERY_CHECK = [
    "📋 Проверить накладную у поставщика",
    "⚖️ Взвесить/пересчитать товар",
    "✅ Количество совпадает с заказом?",
    "📅 Проверить срок годности",
    "🌡 Проверить температуру (мясо, молочка)",
    "🏠 Убрать товар на место хранения",
    "📥 Внести приход во Frontpad",
    "📸 Сфотографировать накладную и отправить бухгалтеру",
]

# ── МИНИМАЛЬНЫЕ ОСТАТКИ — НАПИТКИ ────────────────────────────────────────────
DRINKS = [
    ("Кола 0.5л", 15),
    ("Кола 1л", 10),
    ("Кола 2л", 5),
    ("Фанта 1л", 8),
    ("Фьюсти 0.5л", 10),
    ("Фьюсти 1л", 5),
    ("Пико 1л", 8),
    ("Вода 0.5л", 10),
    ("Сарыагаш", 5),
    ("Детский сок", 10),
    ("Натуральный сок", 5),
    ("Спрайт 1л", 5),
]

PACKAGING = [
    ("Коробка пицца малая", 30),
    ("Коробка пицца средняя", 30),
    ("Коробка пицца большая", 15),
    ("Крафт пакет малый", 20),
    ("Крафт пакет средний", 20),
    ("Крафт пакет большой", 20),
    ("Упаковка фри", 40),
    ("Фри бумажная", 30),
    ("Донер упаковка", 20),
    ("Бургер бокс", 20),
    ("Стакан 350мл", 30),
    ("Крышки", 50),
    ("Соусница 30мл", 50),
    ("Салфетки (пачки)", 5),
    ("Трубочки", 50),
]

SUPPLIERS = [
    "🍗 Курица",
    "🥩 Фарш/Конина",
    "🌭 Колбаса",
    "🍞 Булочки",
    "🌯 Лаваш",
    "🧀 Сыр (из другого города)",
    "🥤 Напитки (Coca-Cola)",
    "📦 Упаковка",
    "🍯 Соусы/Майонез",
    "☕ Сиропы/Кофе",
    "🧹 Хозтовары",
    "❄️ Заморозка",
]

# ── СОСТОЯНИЕ ────────────────────────────────────────────────────────────────
user_state = {}
checklist_session = {}
stock_session = {}
stoplist = {
    "Пицца": True, "Донер": True, "Бургер": True,
    "Чикен": True, "Фри": True, "Кофе": True, "Наггетсы": True
}
returns_today = []
oil_log = {}
delivery_session = {}
low_stock_alerts = []

def get_state(uid): return user_state.get(uid, {})
def set_state(uid, **kw): user_state[uid] = kw
def now_str(): return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

def notify_manager(text):
    try: bot.send_message(MANAGER_ID, text, parse_mode="HTML")
    except: pass

# ── КЛАВИАТУРЫ ───────────────────────────────────────────────────────────────
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🧾 Кассир"), KeyboardButton("👨‍🍳 Кухня"))
    kb.row(KeyboardButton("🔪 Заготовщик (Айша)"), KeyboardButton("🥖 Тесто (Лейла)"))
    kb.row(KeyboardButton("📦 Приёмка товара"), KeyboardButton("📊 Бухгалтер"))
    kb.row(KeyboardButton("👁 Менеджер"))
    return kb

def cashier_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Открытие смены"), KeyboardButton("🔴 Закрытие смены"))
    kb.row(KeyboardButton("⛔ Стоп-лист"), KeyboardButton("🥤 Соки"))
    kb.row(KeyboardButton("📦 Упаковка"), KeyboardButton("⚠️ Возврат/Жалоба"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def kitchen_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Открытие кухни"), KeyboardButton("🔴 Закрытие кухни"))
    kb.row(KeyboardButton("🛢 Замена масла"), KeyboardButton("📊 Остатки кухни"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def prep_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Задачи заготовщика"))
    kb.row(KeyboardButton("📊 Остатки заготовок"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def leyla_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Задачи по тесту"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def accountant_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Задачи бухгалтера"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def manager_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("📊 Сводка дня"), KeyboardButton("⛔ Стоп-лист"))
    kb.row(KeyboardButton("⚠️ Возвраты"), KeyboardButton("🛢 Статус масла"))
    kb.row(KeyboardButton("⚠️ Низкие остатки"), KeyboardButton("🛒 Список закупа"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def yes_no_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Да"), KeyboardButton("❌ Нет"))
    return kb

def stoplist_kb():
    kb = InlineKeyboardMarkup()
    for item in stoplist:
        s = "✅" if stoplist[item] else "⛔"
        kb.add(InlineKeyboardButton(f"{s} {item}", callback_data=f"stop_{item}"))
    return kb

# ── СТАРТ ────────────────────────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start(msg):
    set_state(msg.from_user.id, step="main")
    bot.send_message(msg.chat.id,
        "👋 Добро пожаловать в систему <b>Пицца Хан</b>!\n\nВыберите свою роль:",
        reply_markup=main_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🏠 Главное меню")
def go_main(msg):
    set_state(msg.from_user.id, step="main")
    bot.send_message(msg.chat.id, "Главное меню:", reply_markup=main_menu())

# ── РОЛИ ─────────────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🧾 Кассир")
def cashier(msg):
    set_state(msg.from_user.id, step="cashier")
    bot.send_message(msg.chat.id, "🧾 <b>Режим кассира</b>", reply_markup=cashier_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👨‍🍳 Кухня")
def kitchen(msg):
    set_state(msg.from_user.id, step="kitchen")
    bot.send_message(msg.chat.id, "👨‍🍳 <b>Режим кухни</b>", reply_markup=kitchen_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🔪 Заготовщик (Айша)")
def prep(msg):
    set_state(msg.from_user.id, step="prep")
    bot.send_message(msg.chat.id, "🔪 <b>Заготовщик</b>", reply_markup=prep_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🥖 Тесто (Лейла)")
def leyla(msg):
    set_state(msg.from_user.id, step="leyla")
    bot.send_message(msg.chat.id, "🥖 <b>Заготовка теста</b>", reply_markup=leyla_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "📊 Бухгалтер")
def accountant(msg):
    set_state(msg.from_user.id, step="accountant")
    bot.send_message(msg.chat.id, "📊 <b>Бухгалтер</b>", reply_markup=accountant_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👁 Менеджер")
def manager(msg):
    if msg.from_user.id != MANAGER_ID:
        bot.send_message(msg.chat.id, "⛔ Только для менеджера.")
        return
    set_state(msg.from_user.id, step="manager")
    bot.send_message(msg.chat.id, "👁 <b>Менеджер</b>", reply_markup=manager_menu(), parse_mode="HTML")

# ── ЧЕКЛИСТЫ ─────────────────────────────────────────────────────────────────
def start_checklist(uid, cid, items, title, finish_msg, notify_title, back_menu):
    checklist_session[uid] = {
        "items": items, "idx": 0, "results": [],
        "title": title, "finish_msg": finish_msg,
        "notify_title": notify_title, "back_menu": back_menu
    }
    send_check_item(uid, cid)

def send_check_item(uid, cid):
    s = checklist_session[uid]
    idx = s["idx"]
    if idx >= len(s["items"]):
        finish_checklist(uid, cid)
        return
    total = len(s["items"])
    bot.send_message(cid,
        f"📋 <b>{s['title']}</b> [{idx+1}/{total}]\n\n{s['items'][idx]}\n\nВыполнено?",
        reply_markup=yes_no_kb(), parse_mode="HTML")
    set_state(uid, step="checklist")

def finish_checklist(uid, cid):
    s = checklist_session[uid]
    done = sum(1 for r in s["results"] if r)
    total = len(s["items"])
    failed = [s["items"][i] for i, r in enumerate(s["results"]) if not r]
    text = f"✅ <b>{s['finish_msg']}</b>\nВыполнено: {done}/{total}"
    if failed:
        text += "\n\n❌ Не выполнено:\n" + "\n".join(f"• {f}" for f in failed)
    bot.send_message(cid, text, parse_mode="HTML", reply_markup=s["back_menu"])
    notify_manager(
        f"📋 <b>{s['notify_title']}</b> — {now_str()}\n"
        f"Выполнено: {done}/{total}" +
        (("\n❌ Не выполнено:\n" + "\n".join(f"• {f}" for f in failed)) if failed else "")
    )

@bot.message_handler(func=lambda m: m.text == "✅ Открытие смены")
def open_shift(msg):
    start_checklist(msg.from_user.id, msg.chat.id, CASHIER_OPEN,
        "Открытие смены", "Смена открыта!", "Открытие смены", cashier_menu())

@bot.message_handler(func=lambda m: m.text == "🔴 Закрытие смены")
def close_shift(msg):
    start_checklist(msg.from_user.id, msg.chat.id, CASHIER_CLOSE,
        "Закрытие смены", "Смена закрыта!", "Закрытие смены", cashier_menu())

@bot.message_handler(func=lambda m: m.text == "✅ Открытие кухни")
def open_kitchen(msg):
    start_checklist(msg.from_user.id, msg.chat.id, KITCHEN_OPEN,
        "Открытие кухни", "Кухня готова!", "Открытие кухни", kitchen_menu())

@bot.message_handler(func=lambda m: m.text == "🔴 Закрытие кухни")
def close_kitchen(msg):
    start_checklist(msg.from_user.id, msg.chat.id, KITCHEN_CLOSE,
        "Закрытие кухни", "Кухня закрыта!", "Закрытие кухни", kitchen_menu())

@bot.message_handler(func=lambda m: m.text == "✅ Задачи заготовщика")
def prep_tasks(msg):
    start_checklist(msg.from_user.id, msg.chat.id, PREP_AYSHA,
        "Заготовщик (Айша)", "Заготовки выполнены!", "Заготовщик", prep_menu())

@bot.message_handler(func=lambda m: m.text == "✅ Задачи по тесту")
def leyla_tasks(msg):
    start_checklist(msg.from_user.id, msg.chat.id, PREP_LEYLA,
        "Тесто (Лейла)", "Тесто готово!", "Тесто Лейла", leyla_menu())

@bot.message_handler(func=lambda m: m.text == "✅ Задачи бухгалтера")
def accountant_tasks(msg):
    start_checklist(msg.from_user.id, msg.chat.id, ACCOUNTANT,
        "Бухгалтер", "Задачи выполнены!", "Бухгалтер", accountant_menu())

@bot.message_handler(func=lambda m: m.text in ["✅ Да", "❌ Нет"] and
    get_state(m.from_user.id).get("step") == "checklist")
def checklist_answer(msg):
    uid = msg.from_user.id
    s = checklist_session.get(uid)
    if not s: return
    s["results"].append(msg.text == "✅ Да")
    s["idx"] += 1
    send_check_item(uid, msg.chat.id)

# ── СТОП-ЛИСТ ────────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text in ["⛔ Стоп-лист", "⛔ Стоп-лист"])
def show_stoplist(msg):
    bot.send_message(msg.chat.id,
        "⛔ <b>Стоп-лист</b>\nНажми на позицию чтобы изменить:",
        reply_markup=stoplist_kb(), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def toggle_stop(call):
    item = call.data.replace("stop_", "")
    if item in stoplist:
        stoplist[item] = not stoplist[item]
        status = "✅ ЕСТЬ" if stoplist[item] else "⛔ СТОП"
        notify_manager(f"⛔ <b>Стоп-лист</b>\n{item}: {status}\n{now_str()}")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=stoplist_kb())
    bot.answer_callback_query(call.id)

# ── СОКИ (КАССИР) ────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🥤 Соки")
def start_drinks(msg):
    uid = msg.from_user.id
    stock_session[uid] = {"items": DRINKS, "idx": 0, "results": {}, "type": "drinks"}
    set_state(uid, step="stock_input")
    send_stock_item(uid, msg.chat.id)

# ── УПАКОВКА (КАССИР) ────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 Упаковка")
def start_packaging(msg):
    uid = msg.from_user.id
    stock_session[uid] = {"items": PACKAGING, "idx": 0, "results": {}, "type": "packaging"}
    set_state(uid, step="stock_input")
    send_stock_item(uid, msg.chat.id)

# ── ОСТАТКИ КУХНИ ────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📊 Остатки кухни")
def start_kitchen_stock(msg):
    uid = msg.from_user.id
    items = [(k, v) for k, v in STOCK_MINS.items()]
    stock_session[uid] = {"items": items, "idx": 0, "results": {}, "type": "kitchen"}
    set_state(uid, step="stock_input")
    send_stock_item(uid, msg.chat.id)

@bot.message_handler(func=lambda m: m.text == "📊 Остатки заготовок")
def start_prep_stock(msg):
    uid = msg.from_user.id
    items = [(k, v) for k, v in STOCK_MINS.items() if "Тесто" in k or "Курица" in k or "Соус" in k]
    stock_session[uid] = {"items": items, "idx": 0, "results": {}, "type": "prep"}
    set_state(uid, step="stock_input")
    send_stock_item(uid, msg.chat.id)

def send_stock_item(uid, cid):
    s = stock_session[uid]
    idx = s["idx"]
    items = s["items"]
    if idx >= len(items):
        finish_stock(uid, cid)
        return
    name, mn = items[idx]
    bot.send_message(cid,
        f"📊 [{idx+1}/{len(items)}]\n\n<b>{name}</b>\nМинимум: {mn}\n\nСколько сейчас?",
        parse_mode="HTML")

def finish_stock(uid, cid):
    s = stock_session[uid]
    low = [(name, qty, mn) for (name, mn), qty in zip(s["items"], s["results"].values()) if qty < mn]
    text = f"📊 <b>Остатки записаны</b> — {now_str()}\n\n"
    if low:
        text += "⚠️ МАЛО — нужно заказать:\n"
        for name, qty, mn in low:
            text += f"• {name}: {qty} (мин. {mn})\n"
        low_stock_alerts.extend(low)
    else:
        text += "✅ Всё в норме!"
    back = cashier_menu() if s["type"] in ["drinks", "packaging"] else kitchen_menu()
    bot.send_message(cid, text, parse_mode="HTML", reply_markup=back)
    if low:
        notify_text = f"⚠️ <b>НИЗКИЕ ОСТАТКИ</b> — {now_str()}\n\n"
        for name, qty, mn in low:
            notify_text += f"• {name}: {qty}/{mn}\n"
        notify_manager(notify_text)
    set_state(uid, step=s["type"])

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "stock_input")
def stock_input(msg):
    uid = msg.from_user.id
    s = stock_session.get(uid)
    if not s: return
    try:
        qty = float(msg.text.strip().replace(",", "."))
        name, mn = s["items"][s["idx"]]
        s["results"][name] = qty
        if qty < mn:
            bot.send_message(msg.chat.id, f"⚠️ Мало! Минимум {mn}. Записано: {qty}")
        s["idx"] += 1
        send_stock_item(uid, msg.chat.id)
    except:
        bot.send_message(msg.chat.id, "Введите число:")

# ── ВОЗВРАТ ───────────────────────────────────────────────────────────────────
RETURN_ITEMS = ["Пицца", "Донер", "Бургер", "Чикен", "Фри", "Наггетсы", "Напиток", "Другое"]
RETURN_REASONS = ["Мало сыра", "Мало мяса", "Долго ждали", "Забыли напиток",
                  "Холодная еда", "Ошибка в заказе", "Жалоба на качество", "Другое"]

@bot.message_handler(func=lambda m: m.text == "⚠️ Возврат/Жалоба")
def start_return(msg):
    uid = msg.from_user.id
    set_state(uid, step="return_item")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in RETURN_ITEMS: kb.add(KeyboardButton(item))
    kb.add(KeyboardButton("🏠 Главное меню"))
    bot.send_message(msg.chat.id, "⚠️ <b>Возврат/Жалоба</b>\nКакая позиция?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "return_item"
    and m.text in RETURN_ITEMS)
def return_item(msg):
    uid = msg.from_user.id
    set_state(uid, step="return_reason", return_item=msg.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for r in RETURN_REASONS: kb.add(KeyboardButton(r))
    bot.send_message(msg.chat.id, f"Позиция: <b>{msg.text}</b>\nПричина?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "return_reason"
    and m.text in RETURN_REASONS)
def return_reason(msg):
    uid = msg.from_user.id
    state = get_state(uid)
    item = state.get("return_item", "?")
    returns_today.append({"item": item, "reason": msg.text, "time": now_str(),
                          "who": msg.from_user.first_name})
    bot.send_message(msg.chat.id,
        f"✅ Зафиксировано:\n<b>{item}</b> — {msg.text}\n{now_str()}",
        reply_markup=cashier_menu(), parse_mode="HTML")
    notify_manager(f"⚠️ <b>ВОЗВРАТ</b>\n{item} — {msg.text}\n{now_str()}\nКассир: {msg.from_user.first_name}")
    set_state(uid, step="cashier")

# ── МАСЛО ────────────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛢 Замена масла")
def oil_change(msg):
    uid = msg.from_user.id
    set_state(uid, step="oil")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🛢 Фри (картофель)"), KeyboardButton("🛢 Чикен (курица)"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    bot.send_message(msg.chat.id, "🛢 Какой фритюр?", reply_markup=kb)

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "oil"
    and m.text in ["🛢 Фри (картофель)", "🛢 Чикен (курица)"])
def oil_changed(msg):
    uid = msg.from_user.id
    oil_log[msg.text] = now_str()
    bot.send_message(msg.chat.id,
        f"✅ Масло заменено!\n{msg.text}\n{now_str()}",
        reply_markup=kitchen_menu(), parse_mode="HTML")
    notify_manager(f"🛢 <b>Масло заменено</b>\n{msg.text}\n{now_str()}\nКто: {msg.from_user.first_name}")
    set_state(uid, step="kitchen")

# ── ПРИЁМКА ТОВАРА ────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 Приёмка товара")
def start_delivery(msg):
    uid = msg.from_user.id
    delivery_session[uid] = {"idx": 0, "results": [], "supplier": ""}
    set_state(uid, step="delivery_supplier")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for s in SUPPLIERS: kb.add(KeyboardButton(s))
    kb.add(KeyboardButton("🏠 Главное меню"))
    bot.send_message(msg.chat.id, "📦 <b>Приёмка товара</b>\nОт какого поставщика?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "delivery_supplier"
    and m.text in SUPPLIERS)
def delivery_supplier(msg):
    uid = msg.from_user.id
    delivery_session[uid]["supplier"] = msg.text
    set_state(uid, step="delivery_check")
    send_delivery_item(uid, msg.chat.id)

def send_delivery_item(uid, cid):
    s = delivery_session[uid]
    idx = s["idx"]
    if idx >= len(DELIVERY_CHECK):
        finish_delivery(uid, cid)
        return
    bot.send_message(cid,
        f"📦 <b>Приёмка</b> [{idx+1}/{len(DELIVERY_CHECK)}]\n\n{DELIVERY_CHECK[idx]}",
        reply_markup=yes_no_kb(), parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "delivery_check"
    and m.text in ["✅ Да", "❌ Нет"])
def delivery_answer(msg):
    uid = msg.from_user.id
    s = delivery_session.get(uid)
    if not s: return
    s["results"].append({"item": DELIVERY_CHECK[s["idx"]], "ok": msg.text == "✅ Да"})
    s["idx"] += 1
    send_delivery_item(uid, msg.chat.id)

def finish_delivery(uid, cid):
    s = delivery_session[uid]
    supplier = s["supplier"]
    failed = [r["item"] for r in s["results"] if not r["ok"]]
    text = f"✅ <b>Приёмка завершена</b>\nПоставщик: {supplier}\n{now_str()}"
    if failed:
        text += "\n\n❌ Проблемы:\n" + "\n".join(f"• {f}" for f in failed)
    bot.send_message(cid, text, reply_markup=main_menu(), parse_mode="HTML")
    notify_manager(
        f"📦 <b>ПРИЁМКА</b>\nПоставщик: {supplier}\n{now_str()}\n"
        + (("\n❌ Проблемы:\n" + "\n".join(f"• {f}" for f in failed)) if failed else "\n✅ Всё ок")
    )
    set_state(uid, step="main")

# ── МЕНЕДЖЕР ─────────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📊 Сводка дня")
def daily_summary(msg):
    if msg.from_user.id != MANAGER_ID: return
    stops = [k for k, v in stoplist.items() if not v]
    text = f"📊 <b>СВОДКА ПИЦЦА ХАН</b>\n{now_str()}\n\n"
    text += f"⛔ В стопе: {', '.join(stops) if stops else 'нет'}\n"
    text += f"⚠️ Возвратов: {len(returns_today)}\n"
    text += f"📉 Низких остатков: {len(low_stock_alerts)}\n"
    text += "\n🛢 Масло:\n"
    for fr, t in oil_log.items():
        text += f"  • {fr}: {t}\n"
    if not oil_log: text += "  • Не менялось\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.message_handler(func=lambda m: m.text == "⚠️ Возвраты")
def show_returns(msg):
    if msg.from_user.id != MANAGER_ID: return
    if not returns_today:
        bot.send_message(msg.chat.id, "✅ Возвратов нет.", reply_markup=manager_menu())
        return
    text = f"⚠️ <b>Возвраты ({len(returns_today)}):</b>\n\n"
    for r in returns_today:
        text += f"• {r['item']} — {r['reason']} ({r['time']})\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.message_handler(func=lambda m: m.text == "🛢 Статус масла")
def show_oil(msg):
    if msg.from_user.id != MANAGER_ID: return
    text = "🛢 <b>Статус масла:</b>\n\n"
    for fr in ["🛢 Фри (картофель)", "🛢 Чикен (курица)"]:
        t = oil_log.get(fr, "❌ Не менялось")
        text += f"• {fr}: {t}\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.message_handler(func=lambda m: m.text == "⚠️ Низкие остатки")
def show_low(msg):
    if msg.from_user.id != MANAGER_ID: return
    if not low_stock_alerts:
        bot.send_message(msg.chat.id, "✅ Все остатки в норме!", reply_markup=manager_menu())
        return
    text = f"⚠️ <b>Низкие остатки:</b>\n\n"
    for name, qty, mn in low_stock_alerts[-20:]:
        text += f"• {name}: {qty}/{mn}\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.message_handler(func=lambda m: m.text == "🛒 Список закупа")
def show_purchase(msg):
    if msg.from_user.id != MANAGER_ID: return
    if not low_stock_alerts:
        bot.send_message(msg.chat.id, "✅ Заказывать ничего не нужно!", reply_markup=manager_menu())
        return
    text = f"🛒 <b>СПИСОК ЗАКУПА — {now_str()}</b>\n\n"
    for name, qty, mn in low_stock_alerts:
        text += f"• {name}: есть {qty}, нужно мин. {mn}\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

# ── ЗАДАЧИ НА ПРОСТОЙ ────────────────────────────────────────────────────────
IDLE_CASHIER = [
    "🧹 Протереть все столы и стулья в зале",
    "🧹 Протереть барную стойку и полки",
    "🍯 Протереть и пополнить сиропы",
    "📦 Проверить и пополнить упаковку на стойке",
    "🥤 Проверить и пополнить напитки в холодильнике",
    "🫙 Пополнить соусницы (кетчуп, майонез)",
    "🚽 Проверить и убрать туалет",
    "📱 Проверить агрегаторы — нет ли новых заказов",
    "🧽 Вымыть посуду если есть",
    "🗑 Проверить мусор — вынести если полный",
]

IDLE_KITCHEN = [
    "🧹 Убрать и протереть рабочую станцию",
    "🔪 Нарезать дополнительные овощи про запас",
    "🧀 Натереть дополнительный сыр",
    "🌭 Нарезать дополнительную колбасу",
    "🍗 Проверить курицу на разморозке",
    "📊 Проверить и обновить остатки в боте",
    "🛢 Проверить масло фритюра",
    "🧽 Помыть инвентарь и лотки",
    "❄️ Проверить порядок в холодильнике",
    "🧹 Подмести и помыть полы на кухне",
]

# ── ПЕРЕДАЧА СМЕНЫ ────────────────────────────────────────────────────────────
HANDOVER_NIGHT = [
    "💵 Деньги пересчитаны и сфотографированы",
    "🗑 Мусор вынесен",
    "🧹 Полы на кухне помыты",
    "🧽 Столы и поверхности на кухне помыты",
    "❄️ Заготовки убраны в холодильник/морозилку",
    "📱 Рабочий телефон заряжен",
    "🔌 Всё оборудование выключено (кроме холодильников)",
    "🚽 Туалет убран",
    "🧹 Зал убран, столы протёрты",
]

HANDOVER_STOCKS = [
    ("🍗 Курица для донера (кг)", 5),
    ("🍗 Курица для пиццы (кг)", 5),
    ("🍞 Булочки (шт)", 40),
    ("🌯 Лаваш (шт)", 100),
    ("🧀 Сыр натёртый (кг)", 15),
    ("🥤 Кола 1л (шт)", 10),
    ("🍟 Фри (кг)", 10),
    ("🍕 Тесто малое (шт)", 30),
    ("🍕 Тесто среднее (шт)", 30),
]

handover_session = {}

@bot.message_handler(func=lambda m: m.text == "🔄 Передача смены")
def start_handover(msg):
    uid = msg.from_user.id
    handover_session[uid] = {
        "step": "checklist",
        "idx": 0,
        "results": [],
        "stocks": {},
        "stock_idx": 0,
        "notes": "",
        "shift": "night"
    }
    set_state(uid, step="handover_check")
    bot.send_message(msg.chat.id,
        "🔄 <b>Передача смены</b>\n\nПроходим по чеклисту закрытия:",
        reply_markup=yes_no_kb(), parse_mode="HTML")
    send_handover_item(uid, msg.chat.id)

def send_handover_item(uid, cid):
    s = handover_session[uid]
    idx = s["idx"]
    if idx >= len(HANDOVER_NIGHT):
        # Переходим к остаткам
        s["step"] = "stocks"
        s["stock_idx"] = 0
        send_handover_stock(uid, cid)
        return
    total = len(HANDOVER_NIGHT)
    bot.send_message(cid,
        f"🔄 <b>Передача смены</b> [{idx+1}/{total}]\n\n{HANDOVER_NIGHT[idx]}\n\nВыполнено?",
        reply_markup=yes_no_kb(), parse_mode="HTML")

def send_handover_stock(uid, cid):
    s = handover_session[uid]
    idx = s["stock_idx"]
    if idx >= len(HANDOVER_STOCKS):
        # Переходим к замечаниям
        s["step"] = "notes"
        set_state(uid, step="handover_notes")
        bot.send_message(cid,
            "📝 Есть замечания для следующей смены?\n\nНапишите текст или нажмите 'Нет замечаний'",
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                KeyboardButton("Нет замечаний")))
        return
    name, mn = HANDOVER_STOCKS[idx]
    bot.send_message(cid,
        f"📊 Остатки [{idx+1}/{len(HANDOVER_STOCKS)}]\n\n<b>{name}</b>\nМинимум: {mn}\n\nСколько осталось?",
        parse_mode="HTML")
    set_state(uid, step="handover_stock_input")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "handover_check"
    and m.text in ["✅ Да", "❌ Нет"])
def handover_check_answer(msg):
    uid = msg.from_user.id
    s = handover_session.get(uid)
    if not s: return
    s["results"].append({"item": HANDOVER_NIGHT[s["idx"]], "ok": msg.text == "✅ Да"})
    s["idx"] += 1
    send_handover_item(uid, msg.chat.id)

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "handover_stock_input")
def handover_stock_input(msg):
    uid = msg.from_user.id
    s = handover_session.get(uid)
    if not s: return
    try:
        qty = float(msg.text.strip().replace(",", "."))
        name, mn = HANDOVER_STOCKS[s["stock_idx"]]
        s["stocks"][name] = qty
        s["stock_idx"] += 1
        send_handover_stock(uid, msg.chat.id)
    except:
        bot.send_message(msg.chat.id, "Введите число:")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "handover_notes")
def handover_notes(msg):
    uid = msg.from_user.id
    s = handover_session.get(uid)
    if not s: return
    s["notes"] = "" if msg.text == "Нет замечаний" else msg.text
    finish_handover(uid, msg.chat.id, msg.from_user.first_name)

def finish_handover(uid, cid, name):
    s = handover_session[uid]
    failed = [r["item"] for r in s["results"] if not r["ok"]]
    low = [(n, q, mn) for (n, mn), q in zip(HANDOVER_STOCKS, s["stocks"].values()) if q < mn]

    # Сообщение сотруднику
    text = f"✅ <b>Смена сдана!</b>\n{now_str()}\n"
    if failed:
        text += f"\n❌ Не выполнено ({len(failed)}):\n"
        for f in failed: text += f"• {f}\n"
    else:
        text += "\n✅ Всё выполнено!"
    bot.send_message(cid, text, reply_markup=main_menu(), parse_mode="HTML")

    # Отчёт менеджеру
    report = f"🔄 <b>ПЕРЕДАЧА СМЕНЫ</b>\n{now_str()}\nСдал: {name}\n\n"
    done = len([r for r in s["results"] if r["ok"]])
    total = len(s["results"])
    report += f"📋 Чеклист: {done}/{total}\n"
    if failed:
        report += "\n❌ НЕ ВЫПОЛНЕНО:\n"
        for f in failed: report += f"• {f}\n"
    if s["stocks"]:
        report += "\n📊 ОСТАТКИ:\n"
        for (name_s, mn), qty in zip(HANDOVER_STOCKS, s["stocks"].values()):
            warn = " ⚠️" if qty < mn else " ✅"
            report += f"• {name_s}: {qty}{warn}\n"
    if low:
        report += "\n🛒 НУЖНО ЗАКАЗАТЬ:\n"
        for n, q, mn in low: report += f"• {n}: {q} (мин. {mn})\n"
    if s["notes"]:
        report += f"\n📝 ЗАМЕЧАНИЯ:\n{s['notes']}"
    notify_manager(report)
    set_state(uid, step="main")

# ── ЗАДАЧИ НА ПРОСТОЙ ─────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "😴 Нет заказов")
def idle_tasks(msg):
    uid = msg.from_user.id
    state = get_state(uid)
    role = state.get("step", "cashier")
    if role == "kitchen":
        items = IDLE_KITCHEN
        title = "👨‍🍳 Задачи кухни на простой"
        back = kitchen_menu()
    else:
        items = IDLE_CASHIER
        title = "🧾 Задачи кассира на простой"
        back = cashier_menu()
    text = f"😴 <b>{title}</b>\n\n"
    for i, item in enumerate(items, 1):
        text += f"{i}. {item}\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=back)

# Обновляем меню кассира и кухни с новыми кнопками
def cashier_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Открытие смены"), KeyboardButton("🔴 Закрытие смены"))
    kb.row(KeyboardButton("🔄 Передача смены"), KeyboardButton("😴 Нет заказов"))
    kb.row(KeyboardButton("⛔ Стоп-лист"), KeyboardButton("🥤 Соки"))
    kb.row(KeyboardButton("📦 Упаковка"), KeyboardButton("⚠️ Возврат/Жалоба"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def kitchen_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Открытие кухни"), KeyboardButton("🔴 Закрытие кухни"))
    kb.row(KeyboardButton("🔄 Передача смены"), KeyboardButton("😴 Нет заказов"))
    kb.row(KeyboardButton("🛢 Замена масла"), KeyboardButton("📊 Остатки кухни"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

print("🍕 Пицца Хан бот v2 запущен!")
bot.infinity_polling()
