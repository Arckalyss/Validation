from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class StutteringAction:
    """Action spéciale : le système ne bouge pas."""
    @staticmethod
    def instance() -> "StutteringAction":
        return StutteringAction()

@dataclass(frozen=True)
class Step:
    """Un pas d'exécution : source --action--> target"""
    source: object
    action: object
    target: object
