
#define MAX_NAME_LEN 64
#define GUESSES_PER_KERNEL (100 * 1000)

// MWC64X
// http://cas.ee.ic.ac.uk/people/dt10/research/rngs-gpu-mwc64x.html
uint rnd(uint2 *state)
{
    enum { A=4294883355U};
    uint x=(*state).x, c=(*state).y;  // Unpack the state
    uint res=x^c;                     // Calculate the result
    uint hi=mul_hi(x,A);              // Step the RNG
    x=x*A+c;
    c=hi+(x<c);
    *state=(uint2)(x,c);              // Pack the state back up
    return res;                       // Return the next result
}

//inline uint rnd_range(uint* pseed, ulong min_inc, ulong max_exc)
inline uint rnd_range(uint2* state, ulong min_inc, ulong max_exc)
{
  return rnd(state) % (max_exc - min_inc) + min_inc;
}

uint hash_name(char* name)
{
  uint hash = 0;
  char c;
  for (int i = 0;; i++)
  {
    c = name[i];
    if (!c) break;

    hash += c;
    hash += hash << 10;
    hash ^= hash >> 6;
  }
  hash += hash << 3;
  hash ^= hash >> 11;
  return (hash + (hash << 15));
}

__kernel void sum(__global uint* seeds, uint hash, uint len_min, uint len_max)
{
  int gid = get_global_id(1) * get_global_size(0) + get_global_id(0);
  uint2 seed;
  seed.x = seeds[gid * 2];
  seed.y = seeds[gid * 2 + 1];

  uint len;
  char name[MAX_NAME_LEN];
  // don't block too long, just enque another kernel
  for (ulong i = 0; i < GUESSES_PER_KERNEL; i++)
  {
    len = rnd_range(&seed, len_min, min(len_max + 1, (uint)MAX_NAME_LEN));
    name[len] = 0;
    for (int j = 0; j < len; j++)
    {
      name[j] = rnd_range(&seed, 'a', 'z' + 2);
      if (name[j] > 'z') name[j] = '_';
    }

    if (hash_name(name) == hash) {
      printf("  Solved: %s\n", name);
    }
  }

  seeds[gid * 2] = seed.x;
  seeds[gid * 2 + 1] = seed.y;
}
