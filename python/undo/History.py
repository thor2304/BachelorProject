from typing import Self

from SocketMessages import CommandMessage
from undo.CommandStates import CommandStates


class History(object):
    _instance: Self | None = None

    def __init__(self):
        self.command_state_history: dict[int, CommandStates] = {}
        self.highest_id = 0

    def active_command_state(self) -> CommandStates:
        return self.command_state_history[self.get_highest_id()]

    def get_highest_id(self) -> int:
        return self.highest_id

    def new_command(self, command: CommandMessage) -> None:
        self.command_state_history[command.get_id()] = CommandStates(command)
        self.highest_id = max(self.command_state_history.keys())
        if self.highest_id != command.get_id():
            raise ValueError(f"The provided command does not have the highest id."
                             f"The highest id is {self.highest_id} and the provided id is {command.get_id()}"
                             f"The command with that id is"
                             f" {self.command_state_history[self.highest_id].user_command.data.command}")
        print(f"New command added to history: {command.get_id()} length: {len(self.command_state_history)}")

    def debug_print(self) -> None:
        debug_string = f"History: length={len(self.command_state_history)}\n"
        for key, value in self.command_state_history.items():
            debug_string += f"\tKey: {key}, Value: {value}\n"
        print(debug_string)

    @classmethod
    def get_history(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
