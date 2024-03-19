import {generateVariableSelection, listOfVariablesToDisplay} from "../cobotVariableSelection";
import {
    ResponseMessage,
    ResponseMessageType,
    RobotStateMessage,
    RobotStateMessageData, stateMessageTypes
} from "./responseMessageDefinitions";


let lastRobotStateMessage: RobotStateMessage;

export function handleRobotStateMessage(message: ResponseMessage): void {
    if (message.type !== ResponseMessageType.RobotState) {
        console.log('not a Robot_state message: ', message);
        return;
    }

    lastRobotStateMessage = message;

    generateVariableSelection(message.data, replayRobotStateMessage);
    iterateMessageData(message.data);
}

function replayRobotStateMessage(): void {
    if (lastRobotStateMessage) {
        handleRobotStateMessage(lastRobotStateMessage);
    }
}

function iterateMessageData(data: RobotStateMessageData): void {
    const id: 'stateVariableDisplay' = "stateVariableDisplay"
    const oldStateVariableView: HTMLElement = document.getElementById(id);
    const stateVariableView: HTMLElement = document.createElement('div');
    stateVariableView.id = id;

    Object.entries(data).forEach(([key, value]): void => {
        if (listOfVariablesToDisplay().includes(key)) {
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                Object.entries(value).forEach(([innerKey, innerValue]): void => {
                    generateHtmlFromMessageData(innerKey, stateVariableView, innerValue);
                });
                return;
            }
            generateHtmlFromMessageData(key, stateVariableView, value);
        }
    });

    if (oldStateVariableView) {
        oldStateVariableView.replaceWith(stateVariableView);
    } else {
        document.getElementById('stateVariables').appendChild(stateVariableView);
    }
}

function generateHtmlFromMessageData(messageDataKey: string, stateVariableView: HTMLElement, messageDataValue: stateMessageTypes): void {

    const stateVariableSection: HTMLElement = document.createElement('section');
    stateVariableSection.classList.add('stateVariableSection', 'flex');

    const sectionColumn45: HTMLDivElement = document.createElement('div');
    sectionColumn45.classList.add('column45');

    const sectionColumn55: HTMLDivElement = document.createElement('div');
    sectionColumn55.classList.add('column55');

    const column45Text: HTMLParagraphElement = document.createElement('p');
    column45Text.textContent = messageDataKey;

    const column55Text: HTMLParagraphElement = document.createElement('p');
    column55Text.textContent = prettyPrint(messageDataValue);

    sectionColumn45.appendChild(column45Text);
    sectionColumn55.appendChild(column55Text);
    stateVariableSection.appendChild(sectionColumn45);
    stateVariableSection.appendChild(sectionColumn55);
    stateVariableView.appendChild(stateVariableSection);
}

function prettyPrint(information: stateMessageTypes): string {
    if (typeof information === 'string') {
        return information;
    }
    if (typeof information === 'number') {
        return information.toString();
    }
    if (Array.isArray(information)) {
        return information.join(', ');
    }
    if (typeof information === 'object') {
        return JSON.stringify(information);
    }
}