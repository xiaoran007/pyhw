from dataclasses import dataclass


@dataclass
class HostInfo:
    model = ""
    family = ""
    name = ""
    version = ""
    sku = ""
    serial = ""
    uuid = ""
    vendor = ""
