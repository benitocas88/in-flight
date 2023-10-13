from environs import Env

env = Env()

SECRET_KEY = env.str("SECRET_KEY")

HTTP_REQUEST_TIMEOUT = env.int("HTTP_REQUEST_TIMEOUT", default=60)
