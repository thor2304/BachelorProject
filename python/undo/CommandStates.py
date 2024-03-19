from SocketMessages import CommandMessage
from undo.State import State


class CommandStates:
    def __init__(self, command: CommandMessage):
        self.user_command = command
        self.states: list[State] = []
        self.collapsed = False
        self.collapsed_states: list[State] = []

    def append_state(self, state: State):
        self.states.append(state)

    def collapse(self) -> None:
        self.collapsed = True
        from_state = self.states[0]
        self.collapsed_states = [from_state]
        for to_state in self.states[1:]:
            if from_state.has_un_collapsible_difference(to_state):
                self.collapsed_states.append(to_state)
                from_state = to_state

    def get_undo_commands(self) -> str:
        if not self.collapsed:
            self.collapse()
        output = ""
        for state in reversed(self.collapsed_states):
            output += state.get_apply_commands()
        return output

    def __str__(self):
        states = []
        if self.states is None:
            states = "None"
        return f"User Command: {self.user_command}, States: {states}, Collapsed: {self.collapsed}"

    def __repr__(self):
        return self.__str__()
