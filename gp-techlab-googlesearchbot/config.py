"""Global application configurations"""

from os import environ

# Check for env variables
for env_variable in ["PROJECT", "ENTITY", "ENVIRONMENT"]:
    if env_variable not in environ:
        raise Exception(f"{env_variable} not found in environment")

APP_NAME = "gpi-ipr"
APP_VERSION = "0.0.1"

PROJECT = environ["PROJECT"]
ENTITY = environ["ENTITY"]
ENVIRONMENT = environ["ENVIRONMENT"]

BUCKET = f"{APP_NAME}-{ENTITY}-{ENVIRONMENT}"

print(f"COLD_START {APP_NAME}@{APP_VERSION}")
