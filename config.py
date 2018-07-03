import os
import pathlib


EXPORT_SCRIPT = os.path.join(pathlib.Path(__file__).absolute().parent, "scripts/export_models_and_fitness.sh")

try:
    MONGODB_URI = os.environ["MONGODB_URI"]

except KeyError:
    MONGODB_URI = "mongodb://127.0.0.1:27017/"