import {EventList} from "./interaction/EventList";
import {inputField} from "./interaction/InputField";
import {indicateToUserThatFieldIsLocked, inputFieldIsLocked} from "./interaction/lock_input_field";
import {clearHighlightedCommandItems, highlightSelectedCommandItem} from "./commandHistory";

let current_id: number = 0;

interface Command {
    text: string;
    id: number;
}

const commandInputHistory: Command[] = [];
let historyIndex: number = 0;

export function getTextFromInput(): string {
    return inputField.value.trim();
}

function sendCommand(command: string): void {
    if (command === '') return;
    const customEvent: CustomEvent<{ text: string, id: number }> = new CustomEvent(EventList.CommandEntered, {
        detail: {
            text: command,
            id: current_id++,
        },
    });
    inputField.value = '';
    saveCommandToInputHistory(command, customEvent.detail.id);
    document.dispatchEvent(customEvent);
}

function saveCommandToInputHistory(command: string, commandId: number): void {
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
            if (e.shiftKey) return;
            e.preventDefault();
            if (inputFieldIsLocked() && !e.ctrlKey) {
                indicateToUserThatFieldIsLocked()
                break;
            }
            sendCommand(getTextFromInput());
            break;
        case 'ArrowUp':
            handleArrowPresses(this, e, targetDirection.up);
            break;
        case 'ArrowDown':
            handleArrowPresses(this, e, targetDirection.down);
            break;
        case "1":
            if (e.ctrlKey) {
                e.preventDefault();
                sendCommand("movej([0, -1.57, 1.57, 0, 1.57, 0], a=1.0, v=1)");
            }
            break;
        case "2":
            if (e.ctrlKey) {
                e.preventDefault();
                sendCommand("movej([1.57, 0, 0, 1, 0, 1], a=1.0, v=1)");
            }
            break;
    }
})
