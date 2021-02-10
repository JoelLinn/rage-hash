
#define MAX_NAME_LEN 63
#define GUESSES_PER_KERNEL (100 * 1000)

// charset "_abcdefghijklmnopqrstuvwxyz" <=> '\0'..'\26'
inline char char2num(char c)
{
  if (c > '_')
  {
    // skip '`'
    c -= 1;
  }
  c -= '_';
  return c;
}
inline char num2char(char c)
{
  c += '_';
  if (c > '_')
  {
    // skip '`'
    c += 1;
  }
  return c;
}
void name_real2fast(char* fast, uint* plen_fast, char* real)
{
  uint i = 0;
  for (; real[i] != 0; i++)
  {
    fast[i] = char2num(real[i]);
  }
  *plen_fast = i;
}
void name_fast2real(char* real, char* fast, uint len_fast)
{
  uint i = 0;
  for (; i < len_fast; i++)
  {
    real[i] = num2char(fast[i]);
  }
  real[i] = 0;
}

// charset = '\0'..'\26'
uint hash_name(char* name, uint name_len)
{
  uint hash = 0;
  char c;
  for (int i = 0; i < name_len; i++)
  {
    hash += num2char(name[i]);
    hash += hash << 10;
    hash ^= hash >> 6;
  }
  hash += hash << 3;
  hash ^= hash >> 11;
  return (hash + (hash << 15));
}

// charset = '\0'..'\26'
bool name_add(char* a, char* b, uint len)
{
  char overflow = 0;
  for (uint i = 0; i < len; i++)
  {
    //printf("%d %d %d %d \n", i, a[i], b[i], overflow);
    char c = a[i] + b[i] + overflow;
    overflow = 0;
    if (c > 26)
    {
      overflow = 1;
      c -= 27;
    }
    a[i] = c;
  }
  return !!overflow;
}

// charset = '\0'..'\26'
bool name_next(char* n, uint len)
{
  for (uint i = 0; i < len; i++)
  {
    if (n[i] >= 26) {
      // overflow
      n[i] = 0;
      continue;
    }
    ++n[i];
    return false;
	}
  return true;
}

__kernel void brute(__global char* base_real, __global char* stride_fast, uint skip, uint len, uint count, uint hash)
{
  int gid = get_global_id(1) * get_global_size(0) + get_global_id(0);

  char name[MAX_NAME_LEN + 1];
  char stride[MAX_NAME_LEN];
  for (uint i = 0; i < len; i++)
  {
    name[i] = base_real[i];
    stride[i] = stride_fast[i];
  }
  name[len + 1] = 0;
  name_real2fast(name, &len, name);

  uint i_;
  for (uint i = 0; i < gid; i++)
  {
    i_ = i;
    if (name_add(&name[skip], stride, len - skip))
    {
      // Overflow already
      return;
    }
  }

  for (uint i = 0; i < count; i++)
  {
    if (hash_name(name, len) == hash)
    {
      char name_pretty[MAX_NAME_LEN + 1];
      name_fast2real(name_pretty, name, len);
      printf("  Solved: %s\n", name_pretty);
    }
    if (name_next(&name[skip], len - skip))
    {
      // Overflow
      break;
    }
  }
}
