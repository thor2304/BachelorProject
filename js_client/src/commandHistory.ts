import {EventList} from "./interaction/EventList";
import {highlightCommandIntoElement} from "./SyntaxHighlighting/hast-starry-night";

document.addEventListener(EventList.CommandEntered, function (e: CustomEvent): void {
    createCommandContainer(e.detail.text, e.detail.id);
});

export const commandHistoryDisplay: HTMLElement = document.getElementById("commandHistoryDisplay");

function createCommandContainer(text: string, id: number): void {
    const wrapperElement: HTMLDivElement = document.createElement('div');
    wrapperElement.id = `command-${id}`;
    wrapperElement.classList.add('field', 'flex');

    const idWrapper: HTMLDivElement = document.createElement('div');
    idWrapper.classList.add('idWrapper');
    const contentWrapper: HTMLDivElement = document.createElement('div');
    contentWrapper.classList.add('contentWrapper');

    const buttonsWrapper: HTMLDivElement = document.createElement('div');
    buttonsWrapper.classList.add('buttonsWrapper');
    const commandWrapper: HTMLDivElement = document.createElement('div');
    commandWrapper.classList.add('commandWrapper');
    const responseWrapper: HTMLDivElement = document.createElement('div');
    responseWrapper.classList.add('responseWrapper');

    const idText: HTMLParagraphElement = document.createElement('p');
    const reverseButton: HTMLButtonElement = document.createElement('button');

    idText.textContent = id.toString();
    reverseButton.textContent = 'Reverse';

    idWrapper.appendChild(idText);
    buttonsWrapper.appendChild(reverseButton);

    contentWrapper.appendChild(commandWrapper);
    contentWrapper.appendChild(responseWrapper);

    wrapperElement.appendChild(idWrapper);
    wrapperElement.appendChild(contentWrapper);
    wrapperElement.appendChild(buttonsWrapper);

    highlightCommandIntoElement(text, commandWrapper);

    commandHistoryDisplay.appendChild(wrapperElement).scrollIntoView({behavior: "smooth"})
}

export function highlightSelectedCommandItem(id: number): void {
    const selectedElement: HTMLElement = document.getElementById(`command-${id}`);
    if (selectedElement) {
        selectedElement.classList.add('command-highlighted');
        selectedElement.scrollIntoView({behavior: "smooth", block: "nearest", inline: "nearest"});
    }
}

export function clearHighlightedCommandItems():void  {
    const highlightedElement: HTMLElement = document.querySelector('.command-highlighted');
    if (highlightedElement) {
        highlightedElement.classList.remove('command-highlighted');
    }
}