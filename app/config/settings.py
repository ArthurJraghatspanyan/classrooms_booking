from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  MONGO_URI: str
  SECRET_KEY: str
  ADMIN_PASSWORD: str
  SLACK_TOKEN: str

  model_config = ConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()