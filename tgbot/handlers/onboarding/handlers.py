import datetime

from django.utils import timezone
from telegram import ParseMode, Update, ReplyKeyboardRemove, error
from telegram.ext import CallbackContext, ConversationHandler
from tgbot import states
from telegram import Bot

from users.models import User
from .keyboards import send_contact, send_start, yes_no


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    update.message.reply_text(
        text="Assalomu alaykum botimizga hush kelibsiz !",)
    member_status = False
    try:
        user_id = update.effective_user.id
        chat_id = "@freelanceuzofficial"

        # Get chat member information
        chat_member = context.bot.get_chat_member(chat_id, user_id)

        # Check if the user is a member, administrator, or creator in the chat
        if chat_member.status in ['member', 'administrator', 'creator']:
            member_status = True

    except error.BadRequest as e:
        print(f"Error fetching chat member info: {e}")
    if member_status == False:
        update.message.reply_text(
            text="Iltimos ushbu kanalimizga a'zo bo'ling\n https://t.me/freelanceuzofficial", reply_markup=send_start)
    elif member_status:
        if created or u.registered == False:
            update.message.reply_text(text="Ismingizni kiriting 📝", reply_markup=ReplyKeyboardRemove())
            return states.NAME1
        elif u.registered:
            update.message.reply_text(text=f"Siz ro'yxatdan o'tgansiz ✅\n\nSizning tartib raqamingiz {u.order}",)


def name1(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    name1 = update.message.text
    u.first_name = name1
    u.save()
    update.message.reply_text(text="Familiyangizni kiriting 📝",)
    return states.NAME2


def name2(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    name2 = update.message.text
    u.last_name = name2
    u.save()
    update.message.reply_text(
        text="Telefon raqamingizni kiriting 📲\nYoki yozing maslan: 998901234567", reply_markup=send_contact,)
    return states.PHONE


def phone(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    try:
        if update.message.contact.phone_number.startswith('998'):
            phone_number = update.message.contact.phone_number
        else:
            phone_number = update.message.contact.phone_number.replace('+', '')
    except:
        if len(update.message.text) == 12 and update.message.text.startswith('998'):
            phone_number = update.message.text
        else:
            update.message.reply_text(
                "Telefon raqam xato formatda kiritildi ❌\bQayta kiriting !")
            return states.PHONE
    u.phone_number = phone_number
    u.save()
    update.message.reply_text('Siz frilansmisiz ❓', reply_markup=yes_no)
    return states.FREELANCE
    # nubers = {
    #     0: "0️⃣",
    #     1: "1️⃣",
    #     2: "2️⃣",
    #     3: "3️⃣",
    #     4: "4️⃣",
    #     5: "5️⃣",
    #     6: "6️⃣",
    #     7: "7️⃣",
    #     8: "8️⃣",
    #     9: "9️⃣",
    # }

    # order = str(last_order)

    # order_emoji = ''.join(nubers[int(i)] for i in order)
    # update.message.reply_text(
    #     text=f"<b>Sizning tartib raqamingiz</b>\n\n\n                  <b>{order_emoji}</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    # return ConversationHandler.END


def freelance(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    text = update.message.text
    if text == "Ha ✅":
        u.freelance = True
        u.save()
        update.message.reply_text("Frilanserlikning qaysi turi bilan shug'ullanasiz ❓\n(yozing)", reply_markup=ReplyKeyboardRemove())
        return states.TYPE
    elif text == "Yo'q ❌":
        last_order = User.objects.order_by("order").last().order + 1
        u.order = last_order
        u.registered = True
        u.save()
        nubers = {
            0: "0️⃣",
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
        }

        order = str(last_order)

        order_emoji = ''.join(nubers[int(i)] for i in order)
        update.message.reply_text(
            text=f"<b>Sizning tartib raqamingiz</b>\n\n\n                  <b>{order_emoji}</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        return ConversationHandler.END


def type(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    text = update.message.text
    u.types = text
    last_order = User.objects.order_by("order").last().order + 1
    u.order = last_order
    u.registered = True
    u.save()
    nubers = {
        0: "0️⃣",
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
    }

    order = str(last_order)

    order_emoji = ''.join(nubers[int(i)] for i in order)
    update.message.reply_text(
        text=f"<b>Sizning tartib raqamingiz</b>\n\n\n                  <b>{order_emoji}</b>", reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
    return ConversationHandler.END
    