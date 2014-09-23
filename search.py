from osm2networkx import *
import random, Queue, heapq, math

"""
Searching a street network using Breadth First Search

REQUIREMENTS:

  networkx: http://networkx.github.io/

REFERENCES:

  [1] Russel, Norvig: "Artificial Intelligene A Modern Approach", 3rd ed, Prentice Hall, 2010

"""

"""
The state space in our problem hold:

   1) A node in the street graph
   2) A parent node

"""
class State:

    def __init__(self, node, parent):
        self.node   = node
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, State):
            return self.node['data'].id == other.node['data'].id
        return NotImplemented

"""
Implements BFS on our GPS data
"""
def bfs(graph, start, goal):
    if start == goal:
        print "START === GOAL"
        return None
    
    frontier = [start]
    explored = []
    num_explored = 0
    while len(frontier) > 0:
       node = frontier.pop(0)
       explored.append(node)
       for edge in networkx.edges(graph, node.node['data'].id):
          
           child = State(graph.node[edge[1]], node) 
           if (child not in explored) and (child not in frontier):
               # HINT: Goal - Check
               if child == goal:
                   print "Goal found, explored: ", num_explored, "\n\n"
                   return child
               else:
                   frontier.append(child)
               num_explored = num_explored + 1
    print "No path found, explored: ", num_explored

    return None

"""
Implements UCS on our GPS data
"""

def foundin(queue, cost, node):
    for item in queue:
        if node in item:
            if cost<item[0]:
                item = (cost,item[1])
                heapq.heapify(queue)
            return item[0]
    return

def getdistance(node1, node2):
    lat1 = node1.node['data'].lat
    lon1 = node1.node['data'].lon
    lat2 = node2.node['data'].lat
    lon2 = node2.node['data'].lon
    return math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
        

def ucs(graph, start, goal):
    print "UCS in progress..."
    if start == goal:
        print "START === GOAL"
        return 0

    #Initialize frontier with heapq
    frontier =[]
    heapq.heappush(frontier,(0,start))

    explored = []
    num_explored = -1

    while len(frontier) > 0:
       #Pop the first node in the priority queue
       totalcost, node = heapq.heappop(frontier)  
       num_explored = num_explored + 1

       if node == goal:
            #print "Goal found, explored: ", num_explored, "\n\n"
            #print "Path cost: ", totalcost, "\n"
            #return node
            return num_explored

       explored.append(node)

       for edge in networkx.edges(graph, node.node['data'].id):
            child = State (graph.node[edge[1]], node) 
            childcost = getdistance (node,child)

            present = foundin (frontier, totalcost + childcost, child)

            if present:
                continue

            elif (child not in explored):
               heapq.heappush(frontier,(totalcost+childcost,child))

            
    print "No path found, explored: ", num_explored

    return num_explored


"""
Implements Bidirectional Search on our GPS data
"""	
def presentin (queue, node, i):
    for item in queue:
        if node in item:
            #print node.node['data'].id, " is in ", i
            return node
    return

def bi(graph, start, goal):
    print "BiSearch in progress..."
    if start == goal:
        print "START === GOAL"
        return 0

    #Initialize frontiers with heapq for efficient pushing/popping and path cost storage
    frontier1 =[]
    frontier2 =[]
    heapq.heappush(frontier1,(0,start))
    heapq.heappush(frontier2,(0,goal))

    #Also initialize a hash table for efficient lookup of nodes.
    frontierhash1 = {}
    frontierhash2 = {}
    frontierhash1[start.node['data'].id] = start
    frontierhash2[goal .node['data'].id] = goal
    
    explored1 = []
    explored2 = []

    num_explored1 = -1
    num_explored2 = -1

    while len(frontier1) > 0 and len(frontier2) > 0:
       #Pop the first node from the priority queue and hash table
       totalcost1, node1 = heapq.heappop(frontier1)
       frontierhash1.pop(node1.node['data'].id, None)  
       num_explored1 = num_explored1 + 1

       if node1.node['data'].id in frontierhash2:
            #print "1Goal found, explored: ", num_explored1 ,"+", num_explored2, "=", num_explored1 + num_explored2,"\n\n"
            #print "1Path cost: ", totalcost1 + totalcost2, "\n"
            #return node1
            return num_explored1 + num_explored2

       explored1.append(node1)

       for edge in networkx.edges(graph, node1.node['data'].id):
            child = State (graph.node[edge[1]], node1) 
            childcost = getdistance (node1, child)

            present = foundin (frontier1, totalcost1 + childcost, child)

            if present:
                continue

            elif (child not in explored1):
               heapq.heappush(frontier1,(totalcost1 + childcost, child))
               frontierhash1[child.node['data'].id] = child

       #Repeat the same thing from node2
       totalcost2, node2 = heapq.heappop(frontier2)  
       num_explored2 = num_explored2 + 1

       if node2.node['data'].id in frontierhash1:
            #print "2Goal found, explored: ", num_explored1 ,"+", num_explored2, "=", num_explored1 + num_explored2,"\n\n"
            #print "2Path cost: ",  totalcost1 + totalcost2, "\n"
            #return node2
            return num_explored1 + num_explored2

       explored2.append(node2)

       for edge in networkx.edges(graph, node2.node['data'].id):
            child = State (graph.node[edge[1]], node2) 
            childcost = getdistance (node2,child)

            present = foundin (frontier2, totalcost2 + childcost, child)

            if present:
                continue

            elif (child not in explored2):
               heapq.heappush(frontier2,(totalcost2 + childcost, child))
               frontierhash2[child.node['data'].id] = child

    print "No path found, explored: ", num_explored1 + num_explored2

    return num_explored1 + num_explored2


"""
Implements TRIdirectional Search on our GPS data
""" 

def tri(graph, start1, start2, start3):
    print "TriSearch in progress..."

    #Initialize frontier1 with heapq
    frontier1 =[]
    heapq.heappush(frontier1,(0,start1))

    #Initialize frontier2 with heapq
    frontier2 =[]
    heapq.heappush(frontier2,(0,start2))

    #Initialize frontier2 with heapq
    frontier3 =[]
    heapq.heappush(frontier3,(0,start3))

    explored1 = []
    explored2 = []
    explored3 = []

    num_explored1 = -1
    num_explored2 = -1
    num_explored3 = -1

    common1 = None
    common2 = None
    common3 = None

    check12 = 1
    check13 = 1
    check23 = 1

    result = []

    while len(frontier1) > 0 and len(frontier2) > 0 and len(frontier3) > 0:  
       #Pop the first node in the priority queue
       totalcost1, node1 = heapq.heappop(frontier1)  
       num_explored1 = num_explored1 + 1

       if ((check12) and presentin(frontier2, node1, 2)):
            check12 = None
            result.append(node1)
            #print "Intersection of 1 & 2 : ", node1.node['data'].id
            if len(result) == 2: return num_explored1 + num_explored2 + num_explored3

       if ((check13) and presentin(frontier3, node1, 3)):
            check13 = None
            result.append(node1)
            #print "Intersection of 1 & 3 : ", node1.node['data'].id
            if len(result) == 2: return num_explored1 + num_explored2 + num_explored3

       explored1.append(node1)

       for edge in networkx.edges(graph, node1.node['data'].id):
            child = State (graph.node[edge[1]], node1) 
            childcost = getdistance (node1, child)

            present = foundin (frontier1, totalcost1 + childcost, child)

            if present:
                continue

            elif (child not in explored1):
               heapq.heappush(frontier1,(totalcost1 + childcost, child))

       #Pop the first node in the priority queue
       totalcost2, node2 = heapq.heappop(frontier2)  
       num_explored2 = num_explored2 + 1

       if ((check12) and presentin(frontier1, node2, 1)):
            check12 = None
            result.append(node2)
            #print "Intersection of 1 & 2 : ", node2.node['data'].id
            if len(result) == 2: return num_explored1 + num_explored2 + num_explored3

       if ((check23) and presentin(frontier3, node2, 3)):
            check23 = None
            result.append(node2)
            #print "Intersection of 2 & 3 : ", node2.node['data'].id
            if len(result) == 2: return num_explored1 + num_explored2 + num_explored3

       explored2.append(node2)

       for edge in networkx.edges(graph, node2.node['data'].id):
            child = State (graph.node[edge[1]], node2) 
            childcost = getdistance (node2,child)

            present = foundin (frontier2, totalcost2 + childcost, child)

            if present:
                continue

            elif (child not in explored2):
               heapq.heappush(frontier2,(totalcost2 + childcost, child))

       #Pop the first node in the priority queue
       totalcost3, node3 = heapq.heappop(frontier3)  
       num_explored3 = num_explored3 + 1

       if ((check13) and presentin(frontier1, node3, 1)):
            check13 = None
            result.append(node3)
            #print "Intersection of 1 & 3 : ", node3.node['data'].id
            if len(result) == 2: return num_explored1 + num_explored2 + num_explored3

       if ((check23) and presentin(frontier2, node3, 2)):
            check23 = None
            result.append(node3)
            #print "Intersection of 2 & 3 : ", node3.node['data'].id
            if len(result) == 2: return num_explored1 + num_explored2 + num_explored3

       explored3.append(node3)

       for edge in networkx.edges(graph, node3.node['data'].id):
            child = State (graph.node[edge[1]], node3) 
            childcost = getdistance (node3,child)

            present = foundin (frontier3, totalcost3 + childcost, child)

            if present:
                continue

            elif (child not in explored3):
               heapq.heappush(frontier3,(totalcost3 + childcost, child))
            
    print "No path found, explored: ", num_explored1 + num_explored2 + num_explored3

    return num_explored1 + num_explored2 + num_explored3

"""
Backtrack and output your solution
"""
def backtrack(state, graph):
    if state.parent != None:
        print "Node: ", state.node['data'].id
        if len(state.node['data'].tags) > 0:            
            for key in state.node['data'].tags.keys():
                print "       N: ", key, " ", state.node['data'].tags[key]        
              
        for edge in networkx.edges(graph, state.node['data'].id):
            if len(graph.node[edge[1]]['data'].tags) > 0:
                for key in graph.node[edge[1]]['data'].tags:
                    print "       E: ", graph.node[edge[1]]['data'].tags[key]
        backtrack(state.parent, graph)

"""
The setup
"""

print "\n\n-----Searching ATLANTA ------\n\n"
only_roads = True
graph = read_osm('atlanta.osm', only_roads)
print "Node1, Node2, Node3 Search Stats ===>"

for i in range(100):
    num1 = random.randint(0, len(graph.nodes()))
    num2 = random.randint(0, len(graph.nodes()))
    num3 = random.randint(0, len(graph.nodes()))
    

    nodes_ucs = 0
    nodes_bi = 0
    nodes_tri = 0

    first     = graph.node[graph.nodes()[num1]]
    second    = graph.node[graph.nodes()[num2]]
    third     = graph.node[graph.nodes()[num3]] 

    #print "NUMBER OF NODES: ", len(graph.nodes())
    #print "NUMBER OF EDGES: ", len(graph.edges())
    #print "START:           ", num1, "->", first['data'].id
    #print "STOP :           ", num2, "->", second['data'].id
    #print "Third :          ", num3, "->", third['data'].id

    #state = bfs(graph, State(first, None), State(second, None))
    
    nodes_ucs += ucs(graph, State(first, None), State(second, None))
    nodes_ucs += ucs(graph, State(second, None), State(third, None))
    nodes_ucs += ucs(graph, State(third, None), State(first, None))

    nodes_bi  += bi (graph, State(first, None), State(second, None))
    nodes_bi  += bi (graph, State(third, None), State(second, None))
    nodes_bi  += bi (graph, State(first, None), State(third, None))

    nodes_tri += tri(graph, State(first, None), State(second, None), State(third, None))
    print num1, ",", num2, ",", num3, " ===> nodes_ucs = ", nodes_ucs, " | nodes_bi = ", nodes_bi, " | nodes_tri = ", nodes_tri
    
    #if state != None:
        #backtrack(state, graph)
print "\n\n"
