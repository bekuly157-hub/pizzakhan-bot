#!/usr/bin/env python3
"""
Пицца Хан — Telegram Bot
Запуск: pip install pyTelegramBotAPI && python pizzakhan_bot.py
"""

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json, os, datetime

TOKEN = "8827374656:AAFbMRgbnic89nWV5we8nNTsHs2icx75D_A"
MANAGER_ID = 8770900575

bot = telebot.TeleBot(TOKEN)

# ── ДАННЫЕ ──────────────────────────────────────────────────────────────────
PACKAGING = {
    "Коробка пицца маленькая": 30,
    "Коробка пицца средняя": 30,
    "Коробка пицца большая": 15,
    "Крафт пакет большой": 20,
    "Крафт пакет маленький": 20,
    "Упаковка фри": 40,
    "Фри бумажная": 30,
    "Донер упаковка": 20,
    "Бургер бокс": 20,
    "Стакан 350мл": 30,
    "Крышки": 50,
    "Соусница 30мл": 50,
    "Салфетки (пачки)": 5,
    "Трубочки": 50,
}

OPEN_CHECKLIST = [
    "Протереть кассу и барную стойку",
    "Проверить наличие сдачи",
    "Сиропы — протёрты, не липкие",
    "Кофемашина включена, холдер чистый",
    "Стаканы / крышки / соломки есть",
    "Проверить стоп-лист с кухней",
    "Упаковка на месте",
    "Зарядить рабочий телефон",
]

CLOSE_CHECKLIST = [
    "Протереть сиропы и сироп-стойку",
    "Вымыть холдер кофемашины",
    "Вынести мусор",
    "Закрыть кассу, сдать деньги",
    "Передать ключ следующей смене",
    "Выключить чайник и кофемашину",
    "Убрать рабочее место бара",
    "Обновить остатки в программе",
]

KITCHEN_CHECKLIST = [
    "Проверить температуру масла фритюра",
    "Нарезать сыр по нормам (140/200/230г)",
    "Отмерить фарш порциями (60г)",
    "Разморозить следующую партию курицы",
    "Нарезать колбасу и фитексу",
    "Приготовить пицца-соус",
    "Нарезать овощи для донера",
    "Убрать рабочее место",
]

PREP_CHECKLIST = [
    "Промыть курицу (10 кг)",
    "Замариновать курицу",
    "Расфасовать по 1.5–2 кг, в морозилку",
    "Приготовить котлеты куриные (150г)",
    "Замешать чикен-смесь",
    "Приготовить соусы",
    "Нарезать колбасу и фитексу",
    "Обновить счётчики",
]

STOPLIST_ITEMS = ["Пицца", "Донер", "Бургер", "Чикен", "Фри", "Кофе", "Наггетсы"]

SUPPLIERS = {
    "🍞 Булочки": "",
    "🌯 Лаваш": "",
    "🥤 Напитки (Coca-Cola)": "",
    "🍗 Курица": "",
    "🌭 Колбаса": "",
    "📦 Упаковка": "",
    "🍯 Соусы/Майонез": "",
    "🥩 Фарш": "",
    "🐴 Конина": "",
}

DELIVERY_CHECKLIST = [
    "Проверить накладную у поставщика",
    "Взвесить/пересчитать товар",
    "Совпадает с заказом?",
    "Проверить срок годности",
    "Убрать на место хранения",
    "Внести приход во Frontpad",
]

# ── СОСТОЯНИЕ ────────────────────────────────────────────────────────────────
user_state = {}
pkg_session = {}
checklist_session = {}
stoplist = {item: True for item in STOPLIST_ITEMS}
returns_today = []
oil_log = {}
delivery_session = {}

def get_state(uid): return user_state.get(uid, {})
def set_state(uid, **kwargs): user_state[uid] = kwargs

def now_str(): return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
def today_str(): return datetime.datetime.now().strftime("%d.%m.%Y")

def notify_manager(text):
    try: bot.send_message(MANAGER_ID, text, parse_mode="HTML")
    except: pass

# ── КЛАВИАТУРЫ ───────────────────────────────────────────────────────────────
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🧾 Кассир"), KeyboardButton("👨‍🍳 Кухня"))
    kb.row(KeyboardButton("🔪 Заготовщик"), KeyboardButton("📦 Приёмка товара"))
    kb.row(KeyboardButton("👁 Менеджер"))
    return kb

def cashier_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Открытие смены"), KeyboardButton("🔴 Закрытие смены"))
    kb.row(KeyboardButton("⛔ Стоп-лист"), KeyboardButton("📦 Упаковка"))
    kb.row(KeyboardButton("⚠️ Возврат/Жалоба"), KeyboardButton("🛢 Замена масла"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def kitchen_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Чеклист кухни"), KeyboardButton("🛢 Замена масла"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def prep_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Задачи заготовщика"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def manager_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("📊 Сводка дня"), KeyboardButton("⛔ Стоп-лист (просмотр)"))
    kb.row(KeyboardButton("⚠️ Возвраты сегодня"), KeyboardButton("🛢 Статус масла"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    return kb

def yes_no_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("✅ Да"), KeyboardButton("❌ Нет"))
    return kb

def stoplist_kb():
    kb = InlineKeyboardMarkup()
    for item in STOPLIST_ITEMS:
        status = "✅" if stoplist.get(item) else "⛔"
        kb.add(InlineKeyboardButton(f"{status} {item}", callback_data=f"stop_{item}"))
    return kb

# ── СТАРТ ────────────────────────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start(msg):
    uid = msg.from_user.id
    set_state(uid, step="main")
    bot.send_message(uid,
        "👋 Привет! Это бот <b>Пицца Хан</b>.\n\nВыбери свою роль:",
        reply_markup=main_menu(), parse_mode="HTML")

# ── ГЛАВНОЕ МЕНЮ ─────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🏠 Главное меню")
def go_main(msg):
    set_state(msg.from_user.id, step="main")
    bot.send_message(msg.chat.id, "Главное меню:", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "🧾 Кассир")
def cashier(msg):
    set_state(msg.from_user.id, step="cashier")
    bot.send_message(msg.chat.id, "🧾 <b>Режим кассира</b>\nВыбери действие:",
        reply_markup=cashier_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👨‍🍳 Кухня")
def kitchen(msg):
    set_state(msg.from_user.id, step="kitchen")
    bot.send_message(msg.chat.id, "👨‍🍳 <b>Режим кухни</b>\nВыбери действие:",
        reply_markup=kitchen_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🔪 Заготовщик")
def prep(msg):
    set_state(msg.from_user.id, step="prep")
    bot.send_message(msg.chat.id, "🔪 <b>Режим заготовщика</b>\nВыбери действие:",
        reply_markup=prep_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "👁 Менеджер")
def manager(msg):
    if msg.from_user.id != MANAGER_ID:
        bot.send_message(msg.chat.id, "⛔ Только для менеджера.")
        return
    set_state(msg.from_user.id, step="manager")
    bot.send_message(msg.chat.id, "👁 <b>Режим менеджера</b>",
        reply_markup=manager_menu(), parse_mode="HTML")

# ── ЧЕКЛИСТЫ ─────────────────────────────────────────────────────────────────
def start_checklist(uid, chat_id, items, title, finish_msg, notify_title):
    checklist_session[uid] = {
        "items": items, "idx": 0, "results": [],
        "title": title, "finish_msg": finish_msg, "notify_title": notify_title
    }
    send_checklist_item(uid, chat_id)

def send_checklist_item(uid, chat_id):
    s = checklist_session[uid]
    idx = s["idx"]
    items = s["items"]
    if idx >= len(items):
        finish_checklist(uid, chat_id)
        return
    total = len(items)
    bot.send_message(chat_id,
        f"📋 <b>{s['title']}</b> [{idx+1}/{total}]\n\n{items[idx]}\n\nВыполнено?",
        reply_markup=yes_no_kb(), parse_mode="HTML")
    set_state(uid, step="checklist")

def finish_checklist(uid, chat_id):
    s = checklist_session[uid]
    done = sum(1 for r in s["results"] if r)
    total = len(s["items"])
    failed = [s["items"][i] for i, r in enumerate(s["results"]) if not r]
    text = f"✅ <b>{s['finish_msg']}</b>\nВыполнено: {done}/{total}"
    if failed:
        text += "\n\n❌ Не выполнено:\n" + "\n".join(f"• {f}" for f in failed)
    bot.send_message(chat_id, text, parse_mode="HTML",
        reply_markup=cashier_menu() if "Кассир" in s["title"] or "смен" in s["title"]
        else kitchen_menu())
    notify_manager(
        f"📋 <b>{s['notify_title']}</b> — {now_str()}\n"
        f"Выполнено: {done}/{total}"
        + (("\n❌ Не выполнено:\n" + "\n".join(f"• {f}" for f in failed)) if failed else "")
    )

@bot.message_handler(func=lambda m: m.text == "✅ Открытие смены")
def open_shift(msg):
    uid = msg.from_user.id
    start_checklist(uid, msg.chat.id, OPEN_CHECKLIST,
        "Открытие смены", "Смена открыта!", "Открытие смены")

@bot.message_handler(func=lambda m: m.text == "🔴 Закрытие смены")
def close_shift(msg):
    uid = msg.from_user.id
    start_checklist(uid, msg.chat.id, CLOSE_CHECKLIST,
        "Закрытие смены", "Смена закрыта!", "Закрытие смены")

@bot.message_handler(func=lambda m: m.text == "✅ Чеклист кухни")
def kitchen_check(msg):
    uid = msg.from_user.id
    start_checklist(uid, msg.chat.id, KITCHEN_CHECKLIST,
        "Чеклист кухни", "Кухня готова!", "Чеклист кухни")

@bot.message_handler(func=lambda m: m.text == "✅ Задачи заготовщика")
def prep_check(msg):
    uid = msg.from_user.id
    start_checklist(uid, msg.chat.id, PREP_CHECKLIST,
        "Задачи заготовщика", "Заготовки выполнены!", "Заготовщик")

@bot.message_handler(func=lambda m: m.text in ["✅ Да", "❌ Нет"] and
    get_state(m.from_user.id).get("step") == "checklist")
def checklist_answer(msg):
    uid = msg.from_user.id
    s = checklist_session.get(uid)
    if not s: return
    s["results"].append(msg.text == "✅ Да")
    s["idx"] += 1
    send_checklist_item(uid, msg.chat.id)

# ── СТОП-ЛИСТ ────────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "⛔ Стоп-лист")
def show_stoplist(msg):
    bot.send_message(msg.chat.id,
        "⛔ <b>Стоп-лист</b>\nНажми на позицию чтобы изменить статус:",
        reply_markup=stoplist_kb(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "⛔ Стоп-лист (просмотр)")
def show_stoplist_manager(msg):
    stops = [k for k, v in stoplist.items() if not v]
    avail = [k for k, v in stoplist.items() if v]
    text = "⛔ <b>Стоп-лист сейчас:</b>\n\n"
    if stops:
        text += "🔴 В стопе:\n" + "\n".join(f"• {s}" for s in stops) + "\n\n"
    text += "✅ Есть:\n" + "\n".join(f"• {a}" for a in avail)
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def toggle_stop(call):
    item = call.data.replace("stop_", "")
    if item in stoplist:
        stoplist[item] = not stoplist[item]
        status = "✅ ЕСТЬ" if stoplist[item] else "⛔ СТОП"
        notify_manager(f"⛔ <b>Стоп-лист изменён</b>\n{item}: {status}\n{now_str()}")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
        reply_markup=stoplist_kb())
    bot.answer_callback_query(call.id)

# ── УПАКОВКА ─────────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 Упаковка")
def start_packaging(msg):
    uid = msg.from_user.id
    pkg_session[uid] = {"items": list(PACKAGING.keys()), "idx": 0, "results": {}}
    set_state(uid, step="packaging")
    send_pkg_item(uid, msg.chat.id)

def send_pkg_item(uid, chat_id):
    s = pkg_session[uid]
    idx = s["idx"]
    items = s["items"]
    if idx >= len(items):
        finish_packaging(uid, chat_id)
        return
    item = items[idx]
    mn = PACKAGING[item]
    bot.send_message(chat_id,
        f"📦 <b>Упаковка</b> [{idx+1}/{len(items)}]\n\n"
        f"<b>{item}</b>\nМинимум: {mn} шт\n\nСколько сейчас?",
        parse_mode="HTML")

def finish_packaging(uid, chat_id):
    s = pkg_session[uid]
    low = [(k, v, PACKAGING[k]) for k, v in s["results"].items() if v < PACKAGING[k]]
    ok = [(k, v) for k, v in s["results"].items() if v >= PACKAGING[k]]
    text = f"📦 <b>Проверка упаковки завершена</b> — {now_str()}\n\n"
    if low:
        text += "⚠️ МАЛО — нужно заказать:\n"
        for k, v, mn in low:
            text += f"• {k}: {v} шт (мин. {mn})\n"
    else:
        text += "✅ Всё в норме!\n"
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🏠 Главное меню"))
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=cashier_menu())
    if low:
        notify_text = f"📦 <b>МАЛО УПАКОВКИ</b> — {now_str()}\n\n"
        for k, v, mn in low:
            notify_text += f"⚠️ {k}: {v}/{mn} шт\n"
        notify_manager(notify_text)
    set_state(uid, step="cashier")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "packaging")
def packaging_input(msg):
    uid = msg.from_user.id
    s = pkg_session.get(uid)
    if not s: return
    try:
        qty = int(msg.text.strip())
        item = s["items"][s["idx"]]
        s["results"][item] = qty
        mn = PACKAGING[item]
        if qty < mn:
            bot.send_message(msg.chat.id, f"⚠️ Мало! Минимум {mn} шт. Запишем {qty}.")
        s["idx"] += 1
        send_pkg_item(uid, msg.chat.id)
    except:
        bot.send_message(msg.chat.id, "Введите число:")

# ── ВОЗВРАТ/ЖАЛОБА ───────────────────────────────────────────────────────────
RETURN_ITEMS = ["Пицца", "Донер", "Бургер", "Чикен", "Фри", "Наггетсы", "Напиток"]
RETURN_REASONS = ["Мало сыра", "Мало мяса", "Долго ждали", "Забыли напиток",
                  "Холодная еда", "Ошибка в заказе", "Другое"]

@bot.message_handler(func=lambda m: m.text == "⚠️ Возврат/Жалоба")
def start_return(msg):
    uid = msg.from_user.id
    set_state(uid, step="return_item")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in RETURN_ITEMS:
        kb.add(KeyboardButton(item))
    kb.add(KeyboardButton("🏠 Главное меню"))
    bot.send_message(msg.chat.id, "⚠️ <b>Возврат/Жалоба</b>\nКакая позиция?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "return_item"
    and m.text in RETURN_ITEMS)
def return_item_selected(msg):
    uid = msg.from_user.id
    set_state(uid, step="return_reason", return_item=msg.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for r in RETURN_REASONS:
        kb.add(KeyboardButton(r))
    bot.send_message(msg.chat.id, f"Позиция: <b>{msg.text}</b>\nПричина?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "return_reason"
    and m.text in RETURN_REASONS)
def return_reason_selected(msg):
    uid = msg.from_user.id
    state = get_state(uid)
    item = state.get("return_item", "?")
    reason = msg.text
    entry = {"item": item, "reason": reason, "time": now_str(),
             "who": msg.from_user.first_name}
    returns_today.append(entry)
    bot.send_message(msg.chat.id,
        f"✅ Зафиксировано:\n<b>{item}</b> — {reason}\n{now_str()}",
        reply_markup=cashier_menu(), parse_mode="HTML")
    notify_manager(
        f"⚠️ <b>ВОЗВРАТ/ЖАЛОБА</b>\n"
        f"Позиция: {item}\nПричина: {reason}\nВремя: {now_str()}\n"
        f"Кассир: {msg.from_user.first_name}")
    set_state(uid, step="cashier")

# ── ЗАМЕНА МАСЛА ─────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "🛢 Замена масла")
def oil_change(msg):
    uid = msg.from_user.id
    set_state(uid, step="oil")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🛢 Фри (картофель)"), KeyboardButton("🛢 Чикен (курица)"))
    kb.row(KeyboardButton("🏠 Главное меню"))
    bot.send_message(msg.chat.id, "🛢 <b>Замена масла</b>\nКакой фритюр?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "oil"
    and m.text in ["🛢 Фри (картофель)", "🛢 Чикен (курица)"])
def oil_changed(msg):
    uid = msg.from_user.id
    fryer = msg.text
    oil_log[fryer] = now_str()
    bot.send_message(msg.chat.id,
        f"✅ Масло заменено!\n<b>{fryer}</b>\nВремя: {now_str()}",
        reply_markup=cashier_menu(), parse_mode="HTML")
    notify_manager(f"🛢 <b>Масло заменено</b>\n{fryer}\n{now_str()}\n"
        f"Кто: {msg.from_user.first_name}")
    set_state(uid, step="cashier")

# ── ПРИЁМКА ТОВАРА ────────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📦 Приёмка товара")
def start_delivery(msg):
    uid = msg.from_user.id
    delivery_session[uid] = {"idx": 0, "results": [], "supplier": ""}
    set_state(uid, step="delivery_supplier")
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for s in SUPPLIERS.keys():
        kb.add(KeyboardButton(s))
    kb.add(KeyboardButton("🏠 Главное меню"))
    bot.send_message(msg.chat.id,
        "📦 <b>Приёмка товара</b>\nОт какого поставщика?",
        reply_markup=kb, parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "delivery_supplier"
    and m.text in SUPPLIERS.keys())
def delivery_supplier(msg):
    uid = msg.from_user.id
    delivery_session[uid]["supplier"] = msg.text
    set_state(uid, step="delivery_check")
    send_delivery_item(uid, msg.chat.id)

def send_delivery_item(uid, chat_id):
    s = delivery_session[uid]
    idx = s["idx"]
    if idx >= len(DELIVERY_CHECKLIST):
        finish_delivery(uid, chat_id)
        return
    item = DELIVERY_CHECKLIST[idx]
    bot.send_message(chat_id,
        f"📦 <b>Приёмка</b> [{idx+1}/{len(DELIVERY_CHECKLIST)}]\n\n{item}",
        reply_markup=yes_no_kb(), parse_mode="HTML")

@bot.message_handler(func=lambda m: get_state(m.from_user.id).get("step") == "delivery_check"
    and m.text in ["✅ Да", "❌ Нет"])
def delivery_answer(msg):
    uid = msg.from_user.id
    s = delivery_session.get(uid)
    if not s: return
    s["results"].append({"item": DELIVERY_CHECKLIST[s["idx"]], "ok": msg.text == "✅ Да"})
    s["idx"] += 1
    send_delivery_item(uid, msg.chat.id)

def finish_delivery(uid, chat_id):
    s = delivery_session[uid]
    supplier = s["supplier"]
    failed = [r["item"] for r in s["results"] if not r["ok"]]
    text = f"✅ <b>Приёмка завершена</b>\nПоставщик: {supplier}\n{now_str()}"
    if failed:
        text += "\n\n❌ Проблемы:\n" + "\n".join(f"• {f}" for f in failed)
    bot.send_message(chat_id, text, reply_markup=main_menu(), parse_mode="HTML")
    notify_manager(
        f"📦 <b>ПРИЁМКА ТОВАРА</b>\nПоставщик: {supplier}\n{now_str()}\n"
        f"Принял: {bot.get_chat(uid).first_name}\n"
        + (("\n❌ Проблемы:\n" + "\n".join(f"• {f}" for f in failed)) if failed else "\n✅ Всё ок")
    )
    set_state(uid, step="main")

# ── МЕНЕДЖЕР — СВОДКА ────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.text == "📊 Сводка дня")
def daily_summary(msg):
    if msg.from_user.id != MANAGER_ID: return
    stops = [k for k, v in stoplist.items() if not v]
    text = f"📊 <b>СВОДКА ПИЦЦА ХАН</b>\n{today_str()}\n\n"
    text += f"⛔ В стопе: {', '.join(stops) if stops else 'нет'}\n"
    text += f"⚠️ Возвратов сегодня: {len(returns_today)}\n"
    if returns_today:
        for r in returns_today[-3:]:
            text += f"  • {r['item']} — {r['reason']} ({r['time']})\n"
    text += "\n🛢 Масло:\n"
    for fryer, t in oil_log.items():
        text += f"  • {fryer}: заменено в {t}\n"
    if not oil_log:
        text += "  • Не менялось сегодня\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.message_handler(func=lambda m: m.text == "⚠️ Возвраты сегодня")
def show_returns(msg):
    if msg.from_user.id != MANAGER_ID: return
    if not returns_today:
        bot.send_message(msg.chat.id, "✅ Возвратов сегодня нет.", reply_markup=manager_menu())
        return
    text = f"⚠️ <b>Возвраты сегодня ({len(returns_today)}):</b>\n\n"
    for r in returns_today:
        text += f"• {r['item']} — {r['reason']} ({r['time']})\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

@bot.message_handler(func=lambda m: m.text == "🛢 Статус масла")
def show_oil(msg):
    if msg.from_user.id != MANAGER_ID: return
    text = "🛢 <b>Статус масла:</b>\n\n"
    for fryer in ["🛢 Фри (картофель)", "🛢 Чикен (курица)"]:
        t = oil_log.get(fryer, "❌ Не менялось")
        text += f"• {fryer}: {t}\n"
    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=manager_menu())

# ── ЗАПУСК ───────────────────────────────────────────────────────────────────
print("🍕 Пицца Хан бот запущен!")
bot.infinity_polling()
