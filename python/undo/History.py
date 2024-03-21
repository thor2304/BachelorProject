from typing import Self

from SocketMessages import CommandMessage
from undo.CommandStates import CommandStates
from undo.State import State


class History(object):
    _instance: Self | None = None

    def __init__(self):
        self.command_state_history: dict[int, CommandStates] = {}
        self.active_command_state: CommandStates | None = None

    def get_active_command_state(self) -> CommandStates:
        return self.active_command_state

    def append_state(self, state: State) -> None:
        if self.active_command_state is None:
            print("There is no active command state.")
            return
            # raise ValueError("There is no active command state.")
        self.active_command_state.append_state(state)

    def new_command(self, command: CommandMessage) -> None:
        self.command_state_history[command.get_id()] = CommandStates(command)
        max_id = max(self.command_state_history.keys())
        if max_id != command.get_id():
            raise ValueError(f"The provided command does not have the highest id."
                             f"The highest id is {max_id} and the provided id is {command.get_id()}"
                             f"The command with that id is"
                             f" {self.command_state_history[max_id].user_command.data.command}")
        self.active_command_state = self.command_state_history[command.get_id()]
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
