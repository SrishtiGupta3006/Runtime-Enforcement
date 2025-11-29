#!/usr/bin/env python3
"""
output_LE_parallel.py

Interactive simulation of Least Effort Parallel Enforcer (OR of all enforcer outputs).
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helper.Automata import DFA
from Source.least_effort_parallel import LeastEffortParallelEnforcer

#  Define states and transitions ----------------------
states = ['stop', 'start', 'right', 'left', 'forward', 'back', 'up', 'down']

transition_dict = {
    ('start', 'r'): 'right',
    ('start', 'l'): 'left',
    ('start', 'f'): 'forward',
    ('start', 'b'): 'back',
    ('start', 'u'): 'up',
    ('start', 'd'): 'down',
    ('start', 's'): 'stop',
    
    ('right', 'r'): 'right',
    ('right', 'l'): 'left',
    ('right', 'f'): 'forward',
    ('right', 'b'): 'back',
    ('right', 'u'): 'up',
    ('right', 'd'): 'down',
    ('right', 's'): 'stop',

    ('left', 'r'): 'right',
    ('left', 'l'): 'left',
    ('left', 'f'): 'forward',
    ('left', 'b'): 'back',
    ('left', 'u'): 'up',
    ('left', 'd'): 'down',
    ('left', 's'): 'stop',
    
    ('forward', 'r'): 'right',
    ('forward', 'l'): 'left',
    ('forward', 'f'): 'forward',
    ('forward', 'b'): 'back',
    ('forward', 'u'): 'up',
    ('forward', 'd'): 'down',
    ('forward', 's'): 'stop',
    
    ('back', 'r'): 'right',
    ('back', 'l'): 'left',
    ('back', 'f'): 'forward',
    ('back', 'b'): 'back',
    ('back', 'u'): 'up',
    ('back', 'd'): 'down',
    ('back', 's'): 'stop',
    
    ('up', 'r'): 'right',
    ('up', 'l'): 'left',
    ('up', 'f'): 'forward',
    ('up', 'b'): 'back',
    ('up', 'u'): 'up',
    ('up', 'd'): 'down',
    ('up', 's'): 'stop',
    
    ('down', 'r'): 'right',
    ('down', 'l'): 'left',
    ('down', 'f'): 'forward',
    ('down', 'b'): 'back',
    ('down', 'u'): 'up',
    ('down', 'd'): 'down',
    ('down', 's'): 'stop',
    
    ('stop', 'r'): 'stop',
    ('stop', 'l'): 'stop',
    ('stop', 'f'): 'stop',
    ('stop', 'b'): 'stop',
    ('stop', 'u'): 'up',
    ('stop', 'd'): 'down',
    ('stop', 's'): 'stop',
}

# DFAs ----------------------

phi1 = DFA(
    "Property1",
    ['r', 'l', 'f', 'b', 's', 'u', 'd'],
    states,
    'start',
    lambda q: q in ['right'],
    lambda q, a: transition_dict[(q, a)],
    ['right']
)

phi2 = DFA(
    "Property2",
    ['r', 'l', 'f', 'b', 's', 'u', 'd'],
    states,
    'start',
    lambda q: q in ['right','left'],
    lambda q, a: transition_dict[(q, a)],
    ['right','left']
)

phi3 = DFA(
    "Property3",
    ['r', 'l', 'f', 'b', 's', 'u', 'd'],
    states,
    'start',
    lambda q: q in ['left','forward'],
    lambda q, a: transition_dict[(q, a)],
    ['left', 'forward']
)

# Least Effort Parallel Enforcer --------------------
enforcers = [phi1, phi2, phi3]
le_parallel_enforcer = LeastEffortParallelEnforcer(enforcers)

print("Enter actions one by one (r, l, f, b, s, u, d). Type 'end' to finish.\n")
running_output = []

while True:
    action = input("Next action: ").strip().lower()

    if action == "end":
        print("\nStopped input. Final output sequence:")
        print(running_output)
        break

    if action not in ['r','l','f','b','s','u','d']:
        print("Invalid action! Please enter r, l, f, b, s, u, d or 'end'.")
        continue

    # Feeding input to all enforcers in parallel and OR their outputs
    released_sequence = le_parallel_enforcer.process_event(action)

    if released_sequence:
        running_output.extend(released_sequence)

    print("Running output so far:", running_output)

    # Printing buffer for each enforcer
    for idx, enforcer in enumerate(le_parallel_enforcer.enforcers):
        print(f"Enforcer {idx+1} buffer:", le_parallel_enforcer.candidate[idx])

    print("-"*50)
