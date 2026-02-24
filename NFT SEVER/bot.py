import asyncio
from aiogram import Bot, Dispatcher, types
from config import TOKEN, ADMIN_ID
from database import get_balance, update_balance, set_stake, get_stake, clear_stake
from rocket import Rocket

bot = Bot(token=TOKEN)
dp = Dispatcher()

rocket = Rocket()

# подписка на ракету
async def rocket_update(multiplier, pause):
    text = f"🚀 ракета летить {multiplier:.2f}x"
    if pause:
        text += " ⏳ 5 секунд на ставку!"
    # можно отправлять в канал или обновлять сообщение
    print(text)

rocket.subscribe(rocket_update)

@dp.message(commands=["start"])
async def start(message: types.Message):
    balance = get_balance(message.from_user.id)
    await message.reply(f"привіт твій баланс {balance}⭐\nвведи /stake щоб поставити зірки")

@dp.message(commands=["balance"])
async def balance(message: types.Message):
    bal = get_balance(message.from_user.id)
    await message.reply(f"твій баланс {bal}⭐")

@dp.message(commands=["stake"])
async def stake(message: types.Message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.reply("введи суму як /stake 10")
        return
    amount = int(args[1])
    bal = get_balance(message.from_user.id)
    if amount > bal:
        await message.reply("немає стільки зірок")
        return
    set_stake(message.from_user.id, amount, rocket.multiplier)
    await message.reply(f"ставка {amount}⭐ за множником {rocket.multiplier:.2f}x натисни /take щоб забрати")

@dp.message(commands=["take"])
async def take(message: types.Message):
    stake, mult = get_stake(message.from_user.id)
    if stake == 0:
        await message.reply("немає активної ставки")
        return
    win = int(stake * mult)
    update_balance(message.from_user.id, win)
    clear_stake(message.from_user.id)
    await message.reply(f"ти забрав {win}⭐ 🎉")

# адмін панель
@dp.message(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply("адмін панель\nкоманди:\n/bal user_id\n/add user_id amount\n/sub user_id amount")

@dp.message(commands=["add"])
async def admin_add(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 3:
        return
    user_id, amount = int(args[1]), int(args[2])
    update_balance(user_id, amount)
    await message.reply(f"добавлено {amount}⭐ користувачу {user_id}")

@dp.message(commands=["sub"])
async def admin_sub(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()
    if len(args) < 3:
        return
    user_id, amount = int(args[1]), int(args[2])
    update_balance(user_id, -amount)
    await message.reply(f"забрано {amount}⭐ користувачу {user_id}")

async def main():
    asyncio.create_task(rocket.start())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
