from abc import ABC, abstractmethod

from RobotSocketMessages import VariableObject, VariableTypes
from undo.VariableAssignmentCommandBuilder import VariableAssignmentCommandBuilder


class StateVariable(ABC):
    def __init__(self, name: str, is_collapsible: bool = True,
                 command_for_changing: VariableAssignmentCommandBuilder = None):
        self.name = name
        self.is_collapsible = is_collapsible
        self.command_for_changing = command_for_changing

    def __str__(self):
        collapsible = "Collapsible" if self.is_collapsible else "Not Collapsible"
        return self.name + ": " + collapsible + " " + str(self.command_for_changing)


class RtdeStateVariable(StateVariable):
    def __init__(self, name: str, rtde_variable_name: str, is_collapsible: bool = True,
                 command_for_changing: VariableAssignmentCommandBuilder = None):
        super().__init__(name, is_collapsible, command_for_changing)
        self.is_rtde = True
        self.rtde_variable_name = rtde_variable_name


class CodeStateVariable(StateVariable):
    def __init__(self, name: str, command_for_reading: str, is_collapsible: bool = True,
                 command_for_changing: VariableAssignmentCommandBuilder = None):
        super().__init__(name, is_collapsible, command_for_changing)
        self.is_code = True
        self.command_for_reading = command_for_reading
        "This must be the urscript code that is necessary to return a value for this variable."
        # TODO: Correct typing on the variableTypes.string
        self.socket_representation = VariableObject(name, VariableTypes.String, command_for_reading)
