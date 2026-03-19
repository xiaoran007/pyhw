import pytest
from pyhw.pyhwUtil.pciUtil import PCIManager


def test_pci_manager_singleton():
    manager1 = PCIManager.get_instance()
    manager2 = PCIManager.get_instance()
    
    assert manager1 is not None
    assert manager1 is manager2
