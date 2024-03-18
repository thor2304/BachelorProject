from undo.StateVariable import StateVariable


class StateValue:
    def __init__(self, value, variable: StateVariable):
        self.value = value
        self.variable = variable

    def get_apply_command(self) -> str:
        return self.variable.command_for_changing.build(self.value)

    def __str__(self):
        return f"{self.variable}: {self.value}"
