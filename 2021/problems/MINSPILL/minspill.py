from optparse import OptionParser
import random
import sys
import io
#import numpy as np
#import statprof
#from contextlib import contextmanager
import heapq


#@contextmanager
#def stat_profiler():
    #statprof.start()
    #yield  statprof
    #statprof.stop()
    #statprof.display()


class State:
    def __init__(self, i, j, spill, cost):
        self.i, self. j = i, j
        # spill from i to  j ( how the state is formed efectively give parent state)
        self.spill = spill
        # n liters to spill from i to j
        self.cost = cost
        # cost of the state

class ImplicitDijkstra:
    def __init__(self, in_stream):
        n_containers = int(in_stream.readline())
        self.volumes = [int(in_stream.readline()) for _ in range(n_containers)]

        self.states = {}
        self.queue = []


    def pour(self, volumes, prev_cost, i, j):
        new_volumes  = list(volumes)
        free = self.volumes[j] - new_volumes[j]
        spill = min(free, new_volumes[i])
        new_volumes[i] -= spill
        new_volumes[j] += spill
        new_volumes = tuple(new_volumes)
        new_cost = (prev_cost[0] + spill, prev_cost[1] + 1)
        new_state = State(i, j, spill, new_cost)

        if new_volumes not in self.states or new_state.cost < self.states[new_volumes].cost:
            self.add(new_volumes, new_state)
            return True
        else:
            return False

    def add(self, new_volumes, new_state):
        self.states[new_volumes] = new_state
        heapq.heappush(self.queue, (new_state.cost, new_volumes))

    def run_dijkstra(self):
        i_fill = max(range(len(self.volumes)), key=self.volumes.__getitem__)
        self.results = (self.volumes[i_fill] + 1) * [None]
        self.n_results = 0

        volumes = len(self.volumes) * [0]
        volumes[i_fill] = self.volumes[i_fill]
        volumes = tuple(volumes)
        cost = (0, 0)
        state = State(i_fill, i_fill, self.volumes[i_fill], cost)
        self.add(volumes, state)

        while self.queue and self.n_results < len(self.results):
            cost, volumes = heapq.heappop(self.queue)
            state = self.states[volumes]
            if state.cost < cost:
                # skip closed states
                continue

            # New states can be obtained only by interacting with vessels that have been changed recently.
            # Should be possible to reduce l to [state.i, state.j], but that way I loose some states, not
            # know why exactly.
            for l in range(len(self.volumes)):
                for k in range(len(self.volumes)):
                    if k != l:  #state.i and k != state.j:
                        self.pour(volumes, cost, l, k)
                        #self.pour(volumes, cost, k, l)
                            #if k not in {state.i, state.j} and l not in {state.i, state.j}:
                            #    sys.stderr.write("kl: {} {}  ij: {} {} volumes: {}\n".format(k,l, state.i, state.j, str(volumes)))

            # Final distance to current state: check and save results
            if self.results[volumes[state.i]] is None:
                self.results[volumes[state.i]] = volumes
                self.n_results += 1

            if self.results[volumes[state.j]] is None:
                self.results[volumes[state.j]] = volumes
                self.n_results += 1

        sys.stderr.write("#states: {}\n".format(len(self.states)))

    def get_path(self, volumes):
        path = []
        cost = 0
        state = self.states[tuple(volumes)]
        orig_cost = state.cost
        while state.i != state.j:
            #path.append((state.i, state.j, tuple(volumes)))
            path.append((state.i, state.j))
            cost += state.spill
            volumes[state.i] += state.spill
            volumes[state.j] -= state.spill
            state = self.states[tuple(volumes)]
        assert orig_cost == (cost, len(path))
        return list(reversed(path)), cost

    def output_results(self, stream):
        for vol, res in enumerate(self.results[1:]):
            if res is None:
                stream.write("{}\n".format(vol+1))
            else:
                path, cost = self.get_path(list(res))
                stream.write("{} {} {}\n".format(
                    vol+1, cost, len(path)))
                # for i,j in path:
                #     stream.write("    {}>{}\n".format(i, j))

def solve(in_stream, out_stream):
    dijkstra = ImplicitDijkstra(in_stream)
    dijkstra.run_dijkstra()
    dijkstra.output_results(out_stream)


def make_data(in_stream, problem_size):
    size = problem_size
    max_vol = max(3, int( size ** 0.3))
    volumes = []
    while size > 2:
        vol = random.randint(2, max_vol)
        volumes.append(vol)
        size = size / vol
    problem_setup = io.StringIO()
    problem_setup.write("{}\n".format(len(volumes)))
    for v in volumes:
        problem_setup.write("{}\n".format(v))

    #sys.stdout.write(problem_setup.getvalue())
    #print("====")
    out_stream = io.StringIO()
    problem_setup.seek(0)
    solve(problem_setup, out_stream)

    #sys.stderr.write(out_stream.getvalue())
    #print("====")

    #res_stream = StringIO.StringIO()
    #segment.image_to_stream(res_stream, head=False)
    #assert (out_stream.getvalue() == res_stream.getvalue())

    in_stream.write(problem_setup.getvalue())


'''
Main script body.
'''

parser = OptionParser()
parser.add_option("-p", "--problem-size", dest="size", help="Problem size.", default=None)
parser.add_option("-v", "--validate", action="store_true", dest="validate", help="program size", default=None)
parser.add_option("-r", dest="rand", default=False, help="Use non-deterministic algo")

options, args = parser.parse_args()


if options.rand:
    random.seed(options.rand)
else:
    random.seed(options.size)

if options.size is not None:
    make_data(sys.stdout, int(options.size))
else:
    solve(sys.stdin, sys.stdout)
