from pydantic import BaseModel, Field


class VoiceSettings(BaseModel):
    enabled: bool = True
    pitch: float = 0.0
    speed: float = 1.0
    volume: float = 1.0


class ODASettings(BaseModel):
    name: str = "ODA"
    offline_first: bool = True
    online_fallback: bool = True
    voice: VoiceSettings = Field(default_factory=VoiceSettings)
