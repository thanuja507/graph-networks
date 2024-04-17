import queue
import math

def bfs(graph, start_node, search_node=None):
    # graph: a dictionary representing the graph to be traversed.
    # start_node: a string representing the starting node of the traversal.
    # search_node: an optional string representing the node being searched for in the graph.
    # Note: If the given start_node belongs to one strongly connected component then the other nodes belong to that
           # particular component can only be traversed. But the nodes belonging to other components must not be traversed
           # if those nodes were not reachable from the given start_node.

    #The output depends on whether the search_node is provided or not:
        #1. If search_node is provided, the function returns 1 if the node is found during the search and 0 otherwise.
        #2. If search_node is not provided, the function returns a list containing the order in which the nodes were visited during the search.

    #Useful code snippets (not necessary but you can use if required)
    visited=set()
    qu = queue.Queue()
    qu.put(start_node)
    visited.add(start_node)
    path=[start_node]
    if search_node==None:
        while not qu.empty():
            node = qu.get()
            for neighbour in graph[node].keys():
                if neighbour not in visited:
                    visited.add(neighbour)
                    qu.put(neighbour)
                    path.append(neighbour)
        return path
    else:
        while not qu.empty():
            node = qu.get()
            for neighbour in graph[node].keys():
                if neighbour==search_node:
                    return 1
                if neighbour not in visited:
                    visited.add(neighbour)
                    qu.put(neighbour)
        return 0
# search node not provided, return entire path [list of nconst values of nodes visited]
flag=0

def set_flag():
    global flag
    flag=1

def dfs(graph, start_node, visited=None, path=None, search_node=None):
    # graph: a dictionary representing the graph
    # start_node: the starting node for the search
    # visited: a set of visited nodes (optional, default is None)
    # path: a list of nodes in the current path (optional, default is None)
    # search_node: the node to search for (optional, default is None)
    # Note: If the given start_node belongs to one strongly connected component then the other nodes belong to that
           # particular component can only be traversed. But the nodes belonging to other components must not be traversed
           # if those nodes were not reachable from the given start_node.

    # The function returns:
        # 1. If search_node is provided, the function returns 1 if the node is found and 0 if it is not found.
        # 2. If search_node is not provided, the function returns a list containing the order in which the nodes were visited during the search.

    #Useful code snippets (not necessary but you can use if required)
    # print(graph[start_node])
    if path==None:
        path=[]
    if visited==None:
        visited=set()
    global flag
    flag=0

    def dfs_1(start_node, visited, path):
        if search_node==None:
            if start_node not in visited:
                visited.add(start_node)
                path.append(start_node)
                for neighbour in graph[start_node].keys():
                    if neighbour not in visited:
                        dfs_1(neighbour,visited,path)
            return path
        else:
            if start_node==search_node:
                set_flag()
            if start_node not in visited:
                visited.add(start_node)
                for neighbour in graph[start_node].keys():
                    if neighbour not in visited:
                        dfs_1(neighbour,visited,path)
            return

    res=dfs_1(start_node,set(),[])
    if search_node==None:
        return res
    return flag

    # search node not provided, return entire path [list of nconst id's of nodes visited]

def dijkstra(graph, start_node, end_node):
    # graph: a dictionary representing the graph where the keys are the nodes and the values
            # are dictionaries representing the edges and their weights.
    # start_node: the starting node to begin the search.
    # end_node: the node that we want to reach.

    # Outputs:
        #1. If the end_node is not reachable from the start_node, the function returns 0.

        #2. If the end_node is reachable from the start_node, the function returns a list containing three elements:
                #2.1 The first element is a list representing the shortest path from start_node to end_node.
                     #[list of nconst values in the visited order]
                #2.2 The second element is the total distance of the shortest path.
                     #(summation of the distances or edge weights between minimum visited nodes)
                #2.3 The third element is Hop Count between start_node and end_node.

    # Return the shortest path and distances
    distances=dict.fromkeys(graph.keys(),math.inf)
    track={}
    distances[start_node]=0
    all_nodes=[i for i in graph.keys()]
    def get_min():
        temp=math.inf
        node=None
        for i in all_nodes:
            if distances[i]<temp:
                temp=distances[i]
                node=i
        return node 
    def get_path(track,start_node,end_node):
        path=[]
        hop_count=0
        node=end_node
        while node!=start_node:
            path.append(node)
            hop_count+=1
            if node in track.keys():
                node=track[node]
            else:
                break
        path.append(start_node)
        return [path[::-1],distances[end_node],hop_count]
    while len(all_nodes)>0:
        node = get_min()
        all_nodes.remove(node)
        if node!=end_node:
            for neighbour,dist in graph[node].items():
                temp=distances[node]+dist
                if temp<distances[neighbour]:
                    track[neighbour]=node
                    distances[neighbour]=temp
        else:
            break
    return get_path(track,start_node,end_node)




# (strongly connected components)
def kosaraju(graph):
    # graph: a dictionary representing the graph where the keys are the nodes and the values
            # are dictionaries representing the edges and their weights.
    #Note: Here you need to call dfs function multiple times so you can Implement seperate
         # kosaraju_dfs function if required.

    #The output:
        #list of strongly connected components in the graph,
          #where each component is a list of nodes. each component:[nconst2, nconst3, nconst8,...] -> list of nconst id's.
    order = []
    visited = set()
    def kosaraju_dfs(graph,node,track=None,component=None):
        if node not in visited:
            visited.add(node)
            if component!=None:
                component.append(node)
            for neighbor in graph[node].keys():
                if neighbor not in visited:
                    if track!=None:
                        kosaraju_dfs(graph,neighbor,track)
                    else:
                        kosaraju_dfs(graph,neighbor,None,component)
            if track!=None:
                track.append(node)
    for node in graph.keys():
        kosaraju_dfs(graph,node,order)
    rev_graph={i:{} for i in graph.keys()}

    for k,v in graph.items():
        for ik,iv in v.items():
            rev_graph[ik][k]=iv
    visited.clear()
    components = []
    for node in order[::-1]:
        component = []
        kosaraju_dfs(rev_graph,node,None,component)
        if len(component)>0:
            components.append(component)       
    return components


    

