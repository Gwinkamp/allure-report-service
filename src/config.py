import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import TypeAdapter

load_dotenv()

DEBUG = TypeAdapter(bool).validate_python(os.environ.get('DEBUG'))
ENVIRONMENT = 'debug' if DEBUG else 'production'

ROOT_DIR = Path(__file__).resolve().parent

VALUES_PATH = ROOT_DIR / 'values.yaml'
ENV_VALUES_PATH = ROOT_DIR / f'values.{ENVIRONMENT}.yaml'
