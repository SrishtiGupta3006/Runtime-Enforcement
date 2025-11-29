#!/usr/bin/env python3
"""
output_LE_mono.py

Interactive simulation of least-effort OR-product enforcer.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helper.Automata import DFA
from Source.least_effort_mono import least_effort_monolithic_enforcer


# Defining states and transitions ----------------------
states = ['stop', 'start', 'right', 'left', 'forward', 'back']

transition_dict = {
    ('start', 'r'): 'right',
    ('start', 'l'): 'left',
    ('start', 'f'): 'forward',
    ('start', 'b'): 'back',
    ('start', 's'): 'stop',
    
    ('right', 'r'): 'right',
    ('right', 'l'): 'left',
    ('right', 'f'): 'forward',
    ('right', 'b'): 'back',
    ('right', 's'): 'stop',
    
    ('left', 'r'): 'right',
    ('left', 'l'): 'left',
    ('left', 'f'): 'forward',
    ('left', 'b'): 'back',
    ('left', 's'): 'stop',
    
    ('forward', 'r'): 'right',
    ('forward', 'l'): 'left',
    ('forward', 'f'): 'forward',
    ('forward', 'b'): 'back',
    ('forward', 's'): 'stop',
    
    ('back', 'r'): 'right',
    ('back', 'l'): 'left',
    ('back', 'f'): 'forward',
    ('back', 'b'): 'back',
    ('back', 's'): 'stop',
    
    ('stop', 'r'): 'stop',
    ('stop', 'l'): 'stop',
    ('stop', 'f'): 'stop',
    ('stop', 'b'): 'stop',
    ('stop', 's'): 'stop',
    
}

# Define DFAs ----------------------
phi1 = DFA(
    "Property1",
    ['r', 'l', 'f', 'b', 's'],
    states,
    'start',
    lambda q: q in ['right'],               # accepting state
    lambda q, a: transition_dict[(q, a)],
    ['right']
)

phi2 = DFA(
    "Property2",
    ['r', 'l', 'f', 'b', 's'],
    states,
    'start',
    lambda q: q in ['left'],       # accepting state
    lambda q, a: transition_dict[(q, a)],
    ['left']
)

# Least Effort Monolithic Enforcer (OR-Product) ------------------------
enforcer_fn = least_effort_monolithic_enforcer("OR_Product", phi1, phi2)

running_output = []

print("Enter actions one by one (r, l, f, b, s). Type 'end' to finish.\n")

while True:
    action = input("Next action: ").strip().lower()

    if action == "end":
        # Releasing the remaining buffer
        remaining = enforcer_fn(None)
        if remaining:
            running_output.extend(remaining)
        print("\nStopped input. Final output sequence:")
        print(running_output)
        break

    if action not in ['r', 'l', 'f', 'b', 's']:
        print("Invalid action! Please enter r, l, f, b, s or 'end'.")
        continue
    
    released, buffer_snapshot = enforcer_fn(action, debug=True)
    print("Buffer (not yet released):", buffer_snapshot)

    if released:
        running_output.extend(released)

    print("Running output so far:", running_output)
    print("-" * 50)
