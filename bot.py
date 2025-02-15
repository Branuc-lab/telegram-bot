
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# === 1⃣ Configuration du bot ===
TOKEN = "7760633346:AAF4RBNscQpQgKQprs3FUuLKM80mQW7MYFI"  # Remplace avec le Token donné par BotFather
PREMIUM_CHANNEL_ID = "-4641495100"  # Remplace avec l'ID de ton canal privé
ADMIN_ID = 7940719175  # Remplace avec ton ID Telegram

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# === 2⃣ Clavier principal ===
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/premium"), KeyboardButton(text="/my_status")]
    ],
    resize_keyboard=True
)

# === 3⃣ Vérification de l'abonnement ===
async def is_premium_member(user_id):
    try:
        member = await bot.get_chat_member(PREMIUM_CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# === 4⃣ Commande /start ===
@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("👋 Bienvenue sur mon bot !", reply_markup=main_keyboard)

# === 5⃣ Commande /premium ===
@router.message(Command("premium"))
async def premium_command(message: Message):
    await message.answer(
        "💎 Deviens membre Premium et accède à notre canal privé !\n\n"
        "🔹 Prix : 2000 DA / mois\n"
        "💳 Paiement via : Western Union, CIB, PayPal\n\n"
        "📩 Après paiement, envoie une preuve à @TON_ADMIN pour être ajouté."
    )

# === 6⃣ Vérifier son statut Premium ===
@router.message(Command("my_status"))
async def check_status(message: Message):
    is_member = await is_premium_member(message.from_user.id)
    if is_member:
        await message.answer("✅ Tu es membre Premium !")
    else:
        await message.answer("❌ Tu n'es pas membre Premium. Utilise /premium pour t'abonner.")

# === 7⃣ Ajout Manuel au Canal ===
@router.message(lambda message: message.text.startswith("/add_premium "))
async def add_premium_user(message: Message):
    if message.from_user.id == ADMIN_ID:  # Vérifie que c'est l'admin
        user_id = message.text.split(" ")[1]
        try:
            await bot.add_chat_members(PREMIUM_CHANNEL_ID, user_id)
            await message.answer(f"✅ L'utilisateur {user_id} a été ajouté au canal Premium !")
        except Exception as e:
            await message.answer(f"❌ Erreur : {e}")

# === 8⃣ Expulser un utilisateur du Canal Premium ===
@router.message(lambda message: message.text.startswith("/remove_premium "))
async def remove_premium_user(message: Message):
    if message.from_user.id == ADMIN_ID:
        user_id = message.text.split(" ")[1]
        try:
            await bot.ban_chat_member(PREMIUM_CHANNEL_ID, user_id)
            await message.answer(f"🚫 L'utilisateur {user_id} a été retiré du canal Premium.")
        except Exception as e:
            await message.answer(f"❌ Erreur : {e}")

# === 9⃣ Notifications Admin ===
async def notify_admin(payment_info):
    await bot.send_message(ADMIN_ID, f"💰 Nouveau paiement reçu : {payment_info}")

# === 🔟 Lancer le bot ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
