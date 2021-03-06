#!/usr/bin/env python
from optparse import OptionParser
import io
from random import randint
import random
import sys
import time
import heapq



class Edge:
    def __init__(self, idx, va, vb, price, mark):
        self.idx = idx
        self.va = va
        self.vb = vb
        self.value = (mark, price)


def read_edges(in_stream):
    n_vtx, n_edges = [ int(token) for token in in_stream.readline().split()]
    edges = []
    for i in range(n_edges):
        va, vb, price, mark =  [int(token) for token in in_stream.readline().split()]
        edges.append(Edge(i, va, vb, price, mark))
    return n_vtx, edges


class BigLoko:
    
    def __init__(self, n_vtx, edges) :
        
        self.edges = edges
        self.node_value = [ (6, 0, i) for i in range(n_vtx) ]
        self.node_parent_edge = n_vtx*[-1]
        self.adj = [ [] for n in range(n_vtx) ]
        for edge in edges:
            self.adj[edge.va].append((edge.vb, edge.idx))
            self.adj[edge.vb].append((edge.va, edge.idx))

        
    def check_unique(self):
        if len(self.heap) < 2:
            return True
        min_three = min([h[0] for h in self.heap[1:3]])
        return self.heap[0][0] != min_three
      
    def prim(self, start_vtx = 0, known_unique=True):
        self.node_value[start_vtx] = (0, 0)
        self.heap = [((0,0), start_vtx)]
        heapq.heapify(self.heap)

        n_processed = 0
        while len(self.heap):
            #try:
            #except IndexError:
                #pass
            if not known_unique and not self.check_unique():
                raise Exception("Not unique: {}".format(self.heap[0:3]))
            value, vtx = heapq.heappop(self.heap)
            if value > self.node_value[vtx]:
                continue
            n_processed += 1
            self.node_value[vtx] = (0,0)
            for ngh, i_edge in self.adj[vtx]:
                e_value = self.edges[i_edge].value
                if e_value < self.node_value[ngh]:
                    # e = self.edges[i_edge]
                    # print(vtx, ngh, e.idx, e.value)
                    self.node_value[ngh] = e_value
                    self.node_parent_edge[ngh] = i_edge
                    heapq.heappush(self.heap, (e_value, ngh) )
        assert(n_processed == len(self.node_parent_edge))
      
    def get_spanning_tree(self):
        return self.node_parent_edge[1:]



"""        
    # output reduced graph
    #graph.graph_output(in_stream)
    in_stream.write(image_stream.getvalue())
"""    


def solve(in_stream, out_stream, check) :
    n_vtx, edges = read_edges(in_stream)
    si = BigLoko(n_vtx, edges)
    #si.read_image(in_stream)
    si.prim(known_unique=not check)
    s_tree = si.get_spanning_tree()
    for s in s_tree:
        out_stream.write("%d\n"%s)

FREE = 0
OPEN = 1
CLOSED = 2

class MakeGraph:
    def __init__(self, problem_size):
        import numpy as np
        import scipy.spatial as sc_sp
        from collections import deque

        self.q = deque()
        self.edges=[]
        scale = np.sqrt(problem_size)

        self.neighbourhood = int(6 + np.log(problem_size))
        self.points = scale * np.random.rand(problem_size, 2)
        self.kd_tree = sc_sp.KDTree(self.points, leafsize=10)
        self.status = np.full(len(self.points), FREE)
        
        r_weights = np.random.rand(self.neighbourhood * problem_size, 2)
        max_price = 1e6 * scale    # in thousends Kc
        weights = np.empty_like(r_weights, dtype=int)
        weights[:, 0] = r_weights[:,0] * max_price
        weights[:, 1] = r_weights[:, 1] * 5 + 1
        weights = np.unique(weights, axis=0)
        self.weights = np.random.permutation(weights)
        #sys.stderr.write(f"n_weights:  {len(weights)}\n")

    def bfs(self, start_point):
        import numpy as np
        
        
        if self.status[start_point] == CLOSED:
            return
        assert self.status[start_point] == FREE, self.status[start_point]
        self.status[start_point] = OPEN
        self.q.append(start_point)        
        neighbourhood = self.neighbourhood        
        
        while len(self.q):
            i_point = self.q.popleft()            
            assert self.status[i_point] == OPEN, self.status[i_point]
            
            dists, neighbors = self.kd_tree.query(self.points[i_point], neighbourhood)    
            selected = np.random.permutation(np.arange(neighbourhood, dtype=int))
            # bounded connection to both unvisited and opened nodes
            #use=[np.random.randint(1, 3), np.random.randint(0,1)]
            # connect all unvisited
            n_duplicate = np.random.randint(2,len(selected))
            use=[len(selected), n_duplicate]
            for s in selected:
                d, ng = dists[s], neighbors[s]
                if ng == i_point:
                    continue
                #d = np.linalg.norm(points[i_point] - points[ng])
                opened_ng = int(self.status[ng] >= OPEN)
                if not opened_ng:
                    # unvisited neighbour
                    assert self.status[ng] == FREE
                    self.status[ng] = OPEN
                    self.q.append(ng)
                
                if use[opened_ng] > 0:
                    # visited                              
                    use[opened_ng]-=1
                    price, mark = self.weights[len(self.edges)]
                    #sys.stderr.write(f"{(i_point, ng, price, mark)}\n")
                    self.edges.append((i_point, ng, price, mark))            
                    
                      
                if use[0] == 0 and use[1] == 0:
                    break
            self.status[i_point] = CLOSED

    def get_edges(self):
        for ip in range(len(self.points)):
            self.bfs(ip)
        for ip, p in enumerate(self.points):
            assert(self.status[ip] == CLOSED)

        return self.edges



def make_data(in_stream, problem_size):
    '''
    1. Generate N points in plane
    2. Make Kd tree
    3. For every point find K  neighbors, and generate edges to them with random weights.
    '''

    mg = MakeGraph(problem_size)
    edges = mg.get_edges()
    #sys.stderr.write(f"n edges: {len(edges)}\n")
    #eset={}
    #for e in edges:
        #u,v,price, mark = e
        #key = (price, mark)
        #val = (u, v)
        #if key in eset:
             #sys.stderr.write(f"duplicate: {e}  of {eset[key]}\n")
        #eset[key] = val
       
    #print("unconnected: ", sum( status[ip] == -1 for ip, p in enumerate(points)))
    #for ip, p in enumerate(points):
        #assert(status[ip] > -1)
            
    # Output setting
    in_stream.write("{} {}\n".format(problem_size, len(edges)))
    for edge in edges:
        in_stream.write("{} {} {} {}\n".format(*edge))

    # fill_img.image_to_stream(sys.stdout)
    # input_img.image_to_stream(sys.stdout)

'''
Main script body.
'''

parser = OptionParser()
parser.add_option("-p", "--problem-size", dest="size", help="Problem size.", default=None)
parser.add_option("-v", "--validate", action="store_true", dest="validate", help="program size", default=None)
parser.add_option("-r", dest="rand", default=False, help="Use non-deterministic algo")

options, args = parser.parse_args()

#random.seed(1234)


if options.rand:
    random.seed(options.rand)

if options.size is not None:
    input_stream = io.StringIO()
    random.seed(options.size)
    make_data(input_stream, int(options.size))
    input_stream.seek(0)
    output_stream = io.StringIO()
    tick  = time.clock()
    solve(input_stream, output_stream, check=True)
    tock = time.clock()
    #sys.stderr.write("time: {}\n".format(tock - tick))
    sys.stdout.write(input_stream.getvalue())

else :
    #with open("input_1", "r") as in_stream:
    #    solve(in_stream, sys.stdout)
    solve(sys.stdin, sys.stdout, check=True)













# class BigLoko:
#     def __init__(self, size) :
#         self.image=[]
#         self.img_side = size
#
#     def fill(self, num):
#         self.image=self.img_side * self.img_side * [num]
#
#     def pidx(self,i_row,i_col):
#         return i_row*self.img_side + i_col
#
#     def image_to_stream(self, stream):
#         stream.write( "{:d}\n".format(( self.img_side )) )
#         for row in range(self.img_side):
#             for col in range(self.img_side):
#                 stream.write( "{:3d} ".format(( self.image[self.pidx(row,col)]) ))
#             stream.write("\n")
#
#     def neighbours(self, ii):
#         N=self.img_side
#         ngh_list = [ii - 1, ii + 1, ii - N, ii + N]
#         if ii / N == 0:            ngh_list[2] = -1  # top
#         if ii / N == N - 1:   ngh_list[3] = -1  # bottom
#         if ii % N == 0:            ngh_list[0] = -1  # left
#         if ii % N == N - 1:   ngh_list[1] = -1  # right
#         return filter(lambda item: item != -1, ngh_list)
#
#     def _fill_line(self, A, B, inc):
#         """
#         Correlated random line (vertiacl or horizontal), assume points A an B
#         are filled
#         :param A: start index in image
#         :param B: end index in image
#         :param inc: increment of index
#         :return:
#         """
#
#         if B == A + inc:
#             return
#         else:
#             #print("A: {},{} B:{}, {}".format(A / self.img_side, A % self.img_side, B / self.img_side, B % self.img_side))
#             dist = (B-A)/inc
#             AC_dist = (dist/2)
#             BC_dist = dist - AC_dist
#             C = A + AC_dist*inc
#             A_val = self.image[A]
#             B_val = self.image[B]
#             scale = 0.5 * self.max_diff * 0.5 * dist * math.pow(float(dist)/self.img_side, 0.3)
#             C_value=int(( A_val +  B_val) / 2.0  + scale * random.uniform(-1, 1))
#             #C_value = int((A_val + B_val) / 2.0 )
#             # guarantee that difference is not larger then 'max_diff'
#             """
#             if A_val > B_val:
#                 A_val, B_val = B_val, A_val
#             # B is biger
#             C_max = A_val + int(self.max_diff * AC_dist *0.5)
#             C_min = B_val - int(self.max_diff * BC_dist*0.5)
#             C_value = min( C_max, C_value, self.max)
#             C_value = max( C_min, C_value, self.min)
#             #print("Av: {} Cv: {} Bv:{} {} {} {}".format(A_val, C_value, B_val, self.max_diff, AC_dist, BC_dist))
#             """
#             self.image[C] = C_value
#             self._fill_line(A,C,inc)
#             self._fill_line(C, B, inc)
#
#     def _fill_h_line(self, A, B):
#         self._fill_line(self.pidx(A[0],A[1]), self.pidx(B[0],B[1]), 1)
#
#     def _fill_v_line(self, A, B):
#         self._fill_line(self.pidx(A[0], A[1]), self.pidx(B[0], B[1]), self.img_side)
#
#     def _fill_h_split(self, A, B):
#         ar, ac = A
#         br, bc = B
#         if (ar + 1 == br): return
#         cr = (ar+br)/2
#         self._fill_h_line( (cr, ac), (cr, bc))
#         #self.plot()
#         self._fill_v_split( A, (cr,bc))
#         self._fill_v_split( (cr, ac), B)
#
#     def _fill_v_split(self, A, B):
#         ar, ac = A
#         br, bc = B
#         if (ac + 1 == bc): return
#         cc = (ac+bc)/2
#         self._fill_v_line( (ar, cc), (br, cc) )
#         #self.plot()
#         self._fill_h_split( A, (br,cc))
#         self._fill_h_split( (ar, cc), B)
#
#     def smooth(self):
#         for i in range(len(self.image)):
#             ngh_vals = [ self.image[n] for n in self.neighbours(i) ]
#             ngh_vals.append(self.image[i])
#             self.image[i] = sum(ngh_vals) / len(ngh_vals)
#
#     def fill_random(self, max_diff):
#         """
#         Fill image with corellated random values in range 0:1024, with given maximal
#         difference between neighbouring values.
#         :param n:
#         :return: range of values
#         """
#
#         self.min=0
#         self.abs_max=2048
#         self.max_diff=max_diff -1
#         self.max = min(self.abs_max, self.max_diff * self.img_side / 4)
#
#         self.fill(0)
#         N= self.img_side -1
#         # corners
#         self.image[self.pidx(0, 0)] = random.randint(self.min, self.max)
#         self.image[self.pidx(0, N)] = random.randint(self.min, self.max)
#         self.image[self.pidx(N, 0)] = random.randint(self.min, self.max)
#         self.image[self.pidx(N, N)] = random.randint(self.min, self.max)
#         # horizontal border
#         self._fill_h_line( (0, 0), (0, N))
#         self._fill_h_line( (N, 0), (N, N))
#         # vertical border
#         self._fill_v_line( (0, 0), (N, 0))
#         self._fill_v_line( (0, N), (N, N))
#         # fill interior
#         self._fill_v_split( (0,0), (N,N) )
#
#         # scale
#         img_max = max(self.image)
#         img_min = min(self.image)
#         self.image = [  int(self.max*float((v-img_min))/(img_max - img_min))  for v in self.image]
#
#         def is_diff_satisfied():
#             for i in range(len(self.image)):
#                 for j in self.neighbours(i):
#                     if abs(self.image[i] - self.image[j]) > max_diff:
#                         #print("diff: ", abs(self.image[i] - self.image[j]) )
#                         return False
#             return True
#
#         # smooth
#         for n_smooth in range(10):
#             #print(n_smooth)
#             if is_diff_satisfied(): break
#             self.smooth()
#         assert(n_smooth < 10)
#
#         # check max diff
#         for i in range(len(self.image)):
#             if self.image[i] > self.max or  self.image[i] < self.min:
#                 print("max, min: ", self.image[i], self.max, self.min)
#
#     def plot(self):
#         import numpy as np
#         import matplotlib.pyplot as plt
#
#         img = np.array(self.image).reshape((self.img_side, self.img_side))
#         plt.imshow(img, interpolation="nearest")
#         plt.show()
#
#     def scale_value(self, row, col, range):
#         idx = self.pidx(row,col)
#         self.image[idx] = int(range[0] + (float(self.image[idx])/self.max) * (range[1] - range[0]))
