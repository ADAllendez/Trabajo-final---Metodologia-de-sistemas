import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Carga .env SOLO en local (en Railway no molesta)
load_dotenv()

MYSQL_USER = os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD") or os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQLPORT") or os.getenv("MYSQL_PORT") or "3306"
MYSQL_DB = os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DB")

print("MYSQL_HOST =", MYSQL_HOST)
print("MYSQL_PORT =", MYSQL_PORT)
if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB]):
    raise RuntimeError("❌ Variables de entorno MySQL no cargadas correctamente")

DATABASE_URL = (
    f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session