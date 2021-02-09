import numpy as np
import os
import pyopencl as cl
import sys

print("Thanks to xSonoro & XeClutch for their work.")
print("")

if len(sys.argv) != 4:
    print("Invalid Arguments.")
    exit()

hash = int(sys.argv[1], 16)
len_min = int(sys.argv[2])
len_max = int(sys.argv[3])

parallel = 100000
sequential = 100000
rnd_gen = np.random.default_rng()
seeds = np.empty(parallel * 2, dtype=np.uint32)
for i in range(parallel * 2):
    t = np.uint32
    seeds[i] = rnd_gen.integers(low=np.iinfo(t).min, high=np.iinfo(t).max, dtype=t, endpoint=True)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
buf_seeds = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=seeds)

cl_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rage-hash.cl')
f = open(cl_filename , mode='r')
prg = cl.Program(ctx, f.read()).build()
f.close()

print("Solving hash: 0x{:02x}".format(hash))
sys.stdout.flush()

knl = prg.sum
for i in range(sequential):
    knl(
        queue,
        (parallel,),
        None,
        buf_seeds,
        cl.cltypes.uint(hash),
        cl.cltypes.uint(len_min),
        cl.cltypes.uint(len_max))
