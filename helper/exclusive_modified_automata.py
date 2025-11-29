# ExclusiveModifiedAutomata.py

import sys
import os
import io
from contextlib import redirect_stdout

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Source')))

from exclusive_mono import A1_mod, A2_mod
from Enforcer import enforcer

input_trace = ['f', 'o', 'f', 'o', 'l', 'n']

# Helper to capture printed output
def trace_enforcer(dfa, input_trace):
    current_state = dfa.q0
    print(f"Initial state: {current_state}")
    output = []
    for a in input_trace:
        next_state = dfa.d(current_state, a)
        output.append(a)
        print(f"Input: {a}, Current State: {current_state} -> Next State: {next_state}")
        current_state = next_state
    print("Output sequence:", output)


# Run for A1_mod
print("Tracing A1_mod:")
trace_enforcer(A1_mod, input_trace)

# Run for A2_mod
print("\nTracing A2_mod:")
trace_enforcer(A2_mod, input_trace)
