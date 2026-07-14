from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNELS, MAIN_MENU, CONTENT_MAP, ADMIN_USERNAME


def channels_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ch in CHANNELS:
        builder.add(
            InlineKeyboardButton(
                text=f"📢 {ch['title']}",
                url=f"https://t.me/{ch['username']}",
            )
        )
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")
    )
    return builder.as_markup()


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in MAIN_MENU:
        builder.add(InlineKeyboardButton(text=item["title"], callback_data=item["key"]))
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="📞 Aloqaga chiqish", url=f"https://t.me/{ADMIN_USERNAME}")
    )
    return builder.as_markup()


def submenu_kb(parent_key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, item in CONTENT_MAP.items():
        if item["parent"] == parent_key:
            builder.add(InlineKeyboardButton(text=item["title"], callback_data=f"content:{key}"))
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back:main"))
    return builder.as_markup()


def content_view_kb(content_key: str) -> InlineKeyboardMarkup:
    parent = CONTENT_MAP[content_key]["parent"]
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back:{parent}"))
    return builder.as_markup()


def admin_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="➕ Post/Tugma qo'shish", callback_data="admin_post"))
    builder.add(InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"))
    builder.adjust(2)
    return builder.as_markup()


def admin_select_content_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, item in CONTENT_MAP.items():
        builder.add(
            InlineKeyboardButton(text=item["title"], callback_data=f"admin_select:{key}")
        )
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_cancel"))
    return builder.as_markup()
