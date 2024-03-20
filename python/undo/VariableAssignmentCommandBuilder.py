from enum import Enum


class AssignmentStrategies(Enum):
    FUNCTION_CALL = 1
    VARIABLE_ASSIGNMENT = 2


class VariableAssignmentCommandBuilder:
    def __init__(self, command: str, strategy: AssignmentStrategies):
        self.command = command
        self.strategy = strategy

    def build(self, value: str = None) -> str:
        if self.strategy == AssignmentStrategies.FUNCTION_CALL:
            return self._build_function_call(value)
        elif self.strategy == AssignmentStrategies.VARIABLE_ASSIGNMENT:
            return self._build_variable_assignment(value)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def _build_function_call(self, value: str) -> str:
        return f"{self.command}({value})"

    def _build_variable_assignment(self, value: str) -> str:
        return f"{self.command} = {value}"
