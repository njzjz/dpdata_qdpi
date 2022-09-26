from dpdata.driver import Driver


@Driver.register('qdpi')
class QDPiDriver(Driver.get_driver("hybrid")):
    """QDPi."""
    def __init__(self, model: str) -> None:
        super().__init__([
            {'type':'dftb3'},
            {'type':'dp', "dp": model},
            ])
