from undo.StateVariable import StateVariable


class StateValue:
    def __init__(self, value, variable_definition: StateVariable):
        self.value = value
        self.variable_definition = variable_definition

    def get_apply_command(self) -> str:
        return self.variable_definition.command_for_changing.build(self.value)

    def __str__(self):
        return "{" + f"{self.variable_definition.name}: {self.value}" + "}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, StateValue):
            return False
        return self.value == other.value and self.variable_definition == other.variable_definition
