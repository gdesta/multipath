#! /usr/bin/python
import sys
import timeit
import random
import networkx as nx
import mlbdp_computation
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def mlbdp_simulation(iterations):
    """
    Runs a Monte Carlo simulation of the mlbdp algorithm, 
    by assigning the bandwidth value of each graph edge to a random value from 1 to 100 in a uniform distribution
    
    Attributes:
    iterations: The number of trials for which we run the mlbdp algorithm, (each trial uses a different set of random values)
    """
    g = nx.Graph()
    g.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    g.add_edges_from([(1, 2), (1, 7), (2, 3), (2, 8), (3, 4), (3, 7), (3, 9), (4, 5), (4, 8), (4, 10), (5, 6), (5, 9), (5, 11), (6, 10), (6, 12), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12)])
    
    print "========================================="
    print "Monte Carlo simulation of MLBDP Algorithm"
    print "GENERATING PATHS. PLEASE WAIT.........."
    start = timeit.default_timer()
    mlbdp_ave_tot_bw = 0
    mlbdp_iteration_bw = {}
    iteration_bw_probs = {}
    print "Running ", iterations, " iterations.."
    
    for i in range(iterations):
        for u in g.nodes():
            for v in g.nodes():
                if g.has_edge(u, v):
                    g.edge[u][v]['bw'] = random.randint(1,100) 
        # compute total (sum) bandwidth between node number 1 and node number 12 along 2 paths            
        mlbdp_bandwidth = mlbdp_computation.mlbdp(g, 1, 12)
        print "******COMPLETED ITERATION NUMBER: ", i+1
        print "==========================================================================================="
        mlbdp_ave_tot_bw += mlbdp_bandwidth
        mlbdp_iteration_bw[i+1] = mlbdp_bandwidth #numbering iterations starting from 1 rather than 0
    
    mlbdp_ave_tot_bw /= float(iterations)       
    time_taken = timeit.default_timer() - start
    
    print "SUMMARY OF ITERATION OUTPUTS"
    print "------------------------------------------"
    print "mlbdp_ave_tot_bw (FINAL AVERAGE BW):", mlbdp_ave_tot_bw
    print "Node Disjoint path finding using MLBDP algorithm took: " + str(time_taken) + " seconds" + " for " + str(iterations) + " iterations"
    
    max_bw = max(mlbdp_iteration_bw.values())
    iteration_of_max_bw = max(mlbdp_iteration_bw, key = lambda a : mlbdp_iteration_bw[a])
    print "Maximum mlbdp_iteration_bw: ", max_bw, " at iteration_num: ", iteration_of_max_bw
    
    for i in range(max_bw + 1):
        iteration_bw_probs[i] = 0
    for i in range(len(mlbdp_iteration_bw)):
        iteration_bw_probs[mlbdp_iteration_bw[i+1]] += 1
    for i in range(len(iteration_bw_probs)):
        iteration_bw_probs[i] /= float(len(mlbdp_iteration_bw))
    
    arr = 1.0*np.array(mlbdp_iteration_bw.values())
    print "sample standard deviation: ", np.std(arr, ddof = 1)
    se = scipy.stats.sem(arr) 
    print "standard error: ", se
    ci2 = scipy.stats.t.interval(0.95,len(arr)-1, loc=np.mean(arr), scale=scipy.stats.sem(arr))
    print "95% confidence interval: ", ci2
    print "==========================================================================================="
        
    plt.bar(iteration_bw_probs.keys(), iteration_bw_probs.values(), align='center')
    plt.xticks(np.arange(0, max_bw+1, 10.0))
    
    plt.xlabel('Computed Bandwdith')
    plt.ylabel('Normalized Frequency')
    plt.title('MLBDP on a 12 node graph - ' + str(iterations) + ' trials')
    plt.autoscale()
    plt.show()
    
def main():
    mlbdp_simulation(int(sys.argv[1]))

if __name__ == '__main__': 
    main()