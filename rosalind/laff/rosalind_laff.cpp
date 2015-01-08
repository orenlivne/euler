/*
============================================================
http://rosalind.info/problems/laff

Given: Two protein strings s and t in FASTA format (each
having length at most 10,000 aa).

Return: The maximum local alignment score of s and t,
followed by substrings r and u of s and t, respectively,
that correspond to the optimal local alignment of s and t

Use:
The BLOSUM62 scoring matrix.
Gap opening penalty equal to 11.
Gap extension penalty equal to 1.

If multiple solutions exist, then you may output any one.
============================================================
*/
#include <algorithm>
#include <sstream>
#include <iostream>
#include <fstream>
#include <climits>
#include <ctime>
#include <string>
#include <vector>
#include <map>
using namespace std;

#define MINUS_INFINITY -1000000
#define NONE -1

class Score {
public:
  map< char , int > index;
  vector< vector< int > > m;

  Score(const string& file_name)
  {
    ifstream infile(file_name.c_str());
    string line;
    int count = -1;
    cout << "Reading " << file_name << "\n";
    while (getline(infile, line))
      {
	//	cout << line << "\n";
	istringstream iss(line);
	if (count == -1) {
	  char key;
	  vector<char> keys;
	  while (iss >> key) keys.push_back(key);
 	  int n = keys.size();
	  //	  for (int i = 0; i < n; i++) cout << keys[i] << " ";
	  //	  cout << "\n";
	  m.resize(n);
	  for (int i = 0; i < n; i++) {
	    index[keys[i]] = i;
	    m[i].resize(n);
	  }
	} else {
	  char key;
	  iss >> key;
	  map< char, int > row;
	  int value;
	  int j = -1;
	  while (iss >> value) {
	    j++;
	    m[count][j] = value;
	  }
	}
	count++;
      }
  }
};

/*void alignment_matrix_form(const string& x, const string& y, int** c, int** I, int** J, int i, int j, 
			   const string& gap_symbol)
{
}*/

int ** createIntMatrix(unsigned int rows, unsigned int cols) {
  // Initialize an int matrix with zeros
  cout << "Allocating matrix" << rows << "x" << cols << "\n";
  int ** matrix;
  matrix = (int **) calloc(rows, sizeof(int *));
  for(unsigned int i = 0; i < rows; i++)
    matrix[i] = (int *) calloc(cols, sizeof(int));
  return matrix;
}

void freeIntMatrix(int** matrix, unsigned int rows, unsigned int cols) {
  for(unsigned int i = 0; i < rows; i++)
    free(matrix[i]);
  free(matrix);
}

void optimal_alignment_matrix_form(string& x, string& y, 
				  Score& score, int gap_init, int gap_ext,
				  int debug)
{
  /*
    Optimal local alignment that maximizes the alignment score based on the (symmetric) score score
    and, initial gap penalty gap_init < 0, and a gap extension penalty gap_ext < 0.
    Integrated DP+backtracking, O(mn) time+storage.
  */
  const int RESTART = 0;
  const int m = x.size();
  const int n = y.size();
  clock_t start = clock();
  if (debug >= 1)
    cout << m << " " << n << "\n";
  // All arrays initialized to 0
  int** c = createIntMatrix(m+1, n+1);
  int** d = createIntMatrix(m+1, n+1);
  int** e = createIntMatrix(m+1, n+1);
  int** I = createIntMatrix(m+1, n+1);
  int** J = createIntMatrix(m+1, n+1);
  for (int i = 0; i <= m; i++) {
    for (int j = 0; j <= n; j++) {
      c[i][j] = 0;
      d[i][j] = 0;
      e[i][j] = 0;
      I[i][j] = 0;
      J[i][j] = 0;
    }
  }

  //-----------------------------------
  // Initial condition, first row
  //-----------------------------------
  if (debug >= 1)
    cout << "Init first row\n";
  for (int j = 0; j <= n; j++) d[0][j] = MINUS_INFINITY;
  // Best: empty substring alignment (score=0)
  for (int j = 0; j <= n; j++) {
    e[0][j] = 0;
    I[0][j] = NONE;
    J[0][j] = NONE;
   }
   
  //-----------------------------------
  // Initial condition, first column
  //-----------------------------------
  for (int i = 0; i <= m; i++) d[i][0] = MINUS_INFINITY;
  // Best: empty substring alignment (score=0)
  for (int i = 0; i <= m; i++) {
    e[i][0] = 0;
    I[i][0] = NONE;
    J[i][0] = NONE;
  }
 
  //-----------------------------------
  // Dynamic programming
  //-----------------------------------
  for (int i = 1; i <= m; i++) {
    //    cout << i << "\n";
    char xi = x[i-1];
    if (debug >= 1) {
      if (i % 100 == 0) {
	clock_t t = clock();
	double elapsed_secs = double(t - start) / CLOCKS_PER_SEC;
	cout << i << " " << elapsed_secs << "\n";
      }
    }
    for (int j = 1; j <= n; j++) {
      char yj = y[j-1];
      // Possible types of paths to extend to (i,j)
      //      cout << xi << " " << yj << " " << score.m[score.index[xi]][score.index[yj]] << "\n";
      int d_max = c[i - 1][j - 1] + score.m[score.index[xi]][score.index[yj]];
      int e1 = d[i - 1][j] + gap_init;
      int e2 = e[i - 1][j] + gap_ext;
      int e3 = d[i][j - 1] + gap_init;
      int e4 = e[i][j - 1] + gap_ext;
      int e_max = max(max(max(e1, e2), e3), e4);
      int c_max = max(max(d_max, e_max), RESTART);  // Pick best path (greedy approach)
      // Reconstruct the previous element along the best path             
      int ip, jp;
      if (c_max == d_max) { ip = i - 1; jp = j - 1; }
      else if (c_max == e_max) { 
	if ((e_max == e1) || (e_max == e2)) { ip = i - 1; jp = j; }
	else { ip = i; jp = j - 1; }
      } else { ip = NONE; jp = NONE; }
      // Save (i,j) state in matrix
      d[i][j] = d_max;
      e[i][j] = e_max;
      c[i][j] = c_max;
      I[i][j] = ip;
      J[i][j] = jp;
    }
  }
    
  // Maximize score, back-track path
  // Find argmax(c)
  int c_max = c[0][0], i_max, j_max;
  for (int i = 0; i <= m; i++) {
    for (int j = 0; j <= n; j++) {
      int cij = c[i][j];
      if (cij > c_max) {
	c_max = cij;
	i_max = i;
	j_max = j;
      }
    }
  }
  /*
  for (int i = 0; i <= m; i++) {
    for (int j = 0; j <= n; j++)
      cout << c[i][j] << " ";
    cout << "\n";
  }
  */
  
  //  if (debug >= 1) cout << "Starting back-tracking at " << i_max << " " << j_max << "\n";
  if (debug >= 2) {
    cout << c;
    cout << I;
    cout << J;
  }
  cout << c[i_max][j_max] << "\n";

  /*
    Return the augmented-aligned strings of the original strings x and y
    from the DP matrix (result of global_alignment_matrix()) c.
  */
  string gap_symbol("-");
  string s = "";
  string t = "";
  int i = i_max;
  int j = j_max;
  while (true) {
    //    cout << i << " " << j << "\n";
    int ip = I[i][j];
    int jp = J[i][j];
    if ((ip == NONE) || (jp == NONE)) break;
    if (ip == i) s = gap_symbol + s;
    else s = x[i-1] + s;
    if (jp == j) t = gap_symbol + t;
    else t = y[j-1] + t;
    i = ip;
    j = jp;
  }
  cout << s << "\n";
  cout << t << "\n";

  freeIntMatrix(c, m+1, n+1);
  freeIntMatrix(d, m+1, n+1);
  freeIntMatrix(e, m+1, n+1);
  freeIntMatrix(I, m+1, n+1);
  freeIntMatrix(J, m+1, n+1);
  //  alignment_matrix_form(x, y, c, I, J, i_max, j_max, gap_symbol);
}

vector<string> fafsa_values(const string& file_name)
{
  vector<string> s;
  ifstream infile(file_name.c_str());
  string line;
  int count = -1;
  while (getline(infile, line))
    {
      //      line[line.size()-1] = '\0';
      //      line.erase(remove(line.begin(), line.end(), '\n'), line.end());
      //      cout << "'" << line << "'\n";
      if (line[0] == '>') {
	count++;
	string v("");
	s.push_back(v);
	cout << count << "\n";
      } else {
	s[count].append(line.substr(0, line.size()-1));
      }
    }
  return s;
}
    
void laff(string f, int debug)
{
  /* Main driver to solve the LAFF problem. */
  vector<string> s = fafsa_values(f);
  for (int i = 0; i < s.size(); i++) cout << "'" << s[i] << "'" << "\n";
  Score score("c:/ober/code/misc/rosalind/blosum62.dat");
  optimal_alignment_matrix_form(s[0], s[1], score, -11, -1, debug);
}

int main(int argc, char **argv) {
  laff(argv[1], 1);
  //  laff("rosalind_laff_sample2.dat", 1);
  //  laff("rosalind_laff.dat", 1);
  return 0;
}
