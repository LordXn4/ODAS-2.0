from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from .config import (
    BACKUP_DIR,
    CURRENT_VERSION,
    UPDATE_DIR,
    UPDATE_MANIFEST_URL,
    VERSION_FILE,
)


class UpdateError(Exception):
    pass


class UpdateManager:
    """Gerencia atualização segura da instalação da ODA."""

    def __init__(self):
        UPDATE_DIR.mkdir(parents=True, exist_ok=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    def current_version(self) -> str:
        if VERSION_FILE.exists():
            value = VERSION_FILE.read_text().strip()
            if value:
                return value

        VERSION_FILE.write_text(CURRENT_VERSION + "\n")
        return CURRENT_VERSION

    def check(self) -> dict | None:
        if not UPDATE_MANIFEST_URL:
            return None

        try:
            with urllib.request.urlopen(
                UPDATE_MANIFEST_URL,
                timeout=10,
            ) as response:
                manifest = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise UpdateError(
                f"Não foi possível consultar atualização: {exc}"
            ) from exc

        remote_version = str(manifest.get("version", "")).strip()

        if not remote_version:
            raise UpdateError("Manifesto sem versão.")

        if remote_version == self.current_version():
            return None

        return manifest

    def download(self, url: str, expected_sha256: str) -> Path:
        target = UPDATE_DIR / "update.zip"

        try:
            urllib.request.urlretrieve(url, target)
        except Exception as exc:
            raise UpdateError(
                f"Falha no download: {exc}"
            ) from exc

        digest = hashlib.sha256()

        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)

        actual_sha256 = digest.hexdigest().lower()

        if actual_sha256 != expected_sha256.lower():
            target.unlink(missing_ok=True)
            raise UpdateError("Hash SHA-256 da atualização não confere.")

        return target

    def backup(self, version: str) -> Path:
        backup = BACKUP_DIR / version

        if backup.exists():
            shutil.rmtree(backup)

        backup.mkdir(parents=True)

        for item in (
            ROOT_ITEMS := [
                "oda",
                "VERSION",
            ]
        ):
            source = Path(__file__).resolve().parents[2] / item

            if not source.exists():
                continue

            destination = backup / item

            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        return backup

    def install(self, package: Path, version: str) -> None:
        root = Path(__file__).resolve().parents[2]
        backup = self.backup(self.current_version())

        try:
            with tempfile.TemporaryDirectory() as temp:
                temp_path = Path(temp)

                with zipfile.ZipFile(package, "r") as archive:
                    archive.extractall(temp_path)

                source_root = temp_path / "oda"

                if not source_root.exists():
                    raise UpdateError(
                        "Pacote inválido: diretório 'oda' ausente."
                    )

                destination = root / "oda"

                for item in source_root.rglob("*"):
                    relative = item.relative_to(source_root)
                    target = destination / relative

                    if item.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target)

                (root / "VERSION").write_text(
                    version.strip() + "\n"
                )

        except Exception as exc:
            self.rollback(backup)
            raise UpdateError(
                f"Atualização falhou. Rollback executado: {exc}"
            ) from exc

        package.unlink(missing_ok=True)

    def rollback(self, backup: Path) -> None:
        root = Path(__file__).resolve().parents[2]

        backup_oda = backup / "oda"

        if backup_oda.exists():
            shutil.rmtree(root / "oda", ignore_errors=True)
            shutil.copytree(backup_oda, root / "oda")

        backup_version = backup / "VERSION"

        if backup_version.exists():
            shutil.copy2(
                backup_version,
                root / "VERSION",
            )

    def update(self) -> bool:
        manifest = self.check()

        if manifest is None:
            return False

        version = str(manifest["version"])
        url = str(manifest["url"])
        sha256 = str(manifest["sha256"])

        package = self.download(url, sha256)
        self.install(package, version)

        return True
