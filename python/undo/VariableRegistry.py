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

    def get_rtde_variables(self) -> list[RtdeStateVariable]:
        return self._rtde_variables


def register_all_code_variables(in_registry: VariableRegistry):
    variables = [
        CodeStateVariable("test", "test"),
        CodeStateVariable("test2", "test2")
    ]

    for variable in variables:
        in_registry.register_code_variable(variable)


def register_all_rtde_variables(in_registry: VariableRegistry):
    variables = [
        RtdeStateVariable("safety status", "safety_status"),
        RtdeStateVariable("runtime state", "runtime_state"),
        RtdeStateVariable("robot mode", "robot_mode"),
        RtdeStateVariable("joints", "joints"),
        RtdeStateVariable("tcp", "tcp"),
        RtdeStateVariable("payload", "payload"),
    ]

    for variable in variables:
        in_registry.register_rtde_variable(variable)
