from enum import Enum

from pydantic import BaseModel, Field


class DeviceConnection(str, Enum):
    WIFI = "wifi"
    BLUETOOTH = "bluetooth"


class Device(BaseModel):
    name: str
    connection: DeviceConnection
    identifier: str
    device_type: str = "unknown"
    manufacturer: str | None = None
    available: bool = True
    capabilities: list[str] = Field(default_factory=list)
