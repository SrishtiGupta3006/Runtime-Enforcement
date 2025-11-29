#!/usr/bin/env python3
"""
strict_serial.py

Strict serial composition (serial_enforcer)
extracted from CompositionalEnforcer.py.

Logic is unchanged.
"""

import sys
sys.path.append("..")

from Enforcer import enforcer


def serial_enforcer(name, *D):
    """
    Enforce DFAs sequentially:
        Input → DFA1 → DFA2 → DFA3 → ... → DFAn

    Returns both the final output and intermediate outputs.

    Logic identical to original CompositionalEnforcer.serial_enforcer.
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


# Optional alias:
def strict_serial(name, *D):
    """
    Wrapper alias: strict_serial ≡ serial_enforcer
    """
    return serial_enforcer(name, *D)
