from oda.android.devices.models import Device


class DeviceManager:
    def __init__(self):
        self._devices: dict[str, Device] = {}

    def add(self, device: Device) -> None:
        self._devices[device.identifier] = device

    def remove(self, identifier: str) -> None:
        self._devices.pop(identifier, None)

    def get(self, identifier: str) -> Device | None:
        return self._devices.get(identifier)

    def all(self) -> list[Device]:
        return list(self._devices.values())

    def find_by_name(self, name: str) -> Device | None:
        normalized = name.strip().lower()

        for device in self._devices.values():
            if device.name.strip().lower() == normalized:
                return device

        return None
