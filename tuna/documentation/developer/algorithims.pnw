Metaheuristic Algorithms
========================

These are some of the algorithms behind the optimizers.

Hill Climbing
-------------

Hill climbing is the basis of the single-state algorithms. They are local-optimizers only that can tend to get stuck with non-optimal solutions::

    S = CandidateSolution():
    while S not ideal and timeRemains():
        R = Tweak(Copy(S))
        if Quality(R) > Quality(S):
            S = R
    return S
