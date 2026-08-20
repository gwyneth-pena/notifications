from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class AppSettings(BaseSettings):

    app_env: Literal["dev", "prod"] = "dev"

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_security_protocol: Literal["PLAINTEXT", "SSL", "SASL_SSL"] = "PLAINTEXT"
    kafka_sasl_mechanism: Literal["PLAIN", "SCRAM-SHA-256", "SCRAM-SHA-512", "GSSAPI"] = "PLAIN"
    kafka_sasl_username: str = "username"
    kafka_sasl_password: str = "password"
    kafka_topics: dict = {
        'email': 'notifications.email',
        'push': 'notifications.push'
    }
    kafka_buffer_max_messages: int = 100000
    kafka_buffer_linger_ms: int = 5
    kafka_buffer_max_kbytes: int = 64000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = AppSettings()