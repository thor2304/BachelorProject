from typing import Self

from SocketMessages import CommandMessage
from undo.CommandStates import CommandStates


class History(object):
    _instance: Self | None = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(History, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.command_state_history: dict[int, CommandStates] = {}

    def active_command_state(self) -> CommandStates:
        return self.command_state_history[self.get_highest_id()]

    def get_highest_id(self) -> int:
        return max(self.command_state_history.keys())

    def new_command(self, command: CommandMessage) -> None:
        self.command_state_history[command.get_id()] = CommandStates(command)

    def debug_print(self) -> None:
        debug_string = "History: \n"
        for key, value in self.command_state_history.items():
            debug_string += f"\tKey: {key}, Value: {value}\n"
        print(debug_string)

    @classmethod
    def get_history(cls) -> Self:
        """Returns a singleton history instance"""
        return cls._instance
