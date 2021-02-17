import numpy
import threading, queue
import heapq

frontier = queue.PriorityQueue()
pathset = set()

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
        self.numExpand = 0
        frontier.put(self)

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
    
    # calculate the cost of the current set
    def get_cost(self):
        return self.pastPath.qsize()

    # define the operator of "gt"
    def __gt__(self, other):
        valself = self.get_heuristic() +  self.get_cost() 
        valoth = other.get_heuristic() +  other.get_cost() 
        if (valoth>valself):
            return False
        else:
            return True    

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
           
    # return the new state
    def successor(self):
        tileset=self.get_tileset()
        for t in tileset:
            if (check_wide(self.CurrentState,-1,t.width,t.height,t.location)): # left
                self.numExpand += 1
                newstate = move_wide(self.CurrentState,-1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    frontier.put(new_State)
                    pathset.add(tranferse_state(newstate))  
            if (check_wide(self.CurrentState,1,t.width,t.height,t.location)): # right
                self.numExpand += 1
                newstate = move_wide(self.CurrentState,1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    frontier.put(new_State)
                    pathset.add(tranferse_state(newstate)) 
            if (check_height(self.CurrentState,-1,t.width,t.height,t.location)): # up
                self.numExpand += 1
                newstate=move_height(self.CurrentState,-1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    frontier.put(new_State)
                    pathset.add(tranferse_state(newstate)) 
            if (check_height(self.CurrentState,1,t.width,t.height,t.location)): # down  
                self.numExpand += 1
                newstate=move_height(self.CurrentState,1,t.width,t.height,t.location, t.tpe)
                if(not(tranferse_state(newstate) in pathset)):
                    new_State=State(newstate)
                    frontier.put(new_State)
                    pathset.add(tranferse_state(newstate)) 
        if(not frontier.empty()):
            realstate=frontier.get()
            self.pastPath.put(self.CurrentState)  
            self.CurrentState=realstate.CurrentState     

    def get_star(self):
        while(not self.is_goal()):
            #if self.numExpand > 1000000:
            #    break
            self.successor()


def main():
    # 06602113211347754775
    # 21132113466547757007
    # 21132113466547757007
    initialstate=State("21132113466547757007")
    print("Initial state:")
    print_state(initialstate.CurrentState)
    initialstate.get_star()
    print("Cost of the solution: "+str(initialstate.pastPath.qsize())+"\n")
    print("Number of states expanded: "+str(initialstate.numExpand)+"\n")
    print("Solution:\n")
    num=initialstate.pastPath.qsize()
    for i in range(0, num):
        print(i)
        print_state(initialstate.pastPath.get()+"\n")
    print(num)
    print_state(initialstate.CurrentState)
main()

