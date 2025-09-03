from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
import sys, os

# Добавляем src в путь
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.db.base import Base  # Сюда подключаем Base всех моделей
from src.models.user import User
from src.models.role import Role

config = context.config
fileConfig(config.config_file_name)

# Метаданные всех моделей
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Для Alembic используем синхронный engine, убираем +asyncpg
    sync_url = config.get_main_option("sqlalchemy.url").replace("+asyncpg", "")
    connectable = create_engine(sync_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
