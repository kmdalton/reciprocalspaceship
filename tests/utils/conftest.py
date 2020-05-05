import pytest
from os import listdir
from os.path import dirname, abspath, basename, join
import re
import gemmi

def get_mtz_by_spacegroup():
    """
    Get absolute paths to MTZ files generated by phenix.fmodel for 
    testing crystallographic symmetry operations.
    """
    datadir = abspath(join(dirname(__file__) + '/../data/fmodel/'))
    files = [join(datadir, i) for i in listdir(datadir) if re.match(r'.*(?<!_p1).mtz$', i)]
    return files


@pytest.fixture(params=get_mtz_by_spacegroup())
def mtz_by_spacegroup(request):
    """Yields paths to MTZ files for each crystallographic spacegroup"""
    return request.param

@pytest.fixture(params=[gemmi.SpaceGroup(n) for n in [1, 4, 5, 19, 152]])
def common_spacegroup(request):
    """Yields common space groups for macromolecular crystals"""
    return request.param