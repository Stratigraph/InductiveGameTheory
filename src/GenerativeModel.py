
from collections import defaultdict

import random
import numpy as np
import networkx as nx

#
# GRAPH SERIES CONSTRUCTION UTILITIES
# =====================================

def build_conditional_probabilities(prob_dict, cutoff):
    '''
    Turn a dict of the form {(src, trg): prob, ...} into {src: {trg1: p}...}

    Args:
        prob_dict:
        cutoff:
    '''

    conditional_probabilities = defaultdict(dict)
    for key, p in prob_dict.iteritems():
        if abs(p) > cutoff:
            conditional_probabilities[key[1]][key[0]] = p
    return conditional_probabilities

def build_null_conditional_probabilities(prob_dict, cutoff):
    '''
    Construct null conditional probabilities with the same shape as the real data

    Args:
        prob_dict: 
        cutoff:
    '''
    mu = np.mean(prob_dict.values())
    sigma = np.std(prob_dict.values())
    prob_null = {}
    for key in prob_dict:
        prob_null[key] = np.random.normal(mu, sigma)

    null_conditional_probabilities = defaultdict(dict)
    for key, p in prob_null.iteritems():
        if abs(p) > cutoff:
            null_conditional_probabilities[key[1]][key[0]] = p
    return null_conditional_probabilities


def build_next_network(starting_graph, conditional_probabilities):
    '''
    Build a notional next network from a seed network and conditional probs.
    '''
    # Find the probability of each next edge, given the current edges
    edge_probs = defaultdict(list)
    #edge_probs = defaultdict(float)
    for edge in starting_graph.edges():
        for next_edge, p in conditional_probabilities[edge].items():
            edge_probs[next_edge].append(p)
            #edge_probs[next_edge] += p
    # Simulate forward:
    next_graph = nx.DiGraph()
    for edge, all_p in edge_probs.iteritems():
        '''
        for p in all_p:
            if p > 0 and random.random() < p*p:
                next_graph.add_edge(edge[0], edge[1])
            elif p < 0 and random.random() < p*p:
                try:
                    next_graph.remove_edge(edge[0], edge[1])
                except: pass
        '''
        p = np.sum(all_p)
        if random.random() < p:
            next_graph.add_edge(edge[0], edge[1])
    
    return next_graph


def build_graph_series(seed, conditional_probabilities, start=1, end=10):
    '''
    Build a whole graph series from a seed and conditional probabilities

    Args:
        seed: An initial graph to start with
        conditional_probabilities: A conditional probabilities dict as 
            generated by build_conditional_probabilities
        start: A start label.
        end: End label; defines how many graphs forward to build.
    '''
    G0 = seed
    sim_graphs = {}
    last_graph = G0
    for y in range(start, end):
        G = build_next_network(last_graph, conditional_probabilities)
        sim_graphs[y] = G
        last_graph = G
    return sim_graphs

def make_graph_ensemble(seed, conditional_probabilities, n, start, end):
    '''
    Generate n realizations from the seed network
    '''
    series_ensemble = defaultdict(list)
    for i in range(n):
        sim_graphs = build_graph_series(seed, conditional_probabilities, start, end)
        for y in range(start, end):
            series_ensemble[y].append(sim_graphs[y])
    return series_ensemble

def make_null_ensemble(seed, conditional_probabilities, cutoff, n, start, end):
    '''
    Generate a null ensemble to compare against the real one
    '''
    null_ensemble = defaultdict(list)
    for i in range(n):
        null_probabilities = build_null_conditional_probabilities(conditional_probabilities, cutoff)
        null_graphs = build_graph_series(seed, null_probabilities, start, end)
        for y in range(start, end):
            null_ensemble[y].append(null_graphs[y])
    return null_ensemble




#
# GRAPH SERIES TESTING FUNCTIONS
# ==============================

def total_degree_error(real_graph, sim_graph):
    error = (len(sim_graph.edges()) - len(real_graph.edges()))**2
    return error

def degree_error(real_graph, sim_graph):
    '''
    Return the MSE of node degrees
    '''
    real_vals = nx.degree(real_graph)
    sim_vals = nx.degree(sim_graph)
    nodes = set(real_graph.nodes() + sim_graph.nodes())
    error = 0.0
    for node in nodes:
        r = real_vals[node] if node in real_vals else 0
        s = sim_vals[node] if node in sim_vals else 0
        error += (s - r)**2.0
    return error/len(nodes)

def closeness_error(real_graph, sim_graph):
    '''
    Return the mean square error of closeness centrality
    '''
    real_vals = nx.closeness_centrality(real_graph)
    sim_vals = nx.closeness_centrality(sim_graph)
    nodes = set(real_graph.nodes() + sim_graph.nodes())
    error = 0.0
    for node in nodes:
        r = real_vals[node] if node in real_vals else 0
        s = sim_vals[node] if node in sim_vals else 0
        error += (s - r)**2.0
    return error/len(nodes)

def betweenness_error(real_graph, sim_graph):
    '''
    Return the mean square error of closeness centrality
    '''
    real_vals = nx.betweenness_centrality(real_graph)
    sim_vals = nx.betweenness_centrality(sim_graph)
    nodes = set(real_graph.nodes() + sim_graph.nodes())
    error = 0.0
    for node in nodes:
        r = real_vals[node] if node in real_vals else 0
        s = sim_vals[node] if node in sim_vals else 0
        error += (s - r)**2.0
    return error/len(nodes)