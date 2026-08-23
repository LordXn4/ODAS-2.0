from pathlib import Path

# ============================================================
# ODA 2.0 - configuração do sistema de atualização
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

# Versão instalada atualmente
CURRENT_VERSION = "2.0.1"

# Arquivo que registra a versão instalada
VERSION_FILE = BASE_DIR / "VERSION"

# Diretório temporário usado para baixar/aplicar atualizações
UPDATE_DIR = BASE_DIR / ".updates"

# Backups para rollback automático
BACKUP_DIR = BASE_DIR / "backups"

# Manifesto público hospedado no GitHub
UPDATE_MANIFEST_URL = (
    "https://raw.githubusercontent.com/"
    "LordXn4/ODAS-2.0/main/update_manifest.json"
)

# Criar diretórios necessários
UPDATE_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
