# %%
from common import INPUT_DIR, check_test, get_data, parse_mat, in_mat
import numpy as np

# %%
import numpy as np

class Region:
    def __init__(self, plant, shape):
        self.plant=plant
        self.idxs=[]
        self.edges=0
        self.to_visit=np.zeros(shape)
        self.visited=np.zeros(shape)
    def add_idx(self, idx):
        if self.visited[*idx]==0: # if it is already visited, we skip
            self.idxs.append(idx)
            self.to_visit[*idx]=1
    def visit(self, idx):
        self.to_visit[*idx]=0
        self.visited[*idx]=1
    def add_edge(self):
        self.edges+=1
    def compute_cost(self):
        return self.edges*len(self.idxs)

class Map:
    def __init__(self, map_):
        self.map=map_
        self.shape = self.map.shape
        self.visited=np.zeros(self.map.shape)
        self.regions=[]
    def in_region(self, idx, region):
        return self.map[*idx]==region.plant
    
    def get_first(self, where):
        if np.all(where==1):
            return None
        idx0=np.where(where==0)
        idx = np.array([idx_i[0] for idx_i in idx0])
        return idx
    def get_first_region(self):
        return self.get_first(self.visited)
        # if np.all(self.visited==1):
        #     return None
        # idx0=np.where(self.visited==0)
        # idx = np.array([idx_i[0] for idx_i in idx0])
        # return idx
    def get_next_explore(self, region):
        return self.get_first(1-region.to_visit) # strange but works
        # if np.all(region.to_visit==0):
        #     return None
        # idx0=np.where(region.to_visit==0)
        # idx = np.array([idx_i[0] for idx_i in idx0])
        # return idx
    def explore(self, region, idx):        
        self.visited[*idx]=1
        region.visit(idx)
        deltas=np.array([[0,1],[1,0],[0,-1],[-1,0]])
        for delta in deltas:
            idx_dest=idx+delta
            if not in_mat(idx_dest, self.shape):
                region.add_edge()
                continue
            if not self.in_region(idx_dest, region):
                region.add_edge()
                continue
            region.add_idx(idx)

        
    def find_regions(self):
        idx = self.get_first_region()
        while idx is not None:
            region = Region(self.map[*idx], self.shape)            
            self.regions.append(region)            
            region.add_idx(idx)        
            while idx is not None:            
                self.explore(region, idx)
                idx = self.get_next_explore(region)

        idx = self.get_first_region()
    def compute_cost(self):
        cost=0
        for region in self.regions:
            cost+=region.compute_cost()
        return cost


def solve_quiz1(fn=None, test_data=None):
    data = get_data(fn, test_data)
    map_ = parse_mat(data)
    map_ = Map(map_)
    regions = map_.find_regions()
    cost = map_.compute_cost()
    return cost, regions


if __name__=="__main__":
    quiz_fn = INPUT_DIR / "day12.txt"


    # TEST 0
    test_data="""AAA000
AAA000
BBB111
CCC111"""
    cost, regions = solve_quiz1(test_data=test_data)

    # TEST1
    test_data = """AAAA
BBCD
BBCC
EEEC"""

    cost, region = solve_quiz1(test_data=test_data)
    check_test(1.1, cost, true_result=140)
    
    # TEST 2
    test_data =   """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""  
    
    cost, region =  solve_quiz1(test_data=test_data)
    check_test(1.2, cost, true_result=772)

    # TEST 3
    test_data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    cost, region =  solve_quiz1(test_data=test_data)
    check_test(1.3, cost, true_result=1930)


    print("Quiz1 result is", solve_quiz1(fn=quiz_fn))
#    print("Quiz2 result is", solve_quiz1(fn=quiz_fn, blink_times=75))
