import {Message, MessageType} from "./messageDefinitions";
import {getChildWithTag} from "../Toolbox/DomTools";

export function handleAckResponseMessage(message: Message): void {
    if (message.type !== MessageType.AckResponse) {
        console.log('not an Ack_response message: ', message);
        return
    }

    const liElement = document.getElementById(`command-${message.data.id}`);
    if (!liElement) {
        console.log(`no command with id: ${message.data.id}`, message);
        return
    }

    let subList = getChildWithTag(liElement, 'ul');
    if (!subList) {
        subList = document.createElement('ul');
        // move styling to css
        subList.style.listStyleType = 'none';
        subList.style.padding = '.25em';
    }
    const subListItem = document.createElement('li');

    // Move styling to css
    subListItem.style.backgroundColor = (message.data.status === 'Ok') ? 'green' : 'red';
    subListItem.textContent = message.data.message;
    subListItem.style.padding = '.25em';

    subList.appendChild(subListItem);

    liElement.appendChild(subList);

    console.log(message);
}