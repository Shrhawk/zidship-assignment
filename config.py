from environs import Env

env = Env()
env.read_env()

DB_SEVER_ADDRESS = env("DB_SEVER_ADDRESS")
DB_PORT = env("DB_PORT")
DB_USERNAME = env("DB_USERNAME")
DB_PASSWORD = env("DB_PASSWORD")
DB_NAME = env("DB_NAME")

EASYPOST_API_KEY = env("EASYPOST_API_KEY")

TEST_DB_SEVER_ADDRESS = env("TEST_DB_SEVER_ADDRESS")
TEST_DB_NAME = env("TEST_DB_NAME")
TEST_DB_PASSWORD = env("TEST_DB_PASSWORD")
TEST_DB_PORT = env("TEST_DB_PORT")
TEST_DB_USERNAME = env("TEST_DB_USERNAME")
