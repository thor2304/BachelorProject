import {Message, MessageType, RobotStateMessageData} from "./messageDefinitions";

export function handleRobotStateMessage(message: Message): void {
    if (message.type !== MessageType.RobotState) {
        console.log('not a Robot_state message: ', message);
        return;
    }

    iterateMessageData(message.data);

}

function iterateMessageData(data: any) {
    Object.entries(data).forEach(([key, value]) => {
        if(typeof value === 'object' && !Array.isArray(value) && value !== null) {
            const headline = document.createElement('h3');
            headline.textContent = key;
            document.getElementById('stateVariables').appendChild(headline);
            iterateMessageData(value);
            return;
        }
        generateHtmlFromMessageData(key, value);
    });
}

function generateHtmlFromMessageData(messageDataKey: string, messageDataValue: any) {
    const stateVariableView: HTMLElement = document.getElementById('stateVariables');
    stateVariableView.classList.add('stateVariableView');

    const stateVariableSection: HTMLElement = document.createElement('section');
    stateVariableSection.classList.add('stateVariableSection', 'flex');

    const sectionColumn45: HTMLDivElement = document.createElement('div');
    sectionColumn45.classList.add('column45');

    const sectionColumn55: HTMLDivElement = document.createElement('div');
    sectionColumn55.classList.add('column55');

    const column45Text: HTMLParagraphElement = document.createElement('p');
    column45Text.textContent = messageDataKey;

    const column55Text: HTMLParagraphElement = document.createElement('p');
    column55Text.textContent = messageDataValue;

    sectionColumn45.appendChild(column45Text);
    sectionColumn55.appendChild(column55Text);
    stateVariableSection.appendChild(sectionColumn45);
    stateVariableSection.appendChild(sectionColumn55);
    stateVariableView.appendChild(stateVariableSection);
}