# bot/handlers/staff/main_handler.py
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# --- وارد کردن وضعیت‌ها از فایل مرکزی ---
from .states import StaffStates

# --- وارد کردن تمام توابع هندلر از ماژول‌های مختلف ---
# توابع ثبت‌نام
from ..registration import (
    start_command,
    receive_full_name,
    receive_password,
    select_hospital,
    select_unit,
    registration_cancel,
)
# توابع پنل کاربری
from .menu_logic import back_to_main_menu_handler, exit_panel_handler
from .schedule.schedule_handler import show_schedule_handler, navigate_schedule_handler, export_schedule_handler
from .requests.requests_handler import * # وارد کردن تمام هندلرهای درخواست‌ها
from .patterns.patterns_handler import view_patterns_handler
from .swap.swap_handler import * # وارد کردن تمام هندلرهای جابجایی
from .swap.request_management_handler import * # وارد کردن تمام هندلرهای مدیریت درخواست جابجایی


# --- تعریف ConversationHandler جامع و اصلی ---
main_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_command) # نقطه ورود واحد برای کل ربات
    ],
    states={
        # --- وضعیت‌های ثبت‌نام ---
        StaffStates.AWAIT_FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_full_name)],
        StaffStates.AWAIT_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)],
        StaffStates.SELECT_HOSPITAL: [CallbackQueryHandler(select_hospital, pattern="^reg_hospital_")],
        StaffStates.SELECT_UNIT: [CallbackQueryHandler(select_unit, pattern="^reg_unit_")],

        # --- وضعیت‌های پنل Staff ---
        StaffStates.MAIN_MENU: [
            CallbackQueryHandler(show_schedule_handler, pattern="^show_schedule$"),
            CallbackQueryHandler(manage_requests_entry, pattern="^manage_requests$"),
            CallbackQueryHandler(view_patterns_handler, pattern="^view_patterns$"),
            CallbackQueryHandler(initiate_swap_handler, pattern="^initiate_swap_"),
            CallbackQueryHandler(show_my_sent_requests_handler, pattern="^my_sent_requests$"),
            CallbackQueryHandler(show_incoming_requests_handler, pattern="^incoming_requests_inbox$"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
            CallbackQueryHandler(exit_panel_handler, pattern="^exit_panel$"),
        ],
        StaffStates.SHOWING_SCHEDULE: [
            CallbackQueryHandler(navigate_schedule_handler, pattern="^nav_schedule_"),
            CallbackQueryHandler(export_schedule_handler, pattern="^export_schedule_ics_"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
        StaffStates.REQUESTS_MENU: [
            CallbackQueryHandler(new_request_handler, pattern="^req_new$"),
            CallbackQueryHandler(track_requests_handler, pattern="^req_track$"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
        StaffStates.REQUEST_CHOOSE_TYPE: [
            CallbackQueryHandler(choose_request_type_handler, pattern="^req_type_"),
            CallbackQueryHandler(manage_requests_entry, pattern="^req_back_to_menu$"),
        ],
        StaffStates.REQUEST_CHOOSE_DATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, choose_request_date_handler)
        ],
        StaffStates.REQUEST_CHOOSE_SHIFT_TYPE: [
            CallbackQueryHandler(choose_shift_type_handler, pattern="^req_shift_"),
            CallbackQueryHandler(manage_requests_entry, pattern="^req_back_to_date$"),
        ],
        StaffStates.REQUEST_TRACKING: [
            CallbackQueryHandler(delete_request_handler, pattern="^req_delete_"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
        StaffStates.VIEWING_PATTERNS: [
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
        StaffStates.SWAP_SELECT_SHIFT: [
            CallbackQueryHandler(select_shift_for_swap_handler, pattern="^swap_select_shift_"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
        StaffStates.SWAP_SELECT_TARGET_DAY: [
            CallbackQueryHandler(select_target_day_handler, pattern="^swap_select_day_"),
            CallbackQueryHandler(initiate_swap_handler, pattern="^swap_back_to_shift_select$"),
            CallbackQueryHandler(back_to_day_selection_handler, pattern="^swap_back_to_day_select$"),
        ],
        StaffStates.SWAP_SELECT_TARGETS: [
            CallbackQueryHandler(toggle_target_handler, pattern="^swap_toggle_target_"),
            CallbackQueryHandler(confirm_target_selection_handler, pattern="^swap_confirm_selection$"),
            # بازگشت به مرحله انتخاب روز
            CallbackQueryHandler(back_to_day_selection_handler, pattern="^swap_back_to_day_select$"),

        ],
        StaffStates.SWAP_CONFIRM: [
            CallbackQueryHandler(send_final_swap_request_handler, pattern="^swap_send_final$"),
            # بازگشت به مرحله انتخاب همکاران با استفاده از تابع جدید
            CallbackQueryHandler(back_to_target_selection_handler, pattern="^swap_back_to_target_select$"),

        ],
        StaffStates.VIEWING_MY_SWAPS: [
            CallbackQueryHandler(delete_my_sent_request_handler, pattern="^my_req_delete_"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
        StaffStates.VIEWING_INCOMING_SWAPS: [
            CallbackQueryHandler(process_incoming_request_handler, pattern="^inc_req_process_"),
            CallbackQueryHandler(back_to_main_menu_handler, pattern="^back_to_main_menu$"),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", registration_cancel),
        CommandHandler("start", start_command)
    ],
    per_user=True,
    per_chat=True,
)