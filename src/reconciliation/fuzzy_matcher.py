from .reconciliation_engine import reconcile

def fuzzy_match(sources, config=None):
    return reconcile(sources, config)
