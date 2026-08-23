from pydantic import BaseModel, Field

from oda.config.performance import PerformanceSettings


class VoiceSettings(BaseModel):
    enabled: bool = True
    voice: str = "masculina"
    pitch: float = 0.0
    speed: float = 1.0
    volume: float = 1.0


class UpdateSettings(BaseModel):
    enabled: bool = True

    # Verificação automática
    auto_check: bool = True
    check_interval_minutes: int = 60

    # Download e instalação
    auto_download: bool = True
    ask_before_install: bool = True

    # Segurança
    verify_sha256: bool = True
    create_backup: bool = True
    automatic_rollback: bool = True

    # Backups
    max_backups: int = 3

    # Canal de atualização
    channel: str = "stable"

    # Exibir atualização no HUD
    show_in_hud: bool = True


class ODASettings(BaseModel):
    name: str = "ODA"
    offline_first: bool = True
    online_fallback: bool = True

    voice: VoiceSettings = Field(
        default_factory=VoiceSettings
    )

    performance: PerformanceSettings = Field(
        default_factory=PerformanceSettings
    )

    update: UpdateSettings = Field(
        default_factory=UpdateSettings
    )
