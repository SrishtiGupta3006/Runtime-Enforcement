# output_exclusive_mono.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../source")))

from helper.product import product
from exclusive_mono import A1_mod, A2_mod


# Building the Exclusive Monolithic Product DFA

print("\n --- Exclusive Monolithic Product DFA ---")

# AND-product of the modified DFAs A1′ and A2′
A_and = product(A1_mod, A2_mod, 'Exclusive Product')

print(f"\nInitial state: {A_and.q0}")
print(f"Total states: {len(A_and.Q)}")

print("\nAccepting states:")
for q in A_and.Q:
    if A_and.F(q):
        print(" ", q)

# Interactive Simulation

print("\n--- Interactive Simulation ---")
print("Enter events one by one (valid: f, l, o, n). Type 'exit' to stop.\n")

state = A_and.q0

while True:
    a = input("Event: ").strip()

    # Exit condition
    if a == "exit":
        print("Exiting simulation.")
        break

    # Symbol validation
    if a not in A_and.S:
        print("Invalid event.")
        continue

    # Computing next state
    next_state = A_and.d(state, a)
    if next_state is None:
        print(f"No transition from {state} on {a}.")
        break

    print(f"{state} --{a}--> {next_state}")
    state = next_state

print(f"\nFinal state: {state}")
print("Accepted" if A_and.F(state) else "Rejected")
