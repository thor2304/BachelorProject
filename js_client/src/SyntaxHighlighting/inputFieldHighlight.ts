import {getTextFromInput, inputField} from '../input';
import {highlightCommand, highlightCommandIntoElement} from "./hast-starry-night";

const display: HTMLDivElement  = <HTMLDivElement>document.getElementById('syntax-display');

inputField.addEventListener('input', () => {
    highlightCommand(getTextFromInput(), false).then((highlighted) => {
        if (display.firstChild) {
            display.replaceChild(highlighted,display.children[0]);
        }else{
            display.appendChild(highlighted);
        }
    })
});

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    if (display.firstChild) {
        const empty = document.createElement("p")
        display.replaceChild(empty,display.children[0]);
    }
});