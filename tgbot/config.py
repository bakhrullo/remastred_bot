from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass
class DbConfig:
    database_url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool
    channel_id: str


@dataclass
class Miscellaneous:
    sms_brock: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            channel_id=env.str("CHANNEL_ID"),
        ),
        db=DbConfig(
            database_url=env.str("DB_URL")
        ),
        misc=Miscellaneous(
            sms_brock=env.str("SMS_BROCK"),

        )
    )


I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
