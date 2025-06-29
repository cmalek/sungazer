"""Tests for the StartResponse model."""  # noqa: N999

import json
from pathlib import Path

import pytest

from sungazer.models.session import StartResponse


class TestStartResponse:
    """Test cases for the StartResponse model."""

    @pytest.fixture
    def sample_data(self) -> dict:
        """Load sample data from fixture file."""
        fixture_path = Path(__file__).parent / "fixtures" / "Start" / "Start.json"
        with Path(fixture_path).open(encoding="utf-8") as f:
            return json.load(f)

    def test_start_response_from_fixture(self, sample_data: dict) -> None:
        """
        Test StartResponse parsing from fixture data.

        Note: The fixture contains a nested 'supervisor' object, but the current
        model expects flat fields. This test extracts the supervisor data to
        match the model structure.
        """
        # Extract supervisor data to match current model structure
        supervisor_data = sample_data["supervisor"]
        response = StartResponse(**supervisor_data)  # type: ignore[arg-type]

        assert response.SWVER == "2021.9, Build 41001"
        assert response.SERIAL == "ZT01234567890ABCDEF"
        assert response.MODEL == "PVS6"
        assert response.FWVER == "1.0.0"
        assert response.SCVER == 16504
        assert response.EASICVER == 131329
        assert response.SCBUILD == 1185
        assert response.WNMODEL == 400
        assert response.WNVER == 3000
        assert response.WNSERIAL == 16
        assert response.BUILD == 41001

    def test_start_response_with_minimal_data(self) -> None:
        """Test StartResponse with only some fields populated."""
        data = {
            "SWVER": "2021.9, Build 41001",
            "SERIAL": "ZT01234567890ABCDEF",
            "MODEL": "PVS6",
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SWVER == "2021.9, Build 41001"
        assert response.SERIAL == "ZT01234567890ABCDEF"
        assert response.MODEL == "PVS6"
        assert response.FWVER is None
        assert response.SCVER is None
        assert response.EASICVER is None
        assert response.SCBUILD is None
        assert response.WNMODEL is None
        assert response.WNVER is None
        assert response.WNSERIAL is None
        assert response.BUILD is None

    def test_start_response_with_all_fields(self) -> None:
        """Test StartResponse with all fields populated."""
        data = {
            "SWVER": "2022.3, Build 52000",
            "SERIAL": "ZT9876543210FEDCBA",
            "MODEL": "PVS6",
            "FWVER": "2.1.0",
            "SCVER": 18000,
            "EASICVER": 140000,
            "SCBUILD": 2000,
            "WNMODEL": 500,
            "WNVER": 3500,
            "WNSERIAL": 20,
            "BUILD": 52000,
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SWVER == "2022.3, Build 52000"
        assert response.SERIAL == "ZT9876543210FEDCBA"
        assert response.MODEL == "PVS6"
        assert response.FWVER == "2.1.0"
        assert response.SCVER == 18000
        assert response.EASICVER == 140000
        assert response.SCBUILD == 2000
        assert response.WNMODEL == 500
        assert response.WNVER == 3500
        assert response.WNSERIAL == 20
        assert response.BUILD == 52000

    def test_start_response_with_none_values(self) -> None:
        """Test StartResponse with explicit None values."""
        data = {
            "SWVER": None,
            "SERIAL": None,
            "MODEL": None,
            "FWVER": None,
            "SCVER": None,
            "EASICVER": None,
            "SCBUILD": None,
            "WNMODEL": None,
            "WNVER": None,
            "WNSERIAL": None,
            "BUILD": None,
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SWVER is None
        assert response.SERIAL is None
        assert response.MODEL is None
        assert response.FWVER is None
        assert response.SCVER is None
        assert response.EASICVER is None
        assert response.SCBUILD is None
        assert response.WNMODEL is None
        assert response.WNVER is None
        assert response.WNSERIAL is None
        assert response.BUILD is None

    def test_start_response_with_empty_strings(self) -> None:
        """Test StartResponse with empty string values."""
        data = {"SWVER": "", "SERIAL": "", "MODEL": "", "FWVER": ""}
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SWVER == ""
        assert response.SERIAL == ""
        assert response.MODEL == ""
        assert response.FWVER == ""

    def test_start_response_with_zero_values(self) -> None:
        """Test StartResponse with zero numeric values."""
        data = {
            "SCVER": 0,
            "EASICVER": 0,
            "SCBUILD": 0,
            "WNMODEL": 0,
            "WNVER": 0,
            "WNSERIAL": 0,
            "BUILD": 0,
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SCVER == 0
        assert response.EASICVER == 0
        assert response.SCBUILD == 0
        assert response.WNMODEL == 0
        assert response.WNVER == 0
        assert response.WNSERIAL == 0
        assert response.BUILD == 0

    def test_start_response_with_large_numbers(self) -> None:
        """Test StartResponse with large numeric values."""
        data = {
            "SCVER": 999999,
            "EASICVER": 999999,
            "SCBUILD": 999999,
            "WNMODEL": 999999,
            "WNVER": 999999,
            "WNSERIAL": 999999,
            "BUILD": 999999,
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SCVER == 999999
        assert response.EASICVER == 999999
        assert response.SCBUILD == 999999
        assert response.WNMODEL == 999999
        assert response.WNVER == 999999
        assert response.WNSERIAL == 999999
        assert response.BUILD == 999999

    def test_start_response_with_special_characters_in_strings(self) -> None:
        """Test StartResponse with special characters in string fields."""
        data = {
            "SWVER": "2021.9, Build 41001 (Stable)",
            "SERIAL": "ZT01234567890ABCDEF_2023",
            "MODEL": "PVS6-Pro",
            "FWVER": "1.0.0-beta+rc1",
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SWVER == "2021.9, Build 41001 (Stable)"
        assert response.SERIAL == "ZT01234567890ABCDEF_2023"
        assert response.MODEL == "PVS6-Pro"
        assert response.FWVER == "1.0.0-beta+rc1"

    def test_start_response_with_long_strings(self) -> None:
        """Test StartResponse with long string values."""
        long_string = "Very Long String Value " * 10
        data = {
            "SWVER": long_string,
            "SERIAL": long_string,
            "MODEL": long_string,
            "FWVER": long_string,
        }
        response = StartResponse(**data)  # type: ignore[arg-type]

        assert response.SWVER == long_string
        assert response.SERIAL == long_string
        assert response.MODEL == long_string
        assert response.FWVER == long_string
