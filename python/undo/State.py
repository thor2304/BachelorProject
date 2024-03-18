from typing import Self

from undo.StateValue import StateValue


class State:
    def __init__(self, state: list[StateValue] = None):
        self.state = state

    def __str__(self):
        return self.state

    def __repr__(self):
        return self.__str__()

    def get_apply_commands(self) -> str:
        output = ""
        for state_value in self.state:
            output += state_value.get_apply_command()
            output += "\n"
        return output

    def has_un_collapsible_difference(self, other: Self) -> bool:
        # Sort variables by name or reference to their StateVariable
        for self_state, other_state in zip(self.state, other.state):
            if self_state.variable.is_collapsible:
                continue
            if self_state.value != other_state.value:
                return True
        return False