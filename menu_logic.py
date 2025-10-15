# bot/handlers/staff/menu_logic.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .keyboards import create_staff_main_menu
from .states import StaffStates
from ...db_manager import get_user_role, get_user_panel_info


async def staff_panel_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    نقطه ورود و نمایش منوی اصلی پنل کاربری با قابلیت مدیریت پیام‌های تصویری.
    """
    user_id = update.effective_user.id
    query = update.callback_query

    # ... (بخش بررسی نقش کاربر بدون تغییر باقی می‌ماند) ...
    if 'role' not in context.user_data:
        role = await get_user_role(user_id)
        if role != 'staff':
            error_text = "سطح دسترسی شما معتبر نیست. با /start مجدداً تلاش کنید."
            if query:
                await query.answer()
                await query.edit_message_text(text=error_text)
            else:
                await update.message.reply_text(text=error_text)
            return
        context.user_data['role'] = role

    # --- تهیه متن و دکمه‌های منو ---
    user_info = await get_user_panel_info(user_id)
    if user_info:
        welcome_text = (
            f"✨خوش آمدید✨\n"
            f" {user_info['full_name']} عزیز!\n"
            f"واحد: {user_info['unit_name']}\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید: 👇"
        )
    else:
        welcome_text = "به پنل کاربری خود خوش آمدید. لطفاً یکی از گزینه‌های زیر را انتخاب کنید: 👇"
    reply_markup = create_staff_main_menu()

    # --- (منطق اصلاح شده برای ارسال پیام) ---
    if query:
        await query.answer()
        # اگر پیامی که دکمه زیر آن است، عکس دارد
        if query.message.photo:
            # پیام عکس را حذف کن
            await query.message.delete()
            # و یک پیام متنی جدید بفرست
            await context.bot.send_message(
                chat_id=user_id, text=welcome_text, reply_markup=reply_markup
            )
        else:
            # در غیر این صورت، همان پیام متنی را ویرایش کن
            await query.edit_message_text(welcome_text, reply_markup=reply_markup)
    else:
        # برای دستور /start اولیه
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    return StaffStates.MAIN_MENU

async def back_to_main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """کاربر را به منوی اصلی بازمی‌گرداند."""
    # این تابع صرفاً نقطه ورود اصلی را مجدداً فراخوانی می‌کند
    return await staff_panel_entry(update, context)


async def exit_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """پنل کاربری را بسته و مکالمه را پایان می‌دهد."""
    query = update.callback_query
    await query.answer()

    text = "شما با موفقیت از پنل کاربری خود خارج شدید. برای ورود مجدد از دستور /start استفاده کنید."
    await query.edit_message_text(text=text)

    # پایان دادن به ConversationHandler
    return ConversationHandler.END