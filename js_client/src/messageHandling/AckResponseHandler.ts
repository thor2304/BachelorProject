import {Message, MessageType} from "./messageDefinitions";
import {getChildWithClass, getCommandEntry} from "../Toolbox/DomTools";
import {emitCommandFinishedEvent} from "./MessageFinishedHandler";

const errorClass = "error-response"
const successClass = "success-response"

export function handleAckResponseMessage(message: Message): void {
    if (message.type !== MessageType.AckResponse) {
        console.log('not an Ack_response message: ', message);
        return
    }

    const commandWrapper: HTMLElement = getCommandEntry(message.data.id);
    if (!commandWrapper) {
        console.log(`no command with id: ${message.data.id}`, message);
        return
    }
    const contentWrapper: HTMLElement = getChildWithClass(commandWrapper, 'contentWrapper');
    const responseWrapper: HTMLElement = getChildWithClass(contentWrapper, 'responseWrapper');

    const responseParagraph: HTMLParagraphElement = document.createElement('p');
    responseParagraph.classList.add("response");

    const classname = (message.data.status === 'Ok') ? successClass : errorClass
    responseParagraph.classList.add(classname);

    let messageParts = message.data.message.split(':')
    let statusType = messageParts.shift()
    let newMessage = messageParts.join(':')

    statusType = `<span>${statusType}:</span>`
    newMessage = statusType + newMessage

    responseParagraph.innerHTML = newMessage;

    responseWrapper.appendChild(responseParagraph);

    console.log(message);
    
    emitCommandFinishedEvent(message) // For testing purposes. Must be removed later!!
}