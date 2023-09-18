from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.db.db_api import update_user, get_cats, get_prods, get_list_prods, get_prods_search, get_services, \
    get_regions, get_brocks, get_analogs, get_image
from tgbot.filters.back import BackFilter
from tgbot.keyboards.inline import lang_btns, settings_btns, prod_btns, back_kb, role_kb, main_menu_kb, \
    kb_constructor, analog_kb
from tgbot.keyboards.reply import contact_btn, remove_btn
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import UserStartState, UserMenuState, UserSettings, UserSearch, UserFeedback, UserBonus, \
    UserCatalogState
from tgbot.services.code import send_code

_ = i18ns.gettext
__ = i18ns.lazy_gettext


async def user_start(m: Message, status, config, user=None):
    if status == "found":
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
    elif status == "cached":
        #img = await get_image(config, "Bosh menu")
        await m.answer_photo(
            photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
            caption=_("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇"),
            reply_markup=main_menu_kb)
        await UserMenuState.get_menu.set()
    elif status == "created":
        await m.answer(_("Assalomu alaykum 👋\nBotimizga xush kelibsiz iltimos tilni tanlang!"),
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
    if m.content_type == "contact":
        phone = m.contact.phone_number
    else:
        phone = m.text
    code = await send_code(phone, config)
    await state.update_data(code=code, phone=phone)
    await m.answer(_("Iltimos telefon raqamingizga kelgan sms kodni kiriting 📲"), reply_markup=remove_btn)
    await UserStartState.next()


async def get_code(m: Message, state: FSMContext, config):
    data, code = await state.get_data(), m.text
    if code == str(data["code"]):
        await update_user(user_id=m.from_user.id, config=config, data={"phone": data["phone"]})
        await m.answer(_("O'z sohangizni tanlang 👇"), reply_markup=role_kb)
        await UserStartState.next()
    else:
        await m.answer("Notog'ri kod yuborildi ❌\nIltimos qayta urinib ko'ring! 🔄")


async def get_role(c: CallbackQuery, config, redis, lang):
    await update_user(user_id=c.from_user.id, config=config, data={"role": c.data})
    await redis.set(c.from_user.id, lang)
    await c.message.delete()
    await c.message.answer_photo(photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=_("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇"),
        reply_markup=main_menu_kb)
    await UserMenuState.get_menu.set()


async def feedback(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer(_(
        "Bu bo'limda siz bizga izoh yozib qoldirishingiz mumkin, biz izoh bilan tanishib chiqib siz bilan bog'lanamiz ⏳"),
        reply_markup=back_kb)
    await UserFeedback.get_feedback.set()


async def feedback_cmd(m: Message):
    await m.answer(_(
        "Bu bo'limda siz bizga izoh yozib qoldirishingiz mumkin, biz izoh bilan tanishib chiqib siz bilan bog'lanamiz ⏳"),
        reply_markup=back_kb)
    await UserFeedback.get_feedback.set()


async def get_feedback(m: Message, user, config):
    await m.bot.send_message(chat_id=config.tg_bot.channel_id, text=f"👤 Ism: {user['name']}\n"
                                                                    f"📱 Raqam: {user['phone']}\n"
                                                                    f"💬 Izoh: {m.text}")
    await m.answer(_("Izohingiz uchun rahmat!"), reply_markup=main_menu_kb)
    await UserMenuState.get_menu.set()


async def bonus(c: CallbackQuery, config, lang):
    res = await get_brocks(config) #await get_image(config, "Xizmatlar")
    await c.message.delete()
    await c.message.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=_(
            "Siz xizmatlar bo'limidasiz! Bu bo'lim alohida bo'lim hisoblanib, bu yerda siz mushkulingizni yengil qiluvchi "
            "xizmat turlarining raqamlari va ular haqida ma'lumot olish imkoniyatiga ega bo'lasiz Ular bilan tanishing 👇"),
        reply_markup=kb_constructor(cats=res, lang=lang))
    await UserBonus.get_brock.set()


async def bonus_cmd(m: Message, config, lang):
    res = await get_brocks(config) #await get_image(config, "Xizmatlar")
    await m.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=_(
            "Siz xizmatlar bo'limidasiz! Bu bo'lim alohida bo'lim hisoblanib, bu yerda siz mushkulingizni yengil qiluvchi "
            "xizmat turlarining raqamlari va ular haqida ma'lumot olish imkoniyatiga ega bo'lasiz Ular bilan tanishing 👇"),
        reply_markup=kb_constructor(cats=res, lang=lang))
    await UserBonus.get_brock.set()


async def get_brock(c: CallbackQuery, state: FSMContext, config, lang):
    res = await get_regions(config)
    await state.update_data(brock=c.data)
    await c.message.delete()
    await c.message.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=_("Viloyatingizni tanlang"), reply_markup=kb_constructor(res, lang))
    await UserBonus.next()


async def get_region(c: CallbackQuery, state: FSMContext, config, lang):
    data = await state.get_data()
    res = await get_services(config=config, brock=data["brock"], region=c.data)
    if len(res) == 0:
        return await c.answer(_("Ma'lumotlar topilmadi"))
    txt = ""
    for i in res:
        txt += f"👤: {i['name']}\n" \
               f"📱: {i['phone']}\n" \
               f"⚖️: {i['weight']}\n\n"
    await c.message.edit_text(txt, reply_markup=back_kb)


async def settings(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer(_("Sozlamalar bo'limi 🛠:"), reply_markup=settings_btns())
    await UserSettings.choose.set()


async def settings_cmd(m: Message):
    await m.answer(_("Sozlamalar bo'limi 🛠:"), reply_markup=settings_btns())
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
    res = await get_cats(config, "glob") ##await get_image(config, "Bosh kategoriya")
    if len(res) == 0:
        return await c.answer(_("Tovarlar qo'shilmagan ❌"))
    await c.message.delete()
    await c.message.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=_(
            "Katalog bo'limiga xush kelibsiz Siz bu yerda o'zingizga kerakli bo'lgan mahsulotni "
            "toifasi bo'yicha topishingiz mumkin 📃"), reply_markup=kb_constructor(res, lang))
    await UserCatalogState.get_glob_cat.set()


async def cats_cmd(m: Message, lang, config):
    text = _("Katalog bo'limiga xush kelibsiz Siz bu yerda o'zingizga kerakli bo'lgan mahsulotni "
             "toifasi bo'yicha topishingiz mumkin 📃")
    res = await get_cats(config, "glob") #await get_image(config, "Bosh kategoriya	")
    if len(res) == 0:
        return await m.answer(_("Tovarlar qo'shilmagan ❌"), reply_markup=back_kb)
    await m.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=text, reply_markup=kb_constructor(res, lang))
    await UserCatalogState.get_glob_cat.set()


async def get_glob_cat(c: CallbackQuery, lang, config, state: FSMContext):
    await state.update_data(glob_cat_id=c.data)
    text = _("Bo'limi tanlang 👇")
    res = await get_cats(config, "cat", c.data) #await get_image(config, "Bosh kategoriya")
    if len(res) == 0:
        return await c.answer(_("Tovarlar qo'shilmagan ❌"))
    await c.message.delete()
    await c.message.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=text,
        reply_markup=kb_constructor(res, lang, "back_glob"))
    await UserCatalogState.next()


async def get_cat(c: CallbackQuery, lang, config, state: FSMContext):
    res = await get_cats(config, "sub", c.data) #await get_image(config, "Kichik kategoriya")
    await state.update_data(cat_id=c.data)
    if len(res) == 0:
        return await c.answer(_("Tovarlar qo'shilmagan ❌"))
    await c.message.delete()
    await c.message.answer_photo(
        photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
        caption=_("Bo'limi tanlang 👇"),
        reply_markup=kb_constructor(res, lang, "back_cat"))
    await UserCatalogState.next()


async def get_sub_cat(c: CallbackQuery, lang, config, state: FSMContext):
    res = await get_list_prods(c.data, config)
    await state.update_data(sub_cat_id=c.data)
    if len(res) == 0:
        return await c.answer(_("Tovarlar qo'shilmagan ❌"))
    await c.message.delete()
    await c.message.answer(_("Bo'limni tanlang 👇"), reply_markup=prod_btns(res, lang))
    await UserCatalogState.next()


async def get_prod(c: CallbackQuery, lang, config, state: FSMContext):
    res = await get_prods(c.data, config)
    await state.update_data(prod_id=c.data)
    await c.message.edit_text(
        _("🆔 Mahsulot nomi: {name}\n📍 Viloyat/hudud: {region}\n🏙 Ishlab chiqarilgan: {made_in}\n💰 Narxi: {price}\n"
          "📞Telefon raqam: {phone}\n💬 Opisaniya: {descr}").format(name=res[f"name_{lang}"],
                                                                  region=res["region"]
                                                                  [f'name_{lang}'],
                                                                  made_in=res["made_in"],
                                                                  price=res["price"],
                                                                  phone=res["phone"],
                                                                  descr=res[f"descr_{lang}"]),
        reply_markup=analog_kb(c.data))
    await UserCatalogState.next()


async def get_analog(c: CallbackQuery, config, lang):
    res = await get_analogs(config, c.data)
    if len(res) == 0:
        return await c.answer(_("Analoglar topilmadi 😔"))
    await c.message.edit_text(_("Modelni {count} ta analogi topildi 👇").format(count=len(res)),
                              reply_markup=prod_btns(res, lang))
    await UserCatalogState.get_prod.set()


async def search(c: CallbackQuery):
    await c.message.delete()
    await c.message.answer(_("Qidirayotgan mahsoltingizni kiriting 🔎"), reply_markup=back_kb)
    await UserSearch.get_name.set()


async def search_cmd(m: Message):
    await m.answer(_("Qidirayotgan mahsoltingizni kiriting 🔎"), reply_markup=back_kb)
    await UserSearch.get_name.set()


async def get_search(m: Message, lang, config, state: FSMContext):
    res = await get_prods_search(m.text, lang, config)
    if len(res) == 0:
        return await m.answer(_("Hech nima topilmadi ☹️"), reply_markup=back_kb)
    await m.answer(_("Qidiruvingiz bo'yicha {count} ta mahsulot topildi: 🔎 ular bilan tanishing: 👇").
                   format(count=len(res)), reply_markup=prod_btns(res, lang, "back"))
    state_name = await state.get_state()
    if state_name == "UserSearch:get_name":
        await UserSearch.next()


async def get_prod_search(c: CallbackQuery, lang, config, state: FSMContext):
    res = await get_prods(c.data, config)
    await state.update_data(prod_id=c.data)
    await c.message.edit_text(
        _("🆔 Mahsulot nomi: {name}\n📍 Viloyat/hudud: {region}\n🏙 Ishlab chiqarilgan: {made_in}\n💰 Narxi: {price}\n"
          "📞Telefon raqam: {phone}\n💬 Opisaniya: {descr}").format(name=res[f"name_{lang}"],
                                                                  region=res["region"]
                                                                  [f'name_{lang}'],
                                                                  made_in=res["made_in"],
                                                                  price=res["price"],
                                                                  phone=res["phone"],
                                                                  descr=res[f"descr_{lang}"]),
        reply_markup=analog_kb(c.data, "back"))
    await UserSearch.next()


async def get_analog_search(c: CallbackQuery, config, lang):
    res = await get_analogs(config, c.data)
    if len(res) == 0:
        return await c.answer(_("Analoglar topilmadi 😔"))
    await c.message.edit_text(_("Modelni {count} ta analogi topildi 👇").format(count=len(res)),
                              reply_markup=prod_btns(res, lang, "back"))
    await UserSearch.get_prod.set()


async def back(c: CallbackQuery, config, lang, state: FSMContext):
    await c.message.delete()
    data = await state.get_data()
    if c.data == "back":
        #img = await get_image(config, "Bosh menu")
        await c.message.answer_photo(
            photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
            caption=_("Bosh menuga xush kelibsiz. Bo'limlar bilan tanishing! 👇"),
            reply_markup=main_menu_kb)
        return await UserMenuState.get_menu.set()
    elif c.data == "back_glob":
        res = await get_cats(config, "glob") #await get_image(config, "Bosh kategoriya")
        await c.message.answer_photo(
            photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
            caption=_(
                "Katalog bo'limiga xush kelibsiz Siz bu yerda o'zingizga kerakli bo'lgan mahsulotni "
                "toifasi bo'yicha topishingiz mumkin 📃"), reply_markup=kb_constructor(res, lang))
    elif c.data == "back_cat":
        text = _("Bo'limi tanlang 👇")
        res = await get_cats(config, "cat", data["glob_cat_id"]) #await get_image(config, "Bosh kategoriya")
        await c.message.answer_photo(
            photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
            caption=text,
            reply_markup=kb_constructor(res, lang, "back_glob"))
    elif c.data == "back_sub":
        res = await get_cats(config, "sub", data["cat_id"]) #await get_image(config, "Kichik kategoriya")
        await c.message.answer_photo(
            photo="AgACAgQAAxkDAAIDFmUH7hAbaeourxOUZFTpXTlprE1gAALSrjEbwYqFUZbpdHmVk5zfAQADAgADdwADMAQ",
            caption=_("Bo'limi tanlang 👇"),
            reply_markup=kb_constructor(res, lang, "back_cat"))
    elif c.data == "back_prod":
        res = await get_list_prods(data["sub_cat_id"], config)
        await c.message.answer(_("Bo'limni tanlang 👇"), reply_markup=prod_btns(res, lang))
    await UserCatalogState.previous()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(get_lang, state=UserStartState.get_lang)
    dp.register_message_handler(get_name, state=UserStartState.get_name)
    dp.register_message_handler(get_contact, content_types=["contact", "text"], state=UserStartState.get_contact)
    dp.register_message_handler(get_code, state=UserStartState.get_code)
    dp.register_callback_query_handler(get_role, state=UserStartState.get_role)
    dp.register_callback_query_handler(settings, Text(equals="settings"), state=UserMenuState.get_menu)
    dp.register_message_handler(settings_cmd, commands=["settings"], state=UserMenuState.get_menu)
    dp.register_message_handler(cats_cmd, commands=["catalog"], state=UserMenuState.get_menu)
    dp.register_message_handler(feedback_cmd, commands=["feedback"], state=UserMenuState.get_menu)
    dp.register_message_handler(bonus_cmd, commands=["bonus"], state=UserMenuState.get_menu)
    dp.register_message_handler(search_cmd, commands=["search"], state=UserMenuState.get_menu)
    dp.register_callback_query_handler(feedback, Text(equals="feedback"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(bonus, Text(equals="services"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(get_brock, BackFilter(), state=UserBonus.get_brock)
    dp.register_callback_query_handler(get_region, BackFilter(), state=UserBonus.get_region)
    dp.register_message_handler(get_feedback, state=UserFeedback.get_feedback)
    dp.register_callback_query_handler(change_lang, Text(equals="change_lang"), state=UserSettings.choose)
    dp.register_callback_query_handler(get_lang_set, BackFilter(), state=UserSettings.get_lang)
    dp.register_callback_query_handler(change_phone, Text(equals="change_phone"), state=UserSettings.choose)
    dp.register_message_handler(get_phone_set, content_types="contact", state=UserSettings.get_contact)
    dp.register_message_handler(get_code_set, state=UserSettings.get_code)
    dp.register_callback_query_handler(cats, Text(equals="catalog"), state=UserMenuState.get_menu)
    dp.register_callback_query_handler(get_glob_cat, BackFilter(), state=UserCatalogState.get_glob_cat)
    dp.register_callback_query_handler(get_cat, BackFilter(), state=UserCatalogState.get_cat)
    dp.register_callback_query_handler(get_sub_cat, BackFilter(), state=UserCatalogState.get_sub_cat)
    dp.register_callback_query_handler(get_prod, BackFilter(), state=UserCatalogState.get_prod)
    dp.register_callback_query_handler(get_prod_search, BackFilter(), state=UserSearch.get_prod)
    dp.register_callback_query_handler(get_analog, BackFilter(), state=UserCatalogState.get_analog)
    dp.register_callback_query_handler(get_analog_search, BackFilter(), state=UserSearch.get_analog)
    dp.register_callback_query_handler(search, Text(equals="search"), state=UserMenuState.get_menu)
    dp.register_message_handler(get_search, state=[UserSearch.get_name, UserSearch.get_prod])
    dp.register_callback_query_handler(back, Text(startswith="back"), state="*")
