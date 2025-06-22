from __future__ import annotations

from typing import Any, Dict, List, Type, TypeVar

import httpx

from .enums import Status
from .models import (
    CertMQTTFailed,
    ClaimOperationList,
    CommunicationAp,
    CommunicationsInterfaces,
    DataFWResponse,
    DatalessResponse,
    DeviceList,
    DiscoverProgressList,
    DiscoveryInverters,
    EquinoxSystemStatus,
    EssStatusReport,
    Failure,
    FirewallSettingsConfiguration,
    GeneralSettings,
    GridProfile,
    GridProfileSystemStatus,
    InterfaceConfiguration,
    NetworkInterfaces,
    P2pClientPaired,
    P2pPairingInfo,
    PCSSettings,
    PingableDevices,
    PingData,
    PingOptions,
    PowerProductionSetting,
    PowerProductionStatus,
    Progress,
    Result,
    ResultSucceed,
    SystemHealthCheckList,
    SystemHealthCheckListStatus,
    TraceRouteObject,
    TracerouteOptions,
    TunnelOptions,
    TunnelStatus,
    Whitelist,
)

T = TypeVar("T")


class SungazerClient:
    """Client for interacting with the Sungazer PVS6 API."""

    def __init__(
        self, base_url: str = "http://sunpowerconsole.com/cgi-bin", timeout: int = 30
    ):
        """
        Initialize the Sungazer client.

        Args:
            base_url: The base URL for the API
            timeout: Request timeout in seconds

        """
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=timeout)

    def __enter__(self):
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context manager and close the client."""
        self.close()

    def close(self):
        """Close the client."""
        self.client.close()

    def _handle_response(self, response: httpx.Response, model_class: Type[T]) -> T:
        """
        Handle the API response.

        Args:
            response: The response from the API
            model_class: The Pydantic model class to deserialize the response to

        Returns:
            The deserialized response

        Raises:
            httpx.HTTPStatusError: If the response contains an error status code

        """
        response.raise_for_status()

        # If the response is empty, return an empty instance of the model
        if not response.content:
            return model_class()

        data = response.json()
        return model_class.parse_obj(data)  # type: ignore[attr-defined]

    def get(
        self, path: str, model_class: Type[T], params: Dict[str, Any] | None = None
    ) -> T:
        """
        Send a GET request to the API.

        Args:
            path: The path to append to the base URL
            model_class: The Pydantic model class to deserialize the response to
            params: Optional query parameters

        Returns:
            The deserialized response

        """
        response = self.client.get(path, params=params)
        return self._handle_response(response, model_class)

    def post(
        self,
        path: str,
        model_class: Type[T],
        json: Dict[str, Any] | None = None,
        data: Any | None = None,
    ) -> T:
        """
        Send a POST request to the API.

        Args:
            path: The path to append to the base URL
            model_class: The Pydantic model class to deserialize the response to
            json: Optional JSON data to send
            data: Optional form data to send

        Returns:
            The deserialized response

        """
        response = self.client.post(path, json=json, data=data)
        return self._handle_response(response, model_class)

    def delete(self, path: str, model_class: Type[T]) -> T:
        """
        Send a DELETE request to the API.

        Args:
            path: The path to append to the base URL
            model_class: The Pydantic model class to deserialize the response to

        Returns:
            The deserialized response

        """
        response = self.client.delete(path)
        return self._handle_response(response, model_class)

    # Certificate operations
    def renew_mqtt_cert(self) -> Status | CertMQTTFailed:
        """
        Renew the MQTT certificate.

        Runs /usr/local/sbin/cert_client.sh MQTT under the hood and confirms with
        /usr/local/sbin/cert_check.sh if the cert is valid.

        Returns:
            Status if successful, CertMQTTFailed otherwise

        """
        try:
            return self.post("/dl_cgi/cert/mqtt", Status)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                return CertMQTTFailed.parse_obj(e.response.json())
            raise

    # Network operations
    def renew_dhcp_lease(self, network_type: str) -> Status:
        """
        Renew the DHCP lease for the specified network type.

        Args:
            network_type: The network type (eth, wifi, plc)

        Returns:
            Status if successful

        """
        return self.get(f"/dl_cgi/network/interfaceConfig/dhcp/{network_type}", Status)

    def release_dhcp_lease(self, network_type: str) -> Status:
        """
        Release the DHCP lease for the specified network type.

        Args:
            network_type: The network type (eth, wifi, plc)

        Returns:
            Status if successful

        """
        return self.delete(
            f"/dl_cgi/network/interfaceConfig/dhcp/{network_type}", Status
        )

    def get_power_production(self) -> PowerProductionStatus:
        """
        Get the power production status.

        Returns:
            The power production status

        """
        return self.get("/dl_cgi/network/powerProduction", PowerProductionStatus)

    def set_power_production(self, power_production: PowerProductionSetting) -> Status:
        """
        Set the power production status.

        Args:
            power_production: The power production settings

        Returns:
            Status if successful

        """
        return self.post(
            "/dl_cgi/network/powerProduction",
            Status,
            json=power_production.dict(exclude_none=True),
        )

    def begin_checking_cell_primary(self, address: str) -> Status:
        """
        Begin checking for permission to set cellular as a primary network interface.

        Args:
            address: The address to look up

        Returns:
            Status if successful

        """
        return self.post(
            "/dl_cgi/network/checkCellPrimary", Status, json={"address": address}
        )

    def update_interface_config(
        self, network_type: str, config: InterfaceConfiguration
    ) -> InterfaceConfiguration:
        """
        Update the interface configuration.

        Args:
            network_type: The network type (eth, wifi, plc)
            config: The interface configuration

        Returns:
            The updated interface configuration

        """
        return self.post(
            f"/dl_cgi/network/interfaceConfig/{network_type}",
            InterfaceConfiguration,
            json=config.dict(exclude_none=True),
        )

    def get_interface_config(self, network_type: str) -> InterfaceConfiguration:
        """
        Get the interface configuration.

        Args:
            network_type: The network type (eth, wifi, plc)

        Returns:
            The interface configuration

        """
        return self.get(
            f"/dl_cgi/network/interfaceConfig/{network_type}", InterfaceConfiguration
        )

    def update_firewall_settings(
        self, settings: FirewallSettingsConfiguration
    ) -> FirewallSettingsConfiguration:
        """
        Update the firewall settings.

        Args:
            settings: The firewall settings

        Returns:
            The updated firewall settings

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/network/firewallSettings",
                FirewallSettingsConfiguration,
                json=settings.dict(exclude_none=True),
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to update firewall settings: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_firewall_settings(self) -> FirewallSettingsConfiguration:
        """
        Get the firewall settings.

        Returns:
            The firewall settings

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get(
                "/dl_cgi/network/firewallSettings", FirewallSettingsConfiguration
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get firewall settings: {failure.status}"
                raise ValueError(msg) from e
            raise

    def update_network_settings(self, settings: GeneralSettings) -> GeneralSettings:
        """
        Update the network settings.

        Args:
            settings: The network settings

        Returns:
            The updated network settings

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/network/settings",
                GeneralSettings,
                json=settings.dict(exclude_none=True),
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to update network settings: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_network_settings(self) -> GeneralSettings:
        """
        Get the network settings.

        Returns:
            The network settings

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/network/settings", GeneralSettings)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get network settings: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_network_interfaces(self) -> NetworkInterfaces:
        """
        Get the list of network interfaces.

        Returns:
            The list of network interfaces

        """
        return self.get("/dl_cgi/network/interfaces", NetworkInterfaces)

    def get_pingable_devices(self) -> PingableDevices:
        """
        Get the list of pingable devices from devices.lua.

        Returns:
            The list of pingable devices

        """
        return self.get("/dl_cgi/network/getPingableDevices", PingableDevices)

    def ping_status(self) -> PingData:
        """
        Get the status of the ping.

        Returns:
            The ping status

        """
        return self.get("/dl_cgi/network/ping", PingData)

    def start_ping(self, options: PingOptions) -> ResultSucceed:
        """
        Start a ping.

        Args:
            options: The ping options

        Returns:
            ResultSucceed if successful

        """
        return self.post(
            "/dl_cgi/network/ping", ResultSucceed, json=options.dict(exclude_none=True)
        )

    def tunnel_status(self) -> TunnelStatus:
        """
        Get the status of the ssh tunnel.

        Returns:
            The tunnel status

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/network/tunnel", TunnelStatus)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get tunnel status: {failure.status}"
                raise ValueError(msg) from e
            raise

    def start_tunnel(self, options: TunnelOptions) -> Status:
        """
        Start a ssh tunnel.

        Args:
            options: The tunnel options

        Returns:
            Status if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/network/tunnel", Status, json=options.dict(exclude_none=True)
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to start tunnel: {failure.status}"
                raise ValueError(msg) from e
            raise

    def delete_tunnel(self) -> Status:
        """
        Delete all ssh tunnels.

        Returns:
            Status if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.delete("/dl_cgi/network/tunnel", Status)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to delete tunnel: {failure.status}"
                raise ValueError(msg) from e
            raise

    def traceroute_status(self) -> TraceRouteObject:
        """
        Get the status of the traceroute.

        Returns:
            The traceroute status

        """
        return self.get("/dl_cgi/network/traceroute", TraceRouteObject)

    def start_traceroute(self, options: TracerouteOptions) -> ResultSucceed:
        """
        Start a traceroute.

        Args:
            options: The traceroute options

        Returns:
            ResultSucceed if successful

        """
        return self.post(
            "/dl_cgi/network/traceroute",
            ResultSucceed,
            json=options.dict(exclude_none=True),
        )

    # Device operations
    def get_discovery_progress(self) -> DiscoverProgressList:
        """
        Get the discovery progress.

        Returns:
            The discovery progress

        """
        return self.get("/dl_cgi/discovery", DiscoverProgressList)

    def discover(
        self,
        num_devices: int = 200,
        mi_type: str = "ALL",
        device: str = "all",
        interfaces: List[str] | None = None,
        save_config_file: bool = False,
        keep_devices: bool = False,
    ) -> DatalessResponse:
        """
        Start discovering devices.

        Args:
            num_devices: The number of devices to discover
            mi_type: The MI type (ALL, ENPH, SBT)
            device: The device type (allnomi, all, Metstation, i
                allplusmime, allnoinverters, storage)
            interfaces: The interfaces to use (mime, net, ttyUSB0,
                ttyUSB1, ttyUSB2, local)
            save_config_file: Whether to save the config file
            keep_devices: Whether to keep the devices

        Returns:
            DatalessResponse if successful

        Raises:
            ValueError: If the operation fails

        """
        data = {
            "NumDevices": num_devices,
            "MIType": mi_type,
            "Device": device,
            "SaveConfigFile": 1 if save_config_file else 0,
            "KeepDevices": 1 if keep_devices else 0,
        }

        if interfaces:
            data["Interfaces"] = interfaces

        try:
            return self.post("/dl_cgi/discovery", DatalessResponse, json=data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 503:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to start discovery: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_devices(self, detailed: bool = False) -> DeviceList:
        """
        Get the device list.

        Args:
            detailed: Whether each device should contain additional optional attributes

        Returns:
            The device list

        Raises:
            ValueError: If a discovery or claiming operation is in progress

        """
        try:
            return self.get(
                "/dl_cgi/devices/list",
                DeviceList,
                params={"detailed": str(detailed).lower()},
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 503:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Cannot get devices: {failure.status}"
                raise ValueError(msg) from e
            raise

    def start_claim(self, operations: ClaimOperationList) -> Result:
        """
        Start claiming devices.

        Args:
            operations: The claim operations

        Returns:
            Result if successful

        Raises:
            ValueError: If the operation fails or if a discovery is in progress

        """
        try:
            return self.post(
                "/dl_cgi/devices", Result, json=operations.dict(exclude_none=True)
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (500, 503):
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to start claim: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_claim(self) -> Progress:
        """
        Get the claim progress.

        Returns:
            The claim progress

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/devices", Progress)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get claim progress: {failure.status}"
                raise ValueError(msg) from e
            raise

    # Communication operations
    def get_interfaces(self) -> CommunicationsInterfaces:
        """
        Get all information for all communications interfaces.

        Returns:
            The communications interfaces

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get(
                "/dl_cgi/communication/interfaces", CommunicationsInterfaces
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get interfaces: {failure.status}"
                raise ValueError(msg) from e
            raise

    def scan_wifi(self) -> CommunicationAp:
        """
        Scan for WiFi networks.

        Returns:
            The available WiFi networks

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/communication/wifi/scan", CommunicationAp)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to scan WiFi: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_p2p_pairing_info(self) -> P2pPairingInfo:
        """
        Get P2P pairing information.

        Returns:
            The P2P pairing information

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/communication/p2p/pairingInfo", P2pPairingInfo)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get P2P pairing info: {failure.status}"
                raise ValueError(msg) from e
            raise

    def pair_p2p_client(self, client_name: str) -> P2pClientPaired:
        """
        Pair a P2P client.

        Args:
            client_name: The client name

        Returns:
            The pairing result

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/communication/p2p/pair",
                P2pClientPaired,
                json={"client_name": client_name},
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to pair P2P client: {failure.status}"
                raise ValueError(msg) from e
            raise

    # Firmware operations
    def get_firmware_info(self) -> DataFWResponse:
        """
        Get firmware information.

        Returns:
            The firmware information

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/fw", DataFWResponse)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get firmware info: {failure.status}"
                raise ValueError(msg) from e
            raise

    def start_firmware_update(self, url: str, version: str) -> DatalessResponse:
        """
        Start a firmware update.

        Args:
            url: The URL to download the firmware from
            version: The version of the firmware

        Returns:
            DatalessResponse if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/fw", DatalessResponse, json={"URL": url, "VERSION": version}
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to start firmware update: {failure.status}"
                raise ValueError(msg) from e
            raise

    # Grid profile operations
    def get_grid_profiles(self) -> List[GridProfile]:
        """
        Get the list of grid profiles.

        Returns:
            The list of grid profiles

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/gridprofiles", List[GridProfile])
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get grid profiles: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_grid_profile_status(self) -> GridProfileSystemStatus:
        """
        Get the grid profile status.

        Returns:
            The grid profile status

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/gridprofiles/status", GridProfileSystemStatus)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get grid profile status: {failure.status}"
                raise ValueError(msg) from e
            raise

    def set_grid_profile(self, grid_profile_id: str) -> DatalessResponse:
        """
        Set the grid profile.

        Args:
            grid_profile_id: The grid profile ID

        Returns:
            DatalessResponse if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/gridprofiles", DatalessResponse, json={"id": grid_profile_id}
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to set grid profile: {failure.status}"
                raise ValueError(msg) from e
            raise

    # PCS operations
    def get_pcs_settings(self) -> PCSSettings:
        """
        Get the PCS settings.

        Returns:
            The PCS settings

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/pcs/settings", PCSSettings)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get PCS settings: {failure.status}"
                raise ValueError(msg) from e
            raise

    def update_pcs_settings(self, settings: PCSSettings) -> Status:
        """
        Update the PCS settings.

        Args:
            settings: The PCS settings

        Returns:
            Status if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/pcs/settings", Status, json=settings.dict(exclude_none=True)
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to update PCS settings: {failure.status}"
                raise ValueError(msg) from e
            raise

    # System health operations
    def get_system_health_checklist(
        self, category: str = "ALL"
    ) -> SystemHealthCheckList:
        """
        Get the system health checklist.

        Args:
            category: The category to get (ALL, ACPV, PLATFORM, STORAGE)

        Returns:
            The system health checklist

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get(
                "/dl_cgi/system/health/checklist",
                SystemHealthCheckList,
                params={"category": category},
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get system health checklist: {failure.status}"
                raise ValueError(msg) from e
            raise

    def start_system_health_check(
        self, checks: List[str], category: str = "ALL"
    ) -> DatalessResponse:
        """
        Start a system health check.

        Args:
            checks: The checks to run
            category: The category to check (ALL, ACPV, PLATFORM, STORAGE)

        Returns:
            DatalessResponse if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/system/health/check",
                DatalessResponse,
                json={"checks": checks, "category": category},
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to start system health check: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_system_health_check_status(self) -> List[SystemHealthCheckListStatus]:
        """
        Get the system health check status.

        Returns:
            The system health check status

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get(
                "/dl_cgi/system/health/status", List[SystemHealthCheckListStatus]
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get system health check status: {failure.status}"
                raise ValueError(msg) from e
            raise

    # Status operations
    def get_ess_status(self) -> EssStatusReport:
        """
        Get the energy storage system status.

        Returns:
            The energy storage system status

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/status/ess", EssStatusReport)
        except httpx.HTTPStatusError as e:
            if e.response.status_code in (404, 500):
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get ESS status: {failure.status}"
                raise ValueError(msg) from e
            raise

    def get_equinox_status(self) -> EquinoxSystemStatus:
        """
        Get the Equinox system status.

        Returns:
            The Equinox system status

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/status/equinox", EquinoxSystemStatus)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get Equinox status: {failure.status}"
                raise ValueError(msg) from e
            raise

    # Whitelist operations
    def get_whitelist(self) -> Whitelist:
        """
        Get the whitelist.

        Returns:
            The whitelist

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/whitelist", Whitelist)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get whitelist: {failure.status}"
                raise ValueError(msg) from e
            raise

    def update_whitelist(self, whitelist: Whitelist) -> Status:
        """
        Update the whitelist.

        Args:
            whitelist: The whitelist

        Returns:
            Status if successful

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.post(
                "/dl_cgi/whitelist", Status, json=whitelist.dict(exclude_none=True)
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to update whitelist: {failure.status}"
                raise ValueError(msg) from e
            raise

    # Inverter operations
    def get_inverters(self) -> DiscoveryInverters:
        """
        Get the inverters.

        Returns:
            The inverters

        Raises:
            ValueError: If the operation fails

        """
        try:
            return self.get("/dl_cgi/inverters", DiscoveryInverters)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 500:
                failure = Failure.parse_obj(e.response.json())
                msg = f"Failed to get inverters: {failure.status}"
                raise ValueError(msg) from e
            raise
