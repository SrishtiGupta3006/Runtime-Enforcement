# ExclusiveParallelEnforcer.py

import sys
import os

# Import modified DFAs from same folder
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from helper.Automata import DFA


# Helper DFA functions

def dfa_run(dfa, q, word):
    for a in word:
        q = dfa.d(q, a)
    return q


def dfa_accepts(dfa, q, word):

    q_end = dfa_run(dfa, q, word)
    return dfa.F(q_end), q_end


def exclusive_enforcer_step_single(dfa, q, sigma_c, sigma_s, a):

    q_new = dfa.d(q, a)

    candidate = sigma_c + [a]
    full_candidate = sigma_s + candidate

    accepts, _ = dfa_accepts(dfa, q, full_candidate)

    if accepts:
        new_sigma_s = sigma_s + candidate
        return q_new, [], new_sigma_s

    else:
        return q_new, sigma_c + [a], sigma_s


# Parallel Exclusive Enforcer

class ExclusiveParallelEnforcer:

    def __init__(self, dfa_list):
        self.dfas = dfa_list
        self.n = len(dfa_list)

        self.q = [dfa.q0 for dfa in dfa_list]

        # σc_i buffers
        self.sigma_c = [[] for _ in range(self.n)]

        # σs_i buffers
        self.sigma_s = [[] for _ in range(self.n)]

    def reset(self):

        self.q = [dfa.q0 for dfa in self.dfas]
        self.sigma_c = [[] for _ in range(self.n)]
        self.sigma_s = [[] for _ in range(self.n)]

    def step(self, a):

        if a == "":
            debug_info = []
            for i in range(self.n):
                debug_info.append({
                    "enforcer": i + 1,
                    "σc": list(self.sigma_c[i]),
                    "σs": list(self.sigma_s[i]),
                    "state": self.q[i],
                })
        else:
            debug_info = []

            for i in range(self.n):
                dfa = self.dfas[i]
                qi = self.q[i]
                buf = self.sigma_c[i]
                old_sigma_s = self.sigma_s[i]

                qi_new, buf_new, sigma_s_new = exclusive_enforcer_step_single(dfa, qi, buf, old_sigma_s, a)

                # updating stored values
                self.q[i] = qi_new
                self.sigma_c[i] = buf_new
                self.sigma_s[i] = sigma_s_new

                debug_info.append({
                    "enforcer": i + 1,
                    "σc": list(buf_new),
                    "σs": list(sigma_s_new),
                    "state": qi_new,
                })

        flag = False
        sigma_s_global = self.sigma_s[0]

        for i in range(1, self.n):
            if self.sigma_s[i] != sigma_s_global:
                flag = True
                break

        if not flag:
            output = list(sigma_s_global)

            for i in range(self.n):
                self.sigma_s[i] = []

        else:
            output = []

        return output, debug_info
    
    def enforce(self, input_word):

        out = []
        for a in input_word:
            emitted, _ = self.step(a)
            if emitted:
                out.extend(emitted)
        return out
