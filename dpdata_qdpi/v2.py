import numpy as np
from dpdata.driver import Driver
from xtb.ase.calculator import XTB as OldXTB


class XTB(OldXTB):
    """ASE calculator for XTB with net charge."""

    def __init__(self, *args, charge=0, **kwargs):
        self.charge = charge
        super().__init__(*args, **kwargs)

    def _create_api_calculator(self):
        initial_charges = np.zeros(len(self.atoms))
        initial_charges[0] = self.charge
        self.atoms.set_initial_charges(initial_charges)
        return super()._create_api_calculator()


@Driver.register("qdpi/v2")
class QDPiv2Driver(Driver.get_driver("hybrid")):
    """QDPi v2.

    Parameters
    ----------
    model : str
        File name of the model.
    charge : int
        Charge of the system.
    **kwargs
        Keyword arguments for the XTB calculation.
    """

    def __init__(self, model: str, charge: int = 0, **kwargs) -> None:
        super().__init__(
            [
                {"type": "ase", "calculator": XTB(charge=charge), **kwargs},
                {"type": "dp", "dp": model},
            ]
        )
