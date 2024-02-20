const inputField: HTMLInputElement = <HTMLInputElement> document.getElementById("inputField")
export const commandList: HTMLElement = document.getElementById("commandList");

function getTextFromInput2(): string {
    const text: string = inputField.value;
    inputField.value = '';
    return text;
}

function createPTagWithText2(text: string): void{
    const liElement: HTMLLIElement = document.createElement('li');
    liElement.textContent = text;
    commandList.appendChild(liElement).scrollIntoView({behavior: "smooth"})
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