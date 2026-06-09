import telebot
import anthropic
import os
import json
from datetime import datetime

BOT_TOKEN = os.environ.get("CLIENT_BOT_TOKEN", "8696580632:AAG5gw7PKUAxvbha_h-MzvC9lZSXjzee-b0")
OWNER_ID = int(os.environ.get("OWNER_TELEGRAM_ID", "8770900575"))
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

bot = telebot.TeleBot(BOT_TOKEN)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Conversation history per user
user_sessions = {}

MENU_TEXT = """
ПИЦЦЫ МАЛАЯ (27см):
Маргарита 2250 | Сырная 2950 | Болоньезе 2950 | Вегетарианская 2700 | Мексиканская 2700 | С колбасой халял 2700 | Сочная 2950 | Хан 3400 | Хан Острая 2600 | Гавайская 2950 | Цыпленок Ранч 2950 | Морская 2950 | Мясная 3400 | Италия 2950 | Грибная 2600 | Охотничья 2950 | 4 сезона 2950 | Цезарь 1750 | Чизбургер 2950

ПИЦЦЫ СРЕДНЯЯ (33см):
Маргарита 3050 | Сырная 3050 | Болоньезе 3750 | Вегетарианская 3350 | Мексиканская 3750 | С колбасой халял 3750 | Сочная 3750 | Хан 4250 | Хан Острая 3250 | Гавайская 3750 | Цыпленок Ранч 3750 | Морская 3750 | Мясная 4250 | Италия 3750 | Грибная 3250 | Охотничья 3750 | 4 сезона 3750 | Чизбургер 3750

ПИЦЦЫ БОЛЬШАЯ (36см):
Маргарита 3850 | Сырная 3850 | Болоньезе 4550 | Вегетарианская 4400 | Мексиканская 4350 | С колбасой халял 4350 | Сочная 4550 | Хан 5150 | Хан Острая 3950 | Гавайская 4550 | Цыпленок Ранч 4550 | Морская 4550 | Мясная 5150 | Италия 4550 | Грибная 3950 | Охотничья 4550 | 4 сезона 4550 | Чизбургер 4550

ДОНЕР:
Донер с курицей 1350 | Комбо донер+фри+кола 2050

БУРГЕРЫ:
Чикен Бургер 1450 | Комбо бургер+фри+кола 2100

ЗАКУСКИ:
Картофель Фри 550 | Картофельные дольки 750 | Картофельные шарики 10шт 700 | Куриные стрипсы 1150 | Луковые кольца 5шт 600
Наггетсы 5шт 750 | Наггетсы 6шт 750 | Наггетсы 10шт 1500 | Наггетсы 18шт 1500 | Наггетсы 300г 1200
Сырные палочки 5шт 1050 | Сырные палочки пицца 2250

КРЫЛЫШКИ:
5шт 1150 | 10шт 2310 | 20шт 4400 | 30шт 6490 | 40шт 8690 | 50шт 9900 | 60шт 13200
Чикен Mix 6шт 3700 | Чикен Mix 3шт 2850

СОУСЫ:
Барбекю 350 | Чесночный 350 | Сырный 350 | Халапеньо 200

ДОСТАВКА:
Близко: 500 тг | Средняя: 800 тг | Далеко: 1200+ тг | Самовывоз: бесплатно
"""

SYSTEM_PROMPT = f"""Ты — дружелюбный бот-помощник ресторана Pizza Khan (Пицца Хан) в Казахстане.

ВАЖНЫЕ ПРАВИЛА:
1. Отвечай на том языке, на котором пишет клиент (русский или казахский)
2. Будь дружелюбным и помогай оформить заказ
3. Понимай свободный текст — клиент может написать "маргариту и фри" или "маргарита алайық"
4. Если размер пиццы не указан — уточни (малая 27см, средняя 33см, большая 36см)
5. После формирования заказа — спроси адрес доставки или самовывоз
6. Когда заказ полностью готов — выведи итог в формате JSON в конце сообщения вот так:
ORDER_JSON:{{\"items\":[{{\"name\":\"название\",\"qty\":1,\"price\":2250}}],\"total\":2250,\"delivery\":\"доставка/самовывоз\",\"address\":\"адрес или самовывоз\"}}

МЕНЮ И ЦЕНЫ:
{MENU_TEXT}

ИНФОРМАЦИЯ О РЕСТОРАНЕ:
- Адрес: ул. Кулманова 107
- Время работы: 09:00 – 03:00
- Доставка: близко 500тг / средняя 800тг / далеко 1200тг / самовывоз бесплатно

Если клиент спрашивает о блюде которого нет в меню — вежливо скажи что этого нет и предложи альтернативу.
Если клиент жалуется — выслушай, извинись и скажи что передашь информацию администратору.
"""

def get_ai_response(user_id: int, user_message: str) -> str:
    if user_id not in user_sessions:
        user_sessions[user_id] = []
    
    user_sessions[user_id].append({
        "role": "user",
        "content": user_message
    })
    
    # Keep last 20 messages to avoid token overflow
    history = user_sessions[user_id][-20:]
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=history
    )
    
    assistant_message = response.content[0].text
    user_sessions[user_id].append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

def extract_order_json(text: str):
    if "ORDER_JSON:" not in text:
        return None, text
    
    parts = text.split("ORDER_JSON:")
    clean_text = parts[0].strip()
    try:
        order_data = json.loads(parts[1].strip())
        return order_data, clean_text
    except:
        return None, text

def notify_owner(user_id: int, username: str, order_data: dict):
    items_text = "\n".join([
        f"  • {item['name']} x{item['qty']} = {item['price'] * item['qty']} тг"
        for item in order_data.get('items', [])
    ])
    
    delivery = order_data.get('delivery', '')
    address = order_data.get('address', '')
    total = order_data.get('total', 0)
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    message = f"""🔔 НОВЫЙ ЗАКАЗ! #{user_id}

👤 Клиент: @{username or 'без username'} (ID: {user_id})
🕐 Время: {now}

📋 Состав заказа:
{items_text}

💰 Итого: {total} тг
🚗 Доставка: {delivery}
📍 Адрес: {address}
"""
    
    bot.send_message(OWNER_ID, message)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_sessions[user_id] = []  # Reset session
    
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в Pizza Khan!\n\n"
        "Я помогу вам сделать заказ. Просто напишите что хотите заказать, например:\n"
        "«Маргариту среднюю и фри»\n\n"
        "Немесе қазақша жазуыңызға болады:\n"
        "«Маргарита орташа және фри алайық»\n\n"
        "📍 Мы находимся: ул. Кулманова 107\n"
        "⏰ Работаем: 09:00 – 03:00"
    )

@bot.message_handler(commands=['menu'])
def show_menu(message):
    bot.send_message(
        message.chat.id,
        "📋 Наше меню:\n\n"
        "🍕 ПИЦЦЫ: малая (27см), средняя (33см), большая (36см)\n"
        "Маргарита, Сырная, Болоньезе, Мексиканская, Хан, Охотничья, Гавайская, Мясная и другие\n\n"
        "🌯 ДОНЕР: 1350 тг\n"
        "🍔 БУРГЕР: 1450 тг\n"
        "🍟 ЗАКУСКИ: Фри, дольки, наггетсы, крылышки, стрипсы\n\n"
        "Напишите что хотите — я всё пойму! 😊"
    )

@bot.message_handler(commands=['reset'])
def reset(message):
    user_sessions[message.from_user.id] = []
    bot.send_message(message.chat.id, "✅ Заказ очищен. Начнём заново!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    text = message.text
    
    # Show typing indicator
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        response = get_ai_response(user_id, text)
        order_data, clean_response = extract_order_json(response)
        
        # Send response to client
        bot.send_message(message.chat.id, clean_response)
        
        # If order is complete — notify owner
        if order_data:
            notify_owner(user_id, username, order_data)
            # Reset session after order
            user_sessions[user_id] = []
            
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "Извините, произошла ошибка. Пожалуйста, попробуйте ещё раз или позвоните нам."
        )
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Pizza Khan Client Bot запущен...")
    bot.infinity_polling()
