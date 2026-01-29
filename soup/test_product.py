from alicebob_langagesemantics import AB1LanguageSemantics
from stepsynchronousproduct import StepSynchronousProduct

# adapte l'import selon ton nom de fichier : alice_bobproperty.py / alice_bobproperty etc.
from alice_bobproperty import MutualExclusionProperty, DeadlockProperty

def dump_some_successors(sem, n=10):
    roots = sem.initials()
    print("roots =", roots)

    s0 = roots[0]
    acts = sem.actions(s0)
    print("actions(s0) =", acts[:n], " total=", len(acts))

    for a in acts[:n]:
        ns = sem.execute(s0, a)
        print("  action =", a)
        print("  next   =", ns)

if __name__ == "__main__":
    sys_sem = AB1LanguageSemantics()

    # Produit avec une propriété (peu importe laquelle pour ce test)
    prop = MutualExclusionProperty()
    prod = StepSynchronousProduct(sys_sem, prop)

    dump_some_successors(prod, n=6)
