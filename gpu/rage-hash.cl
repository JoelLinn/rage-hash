
#define MAX_NAME_LEN 64

#if __CUDACC__
#define KERNEL __global__
#define FUNC __device__
#define MEM_POINTER
#define get_gid() (blockIdx.x * blockDim.x + threadIdx.x)
#else // OpenCL
#define KERNEL __kernel
#define FUNC
#define MEM_POINTER __global
#define get_gid() (get_global_id(1) * get_global_size(0) + get_global_id(0))
#endif

#define hash_init() 0
FUNC uint hash_addc(uint hash, char c)
{
  hash += c;
  hash += hash << 10;
  hash ^= hash >> 6;
  return hash;
}
FUNC uint hash_adds(uint hash, char* s, uint len_s)
{
  for (uint i = 0; i < len_s; i++)
  {
    hash = hash_addc(hash, s[i]);
  }
  return hash;
}
FUNC uint hash_final(uint hash)
{
  hash += hash << 3;
  hash ^= hash >> 11;
  return (hash + (hash << 15));
}
FUNC inline uint hash_name(char* name, uint len_name)
{
  return hash_final(hash_adds(hash_init(), name, len_name));
}

// brute on width of 9 characters
// 28^4 kernels need to be run, which try 5 characters each
KERNEL void brute9(MEM_POINTER char* base_name, uint skip, uint hash)
{
  int gid = get_gid();

  char name[MAX_NAME_LEN];
  for (uint i = 0; i < skip; i++)
  {
    name[i] = base_name[i];
  }
  name[skip + 9] = 0;

  int remainder = gid;
  for (char i = 0; i < 4; i++)
  {
    char c = remainder % 27;
    if (c > 0) c++; // skip '`'
    name[skip + i] = c + '_';
    remainder /= 27;
  }

  // charset "_abcdefghijklmnopqrstuvwxyz"
  uint hashes[6];
  hashes[0] = hash_adds(hash_init(), name, skip + 4);
  char c[5];
  for (c[0] = '_'; c[0] <= 'z'; c[0]++)
  {
    if (c[0] == '`') c[0]++;
    hashes[1] = hash_addc(hashes[0], c[0]);
    for (c[1] = '_'; c[1] <= 'z'; c[1]++)
    {
      if (c[1] == '`') c[1]++;
      hashes[2] = hash_addc(hashes[1], c[1]);
      for (c[2] = '_'; c[2] <= 'z'; c[2]++)
      {
        if (c[2] == '`') c[2]++;
        hashes[3] = hash_addc(hashes[2], c[2]);
        for (c[3] = '_'; c[3] <= 'z'; c[3]++)
        {
          if (c[3] == '`') c[3]++;
          hashes[4] = hash_addc(hashes[3], c[3]);
          for (c[4] = '_'; c[4] <= 'z'; c[4]++)
          {
            if (c[4] == '`') c[4]++;
            hashes[5] = hash_addc(hashes[4], c[4]);
            if (hash_final(hashes[5]) == hash)
            {
              name[skip + 4] = c[0];
              name[skip + 5] = c[1];
              name[skip + 6] = c[2];
              name[skip + 7] = c[3];
              name[skip + 8] = c[4];
              printf("    Solved: %s\n", name);
            }
          }
        }
      }
    }
  }
}
