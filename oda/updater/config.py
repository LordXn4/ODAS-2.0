from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

CURRENT_VERSION = "2.0.1"
VERSION_FILE = BASE_DIR / "VERSION"

UPDATE_DIR = BASE_DIR / ".updates"
BACKUP_DIR = BASE_DIR / "backups"

UPDATE_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Será preenchido quando o servidor privado de atualização estiver pronto.
UPDATE_MANIFEST_URL = (
    "https://github.com/LordXn4/ODAS-2.0/releases/latest/download/update.json"
)
