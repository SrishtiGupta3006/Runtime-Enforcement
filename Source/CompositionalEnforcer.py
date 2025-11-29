#!/usr/bin/env python3
"""
CompositionalEnforcer.py

Implements several compositional runtime-enforcement mechanisms:

1. AND-Product DFA       
2. OR-Product DFA        
3. Monolithic Enforcer   
4. Serial Enforcer       
5. Least-Effort Monolithic Enforcer 
6. Least-Effort Parallel Enforcer  
"""

import sys
sys.path.append("..")

from Enforcer import enforcer        
import helper.Automata as Automata
from helper.Automata import DFA as BaseDFA


#helper Classes

class state(object):
    def __init__(self, name):
        self.name = name
        self.transit = dict()


class DFA(BaseDFA):
    """
    Extended DFA class used for compositional enforcement.

    Attributes:
        name   : Name of the automaton
        end    : List of accepting states (explicit representation)
        buffer : Temporary buffer (used only in bounded enforcer contexts)
    """

    def __init__(self, name, S, Q, q0, F, d, end, e=('.l',)):
        super().__init__(S, Q, q0, F, d, e)
        self.name = name
        self.end = end
        self.buffer = []

    def runInput(self, sigma, maxBuffer=5):
        """
        Run the input sigma through a bounded enforcer for this DFA.
        Returns: (final_state, output_word)
        """
        output = enforcer(self, list(sigma), maxBuffer)
        return self.q, output

    def checkAccept(self, sigma):
        """
        Checking acceptance using bounded enforcer logic.
        """
        return enforcer(self, list(sigma), maxBuffer=5)

    def __flushBuffer(self):
        self.buffer = []

    # ----------------State Transition Helpers-----------------

    def is_safe(self, current_state, event_sequence):
        """
        Checking if applying event_sequence from current_state reaches an accepting state.
        """
        state = current_state
        for e in event_sequence:
            state = self.d(state, e)
            if state is None:
                return False
        return state in self.end

    def next_state(self, current_state, event_sequence):
        """
        Return the state reached after consuming event_sequence from current_state.
        """
        state = current_state
        for e in event_sequence:
            state = self.d(state, e)
            if state is None:
                break
        return state


################## OR/AND-Product DFAs ########################

def product(A, B, p_name):

    assert A.S == B.S, "Alphabets must match!"

    p_states = [f"{qA}_{qB}" for qA in A.Q for qB in B.Q]
    p_start = f"{A.q0}_{B.q0}"

    def p_F(p_state):
        qA, qB = p_state.split("_", 1)
        return A.F(qA) and B.F(qB)

    p_end = [s for s in p_states if p_F(s)]

    def p_d(p_state, symbol):
        qA, qB = p_state.split("_", 1)
        nextA = A.d(qA, symbol)
        nextB = B.d(qB, symbol)
        if nextA is None or nextB is None:
            return None
        return f"{nextA}_{nextB}"

    return DFA(p_name, A.S, p_states, p_start, p_F, p_d, p_end)


def product_or(A, B, p_name):
    """
    OR-product DFA.

    Accepting condition: at least one DFA accepts.

    States are encoded as "qA_qB".
    """
    assert A.S == B.S, "Alphabets must match!"

    p_states = [f"{qA}_{qB}" for qA in A.Q for qB in B.Q]
    p_start = f"{A.q0}_{B.q0}"

    def p_F(p_state):
        qA, qB = p_state.split("_", 1)
        return A.F(qA) or B.F(qB)

    p_end = [s for s in p_states if p_F(s)]

    def p_d(p_state, symbol):
        qA, qB = p_state.split("_", 1)
        nextA = A.d(qA, symbol)
        nextB = B.d(qB, symbol)
        if nextA is None or nextB is None:
            return None
        return f"{nextA}_{nextB}"

    return DFA(p_name, A.S, p_states, p_start, p_F, p_d, p_end)

######################### Monolithic / Serial Enforcers ############################

def monolithic_enforcer(name, *D):
    """
    Build a monolithic AND-product enforcer combining all DFAs.

    Equivalent to conjunction of all properties.
    """
    def combine(name, *D):
        assert len(D) > 1, "Need at least 2 DFAs"
        combined = product(D[0], D[1], name)
        for i in range(2, len(D)):
            combined = product(combined, D[i], name)
        return combined

    return combine(name, *D)


def serial_enforcer(name, *D):
    """
    Enforce DFAs sequentially:
        Input → DFA1 → DFA2 → DFA3 → ... → DFAn

    Returns both the final output and intermediate outputs.
    """
    def serial_apply(sigma, maxBuffer=5):
        assert len(D) > 0, "No DFAs provided."
        current_output = list(sigma)
        individual_outputs = {}

        for i, dfa in enumerate(D):
            dfa_name = getattr(dfa, 'name', f"Property_{i}")
            current_output = enforcer(dfa, current_output, maxBuffer)
            individual_outputs[dfa_name] = current_output.copy()

        return current_output, individual_outputs

    return serial_apply


################ Least-Effort Monolithic Enforcer ########################

def least_effort_monolithic_enforcer(name, *D):
    """
    Least Effort Monolithic Enforcer
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

        #flushing remaining buffer
        if a is None:
            if sigma_c:
                released = sigma_c.copy()
                sigma_c = []
                if debug:
                    return released, sigma_c.copy()
                return released
            return [] if not debug else ([], sigma_c.copy())

        #append event
        sigma_c.append(a)
        temp_state = q

        #checking acceptance incrementally
        for i, sym in enumerate(sigma_c):
            temp_state = product_dfa.d(temp_state, sym)
            if temp_state is None:
                break
            if product_dfa.F(temp_state):
                #releasing prefix
                released = sigma_c[:i+1]
                sigma_c = []
                q = temp_state
                if debug:
                    return released, sigma_c.copy()
                return released

        return [] if not debug else ([], sigma_c.copy())

    return process_event


################# Least-Effort Parallel Enforcer ########################

class LeastEffortParallelEnforcer:
    """
    Parallel least-effort enforcement:

    - All enforcers see the same input
    - Each tries to release a safe sequence
    - Global output = OR-merge of all safe sequences
    """

    def __init__(self, enforcers):
        self.enforcers = enforcers
        self.n = len(enforcers)

        #current DFA states + candidate buffers
        self.q = [dfa.q0 for dfa in enforcers]
        self.candidate = [[] for _ in enforcers]

        self.output = []

    def process_event(self, a):
        """
        Feed input 'a' to all enforcers in parallel.
        Returns OR-merged safe sequence.
        """
        #appending event to each enforcer's buffer
        for i in range(self.n):
            self.candidate[i].append(a)

        safe_sequences = []

        for i, dfa in enumerate(self.enforcers):
            if dfa.is_safe(self.q[i], self.candidate[i]):
                safe_sequences.append((i, self.candidate[i].copy()))

        #if any enforcer can release
        if safe_sequences:
            released = []

            # OR-merge: maintain order, avoid duplicates
            for idx, seq in safe_sequences:
                for sym in seq:
                    if sym not in released:
                        released.append(sym)

            #appending to global output
            self.output.extend(released)

            #updating DFA states and reset local buffers
            for i in range(self.n):
                self.q[i] = self.enforcers[i].next_state(self.q[i], self.candidate[i])
                self.candidate[i] = []

            return released

        return []  # nothing released

    def get_output(self):
        return self.output
