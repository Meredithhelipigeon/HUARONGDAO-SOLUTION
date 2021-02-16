import numpy
import threading, queue
import heapq

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

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




class :
    

def main():
    print(2)


main()
