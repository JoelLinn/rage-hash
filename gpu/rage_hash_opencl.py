import numpy as np
import os
import pyopencl as cl

from rage_hash import RageHash

class OpenCLRageHash(RageHash):
    def _gpu_init(self):
        self._ctx = cl.create_some_context()
        self._queue = cl.CommandQueue(self._ctx)

        cl_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rage-hash.cl')
        with open(cl_filename , mode='r') as f:
            self._prg = cl.Program(self._ctx, f.read()).build()
        self._knl = self._prg.brute9

    def _gpu_brute9(self, base_name, skip, hash):
        buf_base_name = cl.Buffer(self._ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=base_name)
        self._knl(
            self._queue,
            (pow(27, 4),),
            None,
            buf_base_name,          # name prefix
            cl.cltypes.uint(skip),  # skip
            cl.cltypes.uint(hash))  # hash

if __name__ == "__main__":
    OpenCLRageHash().main()
