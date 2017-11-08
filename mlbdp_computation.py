#! /usr/bin/python
import sys

def mlbdp (g, s, d, bw="bw"):
    """ computes two bandwidth maximizing node-disjoint paths in a graph g from source node s to destination node d, and returns the bandwidth amount
    this is an implementation of the algorithm proposed in the paper: 
    M. Dahshan. Maximum-Bandwidth Node-Disjoint Paths. International Journal of Advanced Computer Science and Applications (IJACSA), 3(3), 2012.
    Attributes:
        g: graph on which paths are computed
        s: source node
        d: destination node
        bw: the name of the property of a graph edge that represents bandwidth
    This function makes a call to the mlbdp_path function (defined below this function) for each 'limit'(unique) bandwidth    
    """    
    limits = set()
    for u in g.nodes():
        for v in g.nodes():
            if g.has_edge(u,v):
                limits.add(g.get_edge_data(u,v)[bw])
    
    total_bw = 0
    red_final = 0
    blue_final = 0
    prev = {}
    limit_bw = 0
    
    for limit in limits:
        print " starting iteration for LIMIT:"
        print limit        
        # the function mlbdp_path is called for each limit bandwidth
        (red, blue, prev_returned, is_break) = mlbdp_path(g, s, d, limit, bw)
        if not is_break:
            if (red + blue) > total_bw:
                total_bw = red + blue
                red_final = red
                blue_final = blue
                prev = dict(prev_returned)
                limit_bw = limit        
    red_path = [d]
    blue_path = [d]
    (r, b) = (d, d)   
    
    if limit_bw == 0:
        print "limit_bw: ", limit_bw 
        print "red_final: ", red_final
        print "blue_final: ", blue_final
        print "prev: ", prev
    if ((red_final == 0) or (blue_final == 0)):
        print "either red path or blue path have 0 capacity"
        for i in g.nodes():
            for j in g.nodes():
                if (g.has_edge(i,j)):
                    if g.get_edge_data(i,j)[bw] <= 0:
                        print "edge with zero capacity:"
                        print (i,j)
        print "limit_bw: ", limit_bw 
        print "red_final: ", red_final
        print "blue_final: ", blue_final
        print "prev: ", prev
        sys.exit("Path generation Terminated. No two disjoint paths exist.")
    
    while prev[(r,b)] != (s,s):
        (r,b) = prev[(r,b)]
        red_path.append(r)
        blue_path.append(b)
    red_path.append(s)
    blue_path.append(s)
    red_path.reverse()
    blue_path.reverse()    
    red_path_distinct = []
    blue_path_distinct = []
    [red_path_distinct.append(node) for node in red_path if node not in red_path_distinct]
    [blue_path_distinct.append(node) for node in blue_path if node not in blue_path_distinct]
    print "==========================================="
    print " FINAL BEST PATH"
    print "limit_bw:"
    print limit_bw
    print "total_bw:"
    print total_bw
    print "red_path_distinct:"
    print red_path_distinct
    print "blue_path_distinct:"
    print blue_path_distinct
    print "==========================================="
    if ((red_final == 0) or (blue_final == 0)):
        sys.exit("Terminating Execution. No second path exists.")
    return total_bw
    
def mlbdp_path(g, s, d, limit, bw = 'bw'):
    """ For a single 'limit' (unique) bandwidth value, computes two bandwidth maximizing node-disjoint paths in a graph g from source node s to destination node d, and returns the bandwidth amount
    this is an implementation of the algorithm proposed in the paper: 
    M. Dahshan. Maximum-Bandwidth Node-Disjoint Paths. International Journal of Advanced Computer Science and Applications (IJACSA), 3(3), 2012.
    Note that, to find the overall result of the algorithm, this function should be called for each limit bandwidth, which is done by the mlbdp function that is defined above
    Attributes:
        g: graph on which paths are computed
        s: source node
        d: destination node
        limit: unique bandwidth value in graph
        bw: the name of the property of a graph edge that represents bandwidth    
    """
    is_break = False
    permanent = set() # virtual nodes
    tentative = set() # virtual nodes
    visited_links = {} # format of its content: {(virtual_node : set(visited_links,...)), ...}
    visited_nodes = {}
    previous = {} # format of its content: {(virtual_node : previous_virtual_node), ...}
    red_bw = {} # format of its content: {(virtual_node : red_path_max_bw) , ...}
    blue_bw = {} # format of its content: {(virtual_node : blue_path_max_bw), ...}
    
    for i in g.nodes():
        for j in g.nodes():
            visited_links[(i,j)] = set()
            visited_nodes[(i,j)] = set()
            if ((i == s) or (j == s)):
                permanent.add((i,j))            
            else:
                tentative.add((i,j))
            red_bw[(i,j)] = 0
            blue_bw[(i,j)] = 0 
                 
    for i in g.nodes():
        for j in g.nodes():
            if (g.has_edge(s,i) and g.has_edge(s,j) and (i != j)):
                if (g.get_edge_data(s,j)[bw] >= limit):
                    red_bw[(i,j)] = g.get_edge_data(s,i)[bw]
                    blue_bw[(i,j)] = g.get_edge_data(s,j)[bw]
                    previous[(i,j)] = (s,s)
        
    tentative2 = set(tentative)
    for i in g.nodes():
        if i != d and i != s: # s is already removed earlier
            tentative2.remove((i,i))                
                        
    while len(tentative2) > 0: 
        tentative3 = set()
        for m in tentative2:
            if blue_bw[m] >= limit:
                tentative3.add((m))
        max_bw = 0
        if len(tentative3) != 0:        
            max_key = max(tentative3, key = lambda a : red_bw[a])
            max_bw = red_bw[max_key]
        if max_bw <= 0:
            print("Break out of while loop: no red path ")
            is_break = True
            return [red_bw[(d,d)], blue_bw[(d,d)], previous, is_break]
        max_keys = []
        if len(tentative3) != 0:    
            max_keys = [c for c in tentative3 if red_bw[c]==max_bw]        
        
        if (len(max_keys) > 1):
            max_key = max(max_keys, key = lambda b : blue_bw[b])                 
        if(blue_bw[max_key] <= 0):
            print("Break out of while loop: no blue path ")
            is_break = True
            return [red_bw[(d,d)], blue_bw[(d,d)], previous, is_break]
        
        permanent.add(max_key)
        tentative2.remove(max_key)
        
        if max_key == (d,d):
            print "!!!Destination reached, returning from while loop!!!!!!"
            return [red_bw[(d,d)], blue_bw[(d,d)], previous, is_break]
        
        (x,y) = max_key #virtual node neighbor with max-red, above-limit-blue path
            
        for v in g.nodes():
            if g.has_edge(x,v):
                if ((v,y) in tentative2):
                    if (x,v) not in visited_links[(x,y)]:
                        if v not in visited_nodes[(x,y)]:
                            if(min(red_bw[(x,y)], g.get_edge_data(x,v)[bw]) > red_bw[(v,y)]):
                                previous[(v,y)] = (x,y)
                                visited_links[(v,y)] = set(visited_links[(x,y)])
                                visited_links[(v,y)].add((x,v))
                                visited_links[(v,y)].add((v,x))
                                for (a,b) in visited_links[(v,y)]:
                                    if a != d:
                                        visited_nodes[(v,y)].add(a)
                                    if b != d:
                                        visited_nodes[(v,y)].add(b)
                                red_bw[(v,y)] = min(red_bw[(x,y)], g.get_edge_data(x,v)[bw])
                                blue_bw[(v,y)] = blue_bw[(x,y)]
        
        for u in g.nodes():
            if g.has_edge(y,u):
                if (x,u) in tentative2:
                    if (y,u) not in visited_links[(x,y)]: 
                        if u not in visited_nodes[(x,y)]:
                            if red_bw[(x,y)] >= red_bw[(x,u)]:
                                if min(blue_bw[(x,y)], g.get_edge_data(y,u)[bw]) >= limit:
                                    previous[(x,u)] = (x,y)
                                    visited_links[(x,u)] = set(visited_links[(x,y)])
                                    visited_links[(x,u)].add((y,u))
                                    visited_links[(x,u)].add((u,y))
                                    for (e,f) in visited_links[(x,u)]:
                                        if e != d:
                                            visited_nodes[(x,u)].add(e)
                                        if f != d:
                                            visited_nodes[(x,u)].add(f)
                                
                                    red_bw[(x,u)] = red_bw[(x,y)]
                                    blue_bw[(x,u)] = min(blue_bw[(x,y)], g.get_edge_data(y,u)[bw])
                            