from tgbot.misc.i18n import i18ns

_ = i18ns.gettext


def txt(analog, lang):
    text, analogs = "", []
    for i in analog:
        if i["analog"] != 0:
            analogs.append(i["analog"])
        text += _(
            "🆔 Mahsulot nomi: {name}\n📍 Viloyat/hudud: {region}\n🏙 Ishlab chiqarilgan: {made_in}\n💰 Narxi: {price}\n"
            "📞Telefon raqam: {phone}\n\n").format(name=i[f"name_{lang}"], region=i["region"][f'name_{lang}'],
                                                made_in=i["made_in"], price=i["price"], phone=i["phone"])
    return text, str(analogs)

