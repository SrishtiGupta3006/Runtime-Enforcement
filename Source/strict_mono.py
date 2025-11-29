#!/usr/bin/env python3
"""
strict_mono.py

Strict monolithic composition (logical monolithic_enforcer)
extracted from CompositionalEnforcer.py.

Logic is unchanged.
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.product import product


def monolithic_enforcer(name, *D):
    """
    Build a monolithic AND-product enforcer combining all DFAs.

    Equivalent to conjunction of all properties.
    Logic identical to original CompositionalEnforcer.monolithic_enforcer.
    """

    def combine(name, *D):
        assert len(D) > 1, "Need at least 2 DFAs"
        combined = product(D[0], D[1], name)
        for i in range(2, len(D)):
            combined = product(combined, D[i], name)
        return combined

    return combine(name, *D)


# Optional alias matching your conceptual name:
def strict_mono(name, *D):
    """
    Wrapper alias: strict_mono ≡ monolithic_enforcer
    """
    return monolithic_enforcer(name, *D)
