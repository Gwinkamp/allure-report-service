import os
from pathlib import Path

from pydantic import TypeAdapter

DEBUG = TypeAdapter(bool).validate_python(os.environ.get('DEBUG'))
ENVIRONMENT = 'debug' if DEBUG else 'production'

ROOT_DIR = Path(__file__).resolve().parent
VALUES_PATH = ROOT_DIR / f'values.{ENVIRONMENT}.yaml'
