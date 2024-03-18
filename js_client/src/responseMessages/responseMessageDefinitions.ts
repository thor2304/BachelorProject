// This is supposed to be a definitions file, but typescript is not good with enums in definition files.
// This is not intended to house business logic, but to define the message types that the server and client will use.

export enum ResponseMessageType {
    AckResponse = 'Ack_response',
    Feedback = 'Feedback',
    RobotState = 'Robot_state',
    CommandFinished = 'Command_finished',
    UndoResponse = 'Undo_response'
}

export enum Status {
    Ok = 'Ok',
    Error = 'Error'
}

export enum UndoStatus {
    Success = 'Success',
    Error = 'Error',
    CommandDidNotExist = 'CommandDidNotExist',
    CommandAlreadyUndone = 'CommandAlreadyUndone'
}

export type ResponseMessage = AckResponseMessage | FeedbackMessage | RobotStateMessage | CommandFinishedMessage | UndoResponseMessage

export type UndoResponseMessageData = {
    id: number,
    status: UndoStatus,
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

export type TCPInformation = {
    pose: [number, number, number, number, number, number],
    speed: [number, number, number, number, number, number],
    force: [number, number, number, number, number, number]
}

export type RobotStateMessageData = {
    safety_status: string,
    runtime_state: string,
    robot_mode: string,
    joints: [number, number, number, number, number, number],
    tcp: TCPInformation,
    payload: number
}

export type stateMessageTypes = string | number | [number, number, number, number, number, number] | TCPInformation


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

export type UndoResponseMessage = {
    type: ResponseMessageType.UndoResponse,
    data: UndoResponseMessageData
}

export type AckResponseMessage = {
    type: ResponseMessageType.AckResponse,
    data: AckResponseMessageData
}

export type FeedbackMessage = {
    type: ResponseMessageType.Feedback,
    data: FeedbackMessageData
}

export type RobotStateMessage = {
    type: ResponseMessageType.RobotState,
    data: RobotStateMessageData
}

export type CommandFinishedMessage = {
    type: ResponseMessageType.CommandFinished,
    data: CommandFinishedMessageData
}
