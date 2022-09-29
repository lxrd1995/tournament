import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_ids: int
    use_redis: bool


@dataclass
class DbConfig:
    path: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config['tg_bot']

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_ids=tg_bot.getint('admin_id'),
            use_redis=tg_bot.getboolean('use_redis')
        ),
        db=DbConfig(
            path=config['db'].get('path')
        )
    )
