// This is supposed to be a definitions file, but typescript is not good with enums in definition files.
// This is not intended to house business logic, but to define the message types that the server and client will use.

export enum MessageType {
    Command = 'Command',
    AckResponse = 'Ack_response',
    Feedback = 'Feedback',
    RobotState = 'Robot_state',
    CommandFinished = 'Command_finished',
    Undo = 'Undo',
    UndoResponse = 'Undo_response'
}

export enum Status {
    Ok = 'Ok',
    Error = 'Error'
}

export enum UndoStatus {
    Error = 'Error',
    Success = 'Success',
    CommandDidNotExist = 'CommandDidNotExist',
    CommandAlreadyUndone = 'CommandAlreadyUndone'
}

export type Message = CommandMessage | UndoMessage | AckResponseMessage | FeedbackMessage | RobotStateMessage | CommandFinishedMessage | UndoResponseMessage

export type UndoResponseMessageData = {
    id: number,
    status: UndoStatus,
}

export type CommandMessageData = {
    id: number,
    command: string,
}

export type UndoMessageData = {
    id: number
}

export type AckResponseMessageData = {
    id: number,
    status: Status,
    command: string,
    message: string
}

export type FeedbackMessageData = {
    id: number,
    message: string
}

export type RobotStateMessageData = {
    safety_status: string,
    runtime_state: string,
    robot_mode: string,
    joints: [number, number, number, number, number, number],
    tcp: {
        pose: [number, number, number, number, number, number],
        speed: [number, number, number, number, number, number],
        force: [number, number, number, number, number, number]
    },
    payload: number
}

export type StringedVariableTypes = 'string' | 'number' | 'boolean' | 'number[]'
export type VariableTypes = string | number | boolean | number[]

export type CommandFinishedVariable = {
    name: string,
    type: StringedVariableTypes,
    value: VariableTypes
}

export type CommandFinishedMessageData = {
    id: number,
    command: string,
    variables: CommandFinishedVariable[]
}

export type CommandMessage = {
    type: MessageType.Command,
    data: CommandMessageData
}

export type UndoResponseMessage = {
    type: MessageType.UndoResponse,
    data: UndoResponseMessageData
}

export type UndoMessage = {
    type: MessageType.Undo,
    data: UndoMessageData
}

export type AckResponseMessage = {
    type: MessageType.AckResponse,
    data: AckResponseMessageData
}

export type FeedbackMessage = {
    type: MessageType.Feedback,
    data: FeedbackMessageData
}

export type RobotStateMessage = {
    type: MessageType.RobotState,
    data: RobotStateMessageData
}

export type CommandFinishedMessage = {
    type: MessageType.CommandFinished,
    data: CommandFinishedMessageData
}
