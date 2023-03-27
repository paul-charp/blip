import os
import json


def get_plugins(plugins_path: list[str]) -> dict[str]:

    plugin_files: list[str] = list()

    for dir in plugins_path:
        if os.path.exists(dir):
            for pos_json in os.listdir(dir):
                if pos_json.endswith('.json'):
                    plugin_files.append(os.path.join(dir, pos_json))

    plugins: dict[str] = {}

    for file in plugin_files:
        with open(file) as f:
            jsondata: dict = json.load(f)

        for key, value in jsondata.get('BlipPlugins').items():
            if plugins.get(key) == None:
                plugins[key] = value

    return plugins


def filter_plugins(plugins: dict[str], **kwargs) -> dict[str]:

    good_plugins: dict[str] = {}

    for name, data in plugins.items():

        good_plugin: bool = False

        for key, value in kwargs.items():
            if not data.get(key) == value:
                good_plugin = False
                break

            else:
                good_plugin = True

        if good_plugin:
            good_plugins[name] = data

    return good_plugins


foo = get_plugins(['E:/RD/dev/blip'])

bar = filter_plugins(foo, name="DefaultResolver")
print(foo, bar)
