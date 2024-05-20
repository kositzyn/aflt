class Settings:
    def __init__(self):
        self.username: str = 'user'
        self.password: str = 'pass'
        self.server: str = 'postgres:5555'
        self.db_name: str = 'inventory'

    @property
    def db_url(self) -> str:
        url = (self.username + ':' + self.password + '@'
               + self.server + '/' + self.db_name)
        return f"postgresql+asyncpg://{url}"

    @property
    def kafka_url(self) -> str:
        return f"kafka:9092"


settings = Settings()
