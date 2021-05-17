import pytest
import numpy as np
import reciprocalspaceship as rs
from reciprocalspaceship import stats
import gemmi

@pytest.mark.parametrize("cell_and_spacegroup", [
    (gemmi.UnitCell(10., 20., 30., 90., 90., 90.), gemmi.SpaceGroup('P 21 21 21')),
    (gemmi.UnitCell(30., 30., 30., 90., 90., 120.), gemmi.SpaceGroup('R 32')),
])
@pytest.mark.parametrize("anomalous", [False, True])
def test_compute_redundancy(cell_and_spacegroup, anomalous):
    """ 
    Test reciprocalspaceship.stats.compute_redundancy.
    """
    dmin = 5.
    cell,spacegroup = cell_and_spacegroup
    hkl = rs.utils.generate_reciprocal_asu(cell, spacegroup, dmin, anomalous=anomalous)
    mult = np.random.choice(10, size=len(hkl))
    hobs = np.repeat(hkl, mult, axis=0)
    result = stats.compute_redundancy(hobs, cell, spacegroup, anomalous)
    assert len(hkl) == len(mult)
    assert np.all(result.loc[(i for i in hkl)].iloc[:,0] == mult.astype(float))
