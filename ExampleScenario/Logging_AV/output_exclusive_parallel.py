# output_exclusive_parallel.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Source')))

from exclusive_parallel import ExclusiveParallelEnforcer
from exclusive_mono import A1_mod, A2_mod


enf = ExclusiveParallelEnforcer([A1_mod, A2_mod])

print("Interactive Exclusive Parallel Enforcer")
print("Enter events one by one (valid: f, o, l, n). Type 'exit' to stop.\n")

final_output = ""   # accumulated global output

# interactive loop 

while True:
    a = input("Enter event: ").strip()

    # exit condition
    if a.lower() in ["exit", "quit", "q"]:
        print("Stopping...")
        break

    # only accept one of the standard events
    if a not in ['f', 'o', 'l', 'n']:
        print("Invalid event! Only f, o, l, n are allowed.")
        continue

    out, debug = enf.step(a)

    for info in debug:
        print(
            f"Enforcer {info['enforcer']} → "
            f"state={info['state']}, "
            f"σc={info['σc']}, "
            f"σs={info['σs']}"
        )

    emitted_string = ''.join(out)

    # appending to global final output
    final_output += emitted_string

    if emitted_string != "":
        print(f"Emitted Output: {out}  -> string: '{emitted_string}'")

    print(f"Final Output so far: '{final_output}'\n")
