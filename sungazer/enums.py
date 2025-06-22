from enum import Enum


class Resultenum(Enum):
    """Enumeration for operation results."""

    succeed = "succeed"  # Operation completed successfully
    error = "error"  # Operation failed with an error


class Result1(Enum):
    """Alternative result enumeration with succeed/fail values."""

    succeed = "succeed"  # Operation succeeded
    fail = "fail"  # Operation failed


class ClaimOpEnum(Enum):
    """Operations that can be performed on device claims."""

    add = "add"  # Add device to system
    delete = "delete"  # Remove device from system
    noop = "noop"  # No operation (placeholder)


class DeviceTypeEnum(Enum):
    """Types of devices that can be discovered and managed."""

    PVS = "PVS"  # Photovoltaic Supervisor
    Inverter = "Inverter"  # Solar inverter
    Power_Meter = "Power Meter"  # Electrical power meter
    MET_Station = "MET Station"  # Meteorological station
    Ground_Current_Monitor = "Ground Current Monitor"  # Ground fault monitor
    Energy_Storage_System = "Energy Storage System"  # Battery storage system
    HUB_ = "HUB+"  # Communication hub
    Battery = "Battery"  # Battery unit
    Storage_Inverter = "Storage Inverter"  # Battery inverter
    ESS_Hub = "ESS Hub"  # Energy storage system hub
    ESS_BMS = "ESS BMS"  # Battery management system
    Gateway = "Gateway"  # Communication gateway
    PV_Disconnect = "PV Disconnect"  # Safety disconnect switch


class MeterSubtypeEnum(Enum):
    """Subtypes for power meter devices."""

    GROSS_CONSUMPTION_LINESIDE = (
        "GROSS_CONSUMPTION_LINESIDE"  # Total consumption before main panel
    )
    GROSS_PRODUCTION = "GROSS_PRODUCTION"  # Total solar production
    NET_CONSUMPTION_LOADSIDE = (
        "NET_CONSUMPTION_LOADSIDE"  # Net consumption after main panel
    )
    NOT_USED = "NOT_USED"  # Meter not in use
    STORAGE_METER = "STORAGE_METER"  # Battery storage meter
    UNKNOWN_TYPE = "UNKNOWN_TYPE"  # Meter type not determined


class PowerProduction(Enum):
    """Power production control states."""

    On = "On"  # Power production enabled
    Off = "Off"  # Power production disabled


class Status(Enum):
    """Generic status enumeration."""

    ok = "ok"  # Status is OK


class Status1(Enum):
    """Alternative status enumeration for failures."""

    failed = "failed"  # Operation failed


class Info(Enum):
    """Information messages for certificate operations."""

    MQTT_certificate_was_created_and_is_invalid_ = (
        "MQTT certificate was created and is invalid."
    )
    MQTT_certificate_creation_failed_ = "MQTT certificate creation failed."


class NetworkType(Enum):
    """Types of network connections."""

    PLC = "PLC"  # Power Line Communication
    ETH = "ETH"  # Ethernet
    WIFI = "WIFI"  # Wireless


class ConfigurationType(Enum):
    """Network configuration types."""

    DHCP = "DHCP"  # Dynamic Host Configuration Protocol
    STATIC = "STATIC"  # Static IP configuration


class Status2(Enum):
    """Status enumeration for ongoing operations."""

    pending = "pending"  # Operation in progress
    success = "success"  # Operation completed successfully
    fail = "fail"  # Operation failed


class DEVICETYPE(Enum):
    """Device type for candidate devices."""

    Inverter = "Inverter"  # Solar inverter device


class MODEL(Enum):
    """AC Module model types."""

    AC_Module_Type_C = "AC_Module_Type_C"  # Type C AC module
    AC_Module_Type_D = "AC_Module_Type_D"  # Type D AC module
    AC_Module_Type_E = "AC_Module_Type_E"  # Type E AC module
    AC_Module_Type_G = "AC_Module_Type_G"  # Type G AC module


class MODELNO(Enum):
    """Numeric model identifiers."""

    integer_10 = 10  # Model number 10 (Type D)
    integer_11 = 11  # Model number 11 (Type E)
    integer_12 = 12  # Model number 12 (Type G)


class STATEDESCR(Enum):
    """Device discovery and initialization states."""

    NEW = "NEW"  # Device just discovered
    PINGING = "PINGING"  # Testing connectivity
    PING_OK = "PING_OK"  # Connectivity confirmed
    PING_ERROR = "PING_ERROR"  # Connectivity failed
    GETTING_VERSION_INFORMATION = (
        "GETTING_VERSION_INFORMATION"  # Retrieving firmware info
    )
    VERSION_INFORMATION_OK = "VERSION_INFORMATION_OK"  # Firmware info retrieved
    VERSION_INFORMATION_ERROR = "VERSION_INFORMATION_ERROR"  # Firmware info failed
    GETTING_PLC_STATS = "GETTING_PLC_STATS"  # Getting PLC statistics
    PLC_STATS_OK = "PLC_STATS_OK"  # PLC stats retrieved
    PLC_STATS_ERROR = "PLC_STATS_ERROR"  # PLC stats failed
    GETTING_PV_INFO = "GETTING_PV_INFO"  # Getting PV information
    PV_INFO_OK = "PV_INFO_OK"  # PV info retrieved
    PV_INFO_ERROR = "PV_INFO_ERROR"  # PV info failed
    OK = "OK"  # Device ready


class Origin(Enum):
    """Origin of device details."""

    mime = "mime"  # Details from microinverter enumeration


class StepStatus(Enum):
    """Status of commissioning or discovery steps."""

    NOT_RUNNING = "NOT_RUNNING"  # Step not started
    RUNNING = "RUNNING"  # Step in progress
    FAILED = "FAILED"  # Step failed
    SUCCEEDED = "SUCCEEDED"  # Step completed successfully


class EssDeviceType(Enum):
    """Energy storage system device types."""

    MIO = "MIO"  # Monitoring I/O device
    MIDC = "MIDC"  # Monitoring & Communications device
    GATEWAY = "GATEWAY"  # Communications gateway
    BATTERY = "BATTERY"  # Energy storage battery
    MICRO_INVERTER = "MICRO_INVERTER"  # Solar microinverter
    STORAGE_INVERTER = "STORAGE_INVERTER"  # Battery inverter


class ContactorError(Enum):
    """Hub Plus contactor error states."""

    NONE = "NONE"  # No error
    STUCK_OPEN = "STUCK_OPEN"  # Contactor stuck in open position
    STUCK_CLOSED_OR_MM_OPEN = (
        "STUCK_CLOSED_OR_MM_OPEN"  # Contactor stuck closed or maintenance mode open
    )
    MM_CLOSED = "MM_CLOSED"  # Maintenance mode closed
    MM_STUCK_OPEN = "MM_STUCK_OPEN"  # Maintenance mode stuck open
    MM_STUCK_CLOSED = "MM_STUCK_CLOSED"  # Maintenance mode stuck closed
    UNKNOWN = "UNKNOWN"  # Unknown error state


class ContactorPosition(Enum):
    """Physical position of the contactor."""

    UNKNOWN = "UNKNOWN"  # Position unknown
    OPEN = "OPEN"  # Contactor is open (disconnected)
    CLOSED = "CLOSED"  # Contactor is closed (connected)


class GridVoltageState(Enum):
    """Grid voltage monitoring states."""

    METER_VOLTAGE_IN_RANGE = "METER_VOLTAGE_IN_RANGE"  # Voltage within acceptable range
    METER_VOLTAGE_OUT_RANGE = (
        "METER_VOLTAGE_OUT_RANGE"  # Voltage outside acceptable range
    )
    METER_PHASE_LOSS = "METER_PHASE_LOSS"  # One or more phases missing
    METER_MISS_CONNECTION = "METER_MISS_CONNECTION"  # Meter connection issue


class GridFrequencyState(Enum):
    """Grid frequency monitoring states."""

    METER_FREQ_IN_RANGE = "METER_FREQ_IN_RANGE"  # Frequency within acceptable range
    METER_FREQ_OUT_RANGE = "METER_FREQ_OUT_RANGE"  # Frequency outside acceptable range


class LoadVoltageState(Enum):
    """Load voltage monitoring states."""

    METER_VOLTAGE_IN_RANGE = "METER_VOLTAGE_IN_RANGE"  # Voltage within acceptable range
    METER_VOLTAGE_OUT_RANGE = (
        "METER_VOLTAGE_OUT_RANGE"  # Voltage outside acceptable range
    )
    METER_PHASE_LOSS = "METER_PHASE_LOSS"  # One or more phases missing
    METER_MISS_CONNECTION = "METER_MISS_CONNECTION"  # Meter connection issue


class LoadFrequencyState(Enum):
    """Load frequency monitoring states."""

    METER_FREQ_IN_RANGE = "METER_FREQ_IN_RANGE"  # Frequency within acceptable range
    METER_FREQ_OUT_RANGE = "METER_FREQ_OUT_RANGE"  # Frequency outside acceptable range


class StorageControllerStatus(Enum):
    """Status of the energy storage controller."""

    UNKNOWN = "UNKNOWN"  # Status unknown
    NOT_RUNNING = "NOT_RUNNING"  # Controller not running
    RUNNING = "RUNNING"  # Controller running


class PcsMode(Enum):
    """Power Control System operation modes."""

    NONE = "NONE"  # No mode specified
    ESS_IMPORT_ONLY = "ESS_IMPORT_ONLY"  # Only import power from grid
    ESS_EXPORT_ONLY = "ESS_EXPORT_ONLY"  # Only export power to grid
    ESS_NO_EXCHANGE = "ESS_NO_EXCHANGE"  # No power exchange with grid


class PcsStatus(Enum):
    """Power Control System operational status."""

    UNKNOWN = "UNKNOWN"  # Status unknown
    DISABLED = "DISABLED"  # PCS is disabled
    ENABLED = "ENABLED"  # PCS is enabled


class OperationalMode(Enum):
    """Energy storage system operational modes."""

    UNKNOWN = "UNKNOWN"  # Mode unknown
    STANDBY = "STANDBY"  # Standby mode
    MANUAL_CHARGE = "MANUAL_CHARGE"  # Manual battery charging
    MANUAL_DCM = "MANUAL_DCM"  # Manual demand charge management
    DCM = "DCM"  # Automatic demand charge management
    TARIFF_OPTIMIZER = "TARIFF_OPTIMIZER"  # Time-of-use optimization
    ENERGY_ARBITRAGE = "ENERGY_ARBITRAGE"  # Energy buying/selling optimization
    SELF_CONSUMPTION = "SELF_CONSUMPTION"  # Maximizing self-consumption
    BACKUP_ONLY = "BACKUP_ONLY"  # Backup power only
    HECO_ZERO_EXPORT = "HECO_ZERO_EXPORT"  # Zero export (Hawaii Electric)


class Category(Enum):
    """System health check categories."""

    ACPV = "ACPV"  # AC photovoltaic components
    PLATFORM = "PLATFORM"  # System platform components
    STORAGE = "STORAGE"  # Energy storage components
    ALL = "ALL"  # All system components


class Status4(Enum):
    """System health check status values."""

    FAILED = "FAILED"  # Check failed
    RUNNING = "RUNNING"  # Check in progress
    SUCCEEDED = "SUCCEEDED"  # Check passed
    UNSUPPORTED = "UNSUPPORTED"  # Check not supported
    WAITING = "WAITING"  # Check pending


class CurrentTransducerStatus(Enum):
    """Status of current transducer devices."""

    OK = "OK"  # Transducer operating normally
    NOT_FOUND = "NOT_FOUND"  # Transducer not detected
    UNKNOWN = "UNKNOWN"  # Status unknown


class CurrentTransducerStatus1(Enum):
    """Simplified status of current transducer devices."""

    OK = "OK"  # Transducer operating normally
    NOT_FOUND = "NOT_FOUND"  # Transducer not detected


class Device(Enum):
    """Device manufacturer/model types for grid profiles."""

    DEV_DELTA = "DEV_DELTA"  # Delta devices
    DEV_ESMM = "DEV_ESMM"  # ESMM devices
    DEV_MIME = "DEV_MIME"  # Enphase microinverters
    DEV_SMA = "DEV_SMA"  # SMA devices
    DEV_SUNSPEC = "DEV_SUNSPEC"  # SunSpec compatible devices


class System1(Enum):
    """System types for grid profile configuration."""

    SITE_PV = "SITE_PV"  # Photovoltaic system only
    SITE_ESS = "SITE_ESS"  # Energy storage system only
    SITE_ALL = "SITE_ALL"  # Complete system (PV + storage)
