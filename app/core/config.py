from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Фонд собирает пожертвования на различные целевые проекты для котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
