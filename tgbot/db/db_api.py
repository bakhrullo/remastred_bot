import aiohttp


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}user/get/{user_id}") as response:
            return await response.json()


async def create_user(name, tg_id, lang, phone, config):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}user/create/",
                                data={"name": name, "tg_id": tg_id, "lang": lang, "phone": phone}) as response:
            return await response.json()


async def update_user(user_id, config, lang=False, phone=False,):
    data = {}
    if phone:
        data["phone"] = phone
    if lang:
        data["lang"] = lang
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f"{config.db.database_url}user/update/{user_id}",
                                 data=data) as response:
            return await response.json()


async def list_glob_cats(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}glob_category/") as response:
            return await response.json()


async def get_glob_cats(config, option):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}glob_category/{option}") as response:
            return await response.json()


async def get_cats(config, option):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}category/", params={"option": option}) as response:
            return await response.json()


async def get_list_prods(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/", params={"cat_id": option}) as response:
            return await response.json()


async def get_prods(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/{option}") as response:
            return await response.json()
