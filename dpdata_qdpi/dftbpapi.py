import os
import tempfile

import numpy as np
from ase.calculators.dftb import Dftb
from dpdata.driver import Driver
from dpdata.unit import EnergyConversion, ForceConversion, LengthConversion
from dpdata.xyz.xyz import coord_to_xyz


@Driver.register("dftbplusapi/dftb3")
class DFTBPlusAPIDriver(Driver):
    """DFTB3 3ob driven by DFTB+ API.

    Parameters
    ----------
    charge : int
        Charge of the system.
    gpu : bool
        Whether to use MAGMA Solver for GPU support.
    """

    def __init__(self, charge: int = 0, gpu: bool = False) -> None:
        # disable OpenMP, which makes DFTB+ slower
        os.environ["OMP_NUM_THREADS"] = "1"
        kwargs = {}
        if gpu:
            kwargs["Hamiltonian_Solver"] = "MAGMA{}"
        slko_dir = os.path.join(os.path.dirname(__file__), "3ob", "skfiles")
        self.calc = Dftb(
            Hamiltonian_="DFTB",
            Hamiltonian_SCC="Yes",
            # enable DFTB3
            Hamiltonian_ThirdOrderFull="Yes",
            Hamiltonian_HubbardDerivs_="",
            # from DOI: 10.1021/ct300849w
            Hamiltonian_HubbardDerivs_H=-0.1857,
            Hamiltonian_HubbardDerivs_N=-0.1535,
            Hamiltonian_HubbardDerivs_O=-0.1575,
            Hamiltonian_HubbardDerivs_C=-0.1492,
            Hamiltonian_HCorrection_="",
            Hamiltonian_HCorrection_Damping_="",
            Hamiltonian_HCorrection_Damping_Exponent=4.0,
            Hamiltonian_charge=charge,
            Hamiltonian_MaxSCCIterations=200,
            slako_dir=os.path.join(slko_dir, ""),
            **kwargs,
        )
        self.length_conversion = LengthConversion("angstrom", "bohr")
        self.energy_conversion = EnergyConversion("hartree", "eV")
        self.force_conversion = ForceConversion("hartree/bohr", "eV/angstrom")

    def label(self, data: dict) -> dict:
        import dftbplus

        coords = data["coords"] * self.length_conversion
        energies = []
        gradients = []
        types = np.array(data["atom_names"])[data["atom_types"]]
        with open("geo_end.gen", "w") as f:
            f.write(coord_to_xyz(data["coords"][0], types))

        with tempfile.NamedTemporaryFile(mode="w") as f:
            cdftb = dftbplus.DftbPlus(
                hsdpath=f.name,
            )
            self.calc.write_dftb_in(f)
            for ii in range(coords.shape[0]):
                cc = coords[ii]
                cdftb.set_geometry(cc)
                energy = cdftb.get_energy()
                gradient = cdftb.get_gradients()
                energies.append(energy)
                gradients.append(gradient)

            cdftb.close()
        energies = np.array(energies) * self.energy_conversion
        forces = -np.array(gradients) * self.force_conversion
        return {**data, "energies": energies, "forces": forces}