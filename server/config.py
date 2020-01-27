from os import getenv

POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = getenv("POSTGRES_DB", "test")
POSTGRES_USER = getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "test")
DB_POOL_SIZE_MIN = getenv("DB_POOL_SIZE_MIN", 1)
DB_POOL_SIZE_MAX = getenv("DB_POOL_SIZE_MAX", 6)

BETTING_DATA_API_PORT = int(getenv("BETTING_DATA_API_PORT", 8000))
BETTING_DATA_API_HOST = getenv("BETTING_DATA_API_HOST", "localhost")

url = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_USER,
                                              POSTGRES_PASSWORD,
                                              POSTGRES_HOST,
                                              POSTGRES_PORT,
                                              POSTGRES_DB)
