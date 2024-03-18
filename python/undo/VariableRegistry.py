from RobotSocketMessages import VariableObject
from undo.StateVariable import CodeStateVariable, RtdeStateVariable


class VariableRegistry:
    def __init__(self):
        self._code_variables: list[CodeStateVariable] = []
        self._rtde_variables: list[RtdeStateVariable] = []

    def register_code_variable(self, variable: CodeStateVariable) -> None:
        self._code_variables.append(variable)

    def register_rtde_variable(self, variable: RtdeStateVariable) -> None:
        self._rtde_variables.append(variable)
        # and some handling of how to enable rtde listening for this variable

    def generate_read_commands(self) -> list[VariableObject]:
        output_list = []
        for variable in self._code_variables:
            if variable.is_code:
                output_list.append(variable.socket_representation)
            else:
                raise ValueError("Variable in code list is not a code variable")
        return output_list

    def get_code_variables(self) -> list[CodeStateVariable]:
        return self._code_variables
