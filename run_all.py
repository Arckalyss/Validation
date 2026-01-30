# run_all.py
"""
Exécution reproductible pour tous les modèles AB1–AB5
et vérification des propriétés P1 et P2.
"""

from ab_models_soup import get_model
from properties_isoup import P1, P2
from verify_nfa import verify_property
from counterexample import print_counterexample

def main():
    models = ["AB1", "AB2", "AB3", "AB4", "AB5"]

    for name in models:
        print(f"\n=== Vérification pour {name} ===")
        model_semantics = get_model(name)

        # Propriété 1 : Mutual exclusion
        prop1 = P1()
        trace1 = verify_property(model_semantics, prop1)
        print_counterexample(trace1, "P1 (Mutual Exclusion)")

        # Propriété 2 : Deadlock freedom
        prop2 = P2(model_semantics)
        trace2 = verify_property(model_semantics, prop2)
        print_counterexample(trace2, "P2 (Deadlock Freedom)")

if __name__ == "__main__":
    main()
