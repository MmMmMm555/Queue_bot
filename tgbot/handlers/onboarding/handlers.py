import datetime

from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from tgbot import states

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command
from .keyboards import send_contact


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    update.message.reply_text(
        text="Assalomu alaykum botimizga hush kelibsiz !",)
    if created:
        update.message.reply_text(text="Ismingizni kiriting",)
        return states.NAME1
    else:
        update.message.reply_text(text="Siz ro'yxatdan o'tgansiz",)


def name1(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    name1 = update.message.text
    u.first_name = name1
    u.save()
    update.message.reply_text(text="Familiyangizni kiriting",)
    return states.NAME2


def name2(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    name2 = update.message.text
    u.last_name = name2
    u.save()
    update.message.reply_text(
        text="Telefon raqamingizni kiriting", reply_markup=send_contact,)
    return states.PHONE


def phone(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    if update.message.contact.phone_number.startswith('998'):
        phone_number = update.message.contact.phone_number
    else:
        phone_number = update.message.contact.phone_number.replace('+', '')
    u.phone_number = phone_number
    last_order = User.objects.order_by("order").last().order + 1
    u.order = last_order
    u.save()
    print(last_order)
    update.message.reply_text(
        text=f"Sizning tartib raqamingiz - {last_order}", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        text="kanalga qo'shiling https://t.me/Asadbek_Jumayev",)
    return ConversationHandler.END
