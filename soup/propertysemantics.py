from abc import ABC, abstractmethod


class PropertySemantics(ABC):
    """
    Sémantique d’un langage de propriétés.

    Une propriété est modélisée comme un automate :
    - elle a des états internes (prop_state),
    - elle observe les pas d'exécution du système (Step),
    - elle évolue en fonction de ces pas.

    Elle est utilisée dans une composition synchrone
    avec une sémantique système (StepSynchronousProduct).
    """

    @abstractmethod
    def initials(self):
        """
        Retourne la liste des états initiaux de la propriété.
        Exemple : ["OK"]
        """
        pass

    @abstractmethod
    def actions(self, step, prop_state):
        """
        Retourne les actions de la propriété autorisées
        lors de l’observation du pas `step`.

        step  : objet Step (source, action, target)
        prop_state : état courant de la propriété

        En pratique, pour une propriété déterministe simple,
        on retourne souvent une liste à un seul élément :
            ["tick"]
        """
        pass

    @abstractmethod
    def execute(self, prop_action, step, prop_state):
        """
        Applique l’action de la propriété et retourne
        le nouvel état de la propriété.

        prop_action : une action retournée par actions()
        step        : le pas d’exécution observé
        prop_state  : état courant de la propriété
        """
        pass

    def is_accepting(self, prop_state) -> bool:
        """
        Indique si l’état de propriété est acceptant.

        Par défaut : aucun état n’est acceptant.
        Les propriétés de sûreté surchargent cette méthode
        pour signaler un état BAD.
        """
        return False
