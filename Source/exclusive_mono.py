# ExclusiveMonoEnforcer.py

from helper.Automata import DFA
from Enforcer import enforcer


def modify_for_exclusive(orig_dfa, own_deciding, other_deciding):


    # Copying original states and create don't-care versions
    Q_new = orig_dfa.Q.copy()
    qX_map = {}  # mapping: original q  → don't-care state qX

    # Prefix: 'q' for A1 states, 'p' for A2 states
    prefix = orig_dfa.Q[0][0]

    # Building don't-care states: prefix + sequential index

    next_index = len(orig_dfa.Q)
    for q in orig_dfa.Q:
        new_state = f"{prefix}{next_index}"
        qX_map[q] = new_state
        Q_new.append(new_state)
        next_index += 1

    # Modified accepting condition 
    F_new = lambda q: (
        orig_dfa.F(q) or
        (q.startswith(prefix) and int(q[len(prefix):]) >= len(orig_dfa.Q))
    )

    d_orig = orig_dfa.d  # original transition function

    # Modified transition function for A′
    
    def d_new(q, a):
        # Case 1: q is a don't-care state
        if q in qX_map.values():
            orig = next(k for k, v in qX_map.items() if v == q)

            # Own deciding event - resume original transition
            if a in own_deciding:
                return d_orig(orig, a)

            # Otherwise remain in don't-care state
            return q

        # Case 2: q is an original state
        else:
            # if event belongs to other DFA's deciding events → enter don't-care
            if a in other_deciding:
                return qX_map[q]

            # Otherwise follow normal transition
            return d_orig(q, a)

    # Building modified DFA
    return DFA(
        S=orig_dfa.S,
        Q=Q_new,
        q0=orig_dfa.q0,
        F=F_new,
        d=d_new,
        e=orig_dfa.e
    )


# ORIGINAL DFAs: A1, A2 ###############################

# DFA A1 (for first enforcer)
def d1(q, a):
    transitions = {
        "q0": {"f": "q1", "l": "q0", "o": "q0", "n": "q0"},
        "q1": {"l": "q2", "f": "q1", "o": "q1", "n": "q1"},
        "q2": {"f": "q1", "l": "q0", "o": "q2", "n": "q0"},
    }
    return transitions[q].get(a, None)

F1 = lambda q: q == "q2"
A1 = DFA(S={"f", "l", "o", "n"}, Q=["q0", "q1", "q2"], q0="q0", F=F1, d=d1)
A1.name = "A1"


# DFA A2 (for second enforcer)
def d2(q, a):
    transitions = {
        "p0": {"o": "p1", "f": "p0", "l": "p0", "n": "p0"},
        "p1": {"n": "p2", "f": "p1", "l": "p1", "o": "p1"},
        "p2": {"f": "p2", "l": "p0", "o": "p1", "n": "p0"},
    }
    return transitions[q].get(a, None)

F2 = lambda q: q == "p2"
A2 = DFA(S={"f", "l", "o", "n"}, Q=["p0", "p1", "p2"], q0="p0", F=F2, d=d2)
A2.name = "A2"


# Modified A1′ and A2′#############################################

Σ_e1 = {"f"}   # A1’s deciding events
Σ_e2 = {"o"}   # A2’s deciding events (blocks A1)

A1_mod = modify_for_exclusive(A1, Σ_e1, Σ_e2)
A2_mod = modify_for_exclusive(A2, Σ_e2, Σ_e1)

__all__ = ["A1_mod", "A2_mod"]
