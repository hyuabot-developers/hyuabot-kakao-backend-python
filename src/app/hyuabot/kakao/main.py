from hypercorn.config import Config

from app.hyuabot.kakao import create_app, AppSettings

hypercorn_config = Config()
app_settings = AppSettings()
app = create_app(app_settings)
