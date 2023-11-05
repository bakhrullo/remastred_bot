from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.misc.i18n import i18ns

_ = i18ns.lazy_gettext

back_btn = InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back")
back_kb = InlineKeyboardMarkup().add(back_btn)

role_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(_("Ishlab chiqaruvchi 👷‍♀️"), callback_data="Ishlab chiqaruvchi"),
    InlineKeyboardButton(_("Ikkalasi ham 👨‍💻️"), callback_data="Ikkalsi ham"),
    InlineKeyboardButton(_("Xaridor  👨️"), callback_data="Xaridor"))

main_menu_kb = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton(_("Qidruv 🔎"), callback_data="search"),
#    InlineKeyboardButton(_("Xizmatlar (bonus) 🚚 "), callback_data="services"),
    InlineKeyboardButton(_("Katalog 📖"), callback_data="catalog"),
    InlineKeyboardButton(_("Sozlamalar ⚙️"), callback_data="settings"),
    InlineKeyboardButton(_("Izoh qoldirish ✏"), callback_data="feedback"))

def settings_btns(locale=None):
    settings_kb = InlineKeyboardMarkup(row_width=1)
    settings_kb.add(
        InlineKeyboardButton(_("🔄 Tilni o'zgartirish", locale=locale), callback_data="change_lang"),
        InlineKeyboardButton(_("📞 Telefon raqamni o'zgartirish", locale=locale), callback_data="change_phone"),
        InlineKeyboardButton(_("🔙 Orqaga", locale=locale), callback_data="back"))
    return settings_kb


def lang_btns(back):
    lang_btn = InlineKeyboardMarkup(row_with=1).add(InlineKeyboardButton("uz 🇺🇿", callback_data="languz"),
                                                    InlineKeyboardButton("ru 🇷🇺", callback_data="langru"),
                                                    InlineKeyboardButton("en 🇺🇸", callback_data="langen"))
    if back:
        lang_btn.add(InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back"))
    return lang_btn


def main_menu_btns(cats, lang):
    main_menu_btn = InlineKeyboardMarkup(row_width=1)
    for cat in cats:
        main_menu_btn.insert(InlineKeyboardButton(cat[f'name_{lang}'], callback_data=cat['id']))
    main_menu_btn.add(
        InlineKeyboardButton(_("Siz uchun maxsus 🎁"), callback_data="contact"),
        InlineKeyboardButton(_("Sozlamalar ⚙️"), callback_data="settings")
    )
    return main_menu_btn


def prod_btns(analogs=False):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(_("Analoglar 🗄"), callback_data="analog"),
           InlineKeyboardButton(_("🔙 Orqaga"), callback_data="back_sub"),
                                   InlineKeyboardButton(_("🏠 Bosh menuga qaytish"), callback_data="back"))
    return kb

def analog_kb(analogs):
    kbs = InlineKeyboardMarkup(row_width=1)
    for analog in analogs:
        kbs.insert(InlineKeyboardButton(text=analog, callback_data=analog))
    kbs.add(InlineKeyboardButton(_("🏠 Bosh menuga qaytish"), callback_data="back"))
    return kbs


def kb_constructor(cats, lang, c_d="back"):
    btn = InlineKeyboardMarkup(row_width=1)
    for cat in cats:
        btn.insert(InlineKeyboardButton(cat[f'name_{lang}'], callback_data=cat['id']))
    btn.insert(InlineKeyboardButton(_("🔙 Orqaga"), callback_data=c_d))
    if c_d != "back":
        btn.insert(InlineKeyboardButton(_("🏠 Bosh menuga qaytish"), callback_data="back"))
    return btn
