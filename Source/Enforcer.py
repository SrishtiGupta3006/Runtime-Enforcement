## imports ########################################################################################
import helper.Automata as Automata
import collections
import itertools
from itertools import islice
import time

#### Function to pre-compute emptiness check for each state in the given automaton ###############
def computeEmptinessDict(autC):
    dictEnf = {}
    for state in autC.Q:
        autC.makeInit(state)
        if autC.isEmpty():
            dictEnf[state] = True
        else:
            dictEnf[state] = False
    return dictEnf

#### Function to compute substring of sigmaC by removing smallest cycle in sigmaC ###############
def computes_substring(iterable, n, automata, k):
    cleanedBuffer = []
    automata.reset(k)
    p1 = k
    for i in range(len(iterable) - n):
        element = list(islice(iterable[i:], 0, 1 + n, 1))
        for j in range(n + 1):
            p2 = automata.step1(element[j])
            if j == 0:
                p3 = p2
        if p2 == p1:
            cleanedBuffer.extend(iterable[i + n + 1:])
            return [n + 1, cleanedBuffer]
        else:
            cleanedBuffer.append(element[0])
        p1 = p3
        automata.makeInit(p3)
        automata.reset(p1)

#### Function returning cleaned sigmaC #########################################################
def clean(sigmaC, phiautomata, maxBuffer, k, event):
    yn = None
    for i in range(len(sigmaC)):
        if yn is None:
            yn = computes_substring(list(sigmaC), i, phiautomata, k)
            if i == 0 and yn is None:
                for t in sigmaC:
                    q_q = phiautomata.d(k, t)
                if phiautomata.d(q_q, event) == q_q:
                    return sigmaC
    if yn is not None:
        yn = yn[1:]
        yn = list(itertools.chain(*yn))
        yn.append(event)
        return yn

#### Bounded Memory Enforcer function ###########################################################
def enforcer(phi, sigma, maxBuffer):
    if maxBuffer < len(phi.Q):
            print(f"Warning: maxBuffer {maxBuffer} smaller than DFA states {len(phi.Q)}, continuing anyway")

    global estart, eend, y, sum
    y = 0
    sum = 0
    sigmaC = collections.deque([], maxlen=maxBuffer)
    sigmaS = []
    q = phi.q0
    dictEnf = computeEmptinessDict(phi)
    phi.q0 = q
    m = q
    estart = time.time()

    for event in sigma:
        t = q
        q = phi.d(q, event)
        Final = phi.F(q)
        if Final:
            for a in sigmaC:
                sigmaS.append(a)
            sigmaS.append(event)
            sigmaC = []
            t = q
        else:
            if dictEnf[q]:
                q = t
            else:
                t = q
                clean_start = time.time()
                if len(sigmaC) >= maxBuffer:
                    phi.q0 = m
                    k = phi.q0
                    for t in sigmaS:
                        k = phi.d(k, t)
                    y += 1
                    sigmaC1 = clean(sigmaC, phi, maxBuffer, k, event)
                    if sigmaC1 == 100:
                        break
                    else:
                        sigmaC = sigmaC1
                    clean_end = time.time()
                    sum += clean_end - clean_start
                else:
                    sigmaC.append(event)
    eend = time.time()
    print("output sequence is " + str(sigmaS))

#### Ideal Enforcer function ####################################################################
def idealenforcer(phi, sigma):
    global istart, iend
    isigmaC = []
    isigmaS = []
    ip = phi.q0
    dictEnf = computeEmptinessDict(phi)
    istart = time.time()

    for event in sigma:
        a = ip
        ip = phi.step1(event)
        Final = phi.F(ip)
        if Final:
            a = ip

        if Final:
            for item in isigmaC:
                isigmaS.append(item)
            isigmaS.append(event)
            isigmaC = []
        else:
            if dictEnf[ip]:
                ip = a
            else:
                isigmaC.append(event)
                a = ip

    iend = time.time()
    print("output sequence is " + str(isigmaS))
    return isigmaS
