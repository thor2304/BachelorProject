from SocketMessages import CommandMessage
from undo.State import State, StateType


class CommandStates:
    def __init__(self, command: CommandMessage):
        self.user_command = command
        self.states: list[State] = []
        self.is_closed = False
        self.previous_states: dict[StateType, tuple[int, State]] = {}

    def append_state(self, state: State):
        from_index, from_state = self.previous_states[state.state_type]

        if self.is_closed and from_state != state:
            raise ValueError("The states differ after the command has been closed.")

        if len(self.states) == 0:
            self.states.append(state)
            return

        previous_state_representation = (len(self.states) - 1, state)

        if from_state.has_un_collapsible_difference(state):
            self.states.append(state)
            self.previous_states[state.state_type] = previous_state_representation
        elif from_state != state:
            self.states.pop(from_index)
            self.states.append(state)
            self.previous_states[state.state_type] = previous_state_representation

    def close(self):
        self.is_closed = True

    def get_undo_commands(self) -> str:
        output = ""
        for state in reversed(self.states):
            output += state.get_apply_commands()
        return output

    def __str__(self):
        if self.states is None:
            states = "None"
        elif len(self.states) == 0:
            states = "Empty"
        else:
            states = len(self.states)

        return f"User Command: {self.user_command}, number of states: {states}"

    def __repr__(self):
        return self.__str__()
