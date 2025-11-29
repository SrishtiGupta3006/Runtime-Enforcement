#!/usr/bin/env python3
"""
least_effort_parallel.py

Parallel least-effort enforcement (LeastEffortParallelEnforcer)
extracted from CompositionalEnforcer.py.

Logic is unchanged.
"""

import sys
sys.path.append("..")

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helper.product import DFA

class LeastEffortParallelEnforcer:
    """
    Parallel least-effort enforcement:

    - All enforcers see the same input
    - Each tries to release a safe sequence
    - Global output = OR-merge of all safe sequences

    Logic identical to original CompositionalEnforcer.LeastEffortParallelEnforcer.
    """

    def __init__(self, enforcers):
        self.enforcers = enforcers
        self.n = len(enforcers)

        # current DFA states + candidate buffers
        self.q = [dfa.q0 for dfa in enforcers]
        self.candidate = [[] for _ in enforcers]

        self.output = []

    def process_event(self, a):
        """
        Feed input 'a' to all enforcers in parallel.
        Returns OR-merged safe sequence.
        """
        # appending event to each enforcer's buffer
        for i in range(self.n):
            self.candidate[i].append(a)

        safe_sequences = []

        for i, dfa in enumerate(self.enforcers):
            if dfa.is_safe(self.q[i], self.candidate[i]):
                safe_sequences.append((i, self.candidate[i].copy()))

        # if any enforcer can release
        if safe_sequences:
            released = []

            # OR-merge: maintain order, avoid duplicates
            for idx, seq in safe_sequences:
                for sym in seq:
                    if sym not in released:
                        released.append(sym)

            # appending to global output
            self.output.extend(released)

            # updating DFA states and reset local buffers
            for i in range(self.n):
                self.q[i] = self.enforcers[i].next_state(self.q[i], self.candidate[i])
                self.candidate[i] = []

            return released

        return []  # nothing released

    def get_output(self):
        return self.output


# Optional alias (if you want a function-style constructor)
def least_effort_parallel(enforcers):
    """
    Wrapper alias: least_effort_parallel ≡ LeastEffortParallelEnforcer(enforcers)
    """
    return LeastEffortParallelEnforcer(enforcers)
