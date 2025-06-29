# type: ignore  # noqa: N999, PGH003
import json
from pathlib import Path

import pytest  # noqa: F401

from sungazer.models import GetCommResponse, Interface, System


def test_get_comm_response_from_json():
    """Test GetCommResponse parsing from real JSON data."""
    # Load test data from Get_Comm.json
    data_path = Path(__file__).parent / "fixtures" / "Get_Comm" / "Get_Comm.json"
    with Path(data_path).open() as f:
        test_data = json.load(f)

    # Parse the response
    response = GetCommResponse(**test_data["networkstatus"])

    # Verify the response was parsed correctly
    assert isinstance(response, GetCommResponse)
    assert response.ts == "1635315583"
    assert response.interfaces is not None
    assert len(response.interfaces) == 4
    assert response.system is not None

    # Verify system information
    assert response.system.interface == "sta0"
    assert response.system.internet == "up"
    assert response.system.sms == "reachable"

    # Verify interfaces
    interfaces = response.interfaces
    assert len(interfaces) == 4

    # Test wan interface
    wan_interface = next(i for i in interfaces if i.interface == "wan")
    assert wan_interface.internet == "down"
    assert wan_interface.ipaddr is None  # Empty string should be None for IPv4Address
    assert wan_interface.link == "disconnected"
    assert wan_interface.mode == "wan"
    assert wan_interface.sms == "unreachable"
    assert wan_interface.state == "down"

    # Test plc interface
    plc_interface = next(i for i in interfaces if i.interface == "plc")
    assert plc_interface.internet == "down"
    assert plc_interface.ipaddr is None
    assert plc_interface.link == "disconnected"
    assert plc_interface.pairing == "unpaired"
    assert plc_interface.sms == "unreachable"
    assert plc_interface.speed == 0
    assert plc_interface.state == "down"

    # Test sta0 interface (WiFi)
    sta0_interface = next(i for i in interfaces if i.interface == "sta0")
    assert sta0_interface.internet == "up"
    assert str(sta0_interface.ipaddr) == "192.168.10.239"
    assert sta0_interface.sms == "reachable"
    assert sta0_interface.ssid == "Starfield"
    assert sta0_interface.status == "connected"

    # Test cell interface
    cell_interface = next(i for i in interfaces if i.interface == "cell")
    assert cell_interface.internet == "down"
    assert cell_interface.ipaddr is None
    assert cell_interface.is_always_on is False
    assert cell_interface.is_primary is False
    assert cell_interface.link == "connected"
    assert cell_interface.modem == "MODEM_OK"
    assert cell_interface.provider == "UNKNOWN"
    assert cell_interface.sim == "SIM_READY"
    assert cell_interface.sms == "unreachable"
    assert cell_interface.state == "DOWN"
    assert cell_interface.status == "NOT_REGISTERED"


def test_interface_model_parsing():
    """Test Interface model parsing with various field combinations."""
    # Test WiFi interface
    wifi_data = {
        "interface": "sta0",
        "internet": "up",
        "ipaddr": "192.168.1.100",
        "ssid": "TestWiFi",
        "status": "connected",
        "sms": "reachable",
    }
    wifi_interface = Interface(**wifi_data)
    assert wifi_interface.interface == "sta0"
    assert wifi_interface.internet == "up"
    assert str(wifi_interface.ipaddr) == "192.168.1.100"
    assert wifi_interface.ssid == "TestWiFi"
    assert wifi_interface.status == "connected"
    assert wifi_interface.sms == "reachable"

    # Test cellular interface
    cell_data = {
        "interface": "cell",
        "internet": "down",
        "ipaddr": "",
        "is_primary": True,
        "is_always_on": False,
        "provider": "Verizon",
        "sim": "SIM_READY",
        "modem": "MODEM_OK",
        "link": "connected",
        "state": "DOWN",
        "status": "NOT_REGISTERED",
        "sms": "unreachable",
    }
    cell_interface = Interface(**cell_data)
    assert cell_interface.interface == "cell"
    assert cell_interface.internet == "down"
    assert cell_interface.ipaddr is None  # Empty string becomes None
    assert cell_interface.is_primary is True
    assert cell_interface.is_always_on is False
    assert cell_interface.provider == "Verizon"
    assert cell_interface.sim == "SIM_READY"
    assert cell_interface.modem == "MODEM_OK"
    assert cell_interface.link == "connected"
    assert cell_interface.state == "DOWN"
    assert cell_interface.status == "NOT_REGISTERED"
    assert cell_interface.sms == "unreachable"

    # Test Ethernet interface
    eth_data = {
        "interface": "wan",
        "internet": "up",
        "ipaddr": "10.0.0.5",
        "link": "connected",
        "mode": "wan",
        "state": "up",
        "sms": "reachable",
    }
    eth_interface = Interface(**eth_data)
    assert eth_interface.interface == "wan"
    assert eth_interface.internet == "up"
    assert str(eth_interface.ipaddr) == "10.0.0.5"
    assert eth_interface.link == "connected"
    assert eth_interface.mode == "wan"
    assert eth_interface.state == "up"
    assert eth_interface.sms == "reachable"


def test_system_model_parsing():
    """Test System model parsing."""
    system_data = {
        "interface": "sta0",
        "internet": "up",
        "sms": "reachable",
    }
    system = System(**system_data)
    assert system.interface == "sta0"
    assert system.internet == "up"
    assert system.sms == "reachable"

    # Test with None values
    system_none_data = {
        "interface": None,
        "internet": None,
        "sms": None,
    }
    system_none = System(**system_none_data)
    assert system_none.interface is None
    assert system_none.internet is None
    assert system_none.sms is None


def test_get_comm_response_empty():
    """Test GetCommResponse with minimal data."""
    minimal_data = {
        "ts": "1234567890",
    }
    response = GetCommResponse(**minimal_data)
    assert response.ts == "1234567890"
    assert response.interfaces is None
    assert response.system is None

    # Test with empty interfaces and system
    empty_data = {
        "interfaces": [],
        "system": None,
        "ts": "1234567890",
    }
    response_empty = GetCommResponse(**empty_data)
    assert response_empty.ts == "1234567890"
    assert response_empty.interfaces == []
    assert response_empty.system is None


def test_interface_ipaddr_parsing():
    """Test Interface IP address parsing edge cases."""
    # Test valid IPv4 address
    valid_ip_data = {"interface": "test", "ipaddr": "192.168.1.1"}
    interface = Interface(**valid_ip_data)
    assert str(interface.ipaddr) == "192.168.1.1"

    # Test empty string (should become None)
    empty_ip_data = {"interface": "test", "ipaddr": ""}
    interface = Interface(**empty_ip_data)
    assert interface.ipaddr is None

    # Test None value
    none_ip_data = {"interface": "test", "ipaddr": None}
    interface = Interface(**none_ip_data)
    assert interface.ipaddr is None

    # Test missing ipaddr field
    no_ip_data = {"interface": "test"}
    interface = Interface(**no_ip_data)
    assert interface.ipaddr is None
