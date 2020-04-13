#include <iostream>
#include <fstream>
#include <cstdlib>
using namespace std;

typedef unsigned int uint;

void merge( istream &in, ostream &out) {
  unsigned int M, N;
  in >> M;
  in >> N;
  unsigned int *a = new unsigned int [M];
  unsigned int *b = new unsigned int [N];
  for(unsigned int i=0;i<M;i++) in >> a[i];
  for(unsigned int i=0;i<N;i++) in >> b[i];
  
  unsigned int i,j;
  for(i=0, j=0; i<M && j<N; ) 
    if (a[i] < b[j]) 
      out << a[i++] << endl;
    else
      out << b[j++] << endl;
  while(i<M) out << a[i++] << endl;  
  while(j<N) out << b[j++] << endl;
  delete [] a;
  delete [] b;
}  
  

void make_dataset(string name, uint size1, uint size2) {
  string name_in=name+".in";
  string name_out=name+".out";
  
  ofstream input(name_in.c_str());
  input << size1 << " " << size2 << endl;
  
  uint value=0;
  for(uint i=0; i < size1; i++) {
    value += rand() % 100;
    input << value << endl;
  }  
  
  value=0;
  for(uint i=0; i < size2; i++) {
    value += rand() % 100;
    input << value << endl;
  }
  input.close();
  
  ifstream merge_in(name_in.c_str());
  ofstream merge_out(name_out.c_str());
  merge(merge_in, merge_out);  
}  
  
  
  

int main() {
    srand (time(NULL));
    make_dataset("10",20,30);
    make_dataset("100",301,197);
    make_dataset("1000",2924,1378);
    make_dataset("100k",178902,98748);
}  