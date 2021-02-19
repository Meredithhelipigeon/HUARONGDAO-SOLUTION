import numpy
import queue
import heapq
import copy
#from copy import copy, deepcopy
# from multiprocessing import queue
frontier = queue.PriorityQueue()
pathset = set()
numExpand = 0

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def tranferse_state(state):
    state=state.replace("3","2")
    state=state.replace("4","2")
    state=state.replace("5","2")
    return state

def print_state(state):
    for i in range(5):
        print(state[4*i:4*i+4])

def check_wide(state,dir,w,h,loc):
    if ((dir==1 and loc%4+w == 4) or (dir==-1 and loc%4+dir == -1)):
        return False
    for n in range(h):
        if (dir==1 and state[loc+w+n*4] != '0'):
            return False
        if (dir==-1 and state[loc+dir+n*4] != '0'):
            return False
    return True

def list_to_str(l):
    ret = ""
    for e in l:
        ret += e
    return ret    


def move_wide(state,dir,w,h,loc,tpe):
    st=list(state)
    for i in range(h):
        if (dir == -1): #left
            st[loc+dir+i*4], st[loc+w-1+i*4] = st[loc+w-1+i*4], st[loc+dir+i*4]
        else:
            st[loc+w+i*4], st[loc+i*4] = st[loc+i*4], st[loc+w+i*4]
    return list_to_str(st)     

def check_height(state,dir,w,h,loc):
    if ((dir==1 and loc//4+h==5) or (dir==-1 and loc//4-1==-1)):
        return False 
    for n in range(w):
        if (dir==1 and state[loc+n+h*4] != '0'):
            return False
        if (dir==-1 and state[loc+dir*4+n] != '0'):
            return False    
    return True    

def move_height(state,dir,w,h,loc,tpe):
    st=list(state)
    for i in range(w):
        if (dir == -1): #up
            st[loc+dir*4+i], st[loc+(h-1)*4+i] =  st[loc+(h-1)*4+i], st[loc+dir*4+i]
        else:
            st[loc+h*4+i], st[loc+i] =  st[loc+i], st[loc+h*4+i]            
    return list_to_str(st)    

class Path():
    # class attribute
    def __init__(self, p):
        self.p = p

    def get_cost(self):
        return len(self.p)


    # define the operator of "gt"
    def __gt__(self, other):
        valself = self.p[-1].get_heuristic()+ self.get_cost()
        valoth = other.p[-1].get_heuristic() + other.get_cost() 
        if (valoth>valself):
            return False
        else:
            return True      


class Tile:
    # class attribute
    def __init__(self, location, height, width, tpe):
        self.location=location
        self.height=height
        self.width=width  
        self.tpe=tpe      

class State():
    # class attribute
    def __init__(self, CurrentState):
        self.CurrentState =  CurrentState
        pathset.add(tranferse_state(CurrentState))
        self.pastPath = queue.Queue()

    # check if it is the goal
    def is_goal(self):
        if self.CurrentState.find('1')==13:
            return True
        else:
           return False     

    # calculate the return value of heuristic function
    def get_heuristic(self):
        diff_x = abs(self.CurrentState.find('1')%4 - 1)   
        diff_y = abs(self.CurrentState.find('1')//4 - 3)  
        return  diff_x+diff_y       

    def __deepcopy__(self,memo):
        id_self = id(self)        # memoization avoids unnecesary recursion
        _copy = memo.get(id_self)
        if _copy is None:
            _copy = type(self)(
                copy.deepcopy(self.CurrentState, memo))
            memo[id_self] = _copy 
        return _copy
    # return the tile set 
    def get_tileset(self):
        tileset = set()
        for i in range(1,8):
            if(i==1):
                tileset.add(Tile(self.CurrentState.find('1'),2,2,'1'))
            elif (i==6):
                tileset.add(Tile(self.CurrentState.find('6'),1,2,'6'))
            elif (i==7):
                for j in range(1,5):   # iterate from 1 to 4   
                    tileset.add(Tile(find_nth(self.CurrentState, "7",j),1,1,'7'))
            else:
                tileset.add(Tile(self.CurrentState.find(str(i)),2,1,chr(i)))
        return tileset          
           
    # add all of the paths
    def successor(self,p):
        global numExpand
        tileset=self.get_tileset()
        ret=[]
        for t in tileset:
            if (check_wide(self.CurrentState,-1,t.width,t.height,t.location)): # left
                numExpand += 1
                newstate = move_wide(self.CurrentState,-1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    np = copy.deepcopy(p)
                    np.append(new_State)
                    frontier.put(Path(np))
                    pathset.add(tranferse_state(newstate))
                    if(new_State.is_goal()):
                        ret=np  
            if (check_wide(self.CurrentState,1,t.width,t.height,t.location)): # right
                numExpand += 1
                newstate = move_wide(self.CurrentState,1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    np = copy.deepcopy(p)
                    np.append(new_State)
                    frontier.put(Path(np))
                    pathset.add(tranferse_state(newstate)) 
                    if(new_State.is_goal()):
                        ret=np 
            if (check_height(self.CurrentState,-1,t.width,t.height,t.location)): # up
                numExpand += 1
                newstate=move_height(self.CurrentState,-1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    np = copy.deepcopy(p)
                    np.append(new_State)
                    frontier.put(Path(np))
                    pathset.add(tranferse_state(newstate)) 
                    if(new_State.is_goal()):
                        ret=np 
            if (check_height(self.CurrentState,1,t.width,t.height,t.location)): # down  
                numExpand += 1
                newstate=move_height(self.CurrentState,1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    np = copy.deepcopy(p)
                    np.append(new_State)
                    frontier.put(Path(np))
                    pathset.add(tranferse_state(newstate)) 
                    if(new_State.is_goal()):
                        ret=np 
        return ret
    

    def get_star(self):
        ret=[]
        i = 0
        while (not frontier.empty()):
            np = frontier.get().p
            ret=np[-1].successor(np)
            if ret:
                break
            i += 1
        return ret


def main():
    # 06602113211347754775
    # 21132113466547757007
    # 21132113466547757007
    initialstate=State("21132113466547757007")
    l = []
    l.append(initialstate)
    initialpath = Path(l)
    frontier.put(initialpath)
    print("Initial state:")
    print_state(initialstate.CurrentState)
    ret=initialstate.get_star()
    print("Cost of the solution: "+str(len(ret))+"\n")
    print("Number of states expanded: "+str(numExpand)+"\n")
    print("Number of frontier "+str(frontier.qsize()))
    print("Solution:\n")
    num=len(ret)
    for i in range(0, num):
        print(i)
        print_state(ret[i].CurrentState)


import time
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))

