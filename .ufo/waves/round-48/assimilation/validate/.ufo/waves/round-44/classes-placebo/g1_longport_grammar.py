"""Placebo class for the round-44 skip-work control: delegates to the v4 run-F
generator, so the run is real but carries none of the targeted class shapes."""

def cases(rng, h):
    return h.cases_f(rng)
