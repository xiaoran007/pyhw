import pypci


class PCIManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = pypci.PCI()
        return cls._instance
