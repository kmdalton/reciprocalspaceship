from reciprocalspaceship import DataSet
import msgpack
import numpy as np


# These are just functions which convert raw bytes from 
# the msgpack to formats the DataSet constructor may parse
handlers = {
    'double' : lambda x: np.frombuffer(x, dtype='float64'),
    'bool' : lambda x: np.frombuffer(x, dtype='bool'),
    'vec3<double>' : lambda x: np.frombuffer(x, dtype='float64').reshape((-1, 3)).tolist(),
    'vec2<double>' : lambda x: np.frombuffer(x, dtype='float64').reshape((-1, 2)).tolist(),
    'int6' : lambda x: np.frombuffer(x, dtype='int32').reshape((-1, 6)).tolist(),
    'std::size_t' : lambda x: np.frombuffer(x, dtype='int64'),
    'cctbx::miller::index<>' : lambda x: np.frombuffer(x, dtype='int32').reshape((-1, 3)).tolist(),
    'int' : lambda x: np.frombuffer(x, dtype='int32'),
}


def read_refl(reflfile : str) -> DataSet:
    """
    A parser for DIALS `.refl` files in the current (msgpack) format.

    Parameters 
    ----------
    reflfile : str
        DIALS reflection file `.refl`

    Returns
    -------
    reciprocalspaceship.DataSet
    """
    with open(reflfile, 'rb') as f:
        refl_msgpack = msgpack.load(f)
        data = refl_msgpack[2]['data']
        columns = {k : handlers[v[0]](v[1][1]) for k,v in data.items()}
        ds = DataSet(columns)
    return ds


