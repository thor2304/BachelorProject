const inputField: HTMLTextAreaElement = <HTMLTextAreaElement>document.getElementById("inputField")
export const commandList: HTMLElement = document.getElementById("commandList");

interface Command {
    text: string;
    id: number;
}
const commandHistory: Command[] = [];
let historyIndex: number = 0;

function getTextFromInput(): string {
    return inputField.value.trim();
}

function createPTagWithText(text: string, id: number): void {
    const liElement: HTMLLIElement = document.createElement('li');
    liElement.id = `command-${id}`;
    liElement.textContent = text;
    liElement.classList.add('field');
    commandList.appendChild(liElement).scrollIntoView({behavior: "smooth"})
}

function sendCommand(command: string): void {
    if (command === '') return;
    const customEvent: CustomEvent<{ text: string, id: number}> = new CustomEvent('commandEntered', {
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
        const existingIndex: number = commandHistory.findIndex((item: Command): boolean => item.text === command);

        if (existingIndex > -1) {
            commandHistory.splice(existingIndex, 1);
        }

        commandHistory.push({text: command, id: commandId});
        historyIndex = commandHistory.length;
    }
}

function highlightSelectedCommandItem(id: number) {
    const selectedElement: HTMLElement = document.getElementById(`command-${id}`);
    if(selectedElement) {
        selectedElement.classList.add('command-highlighted');
    }
}

function clearHighlightedCommandItems() {
    const highlightedElement: HTMLElement = document.querySelector('.command-highlighted');
    if(highlightedElement) {
        highlightedElement.classList.remove('command-highlighted');
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

let current_id: number = 0;
inputField.addEventListener('keydown', function (e: KeyboardEvent): void {
    clearHighlightedCommandItems();
    switch (e.key) {
        case 'Enter':
            if (e.key === 'Enter' && e.shiftKey) return;
            e.preventDefault();
            sendCommand(getTextFromInput());
            break;
        case 'ArrowUp':
            if (isCursorOnFirstOrLastLine(this, targetDirection.up) || getTextFromInput() === '') {
                e.preventDefault();
                if (commandHistory.length > 0) {
                    historyIndex = (historyIndex === 0) ? commandHistory.length - 1 : --historyIndex;
                    inputField.value = commandHistory[historyIndex].text;
                    highlightSelectedCommandItem(commandHistory[historyIndex].id);
                }
            }
            break;
        case 'ArrowDown':
            if (isCursorOnFirstOrLastLine(this, targetDirection.down) || getTextFromInput() === '') {
                e.preventDefault();
                if (commandHistory.length > 0 && historyIndex < commandHistory.length) {
                    historyIndex = (historyIndex === commandHistory.length - 1) ? 0 : ++historyIndex;
                    inputField.value = commandHistory[historyIndex].text;
                    highlightSelectedCommandItem(commandHistory[historyIndex].id);
                }
            }
            break;
    }
})

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    createPTagWithText(e.detail.text, e.detail.id);
});