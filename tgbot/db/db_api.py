import aiohttp


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}user/get/{user_id}") as response:
            return await response.json()


async def create_user(tg_id, lang, config):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}user/create/",
                                data={"tg_id": tg_id, "lang": lang}) as response:
            return await response.json()


async def update_user(user_id, config, data):
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=f"{config.db.database_url}user/update/{user_id}",
                                 data=data) as response:
            return await response.json()


async def get_cats(config, option="False", cat_id="False"):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}category/",
                               params={'option': option, 'cat_id': cat_id}) as response:
            return await response.json()


async def get_list_prods(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/", params={"cat_id": option}) as response:
            return await response.json()


async def get_prods(option, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/{option}") as response:
            return await response.json()


async def get_prods_search(option, lang, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/search", params={"option": option,
                                                                                      "lang": lang}) as response:
            return await response.json()


async def get_brocks(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{config.db.database_url}brock/get') as response:
            return await response.json()


async def get_regions(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{config.db.database_url}region/get') as response:
            return await response.json()


async def get_services(config, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{config.db.database_url}service/get', params={"brock": kwargs["brock"],
                                                                                   "region": kwargs["region"]}) \
                as response:
            return await response.json()


async def get_analogs(config, prod_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{config.db.database_url}analog', params={"prod_id": prod_id}) as response:
            return await response.json()


async def get_image(config, option):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{config.db.database_url}images/{option}') as response:
            return await response.json()
