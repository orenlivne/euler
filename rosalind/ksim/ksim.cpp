/*
  Approximate substring matching using dynamic programming.
  To recover all match starts, we solve another DP problem for each
  match endpoint j.
*/
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <vector>
#include <stdlib.h>
#include <time.h>
using namespace std;

#define LINE_SIZE 50000 // Maximum line size in input file

string reverse(const string& normal)
{
  string rev(normal);
  reverse(rev.begin(), rev.end());
  return rev;
}

double diffclock(const clock_t& clock1, const clock_t& clock2) {
  double diffticks = clock1 - clock2;
  double diffms = diffticks/CLOCKS_PER_SEC;
  return diffms;
} 

void print_vector(const vector<int>& c) {
  for (int j = 0; j < c.size(); j++) cout << c[j] << " "; cout << "\n";
}

vector<int> edit_distance_ending_at(const string& x, const string& y, int free_x_gaps) {
  // Edit distance. Lean storage row-by-row DP, O(mn) time, O(n) storage.
  int n = y.length();
  vector<int> c(n+1, 0);
  vector<int> c_old(n+1, 0);
  if (!free_x_gaps) {
    for (int j = 0; j <= n; j++) c[j] = j;
  }
  //print_vector(c);
  for (int i = 1; i <= x.length(); i++) {
    char xi = x[i-1];
    for (int j = 0; j <= n; j++) c_old[j] = c[j];
    c[0] = i;
    for (int j = 1; j <= n; j++)
      c[j] = (xi == y[j-1]) ? c_old[j-1] : min(min(c_old[j-1], c_old[j]), c[j-1]) + 1;
    //    print_vector(c);    
  }
  return c;
}

void ksim(const string& t, const string& s, int k) {
  // Find all occurrences of s starting at any position in t, with at most
  // k mismatches, ins insertions and del deletions.
  vector<int> b = edit_distance_ending_at(s, t, 1);
  //  print_vector(b);
  string rev_s = reverse(s);
  //  cout << rev_s << "\n";
  int m = s.length();
  for (int j = 0; j <= t.length(); j++) {
    //cout << "j " << j << " " << b[j] << " " << k << "\n";
    if (b[j] <= k) {
      int i = max(j - m - k, 0);
      //      cout << "j " << j << " i " << i << "\n";
      string tt = reverse(t.substr(i ,j-i));
      //      cout << "tt " << tt << "\n";
      vector<int> a = edit_distance_ending_at(rev_s, tt, 0);
      //      print_vector(a);
      for (int offset = 0; offset < a.size(); offset++) {
	if (a[offset] <= k)
	  cout << j - offset + 1 << " " << offset << "\n";
      }
    }
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
      else if (line_num == 1) s = str;
      else if (line_num == 2) t = str;
      line_num++;
    }
  //    cout << "k = " << k << "\n";
  //    cout << "s = '" << s << "'\n";
  //    cout << "t = '" << t << "'\n";

  //  clock_t begin=clock();
  ksim(t, s, k);
  clock_t end=clock();
  //  cout << "Time elapsed: " << double(diffclock(end,begin)) << " sec" << endl;
  return 0;
}
