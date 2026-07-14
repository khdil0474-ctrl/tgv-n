from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import database as db
from config import MENU_TITLES, CONTENT_MAP, ADMIN_ID
from keyboards import channels_kb, main_menu_kb, submenu_kb, content_view_kb
from subscription import get_not_subscribed

router = Router()


async def register_and_notify(bot: Bot, user_id: int, username: str, full_name: str):
    """Agar foydalanuvchi yangi bo'lsa, bazaga qo'shadi va adminga xabar beradi."""
    if db.user_exists(user_id):
        return
    total = db.add_user(user_id, username, full_name)
    uname_str = f"@{username}" if username else "yo'q"
    text = (
        "🆕 Yangi a'zo botga qo'shildi!\n\n"
        f"👤 Ism: {full_name}\n"
        f"🔗 Username: {uname_str}\n"
        f"🆔 ID: <code>{user_id}</code>\n\n"
        f"📊 Bu — botning <b>{total}</b>-chi foydalanuvchisi!"
    )
    try:
        await bot.send_message(ADMIN_ID, text)
    except Exception:
        pass


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    not_subscribed = await get_not_subscribed(bot, message.from_user.id)
    if not_subscribed:
        await message.answer(
            "👋 Assalomu alaykum!\n\n"
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling, "
            "so'ng <b>✅ Obunani tekshirish</b> tugmasini bosing:",
            reply_markup=channels_kb(),
        )
        return

    await register_and_notify(
        bot,
        message.from_user.id,
        message.from_user.username or "",
        message.from_user.full_name,
    )

    await message.answer(
        "✅ Xush kelibsiz!\n\nQuyidagi bo'limlardan birini tanlang 👇",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == "check_sub")
async def cb_check_sub(callback: CallbackQuery, bot: Bot):
    not_subscribed = await get_not_subscribed(bot, callback.from_user.id)
    if not_subscribed:
        await callback.answer(
            "❗️ Siz hali barcha kanallarga obuna bo'lmadingiz. Iltimos, barchasiga obuna bo'ling.",
            show_alert=True,
        )
        return

    await register_and_notify(
        bot,
        callback.from_user.id,
        callback.from_user.username or "",
        callback.from_user.full_name,
    )

    await callback.message.edit_text(
        "✅ Obuna tasdiqlandi!\n\nQuyidagi bo'limlardan birini tanlang 👇",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "back:main")
async def cb_back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "📍 Bosh menyu\n\nQuyidagi bo'limlardan birini tanlang 👇",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.in_(["menu_dars", "menu_prompt", "menu_sayt", "menu_bot"]))
async def cb_open_menu(callback: CallbackQuery):
    key = callback.data
    title = MENU_TITLES.get(key, "Bo'lim")
    await callback.message.edit_text(
        f"📍 {title}\n\nKerakli bo'limni tanlang 👇",
        reply_markup=submenu_kb(key),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("back:"))
async def cb_back_submenu(callback: CallbackQuery):
    parent_key = callback.data.split(":", 1)[1]
    if parent_key == "main":
        await callback.message.edit_text(
            "📍 Bosh menyu\n\nQuyidagi bo'limlardan birini tanlang 👇",
            reply_markup=main_menu_kb(),
        )
    else:
        title = MENU_TITLES.get(parent_key, "Bo'lim")
        await callback.message.edit_text(
            f"📍 {title}\n\nKerakli bo'limni tanlang 👇",
            reply_markup=submenu_kb(parent_key),
        )
    await callback.answer()


@router.callback_query(F.data.startswith("content:"))
async def cb_show_content(callback: CallbackQuery):
    content_key = callback.data.split(":", 1)[1]
    if content_key not in CONTENT_MAP:
        await callback.answer("Xatolik yuz berdi.", show_alert=True)
        return

    content = db.get_content(content_key)
    title = CONTENT_MAP[content_key]["title"]
    markup = content_view_kb(content_key)

    if not content:
        await callback.message.answer(
            f"📍 {title}\n\n⏳ Hozircha bu bo'lim uchun material qo'shilmagan. Tez orada qo'shiladi!",
            reply_markup=markup,
        )
        await callback.answer()
        return

    ctype = content["content_type"]
    caption = content["text"] or ""

    if ctype == "text":
        await callback.message.answer(caption, reply_markup=markup)
    elif ctype == "photo":
        await callback.message.answer_photo(content["file_id"], caption=caption, reply_markup=markup)
    elif ctype == "video":
        await callback.message.answer_video(content["file_id"], caption=caption, reply_markup=markup)
    elif ctype == "document":
        await callback.message.answer_document(content["file_id"], caption=caption, reply_markup=markup)
    else:
        await callback.message.answer(
            f"📍 {title}\n\n⏳ Hozircha bu bo'lim uchun material qo'shilmagan.",
            reply_markup=markup,
        )

    await callback.answer()
