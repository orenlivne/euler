/*
  Approximate substring matching using backtracking.
  From http://stackoverflow.com/questions/7557017/approximate-string-matching-using-backtracking
*/
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <stdlib.h>
using namespace std;

#define LINE_SIZE 50000 // Maximum line size in input file

void f(int start, const char* ss, const char* s, const char* t, int k) {
  // ss is the start of the haystack, used only for reporting the match endpoints.
  while (*s && *s == *t) {
    //cout << s << " " << t << " " << start << " " << s - ss << "\n";
    ++s, ++t;    // OK to always match longest segment
  }
  if (!*t) cout << start << " " << s - ss << "\n";  // Matched; print endpoint of match
  if (k) {
    if (*s && *t) f(start, ss, s + 1, t + 1, k - 1);
    if (*s) f(start, ss, s + 1, t, k - 1);
    if (*t) f(start, ss, s, t + 1, k - 1);
  }
}

void ksim(const char* s, const char* t, int k) {
  // Find all occurrences of t starting at any position in s, with at most
  // k mismatches, ins insertions and del deletions.
  for (const char* ss = s; *s; ++s) {
    cout << "Starting from text offset " << s - ss << "\n";
    f(s-ss, ss, s, t, k);
  }
}

int main(int argc, char **argv)
{
  if (argc != 2) {
    cerr << "Usage: " << argv[0] << "<in-file>\n";
    exit(-1);
  }
  // Read input file
  ifstream file(argv[1]);
  string str, s, t;
  int line_num = 0, k;
  while (getline(file, str))
    {
      if (line_num == 0) sscanf(str.c_str(), "%d", &k);
      else if (line_num == 1) t = str;
      else if (line_num == 2) s = str;
      line_num++;
    }
  //  cout << "k = " << k << "\n";
  //  cout << "t = '" << t << "'\n";
  //  cout << "s = '" << s << "'\n";
  ksim(s.c_str(), t.c_str(), k);
  return 0;
}
