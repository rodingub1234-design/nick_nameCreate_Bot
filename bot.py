import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from games_rules import GAMES_RULES
from generator import NicknameGenerator
from database import Database

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота с новым форматом
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
db = Database()
generator = NicknameGenerator()

# Клавиатура с играми
def get_games_keyboard():
    builder = InlineKeyboardBuilder()
    
    games = list(GAMES_RULES.keys())
    for i in range(0, len(games), 2):
        row_games = games[i:i+2]
        for game in row_games:
            builder.button(text=game, callback_data=f"game_{game}")
        builder.adjust(2)
    
    builder.row(
        types.InlineKeyboardButton(text="📊 Статистика", callback_data="stats"),
        types.InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")
    )
    
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    
    welcome_text = """
🎮 <b>Добро пожаловать в генератор игровых никнеймов!</b>

<b>Выбери игру:</b>
"""
    
    await message.answer(welcome_text, reply_markup=get_games_keyboard())

@dp.callback_query(lambda c: c.data.startswith("game_"))
async def process_game(callback_query: types.CallbackQuery):
    await callback_query.answer("Генерирую...")
    
    game_name = callback_query.data.replace("game_", "")
    user_id = callback_query.from_user.id
    
    if game_name not in GAMES_RULES:
        await callback_query.message.answer("Игра не найдена!")
        return
    
    game_rules = GAMES_RULES[game_name]
    nicks = generator.generate(game_name, game_rules, user_id)
    
    if not nicks:
        await callback_query.message.answer("Не удалось сгенерировать ники. Попробуйте снова.")
        return
    
    result_text = f"<b>🎯 Ники для {game_name}:</b>\n\n"
    for i, nick in enumerate(nicks, 1):
        result_text += f"{i}. <code>{nick}</code>\n"
    
    result_text += f"\n<b>Правила:</b>\n"
    result_text += f"• Макс. длина: {game_rules['max_length']}\n"
    result_text += f"• {game_rules['special_rules']}"
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔄 Еще", callback_data=f"regenerate_{game_name}")
    keyboard.button(text="🎮 Другая игра", callback_data="back")
    
    await callback_query.message.edit_text(
        result_text,
        reply_markup=keyboard.as_markup()
    )

@dp.callback_query(lambda c: c.data.startswith("regenerate_"))
async def regenerate_nicks(callback_query: types.CallbackQuery):
    game_name = callback_query.data.replace("regenerate_", "")
    
    await callback_query.answer("Генерирую новые ники...")
    user_id = callback_query.from_user.id
    
    if game_name not in GAMES_RULES:
        await callback_query.message.answer("Игра не найдена!")
        return
    
    game_rules = GAMES_RULES[game_name]
    nicks = generator.generate(game_name, game_rules, user_id)
    
    if not nicks:
        await callback_query.message.answer("Не удалось сгенерировать ники. Попробуйте снова.")
        return
    
    result_text = f"<b>🎯 Новые ники для {game_name}:</b>\n\n"
    for i, nick in enumerate(nicks, 1):
        result_text += f"{i}. <code>{nick}</code>\n"
    
    result_text += f"\n<b>Правила:</b>\n"
    result_text += f"• Макс. длина: {game_rules['max_length']}\n"
    result_text += f"• {game_rules['special_rules']}"
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔄 Еще", callback_data=f"regenerate_{game_name}")
    keyboard.button(text="🎮 Другая игра", callback_data="back")
    
    await callback_query.message.edit_text(
        result_text,
        reply_markup=keyboard.as_markup()
    )

@dp.callback_query(lambda c: c.data == "back")
async def back_to_games(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "<b>Выберите игру:</b>",
        reply_markup=get_games_keyboard()
    )

@dp.callback_query(lambda c: c.data == "stats")
async def show_stats(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    stats = db.get_user_stats(user_id)
    
    if stats:
        total, games_count = stats
        stats_text = f"📊 <b>Ваша статистика:</b>\n\n"
        stats_text += f"• Всего сгенерировано: <b>{total}</b> ников\n"
        stats_text += f"• Для игр: <b>{games_count}</b>"
    else:
        stats_text = "У вас еще нет сгенерированных ников!"
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔙 Назад", callback_data="back")
    
    await callback_query.message.edit_text(
        stats_text,
        reply_markup=keyboard.as_markup()
    )

@dp.callback_query(lambda c: c.data == "favorites")
async def show_favorites(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    favorites = db.get_favorites(user_id)
    
    if not favorites:
        favorites_text = "⭐ У вас пока нет избранных ников!"
    else:
        favorites_text = "⭐ <b>Ваши избранные ники:</b>\n\n"
        for fav in favorites:
            nick_id, game, nickname, date = fav
            favorites_text += f"• <code>{nickname}</code>\n  для <b>{game}</b>\n\n"
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔙 Назад", callback_data="back")
    
    await callback_query.message.edit_text(
        favorites_text,
        reply_markup=keyboard.as_markup()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
📖 <b>Справка по боту:</b>

<b>Команды:</b>
/start - Начать работу
/help - Показать справку
/rules - Правила игр

<b>Как использовать:</b>
1. Выберите игру из списка
2. Получите 5 уникальных ников
3. Нажмите "Еще" для новых вариантов
4. Используйте ник в игре!

<b>Особенности:</b>
• Все ники проверяются на правила игры
• Гарантируется уникальность
"""
    
    await message.answer(help_text)

@dp.message(Command("rules"))
async def cmd_rules(message: types.Message):
    rules_text = "<b>📋 Правила для всех игр:</b>\n\n"
    
    for game_name, rules in GAMES_RULES.items():
        rules_text += f"<b>{game_name}:</b>\n"
        rules_text += f"• Макс. длина: {rules['max_length']} символов\n"
        rules_text += f"• {rules['special_rules']}\n\n"
    
    await message.answer(rules_text)

async def main():
    print(f"🤖 Бот запускается с токеном: {TOKEN[:10]}...")
    print("✅ Бот успешно запущен!")
    print("ℹ️ Перейдите в Telegram и найдите своего бота")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")