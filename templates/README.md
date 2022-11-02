
## Colorado Student Space Weather Experiment (CSSWE)
The routines in this module can be used to load data from the Colorado Student Space Weather Experiment (CSSWE) mission. 

### Instruments
- Fluxgate Magnetometer (FGM)
- Relativistic Electron and Proton Telescope integrated little experiment (REPTile)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
fgm_vars = pyspedas.csswe.fgm(trange=['2013-11-5', '2013-11-6'])

tplot('bfield')
```


#### Relativistic Electron and Proton Telescope integrated little experiment (REPTile)

```python
reptile_vars = pyspedas.csswe.reptile(trange=['2013-11-5', '2013-11-6'])

tplot(['E1flux', 'P1flux'])
```

