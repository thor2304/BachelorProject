import {Message, MessageType, RobotStateMessageData, stateMessageTypes, TCPInformation} from "./messageDefinitions";

let counter = 0;

export function handleRobotStateMessage(message: Message): void {
    if (message.type !== MessageType.RobotState) {
        console.log('not a Robot_state message: ', message);
        return;
    }
    console.log('Robot_state message: ', message, counter++);

    iterateMessageData(message.data);
}

function iterateMessageData(data: RobotStateMessageData) {
    const id = "stateVariableDisplay"
    const oldStateVariableView: HTMLElement = document.getElementById(id);
    const stateVariableView: HTMLElement = document.createElement('div');
    stateVariableView.id = id;

    Object.entries(data).forEach(([key, value]) => {
        generateHtmlFromMessageData(key,stateVariableView, value);

    });

    if (oldStateVariableView) {
        oldStateVariableView.replaceWith(stateVariableView);
    } else {
        document.getElementById('stateVariables').appendChild(stateVariableView);
    }
}

function generateHtmlFromMessageData(messageDataKey: string,
                                     stateVariableView: HTMLElement, messageDataValue:
    TCPInformation | number | [number, number, number, number, number, number] | string) {
    const headline = document.createElement('h3');
    headline.textContent = messageDataKey;

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
    stateVariableSection.appendChild(headline);
    stateVariableSection.appendChild(sectionColumn45);
    stateVariableSection.appendChild(sectionColumn55);
    stateVariableView.appendChild(stateVariableSection);
}

function prettyPrint(information: stateMessageTypes) : string{
    if (typeof information === 'string'){
        return information;
    }
    if (typeof information === 'number'){
        return information.toString();
    }
    if (Array.isArray(information)){
        return information.join(', ');
    }
    if (typeof information === 'object'){
        return JSON.stringify(information);
    }
}