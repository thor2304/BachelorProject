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

    def generate_read_commands(self) -> list[str]:
        output_list = []
        for variable in self._code_variables:
            if variable.is_code:
                output = variable.command_for_reading
                output += "\n"
                output_list.append(output)
            else:
                raise ValueError("Variable in code list is not a code variable")
        return output_list
