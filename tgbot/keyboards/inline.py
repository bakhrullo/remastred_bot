from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext

back_btn = InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back")
back_kb = InlineKeyboardMarkup().add(back_btn)

buy_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(_("✅ Xarid qilish"), callback_data="confirm"),
    back_btn)


async def settings_btns(locale=False):
    settings_kb = InlineKeyboardMarkup(row_width=1)
    if locale:
        settings_kb.add(
            InlineKeyboardButton(_("🔄 Tilni o'zgartirish", locale=locale), callback_data="change_lang"),
            InlineKeyboardButton(_("📞 Telefon raqamni o'zgartirish", locale=locale), callback_data="change_phone"),
            InlineKeyboardButton(_("🔙 Orqaga", locale=locale), callback_data="back"))
    else:
        settings_kb.add(
            InlineKeyboardButton(_("🔄 Tilni o'zgartirish"), callback_data="change_lang"),
            InlineKeyboardButton(_("📞 Telefon raqamni o'zgartirish"), callback_data="change_phone"),
            InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return settings_kb


async def lang_btns(back):
    lang_btn = InlineKeyboardMarkup(row_with=1).add(InlineKeyboardButton("uz 🇺🇿", callback_data="languz"),
                                                    InlineKeyboardButton("ru 🇷🇺", callback_data="langru"),
                                                    InlineKeyboardButton("en 🇺🇸", callback_data="langen"))
    if back:
        lang_btn.add(InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return lang_btn


async def main_menu_btns(cats, lang):
    main_menu_btn = InlineKeyboardMarkup(row_width=1)
    for cat in cats:
        main_menu_btn.insert(InlineKeyboardButton(cat[f'name_{lang}'], callback_data=cat['id']))
    main_menu_btn.add(
            InlineKeyboardButton(_("Siz uchun maxsus 🎁"), callback_data="contact"),
            InlineKeyboardButton(_("Sozlamalar ⚙️"), callback_data="settings")
            )
    return main_menu_btn


async def cat_btns(cats, lang):
    cat_btn = InlineKeyboardMarkup(row_width=1)
    for cat in cats:
        cat_btn.insert(InlineKeyboardButton(cat[f'name_{lang}'], callback_data=cat['id']))
    cat_btn.insert(back_btn)
    return cat_btn


async def prod_btns(prods, lang):
    prod_btn = InlineKeyboardMarkup(row_width=1)
    for prod in prods:
        prod_btn.insert(InlineKeyboardButton(_("{name}\n{price} so'm").format(name=prod[f'name_{lang}'],
                                                                              price=prod['price']),
                                             callback_data=prod['id']))
    prod_btn.insert(back_btn)
    return prod_btn

