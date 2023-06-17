from flight.settings.base import env


class Environment:
    @classmethod
    def is_staging(cls) -> bool:
        return cls.current_environment() == "staging"

    @classmethod
    def is_sandbox(cls) -> bool:
        return cls.current_environment() == "sandbox"

    @classmethod
    def is_development(cls) -> bool:
        return cls.current_environment() == "development"

    @classmethod
    def is_production(cls) -> bool:
        return cls.current_environment() == "production"

    @classmethod
    def current_environment(cls) -> str:
        return env.str("ENVIRONMENT", default="local")


    @classmethod
    def app_env_production(cls) -> str:
        return env.str("APP_ENV", default="production") == "production"
