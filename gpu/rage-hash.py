import numpy as np
import os
import pyopencl as cl
import sys

print("Thanks to xSonoro & XeClutch for their work.")
print("")

def name_next(n, len):
    for i in range(len):
        if n[i] >= ord('z'):
            #overflow
            n[i] = ord('_')
            continue
        elif n[i] == ord('_'):
            # skip '`'
            n[i] = ord('a')
        else:
            n[i] = n[i] + 1
        return True
    return False

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

cl_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rage-hash.cl')
f = open(cl_filename , mode='r')
prg = cl.Program(ctx, f.read()).build()
f.close()

if len(sys.argv) != 4:
    print("Invalid argument count.")
    exit()

hash = int(sys.argv[1], 16)
len_min = int(sys.argv[2])
len_max = min(63, max(len_min, int(sys.argv[3])))

if len_min < 9:
    print("Minimum length needs to be at least 9")
    exit()

base_name = np.empty(64, dtype=np.uint8)
base_name.fill(ord('_'))


print("Solving hash: 0x{:02x}".format(hash))

knl = prg.brute9
for len_full in range(len_min, len_max + 1):
    print("  Length: {: <2}".format(len_full))
    len_pref = len_full - 9
    while True:
        sys.stdout.flush()
        buf_base_name = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=base_name)
        knl(
            queue,
            (pow(28, 4),),
            None,
            buf_base_name,              # name prefix
            cl.cltypes.uint(len_pref),  # skip
            cl.cltypes.uint(hash))      # hash
        if not name_next(base_name, len_pref):
            break
