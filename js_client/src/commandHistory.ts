import {EventList} from "./interaction/EventList";
import {highlightCommandIntoElement} from "./SyntaxHighlighting/hast-starry-night";
import {getCommandEntry} from "./Toolbox/DomTools";

document.addEventListener(EventList.CommandEntered, function (e: CustomEvent): void {
    createCommandContainer(e.detail.text, e.detail.id);
});

export const commandHistoryDisplay: HTMLElement = document.getElementById("commandHistoryDisplay");

function createCommandContainer(text: string, id: number): void {
    const wrapperElement: HTMLDivElement = document.createElement('div');
    wrapperElement.id = `command-${id}`;
    wrapperElement.classList.add('field', 'flex');

    const idWrapper: HTMLDivElement = document.createElement('div');
    idWrapper.classList.add('idWrapper', 'column10', 'center');

    const contentWrapper: HTMLDivElement = document.createElement('div');
    contentWrapper.classList.add('contentWrapper', 'column70');

    const buttonsWrapper: HTMLDivElement = document.createElement('div');
    buttonsWrapper.classList.add('buttonsWrapper', 'column20', 'center');

    const commandWrapper: HTMLDivElement = document.createElement('div');
    commandWrapper.classList.add('commandWrapper');

    const responseWrapper: HTMLDivElement = document.createElement('div');
    responseWrapper.classList.add('responseWrapper');

    const idText: HTMLParagraphElement = document.createElement('p');
    const undoButton: HTMLButtonElement = document.createElement('button');
    undoButton.onclick = function (): void {
        document.dispatchEvent(new CustomEvent(EventList.UndoEvent, {detail: {id: id}}));
    }


    idText.textContent = id.toString();
    undoButton.textContent = 'Undo up to here';

    idWrapper.appendChild(idText);
    buttonsWrapper.appendChild(undoButton);

    contentWrapper.appendChild(commandWrapper);
    contentWrapper.appendChild(responseWrapper);

    wrapperElement.appendChild(idWrapper);
    wrapperElement.appendChild(contentWrapper);
    wrapperElement.appendChild(buttonsWrapper);

    highlightCommandIntoElement(text, commandWrapper);

    commandHistoryDisplay.appendChild(wrapperElement).scrollIntoView({behavior: "smooth"})
}

export function highlightSelectedCommandItem(id: number): void {
    const selectedElement: HTMLElement = getCommandEntry(id);
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