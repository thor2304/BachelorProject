const inputField: HTMLInputElement = <HTMLInputElement> document.getElementById("inputField")
const commandArea: HTMLElement = document.getElementById("commandArea");

function getTextFromInput2(): string {
    const text: string = inputField.value;
    inputField.value = '';
    return text;
}

function createPTagWithText2(text: string): void{
    const pTag: HTMLParagraphElement = document.createElement('p');
    pTag.textContent = text;
    commandArea.appendChild(pTag)
}

inputField.addEventListener('keypress', function (e: KeyboardEvent): void {
    if(e.key === 'Enter') {
        const customEvent: CustomEvent<{ text: string }> = new CustomEvent('commandEntered', {
            detail: {
                text: getTextFromInput2()
            },
        });
        document.dispatchEvent(customEvent);
    }
})

document.addEventListener('commandEntered', function (e: CustomEvent): void {
    createPTagWithText2(e.detail.text);
});
