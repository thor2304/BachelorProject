const inputField: HTMLInputElement = <HTMLInputElement>document.getElementById("inputField")
export const commandList: HTMLElement = document.getElementById("commandList");

const commandHistory: string[] = [];
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
    const customEvent: CustomEvent<{ text: string }> = new CustomEvent('commandEntered', {
        detail: {
            text: command,
            id: current_id++,
        },
    });
    inputField.value = '';
    saveCommandToHistory(command);
    document.dispatchEvent(customEvent);
}

function saveCommandToHistory(command: string): void {
    if (command != '') {
        const existingIndex: number = commandHistory.indexOf(command);

        if (existingIndex > -1) {
            commandHistory.splice(existingIndex, 1);
        }

        commandHistory.push(command);
        historyIndex = commandHistory.length;
    }
}

enum targetDirection {
    up = 'up',
    down = 'down',
}

function isCursorOnLine(textarea: HTMLInputElement, direction: targetDirection): boolean {
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
    switch (e.key) {
        case 'Enter':
            if (e.key === 'Enter' && e.shiftKey) return;
            e.preventDefault();
            sendCommand(getTextFromInput());
            break;
        case 'ArrowUp':
            if (isCursorOnLine(this, targetDirection.up) || getTextFromInput() === '') {
                e.preventDefault();
                if (commandHistory.length > 0) {
                    historyIndex = (historyIndex === 0) ? commandHistory.length - 1 : --historyIndex;
                    inputField.value = commandHistory[historyIndex];
                }
            }
            break;
        case 'ArrowDown':
            if (isCursorOnLine(this, targetDirection.down) || getTextFromInput() === '') {
                e.preventDefault();
                if (commandHistory.length > 0 && historyIndex < commandHistory.length) {
                    historyIndex = (historyIndex === commandHistory.length - 1) ? 0 : ++historyIndex;
                    inputField.value = commandHistory[historyIndex];
                }
            }
            break;
    }
})

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    createPTagWithText(e.detail.text, e.detail.id);
});