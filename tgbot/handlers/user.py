from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.db.db_api import update_user, get_cats, get_prods, list_glob_cats, \
    get_list_prods, get_prods_search
from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import lang_btns, settings_btns, cat_btns, prod_btns, buy_kb, back_kb, \
    search_btns, role_kb, main_menu_kb
from tgbot.keyboards.reply import contact_btn, remove_btn
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import UserStartState, UserMenuState, UserSettings, UserBuyState, UserSearch, UserFeedback
from tgbot.services.code import send_code

_ = i18ns.gettext
__ = i18ns.lazy_gettext


async def user_start(m: Message, status, user):
    if status:
        if user["name"] is None:
            await m.answer(_("Iltimos ismingizni kiriting 👤"))
            await UserStartState.get_name.set()
        elif user["phone"] is None:
            await m.answer(_("Iltimos telefon raqamingizni kiriting yoki tugmacha orqali yuboring 📲"),
                           reply_markup=contact_btn)
            await UserStartState.get_contact.set()
        elif user["role"] is None:
            await m.answer(_("O'z sohangizni tanlang 👇"), reply_markup=role_kb)
            await UserStartState.get_role.set()
        else:
            await m.answer(_("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇"),
                           reply_markup=main_menu_kb)
            await UserMenuState.get_menu.set()
    else:
        await m.reply(_("Assalomu alaykum 👋\nBotimizga xush kelibsiz iltimos tilni tanlang!"),
                      reply_markup=lang_btns(False))
        await UserStartState.get_lang.set()


async def get_lang(c: CallbackQuery, config):
    lang = c.data.replace("lang", "")
    await update_user(user_id=c.from_user.id, config=config, data={"lang": lang})
    await c.message.edit_text(_("Iltimos ismingizni kiriting 👤", locale=lang))
    await UserStartState.next()


async def get_name(m: Message, config):
    await update_user(user_id=m.from_user.id, config=config, data={"name": m.text})
    await m.answer(_("Iltimos telefon raqamingizni kiriting yoki tugmacha orqali yuboring 📲"),
                   reply_markup=contact_btn)
    await UserStartState.next()


async def get_contact(m: Message, state: FSMContext, config):
    phone = m.contact.phone_number
    code = await send_code(phone, config)
    await state.update_data(code=code, phone=phone)
    await m.answer(_("Iltimos telefon raqamingizga kelgan sms kodni kiriting 📲"), reply_markup=remove_btn)
    await UserStartState.next()


async def get_code(m: Message, state: FSMContext, config):
    data, code = await state.get_data(), m.text
    if code == str(data["code"]):
        await update_user(user_id=m.from_user.id, config=config, data={"phone": data["phone"]})
        await m.answer(_("O'z sohangizni tanlang 👇"), reply_markup=role_kb)
        await UserMenuState.get_menu.set()
    else:
        await m.answer("Notog'ri kod yuborildi ❌\nIltimos qayta urinib ko'ring! 🔄")


async def get_role(c: CallbackQuery, config):
    await update_user(user_id=c.from_user.id, config=config, data={"role": c.data})
    await c.message.edit_text(_("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇"),
                              reply_markup=main_menu_kb)
    await UserMenuState.get_menu.set()


async def feedback(c: CallbackQuery):
    await c.message.edit_text(
        "Bu bo'limda siz bizga izoh yozib qoldirishingiz mumkin, biz izoh bilan tanishib chiqib siz bilan bog'lanamiz ⏳",
        reply_markup=back_kb)
    await UserFeedback.get_feedback.set()


async def get_feedback(m: Message, user, config):
    await m.bot.send_message(chat_id=config.tg_bot.channel_id, text=f"👤 Ism: {user['name']}\n"
                                                                    f"📱 Raqam: {user['phone']}\n"
                                                                    f"💬 Izoh: {m.text}")
    await m.answer("Izohingiz uchun rahmat!", reply_markup=main_menu_kb)
    await UserMenuState.get_menu.set()


async def bonus(c: CallbackQuery):
    await
    await c.message.edit_text(
        "Siz xizmatlar bo'limidasiz! Bu bo'lim alohida bo'lim hisoblanib, bu yerda siz mushkulingizni yengil qiluvchi xizmat turlarining raqamlari va ular haqida ma'lumot olish imkoniyatiga ega bo'lasiz Ular bilan tanishing �")



async def settings(c: CallbackQuery):
    await c.message.edit_text(_("Sozlamalar bo'limi 🛠:"), reply_markup=settings_btns())
    await UserSettings.choose.set()


async def change_lang(c: CallbackQuery):
    await c.message.edit_text(_("Tilni tanlang!"), reply_markup=lang_btns(True))
    await UserSettings.get_lang.set()


async def get_lang_set(c: CallbackQuery, config):
    lang = c.data.replace("lang", "")
    await update_user(user_id=c.from_user.id, data={"lang": lang}, config=config)
    await c.message.edit_text(_("Til o'zgartirildi!", locale=lang), reply_markup=settings_btns(lang))
    await UserSettings.choose.set()


async def change_phone(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer(_("Iltimos telefon raqamingizni yuboring 📲"), reply_markup=contact_btn)
    await UserSettings.get_contact.set()


async def get_phone_set(m: Message, state: FSMContext, config):
    phone = m.contact.phone_number
    code = await send_code(phone, config)
    await state.update_data(code=code, phone=phone)
    await m.answer(_("Iltimos telefon raqamingizga kelgan sms kodni kiriting 📲"), reply_markup=remove_btn)
    await UserSettings.get_code.set()


async def get_code_set(m: Message, state: FSMContext, config):
    data, code = await state.get_data(), m.text
    if code == str(data['code']):
        await update_user(m.from_user.id, config, {"phone": data["phone"]})
        await m.answer(_("Raqamingiz o'zgartirildi"), reply_markup=remove_btn)
        await m.answer(_("Sozlamalar bo'limi 🛠:"), reply_markup=settings_btns())
        await UserSettings.choose.set()
    else:
        await m.answer("Notog'ri kod yuborildi ❌\nIltimos qayta urinib ko'ring! 🔄")


async def cats(c: CallbackQuery, lang, config):
    res = await get_cats(config, c.data)
    try:
        await c.message.edit_text(_("{text} bo'limi kategoriyalari 👇").format(text=res[0]["glob_cat"][f"name_{lang}"]),
                                  reply_markup=cat_btns(res, lang))
    except:
        return await c.answer(_("Tovarlar qo'shilmagan ❌"))
    await UserBuyState.get_cat.set()


async def get_cat(c: CallbackQuery, lang, config):
    res = await get_list_prods(c.data, config)
    await c.message.edit_text(_("Modelni tanlang 👇"), reply_markup=prod_btns(res, lang))
    await UserBuyState.next()


async def get_prod(c: CallbackQuery, lang, config):
    res = await get_prods(c.data, config)
    await c.message.edit_text(_("{name}\nm'alumotlar:\n{descr}\n{price} so'm").format(name=res[f'name_{lang}'],
                                                                                      descr=res[f'descr_{lang}'],
                                                                                      price=res['price']),
                              reply_markup=buy_kb)
    await UserBuyState.next()


async def success(c: CallbackQuery):
    await c.message.edit_text(_("Tez orada operatorlarimiz\n siz bilan bog'lanadi 👨‍💻"))


async def search(c: CallbackQuery):
    await c.message.edit_text(_("Qidirayotgan mahsoltingizni kiriting 🔎"))
    await UserSearch.get_name.set()


async def get_search(m: Message, state: FSMContext, lang, config):
    res = await get_prods_search(m.text, lang, config)
    if len(res) == 0:
        return await m.answer(_("Hech nima topilmadi ☹️"), reply_markup=back_kb)
    else:
        kb = await search_btns(res, lang)
        await state.update_data(prod=res[0]["glob_cat"][f"name_{lang}"])
        await UserBuyState.get_cat.set()
        return await m.answer(_("{prod}ning turini tanlang").format(prod=res[0]["glob_cat"][f"name_{lang}"]),
                              reply_markup=kb)


async def back(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer(_("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇"),
                           reply_markup=main_menu_kb)
    await UserMenuState.get_menu.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(get_lang, state=UserStartState.get_lang)
    dp.register_message_handler(get_name, state=UserStartState.get_name)
    dp.register_message_handler(get_contact, content_types="contact", state=UserStartState.get_contact)
    dp.register_message_handler(get_code, state=UserStartState.get_code)
    dp.register_callback_query_handler(get_role, state=UserStartState.get_role)
    dp.register_callback_query_handler(settings, Text(equals="settings"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(feedback, Text(equals="feedback"), state=UserMenuState.get_menu)
    dp.register_message_handler(get_feedback, state=UserFeedback.get_feedback)
    dp.register_callback_query_handler(change_lang, Text(equals="change_lang"), state=UserSettings.choose)
    dp.register_callback_query_handler(get_lang_set, BackFilter(), state=UserSettings.get_lang)
    dp.register_callback_query_handler(change_phone, Text(equals="change_phone"), state=UserSettings.choose)
    dp.register_message_handler(get_phone_set, content_types="contact", state=UserSettings.get_contact)
    dp.register_message_handler(get_code_set, state=UserSettings.get_code)
    dp.register_callback_query_handler(cats, state=UserMenuState.get_menu)
    dp.register_callback_query_handler(get_cat, BackFilter(), state=UserBuyState.get_cat)
    dp.register_callback_query_handler(get_prod, BackFilter(), state=UserBuyState.get_prod)
    dp.register_callback_query_handler(success, BackFilter(), state=UserBuyState.get_conf)
    dp.register_callback_query_handler(search, Text(equals="search"), state=UserBuyState.get_cat)
    dp.register_message_handler(get_search, state=UserSearch.get_name)
    dp.register_callback_query_handler(back, Text(equals="back"), state="*")
