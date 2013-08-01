'''
Cython code to speed up calculating conditional probabilities.
'''

def fast_find_prob(array, A, B, int delta):
    '''
    Find the probability of event A given event B, with interval delta.
        P(B->A)
    Args:
        array: The array to search in.
        A: The target event to examine
        B: The conditional event at time t-delta
        delta: The difference in time to look at
    '''
    cdef double p_ba = 0.0
    cdef double p_a = 0.0
    cdef double p_b = 0.0
    
    cdef int size = len(array)
    cdef int i
    
    for i in range(size):
        events = array[i]
        if A in events:
            p_a += 1
        if B in events:
            p_b += 1
    
    for i in range(delta, size):
        if B in array[i-delta] and A in array[i]:
            p_ba += 1
    
    p_ba /= p_a
    p_a /= size
    p_b /= size
    p_ab = (p_ba * p_a)/p_b
    return p_ab