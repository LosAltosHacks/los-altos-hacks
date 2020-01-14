import os
import importlib

# Determine the environment we want to load, default is development.py
ENV = os.environ.get("ENV", "development")
assert ENV == "development" or ENV == "production"

module = importlib.import_module(
    f".environments.{ENV}", package="config"
)

# TODO better logging of selected env:
print(f"Using env {ENV}")

# update globals of this module (i.e. settings) with imported.
globals().update(vars(module))


def is_development_env():
    return ENV == "development"


def is_production_env():
    return ENV == "production"
