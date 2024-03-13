import {EventList} from "./interaction/EventList";
import {highlightCommandIntoElement} from "./SyntaxHighlighting/hast-starry-night";

document.addEventListener(EventList.CommandEntered, function (e: CustomEvent): void {
    createPTagWithText(e.detail.text, e.detail.id);
});

export const commandHistoryDisplay: HTMLElement = document.getElementById("commandHistoryDisplay");

function createPTagWithText(text: string, id: number): void {
    const liElement: HTMLLIElement = document.createElement('li');
    liElement.id = `command-${id}`;
    liElement.classList.add('field');
    const container = document.createElement('div');
    liElement.appendChild(container);

    highlightCommandIntoElement(text, container);

    commandHistoryDisplay.appendChild(liElement).scrollIntoView({behavior: "smooth"})
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