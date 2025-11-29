#######imports########################################
import sys
import os.path

sys.path.append("../")
from pathlib import Path
sourcedir=Path(__file__).resolve().parent.parent.parent
sourcedir=os.path.join(sourcedir, 'Source')
sys.path = [sourcedir] + sys.path

import Enforcer
import helper.Automata as Automata
import copy
import random
import numpy
import time
import pandas as pd 

# Ideal Enforcer -------------------------------

phi = Automata.DFA(
    # Input alphabets
    ['r', 'l', 'f', 's'],
    # states
    ['stop', 'start', 'right', 'left', 'forward', 'dead'],
    'start',
    lambda q: q in ['stop'],
    lambda q, a: {
        # start
        ('start', 'r'): 'right',
        ('start', 'l'): 'left',
        ('start', 'f'): 'forward',
        ('start', 's'): 'stop',
        #right
        ('right', 'r'): 'right',
        ('right', 'l'): 'left',
        ('right', 'f'): 'forward',
        ('right', 's'): 'stop',
        # left
        ('left', 'r'): 'right',
        ('left', 'l'): 'left',
        ('left', 'f'): 'forward',
        ('left', 's'): 'stop',
        #forward
        ('forward', 'r'): 'right',
        ('forward', 'l'): 'left',
        ('forward', 'f'): 'forward',
        ('forward', 's'): 'stop',
        # stop : it's a trap state, any move after this is dead
        ('stop', 'r'): 'dead',
        ('stop', 'l'): 'dead',
        ('stop', 'f'): 'dead',
        ('stop', 's'): 'dead',
        # dead stays dead
	    ('dead', 'r'): 'dead',
        ('dead', 'l'): 'dead',
        ('dead', 'f'): 'dead',
        ('dead', 's'): 'dead',
    }[(q, a)]
)

# Interactive streaming mode
input_list = []
running_output = []

print("Enter actions one by one (r, l, f, s). Type 'end' to finish.\n")

while True:
    action = input("Next action: ").strip().lower()
    
    if action == "end":
        print("Stopped input. Final output sequence:")
        Enforcer.idealenforcer(copy.copy(phi), input_list)
        print("Running output so far:", running_output)
        break

    if action not in ['r', 'l', 'f', 's']:
        print("Invalid action! Please enter r, l, f, s or 'end'.")
        continue

    # Add new action
    input_list.append(action)

    # Run enforcer and capture its result
    output_seq = Enforcer.idealenforcer(copy.copy(phi), input_list)
    if output_seq:  # only add if something is released
        running_output = output_seq  

    # Show current state
    print("Current input sequence:", "".join(input_list))
    print("Running output so far:", running_output)
    print("-" * 50)