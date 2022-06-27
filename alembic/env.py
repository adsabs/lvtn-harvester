import glob
import importlib
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context


def discover_module(module_name, attr=None):
    opath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    for f in glob.glob("{}/**/{}.py".format(opath, module_name), recursive=True):
        try:
            prefix = f.replace(opath, "").replace("{}.py".format(module_name), "")
            prefix = prefix.replace(os.path.sep, ".")
            if prefix.startswith("."):
                prefix = prefix[1:]
            if prefix.endswith("."):
                prefix = prefix[0:-1]
            module = importlib.import_module("{}.{}".format(prefix, module_name))
            if attr and hasattr(module, attr):
                print(
                    "Automagically imported {} from: {}.{} ({})".format(
                        attr, prefix, module_name, f
                    )
                )
                return getattr(module, "Base")
            else:
                print("Automagically imported {}.{} ({})".format(prefix, module_name, f))
                return module
        except:  # noqa
            pass


def get_app_config(key, default=None):
    try:
        import lvtn_utils as utils

        config = utils.load_config()
        return config.get(key, default)
    except:  # noqa
        return default


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = discover_module("models", "Base")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    cfg = config.get_section(config.config_ini_section)
    if cfg["sqlalchemy.url"] == "autodiscovery":
        cfg["sqlalchemy.url"] = get_app_config("SQLALCHEMY_URL", "intentionally-wrong")
        print("Automagically set sqlalchemy.url={}".format(cfg["sqlalchemy.url"]))

    connectable = engine_from_config(
        cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
