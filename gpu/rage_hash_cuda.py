import numpy as np
import os
import pycuda.driver as cuda
from pycuda.compiler import SourceModule

from rage_hash import RageHash

class CUDARageHash(RageHash):
    def _gpu_init(self):
        import pycuda.autoinit

        cl_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rage-hash.cl')
        with open(cl_filename , mode='r') as f:
            self._mod = SourceModule(f.read()) #, options=["-ccbin", "gcc-9"])
            self._knl = self._mod.get_function("brute9")
        self._base_name_gpu = cuda.mem_alloc(self.NAME_MAX * np.uint8().itemsize)

    def _gpu_brute9(self, base_name, skip, hash):
        cuda.memcpy_htod(self._base_name_gpu, base_name)
        self._knl(
            self._base_name_gpu,    # name prefix
            np.uint32(skip),        # skip
            np.uint32(hash),        # hash
            block=(27 * 27, 1, 1),
            grid =(27 * 27, 1),
            time_kernel = True)     # synchronous

if __name__ == "__main__":
    CUDARageHash().main()
