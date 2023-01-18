import dpdata
from qdpi import QDPiDriver
from dpdata.plugins.ase import ASEMinimizer

ch4 = dpdata.System("ch4.xyz")
qdpi = QDPiDriver(
    model="qdpi-1.0.pb",
    charge=0,
    backend="sqm",
)

# single point calculation
p = ch4.predict(driver=qdpi)
print("Energies:", p['energies'][0])
print("Forces:", p['forces'][0])

# Optimization
lbfgs = ASEMinimizer(
    driver=qdpi,
)
p = ch4.minimize(minimizer=lbfgs)
print("Coordinates:", p['coords'][0])
print("Energies:", p['energies'][0])
print("Forces:", p['forces'][0])
