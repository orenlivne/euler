#include <stdio.h>

/* Returns true if the machine is little-endian, false if the
 * machine is big-endian
 */
int endianness()
{
  int testNum = 1;
  return *((char *) &testNum);/* Returns the byte at the lowest address */
}

/* Returns true if the machine is little-endian, false if the
 * machine is big-endian
 */
int endianness2()
{
  union {
    int theInteger;
    char singleByte;
  } endianTest;
  endianTest.theInteger = 1;
  return endianTest.singleByte;
}

int main()
{ 
  printf("%s\n", endianness() ? "Little Endian" : "Big Endian"); 
  printf("%s\n", endianness2() ? "Little Endian" : "Big Endian");
  return 0;
}
