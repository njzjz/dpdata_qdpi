from pathlib import Path

import dpdata
import pytest

from dpdata_qdpi import QDPiv2Driver


@pytest.fixture
def ch4():
    this_dir = Path(__file__).parent
    ch4 = dpdata.System(str(this_dir / "ch4.xyz"))
    return ch4


@pytest.fixture
def qdpi():
    qdpi = QDPiv2Driver(
        # just for test, no actual v2 model
        model="qdpi-1.0.pb",
        charge=0,
    )
    return qdpi


def test_single_point(ch4, qdpi):
    # single point calculation
    p = ch4.predict(driver=qdpi)
    print("Energies:", p["energies"][0])
    print("Forces:", p["forces"][0])
