import {Message, MessageType, RobotStateMessageData, stateMessageTypes, TCPInformation} from "./messageDefinitions";
import {generateVariableSelection, getListOfCheckedVariables} from "../cobotVariableSelection";
import {emitCommandFinishedEvent} from "./MessageFinishedHandler";

export function handleRobotStateMessage(message: Message): void {
    if (message.type !== MessageType.RobotState) {
        console.log('not a Robot_state message: ', message);
        return;
    }
    iterateMessageData(message.data);
    generateVariableSelection(message.data);
}

function iterateMessageData(data: RobotStateMessageData): void {
    const id: 'stateVariableDisplay' = "stateVariableDisplay"
    const oldStateVariableView: HTMLElement = document.getElementById(id);
    const stateVariableView: HTMLElement = document.createElement('div');
    stateVariableView.id = id;

    const listOfSelectionNodes: NodeListOf<HTMLInputElement> = document.querySelectorAll('.stateVariableSelectionWrapper input');

    Object.entries(data).forEach(([key, value]): void => {
        if(getListOfCheckedVariables(listOfSelectionNodes).includes(key)){
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
    //            const headline: HTMLElement = document.createElement('h3');
    //            headline.textContent = key;
    //            stateVariableView.appendChild(headline);
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

function generateHtmlFromMessageData(messageDataKey: string,
                                     stateVariableView: HTMLElement, messageDataValue:
                                         TCPInformation | number | [number, number, number, number, number, number] | string): void {

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