#include <iostream>
using namespace std;
int main() {
  unsigned int M, N;
  cin >> M;
  cin >> N;
  unsigned int *a = new unsigned int [M];
  unsigned int *b = new unsigned int [N];
  for(unsigned int i=0;i<M;i++) cin >> a[i];
  for(unsigned int i=0;i<N;i++) cin >> b[i];
  
  unsigned int i,j;
  for(i=0, j=0; i<M && j<N; ) 
    if (a[i] < b[j]) 
      cout << a[i++] << endl;
    else
      cout << b[j++] << endl;
  while(i<M) cout << a[i++] << endl;  
  while(j<N) cout << b[j++] << endl;
  delete [] a;
  delete [] b;
}  
  