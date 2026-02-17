import importlib.metadata

import deal


deal.activate()
__version__ = importlib.metadata.version(__name__)
