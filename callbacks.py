# bot/handlers/manager_panel/callbacks_heuristic.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

# مسیردهی نسبی برای دسترسی به فایل‌های مورد نیاز
from ...db_manager import add_or_check_user
from ...db.manager_db import get_managed_units, get_unit_details
from ...db.shift_db import get_shift_types, add_shift_type, edit_shift_type, delete_shift_type
from .states import (
    SELECT_UNIT, UNIT_MENU, SHIFT_MGMT_MENU,
    AWAIT_SHIFT_NAME, AWAIT_SHIFT_WEIGHT,
    SELECT_SHIFT_TO_EDIT, AWAIT_NEW_SHIFT_DETAILS,
    SELECT_SHIFT_TO_DELETE, CONFIRM_DELETE_SHIFT,
)

# --- دکوراتور کنترل دسترسی ---
def manager_only(func):
    """
    یک دکوراتور که بررسی می‌کند آیا کاربر نقش 'manager' را در دیتابیس دارد یا خیر.
    """
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        user_data, status = await add_or_check_user(user)
        if status == "complete" and user_data['role'] == 'manager':
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("⛔️ شما اجازه دسترسی به این پنل را ندارید.")
            return ConversationHandler.END
    return wrapped

# --- توابع کمکی برای ساخت منوها ---

async def build_unit_selection_menu(user_id: int):
    """منوی انتخاب واحد را برای مدیر می‌سازد."""
    managed_units = await get_managed_units(user_id)
    if not managed_units:
        return None, "شما در حال حاضر مدیر هیچ واحدی نیستید."
    message_text = "پنل مدیریت واحد:\n\nلطفاً یکی از واحدهای تحت مدیریت خود را انتخاب کنید:"
    keyboard = [[InlineKeyboardButton(f"{unit['unit_name']} ({unit['hospital_name']})", callback_data=f"manage_unit_{unit['unit_id']}")] for unit in managed_units]
    keyboard.append([InlineKeyboardButton("❌ خروج از پنل", callback_data="exit_panel")])
    return InlineKeyboardMarkup(keyboard), message_text

async def build_unit_specific_menu(context: ContextTypes.DEFAULT_TYPE):
    """منوی اختصاصی یک واحد را می‌سازد."""
    unit_id = context.user_data.get('selected_unit_id')
    unit_name = context.user_data.get('selected_unit_name', 'واحد')
    message_text = f"⚙️ مدیریت واحد: *{unit_name}*"
    keyboard = [
        # دکمه جدید در اینجا اضافه می‌شود
        [InlineKeyboardButton("📊 تخصیص شیفت (برنامه)", callback_data=f"assignment_menu_{unit_id}")],
        [InlineKeyboardButton("⚙️ مدیریت انواع شیفت", callback_data=f"manage_shifts_{unit_id}")],
        [InlineKeyboardButton("📋 تعریف نیازمندی شیفت", callback_data=f"reqs_{unit_id}")],
        [InlineKeyboardButton("👥 پرسنل واحد", callback_data="unit_staff")],
        [InlineKeyboardButton("🔙 بازگشت به لیست واحدها", callback_data="back_to_unit_list")]
    ]
    return InlineKeyboardMarkup(keyboard), message_text

async def build_shift_type_menu(context: ContextTypes.DEFAULT_TYPE):
    """منوی اصلی مدیریت انواع شیفت را می‌سازد."""
    unit_id = context.user_data.get('selected_unit_id')
    unit_name = context.user_data.get('selected_unit_name', 'واحد')
    shift_types = await get_shift_types(unit_id)
    message_text = f"⚙️ مدیریت انواع شیفت برای واحد *{unit_name}*:\n\n" + ("شیفت‌های تعریف شده:\n" + "".join(f"- *{st['name']}* (ارزش: {st['weight']})\n" for st in shift_types) if shift_types else "هنوز هیچ شیفتی برای این واحد تعریف نشده است.")
    keyboard = [
        [InlineKeyboardButton("➕ افزودن", callback_data="add_shift"), InlineKeyboardButton("✏️ ویرایش", callback_data="edit_shift"), InlineKeyboardButton("🗑 حذف", callback_data="delete_shift")],
        [InlineKeyboardButton("🔙 بازگشت به منوی واحد", callback_data=f"manage_unit_{unit_id}")]
    ]
    return InlineKeyboardMarkup(keyboard), message_text

async def build_item_list_for_action(context: ContextTypes.DEFAULT_TYPE, name_key: str, id_key: str, callback_prefix: str, back_callback: str):
    """منوی لیستی برای انتخاب آیتم جهت ویرایش/حذف می‌سازد."""
    items = await get_shift_types(context.user_data.get('selected_unit_id'))
    if not items: return None
    keyboard = [[InlineKeyboardButton(item[name_key], callback_data=f"{callback_prefix}_{item[id_key]}")] for item in items]
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data=back_callback)])
    return InlineKeyboardMarkup(keyboard)

async def build_confirmation_menu(callback_prefix: str, item_id: int, back_callback: str):
    """منوی تایید حذف را می‌سازد."""
    keyboard = [
        [InlineKeyboardButton(" بله، حذف کن ✅", callback_data=f"{callback_prefix}_confirm_{item_id}")],
        [InlineKeyboardButton(" خیر، بازگرد 🔙", callback_data=back_callback)]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- توابع اصلی مکالمه ---

@manager_only
async def panel_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """نقطه ورود به پنل مدیر و نمایش لیست واحدها."""
    user_id = update.effective_user.id
    reply_markup, message_text = await build_unit_selection_menu(user_id)
    if update.callback_query:
        await update.callback_query.answer()
        if not reply_markup: await update.callback_query.edit_message_text(message_text); return ConversationHandler.END
        await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
    else:
        if not reply_markup: await update.message.reply_text(message_text); return ConversationHandler.END
        await update.message.reply_text(message_text, reply_markup=reply_markup)
    return SELECT_UNIT

async def select_unit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """انتخاب یک واحد و نمایش منوی اختصاصی آن."""
    query = update.callback_query; await query.answer()
    if query.data.startswith("manage_unit_"):
        unit_id = int(query.data.split('_')[-1])
        context.user_data['selected_unit_id'] = unit_id
        unit_details = await get_unit_details(unit_id)
        if unit_details: context.user_data['selected_unit_name'] = unit_details['unit_name']
    reply_markup, message_text = await build_unit_specific_menu(context)
    await query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    return UNIT_MENU

async def shift_management_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ورود به منوی مدیریت شیفت."""
    query = update.callback_query; await query.answer()
    reply_markup, message_text = await build_shift_type_menu(context)
    await query.edit_message_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    return SHIFT_MGMT_MENU

# --- Shift Add Callbacks ---
async def ask_for_shift_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    await query.edit_message_text("لطفاً نام شیفت جدید را وارد کنید (مثلاً: صبح):")
    return AWAIT_SHIFT_NAME

async def receive_shift_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['shift_name'] = update.message.text.strip()
    await update.message.reply_text("عالی! حالا ارزش (وزن) این شیفت را به صورت عددی وارد کنید (مثلاً: 1 یا 1.5):")
    return AWAIT_SHIFT_WEIGHT

async def receive_shift_weight_and_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        weight = float(update.message.text.strip())
        if weight <= 0: raise ValueError("Weight must be positive")
        success = await add_shift_type(context.user_data['selected_unit_id'], context.user_data['shift_name'], weight)
        if success: await update.message.reply_text(f"✅ شیفت «{context.user_data['shift_name']}» اضافه شد.")
        else: await update.message.reply_text("⚠️ خطا: نام این شیفت در این واحد تکراری است.")
        reply_markup, message_text = await build_shift_type_menu(context)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
        return SHIFT_MGMT_MENU
    except ValueError:
        await update.message.reply_text("خطا: لطفاً یک عدد مثبت و معتبر برای ارزش شیفت وارد کنید.")
        return AWAIT_SHIFT_WEIGHT

# --- Shift Edit Callbacks ---
async def select_shift_to_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    reply_markup = await build_item_list_for_action(context, 'name', 'shift_type_id', 'shift_edit', 'back_to_shift_menu')
    if not reply_markup:
        _, menu = await build_shift_type_menu(context); await query.edit_message_text("شیفتی برای ویرایش وجود ندارد.", reply_markup=menu)
        return SHIFT_MGMT_MENU
    await query.edit_message_text("کدام شیفت را ویرایش می‌کنید؟", reply_markup=reply_markup)
    return SELECT_SHIFT_TO_EDIT

async def ask_for_new_shift_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    context.user_data['shift_id_to_edit'] = int(query.data.split('_')[-1])
    await query.edit_message_text("نام و ارزش جدید را با کاما (,) جدا করে وارد کنید.\nمثال: عصر, 1.5")
    return AWAIT_NEW_SHIFT_DETAILS

async def receive_new_shift_details_and_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        new_name, new_weight_str = map(str.strip, update.message.text.strip().split(','))
        new_weight = float(new_weight_str)
        if new_weight <= 0: raise ValueError("Weight must be positive")
        success = await edit_shift_type(context.user_data['shift_id_to_edit'], new_name, new_weight)
        if success: await update.message.reply_text("✅ شیفت با موفقیت ویرایش شد.")
        else: await update.message.reply_text("⚠️ خطا: نام شیفت تکراری است یا خطایی در ویرایش رخ داد.")
        reply_markup, message_text = await build_shift_type_menu(context)
        await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
        return SHIFT_MGMT_MENU
    except (ValueError, IndexError):
        await update.message.reply_text("فرمت ورودی اشتباه است. لطفاً نام و ارزش (عدد مثبت) را با کاما جدا کنید. مثال: شب, 2")
        return AWAIT_NEW_SHIFT_DETAILS

# --- Shift Delete Callbacks ---
async def select_shift_to_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    reply_markup = await build_item_list_for_action(context, 'name', 'shift_type_id', 'shift_delete', 'back_to_shift_menu')
    if not reply_markup:
        _, menu = await build_shift_type_menu(context); await query.edit_message_text("شیفتی برای حذف وجود ندارد.", reply_markup=menu)
        return SHIFT_MGMT_MENU
    await query.edit_message_text("کدام شیفت را حذف می‌کنید؟", reply_markup=reply_markup)
    return SELECT_SHIFT_TO_DELETE

async def confirm_delete_shift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    shift_id = int(query.data.split('_')[-1])
    reply_markup = await build_confirmation_menu("shift_delete", shift_id, 'back_to_shift_menu')
    await query.edit_message_text("آیا از حذف این شیفت مطمئن هستید؟", reply_markup=reply_markup)
    return CONFIRM_DELETE_SHIFT

async def execute_delete_shift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query; await query.answer()
    shift_id = int(query.data.split('_')[-1])
    success = await delete_shift_type(shift_id)
    if success: await query.edit_message_text("✅ شیفت با موفقیت حذف شد.")
    else: await query.edit_message_text("⚠️ عملیات حذف با خطا مواجه شد.")
    reply_markup, message_text = await build_shift_type_menu(context)
    await query.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
    return SHIFT_MGMT_MENU

# --- General Callbacks ---
async def exit_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """از پنل خارج می‌شود."""
    query = update.callback_query; await query.answer()
    await query.edit_message_text("شما از پنل مدیریت خارج شدید.")
    return ConversationHandler.END