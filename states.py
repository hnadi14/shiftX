# bot/handlers/manager_panel/states.py
# این فایل تمام وضعیت‌های مکالمه پنل مدیر را به صورت متمرکز نگهداری می‌کند.

(
    # --- جریان اصلی پنل ---
    SELECT_UNIT,
    UNIT_MENU,

    # --- جریان فرعی مدیریت انواع شیفت ---
    SHIFT_MGMT_MENU,
    AWAIT_SHIFT_NAME,
    AWAIT_SHIFT_WEIGHT,
    SELECT_SHIFT_TO_EDIT,
    AWAIT_NEW_SHIFT_DETAILS,
    SELECT_SHIFT_TO_DELETE,
    CONFIRM_DELETE_SHIFT,

    # --- جریان فرعی تعریف نیازمندی شیفت ---
    REQS_SELECT_SECTION,
    REQS_SELECT_MONTH,
    REQS_SELECT_DAY,
    REQS_SELECT_SHIFT_TYPE,
    REQS_AWAIT_STAFF_COUNT,
    REQS_SEQUENTIAL_INPUT,

    # --- جریان پرسنل واحد ---
    UNIT_STAFF_LIST,
    STAFF_MENU,

    # --- جریان مدیریت الگوها ---
    PATTERN_MENU,
    ADD_PATTERN_DETAILS,
    SELECT_SHIFT,
    SELECT_MULTIPLE_SHIFTS,
    SELECT_CO_WORKER,
    VIEW_PATTERNS,
    DELETE_PATTERN,
    SELECT_PATTERN_TO_DELETE,
    CONFIRM_DELETE,
    ADD_ANOTHER_COMBINATION,

    # --- مدیریت واحد و بخش پرسنل ---
    PERSONAL_SECTIONS_LIST,
    ADD_SECTION,
    CONFIRM_DELETE_SECTION,
    CONFIRM_DELETE_UNIT,

    # --- وضعیت‌های جدید برای نمایش تقویمی نیازمندی‌ها ---
    REQUIREMENTS_CALENDAR_VIEW,
    REQUIREMENTS_DAILY_VIEW,

    # --- وضعیت‌های جدید برای تخصیص شیفت (برنامه) ---
    ASSIGNMENT_MENU,  # منوی اصلی تخصیص شیفت
    GENERATE_SCHEDULE,  # تولید برنامه برای ماه بعد
    VIEW_SCHEDULE_SELECT_YEAR,  # انتخاب سال برای مشاهده برنامه
    VIEW_SCHEDULE_SELECT_MONTH,  # انتخاب ماه
    VIEW_SCHEDULE_CALENDAR,  # نمایش تقویم ماه
    VIEW_DAY_DETAILS,  # جزئیات یک روز خاص
    DELETE_SHIFT_SELECT,  # انتخاب شیفت برای حذف
    ADD_SHIFT_SELECT,  # انتخاب شیفت/بخش برای اضافه کردن
    SWAP_SHIFT_SELECT,  # انتخاب شیفت مبدأ برای جابه‌جایی
    REPORTS_MENU,  # منوی گزارش‌ها
    REPORT_SINGLE_SELECT_STAFF,  # انتخاب پرسنل برای گزارش تک کاربر
    CONFIRM_ACTION,  # تایید عملیات حساس (حذف/اضافه/جابه‌جایی)
    SWAP_AWAIT_TARGET_DAY,  # [NEW] منتظر دریافت روز مقصد برای جابجایی
    REVIEW_CHANGE_REQUESTS, # [NEW] وضعیت جدید برای بررسی درخواست‌های جابجایی

    # [NEW] وضعیت‌های جدید برای جریان حذف پیشنهادی
    SUGGEST_DELETE_SELECT_SHIFT,
    SUGGEST_DELETE_SELECT_CANDIDATE,

    # وضعیت‌های جدید برای جریان گزارش فردی
    REPORT_SINGLE_SELECT_YEAR,
    REPORT_SINGLE_SELECT_MONTH,

) = range(51)  # به‌روزرسانی تعداد کل وضعیت‌ها
