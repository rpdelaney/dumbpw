try:
    import importlib.metadata

    __version__ = importlib.metadata.version(__name__)
except ModuleNotFoundError:
    __version__ = "UNKNOWN"
