import {Message, MessageType} from "./messageDefinitions";
import {getChildWithTag} from "../Toolbox/DomTools";
import {emitCommandFinishedEvent} from "./MessageFinishedHandler";

const errorClass = "error-response"
const successClass = "success-response"

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
        subList.classList.add("response-list")
    }
    const subListItem = document.createElement('li');

    // Move styling to css
    subListItem.classList.add("response");
    const classname = (message.data.status === 'Ok') ? successClass : errorClass
    subListItem.classList.add(classname);
    subListItem.textContent = message.data.message;

    subList.appendChild(subListItem);

    liElement.appendChild(subList);

    console.log(message);
    
    emitCommandFinishedEvent(message) // For testing purposes. Must be removed later!!
}