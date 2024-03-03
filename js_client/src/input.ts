const inputField: HTMLInputElement = <HTMLInputElement> document.getElementById("inputField")
export const commandList: HTMLElement = document.getElementById("commandList");

const commandHistory: string[] = [];
let historyIndex: number = 0;

function getTextFromInput2(): string {
    const text: string = inputField.value.trim();
    inputField.value = '';
    return text;
}

function createPTagWithText2(text: string, id: number): void{
    const liElement: HTMLLIElement = document.createElement('li');
    liElement.id = `command-${id}`;
    liElement.textContent = text;
    liElement.classList.add('field');
    commandList.appendChild(liElement).scrollIntoView({behavior: "smooth"})
}

function saveCommandToHistory(command: string): void {
    if(command != ''){
        commandHistory.push(command);
        historyIndex = commandHistory.length;
    }
}

let current_id: number = 0;
inputField.addEventListener('keydown', function (e: KeyboardEvent): void {
    console.log(commandHistory)
    switch (e.key) {
        case 'Enter':
            const customEvent: CustomEvent<{ text: string }> = new CustomEvent('commandEntered', {
                detail: {
                    text: getTextFromInput2(),
                    id: current_id++,
                },
            });
            e.preventDefault();
            saveCommandToHistory(customEvent.detail.text);
            document.dispatchEvent(customEvent);
            break;
        case 'ArrowUp':
            e.preventDefault();
            if (commandHistory.length > 0) {
                historyIndex = (historyIndex === 0) ? commandHistory.length - 1 : --historyIndex;
                inputField.value = commandHistory[historyIndex];
            }
            break;
        case 'ArrowDown':
            e.preventDefault();
            if (commandHistory.length > 0 && historyIndex < commandHistory.length ) {
                historyIndex = (historyIndex === commandHistory.length - 1) ? 0 : ++historyIndex;
                inputField.value = commandHistory[historyIndex];
            }
            break;
    }
})

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    createPTagWithText2(e.detail.text, e.detail.id);
});