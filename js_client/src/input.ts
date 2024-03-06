import {highlightCommandIntoElement} from "./SyntaxHighlighting/hast-starry-night";

const inputField: HTMLInputElement = <HTMLInputElement> document.getElementById("inputField")
export const commandList: HTMLElement = document.getElementById("commandList");

function getTextFromInput2(): string {
    const text: string = inputField.value;
    inputField.value = '';
    return text;
}

function createPTagWithText2(text: string, id: number): void{
    const liElement: HTMLLIElement = document.createElement('li');
    liElement.id = `command-${id}`;
    // liElement.textContent = text;
    liElement.classList.add('field');

    highlightCommandIntoElement(text, liElement);

    commandList.appendChild(liElement).scrollIntoView({behavior: "smooth"})
}

let current_id: number = 0;
inputField.addEventListener('keypress', function (e: KeyboardEvent): void {
    if(e.key === 'Enter') {
        const customEvent: CustomEvent<{ text: string }> = new CustomEvent('commandEntered', {
            detail: {
                text: getTextFromInput2(),
                id: current_id++,
            },
        });
        document.dispatchEvent(customEvent);
    }
})

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    createPTagWithText2(e.detail.text, e.detail.id);
});