import numpy as np
import os
import pyopencl as cl
import sys

print("Thanks to xSonoro & XeClutch for their work.")
print("")

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

cl_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rage-hash.cl')
f = open(cl_filename , mode='r')
prg = cl.Program(ctx, f.read()).build()
f.close()

if len(sys.argv) != 4:
    print("Invalid Arguments.")
    exit()

hash = int(sys.argv[1], 16)
print("Only len 8 for now")
# len_min = int(sys.argv[2])
# len_max = int(sys.argv[3])

kernel_hash_count = pow(27, 4)
parallel_pow = 4 # 27 ^ x
base_real = b'_' * 64
stride_fast = np.empty((64,), dtype=np.uint8)
stride_fast.fill(0)
stride_fast[parallel_pow] = 1

mf = cl.mem_flags
buf_base_real = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=base_real)
buf_stride_fast = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=stride_fast)

print("Solving hash: 0x{:02x}".format(hash))
sys.stdout.flush()

knl = prg.brute
knl(
    queue,
    (pow(27, parallel_pow),),
    None,
    buf_base_real,
    buf_stride_fast,
    cl.cltypes.uint(0),                 # skip
    cl.cltypes.uint(8),                 # len
    cl.cltypes.uint(kernel_hash_count), # count
    cl.cltypes.uint(hash))              # hash
