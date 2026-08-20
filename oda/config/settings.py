from pydantic import BaseModel, Field

from oda.config.performance import PerformanceSettings


class VoiceSettings(BaseModel):
    enabled: bool = True
    voice: str = "masculina"
    pitch: float = 0.0
    speed: float = 1.0
    volume: float = 1.0


class ODASettings(BaseModel):
    name: str = "ODA"
    offline_first: bool = True
    online_fallback: bool = True

    voice: VoiceSettings = Field(default_factory=VoiceSettings)
    performance: PerformanceSettings = Field(
        default_factory=PerformanceSettings
    )
