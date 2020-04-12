#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
using namespace std;

/*
 * Timings:
 *                      2x17
 * given order          6.6s
 * desat simple         0.083s
 */

#define DEBUG

#ifdef DEBUG
#define dout cout << "DBG: "
#else
#define dout ostream(0)
#endif


typedef unsigned int uint;

struct Node {
  Node() 
  : free_colors(10,true) // colors are from one
  {
    free_colors_sum=45;
    color=0;
  }  
  vector<int> ngh;
  vector<bool> free_colors;
  int free_colors_sum;
  int color;
};

struct Choice {
  int node;
  int color;
  vector<int> other_colors;
};



class Sudoku {
public:
  Sudoku( istream &in, ostream &out) 
  : out(out)
  { 
      make_graph();
      actual_node=0;
      n_solutions=n_backtrace=n_color_node=0;
      read(in);
  }  
  
  ostream &out;
  std::vector<Node> nodes; 
  std::vector<Choice> colored_nodes;
  std::vector<int> unique_solution;
  int top_colored_nodes;
  int actual_node;
  
  int n_backtrace, n_color_node, n_solutions;

  void make_graph();
  void read( istream &in );
  inline int choose_node() { return choose_node_desat();}
  int choose_node_simple();
  int choose_node_desat();
  void color_node(int i_node, int color);
  void color_all();
  void print();
  void print_ngh(const Node &node) {
      for(Node &n :nodes) n.color=0;
      for(auto &ngh :node.ngh) nodes[ngh].color=1;
      cout<<endl;
      print();
  }
  void isomorphisms();
};  

void Sudoku::make_graph() {
  // connection graph
  nodes.resize(81);
  for(int i=0; i<81;i++) {
    int y = i/9;
    int x = i%9;
    int i_ngh=0;
    nodes[i].ngh.resize(20,0);
    // row
    for(int j =0; j<9; j++) 
      if(j!=x) nodes[i].ngh[i_ngh++] = 9*y+j;

    // col  
    for(int j =0; j<9; j++) 
      if(j!=y) nodes[i].ngh[i_ngh++] = 9*j+x;

    // square
    int square=(y/3)*3 + (x/3);  
    for(int j =0; j<9; j++)
      if (j != (3*(y%3)+(x%3)) ) {
          int xx = 3*(square%3) + j%3;
          int yy = 3*(square / 3)+(j/3);
          if (xx!=x && yy !=y) nodes[i].ngh[i_ngh++] = 9*yy + xx;
      }
  }  
  
  colored_nodes.resize(81);
  top_colored_nodes=0;
}

void Sudoku::read(  istream &in  ) {
  int color;
  for(int i=0; i<81;i++) {
    in >> color;
    if (color >0 && color<10) color_node(i, color);
  }  
  //out << "Input:" << endl;
  //print();
  //out << "---------------------" << endl;
}  






/// Color node with given color.
void Sudoku::color_node(int i_node, int color) {
  n_color_node++;

  Node &node=nodes[i_node];
  // color the node
  node.color=color;
  // update free colors in neighbours
  for(int &ngh : node.ngh) nodes[ ngh ].free_colors[ color ]=false;
  colored_nodes[top_colored_nodes].node=i_node;
  colored_nodes[top_colored_nodes].color=color;
/*
   dout << "colored: " << top_colored_nodes
       << " node: " << colored_nodes[top_colored_nodes].node
       << " color: " << colored_nodes[top_colored_nodes].color
       << " other: " << colored_nodes[top_colored_nodes].other_colors.size()
       << endl;
  */
  top_colored_nodes++;
}  

int Sudoku::choose_node_simple() {
  // order of nodes
  while (nodes[actual_node].color!=0) actual_node++;
  return actual_node;
}


int Sudoku::choose_node_desat() {
  // desaturation
  int min_free=10;
  int min_node=81;

  for(int n=0; n< nodes.size(); n++) {
      const Node &node=nodes[n];
      if (node.color ==0) {
          int n_free=0;
          for(int i=1; i<10;i++)  if (node.free_colors[i]) n_free++;
          if (n_free<min_free) {
              min_free=n_free;
              min_node=n;
          }
      }
  }
  actual_node=min_node;
  return actual_node;
}


void Sudoku::color_all() {
  int color;
  int init_top_colored_nodes = top_colored_nodes;
  while (top_colored_nodes >= init_top_colored_nodes) {

    int i_node=choose_node();
    if (i_node != 81)  { // found some node to color
      // find free colors, fill top of colored_nodes
      Node &node=nodes[i_node];
      color=0;
      for(int i=1; i<10;i++) if (node.free_colors[i]) {
        if (color==0) color = i;
        else colored_nodes[top_colored_nodes].other_colors.push_back(i);
      }  
      if (color) {
        color_node(i_node, color);

        continue; 
      }  
    } 
      // dout << "backtrace" << top_colored_nodes << endl;
      // backtrace
      n_backtrace++;

      if (top_colored_nodes == 81) {
          // count / save solution
          if (n_solutions==0) {
              unique_solution.resize(81);
              for(int i=0; i<nodes.size(); i++) unique_solution[i]=nodes[i].color;
          }
          n_solutions++;
      }
      top_colored_nodes--;
      while( top_colored_nodes >= init_top_colored_nodes
        && colored_nodes[top_colored_nodes].other_colors.size() == 0)  {
        nodes[colored_nodes[top_colored_nodes].node].color=0;
        top_colored_nodes--;
      }
      if (top_colored_nodes < init_top_colored_nodes) {
          out << endl;
          out << n_solutions<< endl;
          if (n_solutions==1) print();
          dout << "colored: " << n_color_node << " back: " << n_backtrace << " sol:" << n_solutions << endl;
          return;
      }
      // revert all changes
      nodes[colored_nodes[top_colored_nodes].node].color=0;
      for(Node &node : nodes) {
        for(int j=0; j<node.free_colors.size(); j++) node.free_colors[j]=true;
        for(int &ngh : node.ngh) node.free_colors[ nodes[ ngh ].color ]=false; 
      }

      actual_node=colored_nodes[top_colored_nodes].node;
      // set other color
      color=colored_nodes[top_colored_nodes].other_colors.back();
      colored_nodes[top_colored_nodes].other_colors.pop_back();
      color_node(colored_nodes[top_colored_nodes].node, color);
    }
}  


void Sudoku::print() {
    cout << endl;
    for(int i=0; i<9;i++) {
      // coloring
      for(int j=0; j<9; j++) out << nodes[9*i+j].color << " ";
      // free
      out << "      ";
      for(int j=0; j<9; j++) {
          int n_col=0;
          for(int k=1; k<10;k++) if (nodes[9*i+j].free_colors[k]) n_col++;
          out << n_col << " ";
      }

      out << endl;
    }
}

void Sudoku::isomorphisms() {
/*    vector<int> perm(81);
    auto top = per.begin();
 */
}

  

void make_dataset(string name, uint size1, uint size2) {
}  
  

  
  

int main() {
    srand (time(NULL));
    while (!cin.eof()) {
        Sudoku s(cin, cout);
        s.color_all();
    }
}  
