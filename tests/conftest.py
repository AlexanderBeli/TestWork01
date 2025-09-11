import os
import sys
from pathlib import Path

from dotenv import load_dotenv

env_file = Path(__file__).parent.parent / ".env.test"
if env_file.exists():
    load_dotenv(env_file)
else:
    os.environ.setdefault("REDIS_HOST", "localhost")
    os.environ.setdefault("REDIS_PORT", "6379")
    os.environ.setdefault("REDIS_DB", "0")
    os.environ.setdefault("REDIS_PASSWORD", "test")
    os.environ.setdefault("MONGODB_URL", "mongodb://localhost:27017")
    os.environ.setdefault("MONGODB_NAME", "test_db")
    os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/0")
    os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    os.environ.setdefault("ENVIRONMENT", "test")

project_root = Path(__file__).parent.parent
src_root = project_root / "src"
sys.path.append(str(project_root))
sys.path.append(str(src_root))
