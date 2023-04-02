import importlib
import os
from django.apps import apps


def load_signals():
    """
    Imports any 'signals.py' files found in the app directories.
    """
    app_configs = apps.get_app_configs()
    for app_config in app_configs:
        app_module = importlib.import_module(app_config.name)
        signals_path = os.path.join(
            os.path.dirname(app_module.__file__),
            "signals.py"
            )
        if os.path.exists(signals_path):
            importlib.import_module(f"{app_config.name}.signals")
