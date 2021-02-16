import numpy
import threading, queue
import heapq

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def tranferse_state(state):
    for i in range(len(state)):
        if (state[i]==3 or state[i]==4 or state[i]==5):
            state[i]=2


def check_wide(state,dir,h,loc):
    ret=True 
    if (loc%4+dir == -1 or loc%4+dir == 4):
        ret=False
    for n in range(1,h):
        if (state[loc+dir+(h-1)*4] != 0):
            ret=False
    return ret

def move_wide(state,dir,w,h,loc,tpe):
    for i in range(1,h):
        state[loc+dir+(h-1)*4], state[loc+w-1] = state[loc+w-1], state[loc+dir+(h-1)*4]

def check_height(state,dir,w,loc):
    ret=True
    if (loc/4+dir==-1 or loc/4+dir==5 ):
        ret=False 
    for n in range(1,w):
        if (state[loc+dir*4+w-1] != 0):
            ret=False
    return ret    

 def move_height(state,dir,w,h,loc,tpe):
    for i in range(1,w):
        state[loc+dir*4+w-1]=tpe
        state[loc+h-1]='0'     

class Tile:
    # class attribute
    def __init__(self, location, height, width, type):
        self.location=location
        self.height=height
        self.width=width  
        self.type=type      

class State():
    # class attribute
    def __init__(self, CurrentState):
        self.CurrentState =  CurrentState
        self.pathset = {}
        self.pastPath =[]
        self.numExpand = 0

    # check if it is the goal
    def is_goal(self):
        if self.CurrentState.find('1')==13:
            return True
        else:
           return False     

    # calculate the return value of heuristic function
    def get_heuristic(self):
        diff_x = abs(self.CurrentState.find('1')%4 - 1)   
        diff_y = abs(self.CurrentState.find('1')/4 - 3)  
        return  diff_x+diff_y    
    
    # calculate the cost of the current set
    def get_cost(self):
        return len(self.pastPath)

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
        tileset = {}
        for i in range(1,8):
            if(i==1):
                tileset.add(Tile(self.CurrentState.find('1'),2,2,'1'))
            elif (i==6):
                tileset.add(Tile(self.CurrentState.find('6'),1,2,'6'))
            elif (i==7):
                for j in range(1,5):   # iterate from 1 to 4   
                    tileset.add(Tile(find_nth(self.CurrentState, "7",j),1,1,'7'))
            else:
                tile.set.add(Tile(self.CurrentState.find(char(i)),2,1,char(i)))
        return tileset          
           
    # return the new state
    def successor(self):
        tileset=self.get_tileset
        statelist== queue.PriorityQueue()
        for t in tileset:
            if (check_wide(self.CurrentState,1,t.height,t.location)): # left
                self.numExpand += 1
                newstate = move_wide(self.CurrentState,1,t.width,t.height,t.location, t.type)
            if (check_wide(self.CurrentState,-1,t.height,t.location)): # right
                self.numExpand += 1
                newstate = move_wide(self.CurrentState,-1,t.width,t.height,t.location, t.type)
            if (check_height(self.CurrentState,-1,t.width,t.location)): # up
                self.numExpand += 1
                newstate=move_height(self.CurrentState,-1,t.width,t.height,t.location, t.type)
            if (check_height(self.CurrentState,1,t.width,t.location)): # down  
                self.numExpand += 1
                newstate=move_height(self.CurrentState,1,t.width,t.height,t.location, t.type)        




class :
    

def main():
    print(2)


main()
