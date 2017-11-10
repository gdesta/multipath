# Author: Girmaye Desta

import sys
import random
import networkx as nx
import multipath
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

def perform_simulation(iterations):
    """
    The simulation includes a 
    - Monte Carlo simulation, 
    - Statistical analysis and 
    - plotting a Normalized Frequency Histogram 
        
    Parameters:
    iterations: The number of trials for the Monte Carlo simulation
    """
    g = create_twelve_node_graph()

    print "==========================================================================================="
    print "Monte Carlo simulation"    
    print "Running ", iterations, " iterations.."
    ave_tot_bw, iteration_bw = perform_montecarlo_simulation(g, iterations)
    max_bw = max(iteration_bw.values())
    iteration_of_max_bw = max(iteration_bw, key = lambda a : iteration_bw[a])

    print "==========================================================================================="
    print "SUMMARY OF ITERATION OUTPUTS"
    print "------------------------------------------"
    print "Final Average Bandwidth:", ave_tot_bw
    print "Maximum iteration_bw: ", max_bw, " at iteration_num: ", iteration_of_max_bw
    arr = 1.0*np.array(iteration_bw.values())
    print "sample standard deviation: ", np.std(arr, ddof = 1)
    se = scipy.stats.sem(arr) 
    print "standard error: ", se
    ci2 = scipy.stats.t.interval(0.95,len(arr)-1, loc=np.mean(arr), scale=scipy.stats.sem(arr))
    print "95% confidence interval: ", ci2
    print "==========================================================================================="
    
    # Plot a Normalized Frequency Histogram
    plot_histogram(iterations, iteration_bw, max_bw)

def create_twelve_node_graph():
    """"
    Creates a 12 node graph (refer to the README of this project for the diagram of the graph)
    """
    g = nx.Graph()
    g.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    g.add_edges_from([(1, 2), (1, 7), (2, 3), (2, 8), (3, 4), (3, 7), (3, 9), (4, 5), (4, 8), (4, 10), (5, 6), (5, 9), (5, 11), (6, 10), (6, 12), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12)])
    return g

def perform_montecarlo_simulation(g, iterations):
    """"
    Perform Monte Carlo simulation: Run algorithm (in this case MLBDP algorithm is run) for multiple trials, 
    where bandwidth values of graph edges is picked randomly from a distribution for each iteration
    In this case, a uniform distribution and the range 1 to 100 is chosen
    
    Parameters:
    g: graph
    iterations: number of iterations(trials)    
    """
    ave_tot_bw = 0
    iteration_bw = {}
        
    for i in range(iterations):
        for u in g.nodes():
            for v in g.nodes():
                if g.has_edge(u, v):
                    g.edge[u][v]['bw'] = random.randint(1,100) 
        # Compute total (sum) bandwidth between node number 1 and node number 12 along 2 paths            
        mlbdp_bandwidth = multipath.mlbdp(g, 1, 12)
        print "******COMPLETED ITERATION NUMBER: ", i+1, "*******"
        ave_tot_bw += mlbdp_bandwidth
        iteration_bw[i+1] = mlbdp_bandwidth # Numbering iterations starting from 1 rather than 0
    
    ave_tot_bw /= float(iterations)
    return ave_tot_bw, iteration_bw
    
def plot_histogram(iterations, iteration_bw, max_bw):
    """
    Plot a Normalized Frequency Histogram of the bandwidth results
    """
    iteration_bw_probs = {}
    for i in range(max_bw + 1):
        iteration_bw_probs[i] = 0
    for i in range(len(iteration_bw)):
        iteration_bw_probs[iteration_bw[i+1]] += 1
    for i in range(len(iteration_bw_probs)):
        iteration_bw_probs[i] /= float(len(iteration_bw))
            
    plt.bar(iteration_bw_probs.keys(), iteration_bw_probs.values(), align='center')
    plt.xticks(np.arange(0, max_bw+1, 10.0))
    
    plt.xlabel('Computed Bandwdith')
    plt.ylabel('Normalized Frequency')
    plt.title('MLBDP on a 12 node graph - ' + str(iterations) + ' trials')
    plt.autoscale()
    plt.show()
    
def main():
    perform_simulation(int(sys.argv[1]))

if __name__ == '__main__': 
    main()