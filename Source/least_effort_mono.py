#!/usr/bin/env python3
"""
least_effort_mono.py

Least-Effort Monolithic Enforcer
extracted from CompositionalEnforcer.py.

Logic is unchanged.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.product import product, product_or

def least_effort_monolithic_enforcer(name, *D):
    """
    Least Effort Monolithic Enforcer.

    Logic identical to original CompositionalEnforcer.least_effort_monolithic_enforcer.
    """
    assert len(D) > 0

    # OR-product DFA
    if len(D) == 1:
        product_dfa = D[0]
    else:
        product_dfa = product_or(D[0], D[1], name)
        for i in range(2, len(D)):
            product_dfa = product_or(product_dfa, D[i], name)

    q = product_dfa.q0
    sigma_c = []

    def process_event(a, debug=False):
        nonlocal q, sigma_c

        # flushing remaining buffer
        if a is None:
            if sigma_c:
                released = sigma_c.copy()
                sigma_c = []
                if debug:
                    return released, sigma_c.copy()
                return released
            return [] if not debug else ([], sigma_c.copy())

        # append event
        sigma_c.append(a)
        temp_state = q

        # checking acceptance incrementally
        for i, sym in enumerate(sigma_c):
            temp_state = product_dfa.d(temp_state, sym)
            if temp_state is None:
                break
            if product_dfa.F(temp_state):
                # releasing prefix
                released = sigma_c[:i+1]
                sigma_c = []
                q = temp_state
                if debug:
                    return released, sigma_c.copy()
                return released

        return [] if not debug else ([], sigma_c.copy())

    return process_event


# Optional alias:
def least_effort_mono(name, *D):
    """
    Wrapper alias: least_effort_mono ≡ least_effort_monolithic_enforcer
    """
    return least_effort_monolithic_enforcer(name, *D)
