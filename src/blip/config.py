import os

from blip.utils import import_module_from_file

SETTINGS: list[str] = [
    "BLIP_DEFAULT_SOURCE",
    "BLIP_DEFAULT_RESOLVER",
    "BLIP_LOG_LEVEL",
]

SETTINGS_LISTTYPE: list[str] = [
    "BLIP_PLUGIN_PATH",
    "BLIP_CONTEXT_PATH",
]

CONFIG_FILE_ENV_VAR: str = "BLIP_CONFIG_FILE"


def get_env_config() -> dict[str]:

    env_config: dict = {}

    for env_var in SETTINGS + SETTINGS_LISTTYPE:
        value = os.getenv(env_var)

        if value is not None:
            if env_var in SETTINGS_LISTTYPE:
                value = value.split(os.pathsep)

            env_config[env_var] = value

    return env_config


def get_file_config() -> dict[str]:

    # Get the config_file path from the env.
    config_file: str = os.getenv(f'{CONFIG_FILE_ENV_VAR}')

    if config_file == None:
        raise Exception(
            f'{CONFIG_FILE_ENV_VAR} environment variable not set !') from None

    config_file = os.path.abspath(config_file)

    if not os.path.exists(config_file):
        raise FileNotFoundError(
            f'{CONFIG_FILE_ENV_VAR} at: {config_file} does not exists')

    # Imports the config file.
    config_module = import_module_from_file(config_file)

    # Retrieves the config.
    file_config: dict = {}

    for setting in SETTINGS + SETTINGS_LISTTYPE:

        try:
            value = getattr(config_module, setting)

        except AttributeError as e:
            print(f'{setting} not defined in the blip config file at {config_file}')
            raise

        if value is not None:
            file_config[setting] = value

    return file_config


def merge_configs(env_config: dict[str], file_config: dict[str]) -> dict[str]:

    full_config = {}

    for key, value in file_config.items():
        try:
            if type(value) is list:
                full_config[key] = env_config[key] + file_config[key]

            else:
                full_config[key] = env_config[key]
        except KeyError:
            full_config[key] = file_config[key]

    return full_config


def get_config(key: str) -> dict[str]:
    env_config: dict[str] = get_env_config()
    file_config: dict[str] = get_file_config()
    config = merge_configs(env_config, file_config)

    try:
        return config[key]

    except KeyError:
        print(f'{key} does not exist in blip config')
        raise
