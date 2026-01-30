# isoup/patterns.py

from .isoup import ISoup, IRule


def exclusion_patron1():
    states = {"OK", "BAD"}

    def violation(sys_state):
        return sys_state[0] == "CS" and sys_state[1] == "CS"

    rules = [
        IRule("OK", "BAD", violation),
        IRule("OK", "OK", lambda s: not violation(s)),
        IRule("BAD", "BAD", lambda s: True),
    ]

    return ISoup(
        states=states,
        initial="OK",
        bad="BAD",
        rules=rules
    )

def exclusion_patron2():
    states = {"OK", "BAD"}

    def violation(sys_state):
        return sys_state[0] == "CS" and sys_state[1] == "CS"

    rules = [
        IRule("OK", "BAD", violation),
        IRule("OK", "OK", lambda s: not violation(s)),
    ]

    return ISoup(
        states=states,
        initial="OK",
        bad="BAD",
        rules=rules
    )

def deadlock_patron1(is_deadlock):
    states = {"OK", "BAD"}

    rules = [
        IRule("OK", "BAD", is_deadlock),
        IRule("OK", "OK", lambda s: not is_deadlock(s)),
        IRule("BAD", "BAD", lambda s: True),
    ]

    return ISoup(states, "OK", "BAD", rules)
