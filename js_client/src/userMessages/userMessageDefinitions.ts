// This is supposed to be a definitions file, but typescript is not good with enums in definition files.
// This is not intended to house business logic, but to define the message types that the server and client will use.

export enum UserMessageType {
    Command = 'Command',
    Undo = 'Undo'
}

export type UserMessage = CommandMessage | UndoMessage

export type CommandMessageData = {
    id: number,
    command: string,
}

export type UndoMessageData = {
    id: number
}

export type CommandMessage = {
    type: UserMessageType.Command,
    data: CommandMessageData
}

export type UndoMessage = {
    type: UserMessageType.Undo,
    data: UndoMessageData
}
