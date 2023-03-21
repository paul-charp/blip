"""
Default config file for blip.
Based on the rez packages.py logic.
Environment variable BLIP_CONFIG_FILE should point to this file.

=> idea: make a commands() function, useful ?
    Eventually make all values env-overridable
        make config file stackables
"""

BLIP_PLUGIN_PATH = [
    # Default plugin location, maybe embeded it in the python module.
    './blip/plugins',
]

BLIP_CONTEXT_ROOT = [
    './blip_dev_root'  # Root for testing during development
]
