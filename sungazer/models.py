from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated

from sungazer.enums import (
    Category,  # noqa: TC001
    ClaimOpEnum,  # noqa: TC001
    ConfigurationType,  # noqa: TC001
    ContactorError,  # noqa: TC001
    ContactorPosition,  # noqa: TC001
    CurrentTransducerStatus,  # noqa: TC001
    CurrentTransducerStatus1,  # noqa: TC001
    Device,  # noqa: TC001
    DeviceTypeEnum,  # noqa: TC001
    GridFrequencyState,  # noqa: TC001
    GridVoltageState,  # noqa: TC001
    Info,  # noqa: TC001
    LoadFrequencyState,  # noqa: TC001
    LoadVoltageState,  # noqa: TC001
    NetworkType,  # noqa: TC001
    OperationalMode,  # noqa: TC001
    PcsMode,  # noqa: TC001
    PcsStatus,  # noqa: TC001
    PowerProduction,  # noqa: TC001
    Result1,  # noqa: TC001
    Resultenum,  # noqa: TC001
    Status1,  # noqa: TC001
    Status2,  # noqa: TC001
    Status4,  # noqa: TC001
    StorageControllerStatus,  # noqa: TC001
    System1,  # noqa: TC001
)


class ValueAndUnit(BaseModel):
    value: float | None = None
    unit: str | None = None


class DateDesc(BaseModel):
    __root__: Annotated[
        str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    ] = Field(..., description="YYYY-MM-DD HH:MM:SS", examples=["2020-02-15 01:23:45"])


class Progress(BaseModel):
    result: Resultenum | None = None
    percent: float


class Result(BaseModel):
    result: Resultenum
    success: bool | None = None
    msg: str | None = None


class Failure(BaseModel):
    status: str | None = None


class Interface(BaseModel):
    ssid: str | None = Field(None, examples=["Laneakea"])
    status: str | None = Field(None, examples=["not registered"])
    pairing: str | None = Field(None, examples=["unpaired"])
    speed: int | None = Field(None, examples=[5])
    is_primary: bool | None = Field(
        None,
        description="this is the primary interface, only shows for cell interface",
        examples=[True],
    )
    link: str | None = Field(None, examples=["connected"])
    interface: str | None = Field(None, examples=["wan"])
    internet: str | None = Field(None, examples=["up"])
    ipaddr: str | None = Field(None, examples=["192.168.0.125"])
    mode: str | None = Field(None, examples=["wan"])
    modem: str | None = Field(None, examples=["MODEM_OK"])
    sms: str | None = Field(None, examples=["reachable"])
    state: str | None = Field(None, examples=["up"])


class System(BaseModel):
    interface: str | None = Field(
        None, description="the name of an interface", examples=["wan"]
    )
    internet: str | None = Field(None, description="internet status", examples=["up"])
    sms: str | None = Field(None, description="sms status", examples=["reachable"])


class Networkstatus(BaseModel):
    interfaces: List[Interface] | None = None
    system: System | None = None
    ts: str | None = Field(
        None, description="the system timestamp", examples=["1575501242"]
    )


class CommunicationsInterfaces(BaseModel):
    result: Result1 | None = None
    networkstatus: Networkstatus | None = None


class DiscoverProgress(BaseModel):
    TYPE: str
    PROGR: int
    NFOUND: int


class DiscoverProgressList(BaseModel):
    progress: List[DiscoverProgress]
    complete: bool
    result: Resultenum


class ClaimOperation(BaseModel):
    OPERATION: ClaimOpEnum
    MODEL: str = Field(
        ...,
        description=(
            "Model type of the device to operate on. Should be the same value as "
            "what came from DeviceDetail"
        ),
    )
    SERIAL: str = Field(
        ...,
        description=(
            "Serial number of the device to operate on. Should be the same value "
            "as what came from DeviceDetail"
        ),
    )
    TYPE: str = Field(
        ...,
        description=(
            "Device type of the device to operate on. Should be the same value "
            "as what came from DeviceDetail"
        ),
    )


class ClaimOperationList(BaseModel):
    __root__: List[ClaimOperation]


class DeviceDetail(BaseModel):
    OPERATION: ClaimOpEnum | None = None
    panid: float | None = Field(
        None,
        description=(
            "PAN ID is used to determine whether an MI is A) Un-associated (panid = 0),"
            "B) owned by 'me' (mi.panid == pvs.panid) or C) owned by someone else "
            "(mi.panid != 0 && mi.panid != pvs.panid)"
        ),
    )
    rssi: float | None = Field(
        None,
        description=(
            "Received signal strength indicator. Systems will tend to clump together "
            "by their Receive Signal Strength Indicator"
        ),
    )
    ISDETAIL: str | None = Field(None, description="Legacy field")
    SERIAL: str | None = Field(None, description="The serial number of the device")
    TYPE: str | None = Field(
        None,
        description=(
            "The detailed type of the device (usually includes the manufacturer)"
        ),
        examples=["PVS5-METER-P"],
    )
    STATE: str | None = Field(None, description="Legacy field")
    STATEDESCR: str | None = Field(None, description="Legacy field")
    MODEL: str | None = Field(
        None,
        description="The manufacturer's model of the device",
        examples=["PVS6M0400p"],
    )
    DESCR: str | None = Field(None, description="Legacy field")
    DEVICE_TYPE: DeviceTypeEnum | None = None
    subtype: Any | None = Field(
        None,
        description=(
            "The device subtype. The available values depend on the device type. "
            'For DEVICE_TYPE=="Power Meter" see MeterSubtypeEnum'
        ),
    )
    SWVER: str | None = Field(None, description="Legacy field")
    PORT: str | None = Field(None, description="Legacy field")
    MOD_SN: str | None = Field(None, description="Legacy field")
    NMPLT_SKU: str | None = Field(None, description="Legacy field")
    DATATIME: str | None = Field(None, description="Legacy field")
    ltea_3phsum_kwh: str | None = Field(None, description="Legacy field")
    p_3phsum_kw: str | None = Field(None, description="Legacy field")
    vln_3phavg_v: str | None = Field(None, description="Legacy field")
    i_3phsum_a: str | None = Field(None, description="Legacy field")
    v_mppt1_v: str | None = Field(None, description="Legacy field")
    i_mppt1_a: str | None = Field(None, description="Legacy field")
    t_htsnk_degc: str | None = Field(None, description="Legacy field")
    freq_hz: str | None = Field(None, description="Legacy field")
    CURTIME: str | None = Field(None, description="Legacy field")
    PANEL: str | None = Field(
        None,
        description=(
            "The model of the panel(s) attached to the inverter (valid if DEVICE_TYPE "
            "is Inverter, i.e. for microinverters and string inverters). MIs are "
            "attached to only one panel. String inverters are attached to multiple "
            "panels, `moduleCount` contains how many."
        ),
    )
    moduleCount: int | None = Field(
        None,
        description=(
            "The number of panels for string inverters (valid if DEVICE_TYPE is "
            "Inverter)"
        ),
    )


class DeviceList(BaseModel):
    __root__: List[DeviceDetail]


class SupervisorInfo(BaseModel):
    FWVER: str | None = Field(None, examples=["1.0.0"])
    MODEL: str | None = Field(None, examples=["PVS6"])
    SERIAL: str | None = Field(None, examples=["ZT184585000549A0069"])
    SWVER: str | None = Field(None, examples=["2019.11, Build 5000"])
    SCVER: float | None = Field(None, examples=[16504])
    EASICVER: float | None = Field(None, examples=[67072])
    WNVER: float | None = Field(None, examples=[3000])
    BUILD: float | None = Field(None, examples=[5000])


class MetaData(BaseModel):
    SERIAL: str = Field(
        ..., description="Serial number of device", examples=["ZT992019230700A0032"]
    )
    subtype: Any | None = Field(
        None,
        description=(
            "The device subtype. Valid values depend on the device type. "
            "For meters the valid types are MeterSubtypeEnum"
        ),
    )
    panel: str | None = Field(None, description="The panel model (for inverters)")
    moduleCount: int | None = Field(
        None, description="The number of panels (for string inverters)"
    )
    SUBTYPE: Any | None = Field(None, description='DEPRECATED. An alias for "subtype"')
    modelStr: str | None = Field(None, description='DEPRECATED. An alias for "panel"')


class Zipcode(BaseModel):
    max: float | None = Field(None, examples=[96898])
    min: float | None = Field(None, examples=[96701])


class GridProfile(BaseModel):
    default: bool | None = None
    filename: str | None = Field(None, examples=["8c9c4170.meta"])
    id: str | None = Field(None, examples=["8c9c4170457c88f6dcee7216357681d580a3b9bd"])
    name: str | None = Field(None, examples=["HECO OMH R14H (Legacy)"])
    selfsupply: bool | None = None
    zipcodes: List[Zipcode] | None = None


class P2pPairingInfo(BaseModel):
    client_name: str | None = Field(None, examples=["CM2"])
    fingerprint: str | None = Field(
        None, examples=["22:66:74:4b:97:bf:9a:af:b2:70:4e:4b:79:9c:f6:2f"]
    )


class Body(BaseModel):
    message: str | None = Field(None, examples=["p2p client paired."])


class P2pClientPaired(BaseModel):
    status: int | None = Field(None, examples=[200])
    body: Body | None = None


class Inverter(BaseModel):
    serialNumber: str | None = None


class Ap(BaseModel):
    attributes: str | None = Field(None, examples=["wpa-psk"])
    bssid: str | None = Field(None, examples=["5c:f4:ab:a7:df:18"])
    channel: str | None = Field(None, examples=["6"])
    frequency: str | None = Field(None, examples=["2437"])
    rssi: str | None = Field(None, examples=["-13"])
    ssid: str | None = Field(None, examples=["ZyXEL"])


class DatalessResponse(BaseModel):
    result: Resultenum
    line: float | None = Field(
        None, description="The line in the source code that generated the error"
    )
    description: str | None = None


class DataFWResponse(BaseModel):
    supervisor: SupervisorInfo | None = None
    ATTEMPTS: str | None = Field(None, examples=["0"])
    uptime: str | None = Field(None, examples=["6087"])
    STATE: str | None = Field(None, examples=["complete"])
    PERCENT: str | None = Field(None, examples=["10"])


class PowerProductionSetting(BaseModel):
    powerProduction: PowerProduction | None = None


class PowerProductionStatus(BaseModel):
    powerProduction: PowerProduction | None = None
    result: str | None = None


class CertMQTTFailed(BaseModel):
    status: Status1
    info: Info | None = None


class InterfaceConfiguration(BaseModel):
    networkType: NetworkType | None = None
    configurationType: ConfigurationType | None = None
    ipAddress: str | None = None
    subnetMask: str | None = None
    gateway: str | None = None
    dnsServer: str | None = None


class External(BaseModel):
    device: str | None = None
    port: str | None = None


class Internal(BaseModel):
    device: str | None = None
    port: str | None = None


class FirewallSetting(BaseModel):
    firewallSettingsId: str | None = Field(
        None,
        description=(
            "Some unique string that can be used to reference this single "
            "firewallSetting from the firewallSettings list."
        ),
    )
    external: External | None = None
    internal: Internal | None = None
    protocol: str | None = None
    enable: bool | None = None


class FirewallSettingsConfiguration(BaseModel):
    FirewallSettings: List[FirewallSetting] | None = None


class GeneralSettings(BaseModel):
    lan2PortMode: str | None = None
    lan1IpAddress: str | None = None
    lan1Netmask: str | None = None
    lan1dhcpRange: str | None = None
    dhcpStatus: str | None = None


class ResultSucceed(BaseModel):
    result: Result1


class PingData(BaseModel):
    status: Status2 = Field(
        ...,
        description=(
            "how we decide to keep polling or not. If pending, keep polling, if "
            "success, stop polling. if fail, we failed"
        ),
    )
    source: str | None = Field(None, description="the output of the ping call")


class NetworkInterface(BaseModel):
    interface: str | None = Field(None, description="The interface name")
    alias: str | None = Field(None, description="What should be displayed to the user")


class PingOptions(BaseModel):
    address: str = Field(..., description="The ip address to ping")
    interface: str | None = Field(
        None,
        description=(
            "The interface on the PVS to ping through. If this isn't specified we use "
            "any of them"
        ),
    )
    pingCount: int


class PingableDevice(BaseModel):
    address: str | None = Field(None, description="The IP Address of the device")
    alias: str | None = Field(
        None, description="The name of the device that should be displayed to the user"
    )


class TunnelStatus(BaseModel):
    hostlist: List[str] | None = Field(
        None, description="An array of hostname:port of currently open tunnels"
    )


class TunnelOptions(BaseModel):
    hostname: str | None = Field(
        None, description="The hostname of the server to tunnel through"
    )
    port: int | None = Field(None, description="The remote port number to use")


class TracerouteOptions(BaseModel):
    address: str | None = Field(None, description="The ip address to traceroute to")
    interface: str | None = Field(
        None,
        description=(
            "The interface on the PVS to traceroute through, if this is not provided "
            "we use any interface. Valid interfaces come form the dl_cgi to get "
            "network interfaces"
        ),
    )


class TraceRouteObject(BaseModel):
    status: Status2 = Field(
        ..., description="The process ID of the traceroute that was started"
    )
    source: str | None = Field(
        None,
        description=(
            "The output of the traceroute call that gets called from the PVS "
            "to wherever"
        ),
    )


class Whitelist(BaseModel):
    hostname: str | None = None


class HubPlusStatus(BaseModel):
    serial_number: str | None = None
    last_updated: DateDesc | None = None
    contactor_error: ContactorError | None = None
    contactor_position: ContactorPosition | None = None
    grid_voltage_state: GridVoltageState | None = None
    grid_frequency_state: GridFrequencyState | None = None
    load_voltage_state: LoadVoltageState | None = None
    load_frequency_state: LoadFrequencyState | None = None
    hub_temperature: ValueAndUnit | None = None
    hub_humidity: ValueAndUnit | None = None
    jump_start_voltage: ValueAndUnit | None = None
    aux_port_voltage: ValueAndUnit | None = None
    main_voltage: ValueAndUnit | None = None
    inverter_connection_voltage: ValueAndUnit | None = None
    grid_phase1_voltage: ValueAndUnit | None = None
    grid_phase2_voltage: ValueAndUnit | None = None
    load_phase1_voltage: ValueAndUnit | None = None
    load_phase2_voltage: ValueAndUnit | None = None


class PcsSettings(BaseModel):
    msp_breaker: ValueAndUnit | None = None
    msp_busbar: ValueAndUnit | None = None
    hubplus_breaker: ValueAndUnit | None = None
    hubplus_busbar: ValueAndUnit | None = None


class EssState(BaseModel):
    storage_controller_status: StorageControllerStatus | None = Field(
        None,
        description=(
            "The status of the storage controller. This informs the user about whether "
            "the system is set up and operational."
        ),
    )
    pcs_mode: PcsMode | None = Field(
        None,
        description=(
            "The operational mode of power control system. This defines how the power "
            "control system behaves."
        ),
    )
    pcs_status: PcsStatus | None = Field(
        None,
        description=(
            "The status of the power control system. This informs the user about "
            "whether the power control system is enabled or not."
        ),
    )
    operational_mode: OperationalMode | None = Field(
        None,
        description=(
            "The operational mode of the storage system. This defines how the storage "
            "controller behaves."
        ),
    )
    permission_to_operate: bool | None = Field(
        None,
        description=(
            "The PTO state of the system. If true, the controller will operate "
            "based on the operational_mode. If false, the controller will charge "
            "the system to a set SOC and hold."
        ),
    )


class PhaseReading(BaseModel):
    last_updated: DateDesc | None = None
    current: ValueAndUnit | None = None
    voltage: ValueAndUnit | None = None
    power: ValueAndUnit | None = None


class CheckListItem(BaseModel):
    mandatory: bool | None = Field(None, description="These checks must always be run.")
    check_name: str | None = None


class SystemHealthCheckListItem(BaseModel):
    category: Category | None = None
    check_list: List[CheckListItem] | None = None


class SystemHealthCheckList(BaseModel):
    __root__: List[SystemHealthCheckListItem]


class SystemHealthCheckListStatus(BaseModel):
    check_name: str | None = None
    progress: float | None = None
    status: Status4 | None = None
    errors: List[str] | None = None


class BackupInverterNameplatePower(BaseModel):
    last_updated: DateDesc | None = None
    power: ValueAndUnit | None = None


class NonBackupInverterNameplatePower(BaseModel):
    last_updated: DateDesc | None = None
    power: ValueAndUnit | None = None


class AggregateMiProductionReading(BaseModel):
    last_updated: DateDesc | None = None
    agg_power: ValueAndUnit | None = None


class Meter(BaseModel):
    reading: PhaseReading | None = None


class ProductionMeterReading(BaseModel):
    last_updated: DateDesc | None = None
    agg_power: ValueAndUnit | None = None
    meter: Meter | None = None


class MeterA1(BaseModel):
    reading: PhaseReading | None = None
    current_transducer_status: CurrentTransducerStatus | None = None


class MeterB1(BaseModel):
    reading: PhaseReading | None = None
    current_transducer_status: CurrentTransducerStatus1 | None = None


class ConsumptionMeterReading(BaseModel):
    last_updated: DateDesc | None = None
    agg_power: ValueAndUnit | None = None
    meter_a: MeterA1 | None = None
    meter_b: MeterB1 | None = None


class EquinoxSystemStatus(BaseModel):
    last_updated: DateDesc | None = None
    backup_inverter_nameplate_power: BackupInverterNameplatePower | None = None
    non_backup_inverter_nameplate_power: NonBackupInverterNameplatePower | None = None
    aggregate_mi_production_reading: AggregateMiProductionReading | None = Field(
        None, description="Aggregated average power over polling interval of MIs"
    )
    production_meter_reading: ProductionMeterReading | None = None
    consumption_meter_reading: ConsumptionMeterReading | None = None


class GridProfileDeviceStatus(BaseModel):
    device: Device | None = None
    active_id: str | None = Field(
        None, examples=["a81641c29c2ee61f55807d9435dc4898805b2840"]
    )
    target_id: str | None = Field(
        None, examples=["a81641c29c2ee61f55807d9435dc4898805b2840"]
    )
    percent: float | None = Field(None, examples=[100])
    status: str | None = Field(None, examples=["success"])


class GridProfileSystemStatus(BaseModel):
    system: System1 | None = None
    active_id: str | None = Field(
        None, examples=["a81641c29c2ee61f55807d9435dc4898805b2840"]
    )
    target_id: str | None = Field(
        None, examples=["a81641c29c2ee61f55807d9435dc4898805b2840"]
    )
    devices: List[GridProfileDeviceStatus] | None = None


class PCSSettings(BaseModel):
    main_service_panel_breaker: int | None = None
    main_service_panel_busbar: int | None = None
    hubplus_breaker: int | None = None
    hubplus_busbar: int | None = None
    enable_pcs: bool | None = None


class Inverters(BaseModel):
    __root__: List[Inverter]


class Aps(BaseModel):
    __root__: List[Ap]


class CommunicationAp(BaseModel):
    aps: Aps | None = None
    result: Resultenum | None = None


class StringInverters(BaseModel):
    found: Inverters | None = None
    missing: Inverters | None = None


class MicroInverters(BaseModel):
    found: Inverters | None = None
    missing: Inverters | None = None


class DiscoveryInverters(BaseModel):
    stringInverters: StringInverters | None = None
    microInverters: MicroInverters | None = None


class NetworkInterfaces(BaseModel):
    __root__: List[NetworkInterface]


class PingableDevices(BaseModel):
    __root__: List[PingableDevice]


class MeterA(BaseModel):
    reading: PhaseReading | None = None


class MeterB(BaseModel):
    reading: PhaseReading | None = None


class EssMeterReading(BaseModel):
    last_updated: DateDesc | None = None
    agg_power: ValueAndUnit | None = None
    meter_a: MeterA | None = None
    meter_b: MeterB | None = None


class EnergyStorageSystemStatus(BaseModel):
    last_updated: DateDesc | None = None
    serial_number: str | None = None
    enclosure_humidity: ValueAndUnit | None = None
    enclosure_temperature: ValueAndUnit | None = None
    ess_meter_reading: EssMeterReading | None = None


class BatteryStatus(BaseModel):
    serial_number: str | None = None
    last_updated: DateDesc | None = None
    battery_amperage: ValueAndUnit | None = None
    battery_voltage: ValueAndUnit | None = None
    state_of_charge: ValueAndUnit | None = None
    temperature: ValueAndUnit | None = None


class InverterStatus(BaseModel):
    serial_number: str | None = None
    last_updated: DateDesc | None = None
    ac_current: ValueAndUnit | None = None
    phase_a_current: ValueAndUnit | None = None
    phase_b_current: ValueAndUnit | None = None
    a_n_voltage: ValueAndUnit | None = None
    b_n_voltage: ValueAndUnit | None = None
    ac_power: ValueAndUnit | None = None
    temperature: ValueAndUnit | None = None


class EssStatusReport(BaseModel):
    last_updated: DateDesc | None = None
    battery_status: List[BatteryStatus] | None = None
    ess_status: List[EnergyStorageSystemStatus] | None = None
    hub_plus_status: HubPlusStatus | None = None
    inverter_status: List[InverterStatus] | None = None
    pcs_settings: PcsSettings | None = None
    ess_state: EssState | None = None
