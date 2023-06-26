import random

import aiohttp


async def send_code(number, config):
    rand_int = random.randint(1000, 9999)
    sms_data = {"messages": [{"recipient": f"{number}",
                              "message-id": "abc000000003",
                              "sms": {
                                  "originator": "3700",
                                  "content": {
                                      "text": f"Ваш код подтверждения для ARZON SERYIO BOT: {rand_int}"}}}]}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=config.misc.sms_brock,
                                auth=aiohttp.BasicAuth('bestbrok', 'tM4!-hmV52Z@'),
                                json=sms_data):
            pass
    return rand_int
