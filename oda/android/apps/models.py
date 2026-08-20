from dataclasses import dataclass


@dataclass
class InstalledApp:
    name: str
    package_name: str
    launchable: bool = True
