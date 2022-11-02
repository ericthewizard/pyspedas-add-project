# pyspedas-add-project
This project allows you to generate the initial code for a load routine in PySPEDAS. 

Example input:
```yaml
Mission: Space Weather Follow On-Lagrange 1 (SWFO)
Instruments:
  Fluxgate Magnetometer (FGM):
    examples: b_field
    levels: l2
    datatypes: flux, eflux
  SupraThermal Ion Sensor (STIS):
    examples: swfo_stis_eflux, swfo_stis_flux
    levels: l1, l2 (default)
Default trange: ['2025-11-5', '2025-11-6']
```

Save this as `swfo.yaml`, and create the plug-in by running:

```python
from create import create
create('swfo.yaml')
```

The output files will be stored in the `swfo` directory.