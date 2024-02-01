const inputField = document.getElementById("inputField");
const commandArea = document.getElementById("commandArea");

function getTextFromInput() {
    const text = inputField.value;
    inputField.value = '';
    return text;
}

function createPTagWithText(text){
    const pTag = document.createElement('p');
    pTag.textContent = text;
    commandArea.appendChild(pTag)
}

inputField.addEventListener('keypress', function (e) {
    if(e.key === 'Enter') {
        const customEvent = new CustomEvent('commandEntered', {
            detail: {
                text: getTextFromInput()
            },
        });
        document.dispatchEvent(customEvent);
    }
})

document.addEventListener('commandEntered', function (e) {
    createPTagWithText(e.detail.text);
});
