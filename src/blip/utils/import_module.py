import os
import importlib.util
from types import ModuleType


def import_module_from_file(module_path: str) -> ModuleType:

    if not os.path.exists(module_path):
        raise FileNotFoundError(f'Python module at: {module_path} not found.')

    spec = importlib.util.spec_from_file_location('config_file', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
