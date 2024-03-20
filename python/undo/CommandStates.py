from SocketMessages import CommandMessage
from undo.State import State


class CommandStates:
    def __init__(self, command: CommandMessage):
        self.user_command = command
        self.states: list[State] = []
        self.is_closed = False

    def append_state(self, state: State):
        if self.is_closed and self.states[-1] != state:
            raise ValueError("The states differ after the command has been closed.")

        if len(self.states) == 0:
            self.states.append(state)
            return

        from_state = self.states[-1]
        if from_state.has_un_collapsible_difference(state):
            self.states.append(state)
        else:
            self.states[-1] = state

    def close(self):
        self.is_closed = True

    def get_undo_commands(self) -> str:
        output = ""
        for state in reversed(self.states):
            output += state.get_apply_commands()
        return output

    def __str__(self):
        states = []
        if self.states is None:
            states = "None"
        return f"User Command: {self.user_command}, States: {states}"

    def __repr__(self):
        return self.__str__()
