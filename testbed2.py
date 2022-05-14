import numpy as np
import ctypes
import array
import multiprocessing as mp
import random
from contextlib import contextmanager, closing


def init_shared(ncell):
    '''Create shared value array for processing.'''
    shared_array_base = mp.Array(ctypes.c_float,ncell,lock=False)
    return(shared_array_base)

def tonumpyarray(shared_array):
    '''Create numpy array from shared memory.'''
    nparray= np.frombuffer(shared_array,dtype=ctypes.c_float)
    assert nparray.base is shared_array
    return nparray

def init_parameters(**kwargs):
    '''Initialize parameters for processing in workers.'''

    params = dict()

    for key, value in kwargs.items():
        params[key] = value
    return params


def init_worker(shared_array_,parameters_):
    '''Initialize worker for processing.

    Args:
        shared_array_: Object returned by init_shared
        parameters_: Dictionary returned by init_parameters
    '''
    global shared_array
    global shared_parr
    global dim

    shared_array = tonumpyarray(shared_array_)
    shared_parr = tonumpyarray(parameters_['shared_parr'])

    dim = parameters_['dimensions']

def worker_fun(ix):
    '''Function to be run inside each worker'''

    arr = tonumpyarray(shared_array)
    parr = tonumpyarray(shared_parr)

    arr.shape = dim

    random.seed(ix)
    rint = random.randint(1,10)

    parr[ix] = rint

    arr[ix,...] = arr[ix,...] * rint

##---------------------------------------------------------------------- 



def main():
    nrows = 100
    ncols = 10

    shared_array = init_shared(nrows*ncols)
    shared_parr = init_shared(nrows)

    params = init_parameters(shared_parr=shared_parr,dimensions=(nrows,ncols))

    arr = tonumpyarray(shared_array)
    parr = tonumpyarray(params['shared_parr'])

    arr.shape = (nrows,ncols)


    arr[...] = np.random.randint(1,100,size=(100,10),dtype='int16')


    with closing(mp.Pool(processes=8,initializer = init_worker, initargs = (shared_array,params))) as pool:

        res = pool.map(worker_fun,range(arr.shape[0]))

    pool.close()
    pool.join()

    # check PARR output
    print(parr)


if __name__ == '__main__':
    main()