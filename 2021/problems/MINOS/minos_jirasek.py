import sys
from heapq import heappop, heappush


def gen_labyrinth(m, n):
    G = {}
    LST = {}
    for i in range(1, n * m + 1):
        LST[i] = []
        i % m != 0 and LST[i].append(i + 1)
        i % m != 1 and LST[i].append(i - 1)
        (i - 1) / m > 0 and LST[i].append(i - m)
        (i - 1) / m < n - 1 and LST[i].append(i + m)
        G[i] = {k: [None, 0] for k in LST[i]}
    return G, LST


def prim(G, s):
    closed = [0]*(len(G)+1)
    
    global b
    P, Q = {}, [([None, 0], None, s)]
    uniq = 0
    while Q:        
        pw, p, u = heappop(Q)
        print "vtx: ", u-1
        if u in P:
          #print "vtx: ", u, pw, closed[u]  
          if (pw == closed[u] ):
              print "Not unique: ", u, pw
          continue
        for N in LST[u]:
            if G[u][N][0] is None:                
                G[u][N][0] = G[N][u][0] = b % 256
                b = (b * 1664525 + 1013904223) % (1024*1024*1024*4)
                print "edge: ", u, N, b %256
        P[u] = p
        closed[u] = pw  # save optimal weight for vtx u
        for v, w in G[u].items():
            if v not in P:
                # uniq omezi porovnavani pouze na hodnoty
                # w - vaha hran
                # pw - vzdalenost od pocatku
                
                 
                heappush(Q, ([w[0], pw[1] + 1], u, v))
                uniq -= 1
    return P


def output():
    tmp = ''
    for i, val in enumerate(mapa):
        tmp += hex(val).upper()[-1]
        if (i + 1) % m == 0:
            print tmp
            tmp = ''


def cross_code(mst):
    direction = {-m: 4, -1: 2, 1: 1, m: 8}
    mapa = [0] * (m * n)
    for i in mst.items():
        if i[1]:
            mapa[i[0] - 1] += direction[i[1] - i[0]]
            mapa[i[1] - 1] += direction[i[0] - i[1]]
    return mapa


if __name__ == '__main__':
    userinput = sys.stdin.readline()
    n, m, b = map(lambda x: int(x), userinput.strip().split(' '))
    b %= 256
    graph, LST = gen_labyrinth(m, n)
    MST = prim(graph, 1)
    mapa = cross_code(MST)
    output()
    sys.exit(0)
