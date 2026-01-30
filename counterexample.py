# counterexample.py
"""
Extraction et affichage de contre-exemples pour violations de propriété
"""

def print_counterexample(trace, property_name):
    if trace is None:
        print(f"Property {property_name}: ✅ Satisfait")
        return

    print(f"Property {property_name}: ❌ VIOLÉE")
    print(f"Trace menant à la violation ({len(trace)-1} étapes) :")
    for i, (sys_state, prop_state) in enumerate(trace):
        prefix = "→" if i > 0 else " "
        print(f"{prefix} Step {i}: système={sys_state}, propriété={prop_state}")
    print(f"VIOLATION atteinte !\n")
