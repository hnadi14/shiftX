# bot/handlers/manager_panel/main_menu.py
# نسخه نهایی با ساختار صحیح ConversationHandler برای ناوبری بدون خطا

from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ConversationHandler,
    MessageHandler, filters
)
from .personal_callbacks import (
    unit_staff_entry, staff_menu_entry,
    back_to_staff_list, view_all_month_requests, process_request_action
)
from .pattern_callbacks import (
    pattern_menu_entry, view_patterns,
    select_pattern_to_delete, confirm_delete, back_to_pattern_menu,
    back_to_staff_menu
)
from .add_pattern_callbacks import (
    add_pattern_entry, select_pattern_type, set_pattern_type, select_shift,
    set_shift, toggle_shift_selection, confirm_shift_selection, set_days, set_max_shifts,
    handle_max_shifts_input, set_max_night_shifts, handle_max_night_shifts_input,
    set_max_total_weight, handle_max_total_weight_input, set_max_holiday_shifts,
    handle_max_holiday_shifts_input, set_rotation_pattern, handle_rotation_pattern_input,
    set_priority, handle_priority, select_co_worker, set_co_worker, confirm_pattern,
    back_to_pattern_details
)
from .callbacks import (
    panel_start, select_unit_handler, exit_panel, shift_management_entry,
    ask_for_shift_name, receive_shift_name, receive_shift_weight_and_add,
    select_shift_to_edit, ask_for_new_shift_details, receive_new_shift_details_and_edit,
    select_shift_to_delete, confirm_delete_shift, execute_delete_shift
)
from .requirements_callbacks import (
    requirements_entry, select_section_for_reqs, select_month_for_reqs,
    select_day_for_reqs, select_shift_type_for_reqs, receive_staff_count_for_reqs,
    show_requirements_report, start_sequential_reqs, receive_sequential_req_input,
    copy_last_month_requirements
)
from .personal_unit_callbacks import (
    manage_personal_unit_entry,
    show_add_section_menu,
    add_section_to_personal_and_refresh,
    confirm_section_deletion,
    delete_section_and_refresh,
    set_main_section_and_refresh,
    confirm_unit_deletion,
    delete_unit_and_refresh
)
# [FINAL CHANGE] Import all new and existing handlers
from .heuristic_assignment.callbacks_heuristic import (
    assignment_menu_entry, generate_schedule_handler, execute_generate_schedule,
    view_schedule_handler, view_select_year_handler,
    view_day_details_handler, back_to_assignment_menu, delete_shift_day_handler,
    delete_shift_select_handler, add_shift_day_handler, add_shift_select_shift_handler,
    swap_shift_day_handler, swap_shift_select_handler, confirm_action_handler,
    swap_receive_target_day_handler,
    suggest_delete_start_handler, suggest_delete_select_shift_handler, suggest_delete_select_candidate_handler,
    reports_menu_handler, report_full_select_year_handler,
    report_single_show_handler,
    dispatch_month_selection, report_single_select_year_handler, report_single_select_month_handler,
    report_single_select_staff_handler,
    publish_schedule_handler, review_requests_entry, toggle_request_status_handler
)

from .states import *


manager_panel_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("panel", panel_start)],
    states={
        SELECT_UNIT: [
            CallbackQueryHandler(select_unit_handler, pattern=r"^manage_unit_\d+$"),
            CallbackQueryHandler(exit_panel, pattern=r"^exit_panel$")
        ],
        UNIT_MENU: [
            CallbackQueryHandler(assignment_menu_entry, pattern=r"^assignment_menu_\d+$"),
            CallbackQueryHandler(shift_management_entry, pattern=r"^manage_shifts_\d+$"),
            CallbackQueryHandler(requirements_entry, pattern=r"^reqs_\d+$"),
            CallbackQueryHandler(unit_staff_entry, pattern=r"^unit_staff$"),
            CallbackQueryHandler(panel_start, pattern=r"^back_to_unit_list$")
        ],
        UNIT_STAFF_LIST: [
            CallbackQueryHandler(staff_menu_entry, pattern=r"^staff_\d+$"),
            CallbackQueryHandler(select_unit_handler, pattern=r"^manage_unit_\d+$"),
            CallbackQueryHandler(manage_personal_unit_entry, pattern=r"^manage_personal_unit_\d+$"),
        ],
        STAFF_MENU: [
            CallbackQueryHandler(pattern_menu_entry, pattern=r"^pattern_menu_\d+$"),
            CallbackQueryHandler(view_all_month_requests, pattern=r"^view_requests_\d+$"),
            CallbackQueryHandler(process_request_action, pattern=r"^request_\d+_(Pending|Approved|Rejected)$"),
            CallbackQueryHandler(back_to_staff_list, pattern=r"^back_to_staff_list$"),
            CallbackQueryHandler(back_to_staff_menu, pattern=r"^back_to_staff_menu_\d+$"),

        ],
        PATTERN_MENU: [
            CallbackQueryHandler(view_patterns, pattern=r"^view_patterns_\d+$"),
            CallbackQueryHandler(add_pattern_entry, pattern=r"^add_pattern_\d+$"),
            CallbackQueryHandler(pattern_menu_entry, pattern=r"^pattern_menu_\d+$"),
            CallbackQueryHandler(back_to_staff_menu, pattern=r"^back_to_staff_menu_\d+$"),
        ],
        VIEW_PATTERNS: [
            CallbackQueryHandler(select_pattern_to_delete, pattern=r"^delete_pattern_select_\d+$"),
            CallbackQueryHandler(back_to_pattern_menu, pattern=r"^pattern_menu_\d+$")
        ],
        CONFIRM_DELETE: [
            CallbackQueryHandler(confirm_delete, pattern=r"^confirm_delete$"),
            CallbackQueryHandler(back_to_pattern_menu, pattern=r"^pattern_menu_\d+$")
        ],
        ADD_PATTERN_DETAILS: [
            CallbackQueryHandler(set_pattern_type, pattern=r"^pattern_type_.*$"),
            CallbackQueryHandler(toggle_shift_selection, pattern=r"^toggle_shift_\d+$"),
            CallbackQueryHandler(confirm_shift_selection, pattern=r"^confirm_shift_selection$"),
            CallbackQueryHandler(set_days, pattern=r"^(week_day_even|week_day_odd)$"),
            CallbackQueryHandler(handle_priority, pattern=r"^priority_(high|medium|low)$"),
            CallbackQueryHandler(set_co_worker, pattern=r"^co_worker_\d+$"),
            CallbackQueryHandler(set_co_worker, pattern=r"^no_co_worker$"),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                lambda u, c: handle_max_shifts_input(u, c) if c.user_data.get("awaiting_max_shifts")
                else handle_max_night_shifts_input(u, c) if c.user_data.get("awaiting_max_night_shifts")
                else handle_max_total_weight_input(u, c) if c.user_data.get("awaiting_max_total_weight")
                else handle_max_holiday_shifts_input(u, c) if c.user_data.get("awaiting_max_holiday_shifts")
                else handle_rotation_pattern_input(u, c) if c.user_data.get("awaiting_rotation_pattern")
                else None
            )
        ],
        # --- START OF CHANGES ---
        # وضعیت‌های جدید برای جریان افزودن الگو
        SELECT_SHIFT: [
            CallbackQueryHandler(set_shift, pattern=r"^shift_\d+$"),
            CallbackQueryHandler(back_to_pattern_details, pattern=r"^back_to_pattern_details$"),
        ],
        SELECT_MULTIPLE_SHIFTS: [
            CallbackQueryHandler(toggle_shift_selection, pattern=r"^toggle_shift_\d+$"),
            CallbackQueryHandler(confirm_shift_selection, pattern=r"^confirm_shift_selection$"),
            CallbackQueryHandler(back_to_pattern_details, pattern=r"^back_to_pattern_details$"),
        ],
        SELECT_CO_WORKER: [
            CallbackQueryHandler(set_co_worker, pattern=r"^co_worker_.*$"),
            CallbackQueryHandler(back_to_pattern_details, pattern=r"^back_to_pattern_details$"),
        ],
        # --- END OF CHANGES ---

        SHIFT_MGMT_MENU: [
            CallbackQueryHandler(ask_for_shift_name, pattern=r"^add_shift$"),
            CallbackQueryHandler(select_shift_to_edit, pattern=r"^edit_shift$"),
            CallbackQueryHandler(select_shift_to_delete, pattern=r"^delete_shift$"),
            CallbackQueryHandler(select_unit_handler, pattern=r"^manage_unit_\d+$")
        ],
        AWAIT_SHIFT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_shift_name)],
        AWAIT_SHIFT_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_shift_weight_and_add)],
        SELECT_SHIFT_TO_EDIT: [
            CallbackQueryHandler(ask_for_new_shift_details, pattern=r"^shift_edit_\d+$"),
            CallbackQueryHandler(shift_management_entry, pattern=r"^back_to_shift_menu$")
        ],
        AWAIT_NEW_SHIFT_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_shift_details_and_edit)],
        SELECT_SHIFT_TO_DELETE: [
            CallbackQueryHandler(confirm_delete_shift, pattern=r"^shift_delete_\d+$"),
            CallbackQueryHandler(shift_management_entry, pattern=r"^back_to_shift_menu$")
        ],
        CONFIRM_DELETE_SHIFT: [
            CallbackQueryHandler(execute_delete_shift, pattern=r"^shift_delete_confirm_\d+$"),
            CallbackQueryHandler(shift_management_entry, pattern=r"^back_to_shift_menu$")
        ],
        REQS_SELECT_SECTION: [
            CallbackQueryHandler(select_section_for_reqs, pattern=r"^req_select_section_\d+$"),
            CallbackQueryHandler(select_unit_handler, pattern=r"^manage_unit_\d+$")
        ],
        REQS_SELECT_MONTH: [
            CallbackQueryHandler(select_month_for_reqs, pattern=r"^req_select_month_\d{4}_\d{1,2}$"),
            CallbackQueryHandler(requirements_entry, pattern=r"^back_to_section_select$")
        ],
        REQS_SELECT_DAY: [
            CallbackQueryHandler(copy_last_month_requirements, pattern=r"^req_copy_last_month$"),
            CallbackQueryHandler(start_sequential_reqs, pattern=r"^req_start_sequential$"),
            CallbackQueryHandler(show_requirements_report, pattern=r"^req_show_report$"),
            CallbackQueryHandler(select_day_for_reqs, pattern=r"^req_select_day_\d+$"),
            CallbackQueryHandler(select_month_for_reqs, pattern=r"^back_to_month_select$")
        ],
        REQS_SELECT_SHIFT_TYPE: [
            CallbackQueryHandler(select_shift_type_for_reqs, pattern=r"^req_select_shift_\d+$"),
            CallbackQueryHandler(select_month_for_reqs, pattern=r"^back_to_calendar$")
        ],
        REQS_AWAIT_STAFF_COUNT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_staff_count_for_reqs),
            CallbackQueryHandler(select_shift_type_for_reqs, pattern=r"^back_to_shift_select$")
        ],
        REQS_SEQUENTIAL_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sequential_req_input)],
        PERSONAL_SECTIONS_LIST: [
            CallbackQueryHandler(show_add_section_menu, pattern=r"^add_personal_section_menu_\d+$"),
            CallbackQueryHandler(confirm_section_deletion, pattern=r"^delete_personal_section_\d+_\d+$"),
            CallbackQueryHandler(set_main_section_and_refresh, pattern=r"^set_main_section_\d+_\d+$"),
            CallbackQueryHandler(confirm_unit_deletion, pattern=r"^confirm_delete_personal_unit_\d+$"),
            CallbackQueryHandler(back_to_staff_list, pattern=r"^back_to_staff_list$"),
        ],
        ADD_SECTION: [
            CallbackQueryHandler(add_section_to_personal_and_refresh, pattern=r"^add_personal_section_\d+_\d+$"),
            CallbackQueryHandler(manage_personal_unit_entry, pattern=r"^manage_personal_unit_\d+$"),
        ],
        CONFIRM_DELETE_SECTION: [
            CallbackQueryHandler(delete_section_and_refresh, pattern=r"^execute_delete_section_\d+_\d+$"),
            CallbackQueryHandler(manage_personal_unit_entry, pattern=r"^manage_personal_unit_\d+$"),
        ],
        CONFIRM_DELETE_UNIT: [
            CallbackQueryHandler(delete_unit_and_refresh, pattern=r"^execute_delete_unit_\d+$"),
            CallbackQueryHandler(manage_personal_unit_entry, pattern=r"^manage_personal_unit_\d+$"),
        ],

        ASSIGNMENT_MENU: [
            CallbackQueryHandler(generate_schedule_handler, pattern=r"^generate_schedule_\d+$"),
            CallbackQueryHandler(view_schedule_handler, pattern=r"^view_schedule_\d+$"),
            CallbackQueryHandler(publish_schedule_handler, pattern=r"^publish_schedule_\d+$"),
            CallbackQueryHandler(review_requests_entry, pattern=r"^review_requests_\d+$"),
            CallbackQueryHandler(reports_menu_handler, pattern=r"^reports_menu_\d+$"),
            CallbackQueryHandler(select_unit_handler, pattern=r"^manage_unit_\d+$")
        ],
        REVIEW_CHANGE_REQUESTS: [
            CallbackQueryHandler(toggle_request_status_handler, pattern=r"^toggle_request_\d+$"),
            CallbackQueryHandler(review_requests_entry, pattern=r"^review_requests_\d+$"), # For refresh
            CallbackQueryHandler(assignment_menu_entry, pattern=r"^assignment_menu_\d+$"), # FIX: Call the entry function directly
            CallbackQueryHandler(back_to_assignment_menu, pattern=r"^back_to_assignment_menu_\d+$")
        ],
        GENERATE_SCHEDULE: [
            CallbackQueryHandler(execute_generate_schedule, pattern=r"^execute_generate_\d+_\d+_\d+$"),
            CallbackQueryHandler(back_to_assignment_menu, pattern=r"^assignment_menu_\d+$"),
        ],
        VIEW_SCHEDULE_SELECT_YEAR: [
            CallbackQueryHandler(view_select_year_handler, pattern=r"^view_select_year_\d+_\d+$"),
            CallbackQueryHandler(back_to_assignment_menu, pattern=r"^assignment_menu_\d+$"),
            CallbackQueryHandler(reports_menu_handler, pattern=r"^reports_menu_\d+$"),
        ],
        VIEW_SCHEDULE_SELECT_MONTH: [
            CallbackQueryHandler(dispatch_month_selection, pattern=r"^view_select_month_\d+_\d+_\d+$"),
            CallbackQueryHandler(view_schedule_handler, pattern=r"^view_schedule_\d+$"),
        ],
        VIEW_SCHEDULE_CALENDAR: [
            CallbackQueryHandler(view_day_details_handler, pattern=r"^view_day_details_\d+_\d+_\d+_\d+$"),
            CallbackQueryHandler(view_select_year_handler, pattern=r"^view_select_year_\d+_\d+$"),
        ],
        VIEW_DAY_DETAILS: [
            CallbackQueryHandler(add_shift_day_handler, pattern=r"^add_shift_day_.*$"),
            CallbackQueryHandler(delete_shift_day_handler, pattern=r"^delete_shift_day_.*$"),
            CallbackQueryHandler(swap_shift_day_handler, pattern=r"^swap_shift_day_.*$"),
            CallbackQueryHandler(suggest_delete_start_handler, pattern=r"^suggest_delete_start_.*$"),
            CallbackQueryHandler(dispatch_month_selection, pattern=r"^view_select_month_.*$"),
        ],
        DELETE_SHIFT_SELECT: [
            CallbackQueryHandler(delete_shift_select_handler, pattern=r"^delete_shift_select_.*$"),
            CallbackQueryHandler(view_day_details_handler, pattern=r"^view_day_details_.*$"),
        ],
        ADD_SHIFT_SELECT: [
            CallbackQueryHandler(add_shift_select_shift_handler, pattern=r"^add_shift_select_.*$"),
            CallbackQueryHandler(view_day_details_handler, pattern=r"^view_day_details_.*$"),
        ],
        SWAP_SHIFT_SELECT: [
            CallbackQueryHandler(swap_shift_select_handler, pattern=r"^swap_shift_select_.*$"),
            CallbackQueryHandler(view_day_details_handler, pattern=r"^view_day_details_.*$"),
        ],
        SWAP_AWAIT_TARGET_DAY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, swap_receive_target_day_handler),
            CallbackQueryHandler(swap_shift_day_handler, pattern=r"^swap_shift_day_.*$"),
        ],
        SUGGEST_DELETE_SELECT_SHIFT: [
            CallbackQueryHandler(suggest_delete_select_shift_handler, pattern=r"^sugg_del_select_.*$"),
            CallbackQueryHandler(view_day_details_handler, pattern=r"^view_day_details_.*$"),
        ],
        SUGGEST_DELETE_SELECT_CANDIDATE: [
            CallbackQueryHandler(suggest_delete_select_candidate_handler, pattern=r"^sugg_del_confirm_.*$"),
            CallbackQueryHandler(suggest_delete_start_handler, pattern=r"^suggest_delete_start_.*$"),
        ],
        # [FIX] The CONFIRM_ACTION state is now aware of all possible "back" button callbacks
        # from different flows (add, swap, delete) that lead to it.
        CONFIRM_ACTION: [
            CallbackQueryHandler(confirm_action_handler, pattern=r"^confirm_action_.*$"),
            # For the back button from the delete confirmation menu
            CallbackQueryHandler(view_day_details_handler, pattern=r"^view_day_details_.*$"),
            # For the back button from the add-shift-staff-selection menu
            CallbackQueryHandler(add_shift_day_handler, pattern=r"^add_shift_day_.*$"),
            # For the back button from the swap-shift-target-selection menu
            CallbackQueryHandler(swap_shift_day_handler, pattern=r"^swap_shift_day_.*$"),
        ],
        REPORTS_MENU: [
            CallbackQueryHandler(report_full_select_year_handler, pattern=r"^report_full_entry_\d+$"),
            CallbackQueryHandler(report_single_select_year_handler, pattern=r"^report_single_entry_\d+$"),
            CallbackQueryHandler(back_to_assignment_menu, pattern=r"^assignment_menu_\d+$"),
        ],
        REPORT_SINGLE_SELECT_YEAR: [
            CallbackQueryHandler(report_single_select_month_handler, pattern=r"^rs_select_year_\d+_\d+$"),
            CallbackQueryHandler(reports_menu_handler, pattern=r"^reports_menu_\d+$"),
        ],
        REPORT_SINGLE_SELECT_MONTH: [
            CallbackQueryHandler(report_single_select_staff_handler, pattern=r"^rs_select_month_\d+_\d+_\d+$"),
            CallbackQueryHandler(report_single_select_year_handler, pattern=r"^report_single_entry_\d+$"),
        ],
        REPORT_SINGLE_SELECT_STAFF: [
            CallbackQueryHandler(report_single_show_handler, pattern=r"^report_single_show_\d+_\d+$"),
            # [FIXED] This handler now correctly returns the user to the staff list.
            CallbackQueryHandler(report_single_select_staff_handler, pattern=r"^rs_select_month_.*$"),
            # This handler correctly returns the user from the staff list to the month selection.
            CallbackQueryHandler(report_single_select_month_handler, pattern=r"^rs_select_year_.*$"),
        ],
    },
    fallbacks=[
        CommandHandler("panel", panel_start),
        CallbackQueryHandler(exit_panel, pattern=r"^exit_panel$")
    ],
    per_user=True,
    per_chat=True
)

