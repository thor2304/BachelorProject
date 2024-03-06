import {highlightCommandIntoElement} from "./SyntaxHighlighting/hast-starry-night";
const inputField: HTMLTextAreaElement = <HTMLTextAreaElement>document.getElementById("inputField")
export const commandList: HTMLElement = document.getElementById("commandList");

let current_id: number = 0;

interface Command {
    text: string;
    id: number;
}

const commandInputHistory: Command[] = [];
let historyIndex: number = 0;

function getTextFromInput(): string {
    return inputField.value.trim();
}

function createPTagWithText(text: string, id: number): void {
    const liElement: HTMLLIElement = document.createElement('li');
    liElement.id = `command-${id}`;
    // liElement.textContent = text;
    liElement.classList.add('field');

    highlightCommandIntoElement(text, liElement);

    commandList.appendChild(liElement).scrollIntoView({behavior: "smooth"})
}

function sendCommand(command: string): void {
    if (command === '') return;
    const customEvent: CustomEvent<{ text: string, id: number }> = new CustomEvent('commandEntered', {
        detail: {
            text: command,
            id: current_id++,
        },
    });
    inputField.value = '';
    saveCommandToHistory(command, customEvent.detail.id);
    document.dispatchEvent(customEvent);
}

function saveCommandToHistory(command: string, commandId: number): void {
    if (command != '') {
        const existingIndex: number = commandInputHistory.findIndex((item: Command): boolean => item.text === command);

        if (existingIndex > -1) {
            commandInputHistory.splice(existingIndex, 1);
        }

        commandInputHistory.push({text: command, id: commandId});
        historyIndex = commandInputHistory.length;
    }
}

enum targetDirection {
    up = 'up',
    down = 'down',
}

function isCursorOnFirstOrLastLine(textarea: HTMLTextAreaElement, direction: targetDirection): boolean {
    const cursorPos: number = textarea.selectionStart;
    const selectionEnd: number = textarea.selectionEnd;
    const selectionStart: number = textarea.selectionStart;

    if (selectionStart !== selectionEnd) {
        return false;
    }

    const firstNewLine: number = textarea.value.indexOf('\n');
    const lastNewLine: number = textarea.value.lastIndexOf('\n');

    if ((cursorPos <= firstNewLine || firstNewLine < 0) && direction === targetDirection.up) {
        return true;
    }

    if (cursorPos > lastNewLine && direction === targetDirection.down) {
        return true;
    }

    return false;
}

function inputHistoryNavigation(direction: targetDirection): boolean {
    if (commandInputHistory.length > 0) {
        if (direction === targetDirection.up) {
            historyIndex = (historyIndex === 0) ? commandInputHistory.length - 1 : --historyIndex;
            inputField.value = commandInputHistory[historyIndex].text;
            return true;
        }
        if (direction === targetDirection.down && historyIndex < commandInputHistory.length) {
            historyIndex = (historyIndex === commandInputHistory.length - 1) ? 0 : ++historyIndex;
            inputField.value = commandInputHistory[historyIndex].text;
            return true;
        }
        return false;
    }
    return false;
}

function highlightSelectedCommandItem(id: number) {
    const selectedElement: HTMLElement = document.getElementById(`command-${id}`);
    if (selectedElement) {
        selectedElement.classList.add('command-highlighted');
    }
}

function clearHighlightedCommandItems() {
    const highlightedElement: HTMLElement = document.querySelector('.command-highlighted');
    if (highlightedElement) {
        highlightedElement.classList.remove('command-highlighted');
    }
}

function handleArrowPresses(textArea: HTMLTextAreaElement, e: KeyboardEvent, direction: targetDirection): void {
    if (isCursorOnFirstOrLastLine(textArea, direction) || getTextFromInput() === '') {
        e.preventDefault();
        if (inputHistoryNavigation(direction)) {
            highlightSelectedCommandItem(commandInputHistory[historyIndex].id);
        }
    }
}

inputField.addEventListener('keydown', function (e: KeyboardEvent): void {
    clearHighlightedCommandItems();
    switch (e.key) {
        case 'Enter':
            if (e.key === 'Enter' && e.shiftKey) return;
            e.preventDefault();
            sendCommand(getTextFromInput());
            break;
        case 'ArrowUp':
            handleArrowPresses(this, e, targetDirection.up);
            break;
        case 'ArrowDown':
            handleArrowPresses(this, e, targetDirection.down);
            break;
    }
})

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    createPTagWithText(e.detail.text, e.detail.id);
});