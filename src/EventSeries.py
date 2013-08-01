'''
Created on Jun 24, 2013

@author: dmasad
'''
import copy
import random
from collections import defaultdict

import numpy as np

from fast_calc import *

class EventSeries(object):
    '''
    A class to store and do analysis on series of events, to test hypotheses
    that certain events lead to particular other events.
    '''


    def __init__(self, event_dict=None):
        '''
        Create a new event series.
        
        Args:
            event_dict: A dictionary containing an existing mapping of 
                timestamps to events
        '''
        
        self.event_dict = {}
        self.actors = set()
        
        if event_dict is not None:
            self.event_dict = copy.deepcopy(event_dict)
            for vals in self.event_dict.values():
                for entry in vals:
                    self.actors.add(entry)
            self.keys = self.event_dict.keys()
            self.keys.sort()
            self.array = [self.event_dict[key] for key in self.keys]
        else:
            self.keys = None
            self.array = None
    
    def __getitem__(self, key):
        '''
        Return the entries associated with the given key.
        '''
        return self.event_dict[key]
    
    def __setitem__(self, key, val):
        '''
        Set a new item into the series.
        '''
        self.event_dict[key] = val
        for entry in val:
            self.actors.add(entry)
    
    def find_prob(self, A, B, delta=1):
        '''
        Find the probability of event A given event B, with interval delta.
            P(B->A)
        Args:
            A: The target event to examine
            B: The conditional event at time t-delta
            delta: The difference in time to look at
        '''
        if self.array is None:
            self.keys = self.event_dict.keys()
            self.keys.sort()
            self.array = [self.event_dict[key] for key in self.keys]
        p = fast_find_prob(self.array, A, B, delta)
        return p
        
        
        '''
        # Pre-Cython version
        # Deprecated
        p_ba = 0.0
        p_a = 0.0
        p_b = 0.0
        
        keys = self.event_dict.keys()
        keys.sort()
        for key in keys:
            events = self[key]
            if A in events:
                p_a += 1
            if B in events:
                p_b += 1
        
        for i in range(delta, len(keys)):
            t = keys[i]
            t_lag = keys[i-delta]
            if B in self[t_lag] and A in self[t]:
                p_ba += 1
        
        p_ba /= p_a
        p_a /= len(keys)
        p_b /= len(keys)
        p_ab = (p_ba * p_a)/p_b
        return p_ab
        '''
    
    def find_all_probs(self, delta=1):
        '''
        Find all the conditional probabilities P(B->A) for all A, B
        '''
        conditional_probabilities = {}
        for A in self.actors:
            for B in self.actors:
                conditional_probabilities[(A, B)] = self.find_prob(A, B, delta)
        return conditional_probabilities
    
    def random_reshuffle(self):
        '''
        Reshuffle events while preserving internal structure and return an EventSeries
        '''
        keys = self.event_dict.keys()
        keys.sort()
        keys_to_shuffle = self.event_dict.keys()
        # Distribute the event blocks at random.
        random_events = {}
        for key in keys:
            id = random.choice(range(len(keys_to_shuffle)))
            block_id = keys_to_shuffle.pop(id)
            random_events[key] = self.event_dict[block_id]
        random_series = EventSeries(random_events)
        return random_series

    def find_all_delta_probs(self, delta=1, n=1000):
        '''
        Find all DeltaP(B->A) = P(B->A) - Null(B->A)
        
        Args:
            delta: The time lag to examine
            n: The number of random reshuffles to perform.
        '''
        all_nulls = defaultdict(list)
        for i in range(n):
            null = self.random_reshuffle().find_all_probs(delta)
            for key, p in null.iteritems():
                all_nulls[key].append(p)
        null_model = {}
        
        for key, probs in all_nulls.iteritems():
            null_p = np.mean(probs)
            null_model[key] = null_p
        
        cond_probs = self.find_all_probs(delta)
        delta_probs = {}
        for key, p in cond_probs.iteritems():
            delta_probs[key] = p - null_model[key]
        return delta_probs
            
if __name__ == "__main__":
    # Create data:
    # Events A, B, C are random
    # P(A->D) = 1
    # P(B->E) = 0.85
    events = defaultdict(list)
    for t in range(100):
        for e in ["A", "B", "C"]:
            if random.random() < 0.5:
                events[t].append(e)
        if "A" in events[t] and t < 99:
            events[t+1].append("D")
        if "B" in events[t] and t < 99 and random.random() < 0.85:
            events[t+1].append("E")
    # Test:
    event_series = EventSeries(dict(events))
    
    
            
        