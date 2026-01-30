# common/step.py
class Step:
    def __init__(self, source, action, target):
        self.source = source
        self.action = action
        self.target = target

    def __repr__(self):
        return f"({self.source}) -[{self.action}]-> ({self.target})"


class StutteringAction:
    _instance = None

    @staticmethod
    def instance():
        if StutteringAction._instance is None:
            StutteringAction._instance = StutteringAction()
        return StutteringAction._instance

    def __repr__(self):
        return "τ"
