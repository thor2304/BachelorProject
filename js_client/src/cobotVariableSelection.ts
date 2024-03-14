import {RobotStateMessageData} from "./messageHandling/messageDefinitions";

document.addEventListener('click', (event: MouseEvent): void => {
    const stateVariablePopup: HTMLElement = document.getElementById('stateVariablePopup');
    if (stateVariablePopup && stateVariablePopup.classList.contains('hidden')) {
        stateVariablePopup.classList.remove('hidden');
    } else {
        stateVariablePopup.classList.add('hidden');
    }
});

export function generateVariableSelection(data: RobotStateMessageData): void {
    const id: 'cobotStateVariablesSelectionDisplay' = "cobotStateVariablesSelectionDisplay"
    const oldStateVariableSelection: HTMLElement = document.getElementById(id);
    const stateVariableSelection: HTMLElement = document.createElement('div');
    const headline: HTMLHeadingElement = document.createElement('h3');
    stateVariableSelection.id = id;

    headline.textContent = 'Select State Variables';
    stateVariableSelection.appendChild(headline);


    Object.entries(data).forEach(([key]): void => {
        const variableInputWrapper: HTMLDivElement = document.createElement('div');
        variableInputWrapper.classList.add('stateVariableSelectionWrapper');
        const variableInputLabel: HTMLLabelElement = document.createElement('label');
        const variableInput: HTMLInputElement = document.createElement('input');

        variableInputLabel.textContent = key;
        variableInputLabel.htmlFor = key;

        variableInput.type = 'checkbox';
        variableInput.checked = true;
        variableInput.id = key;
        variableInput.name = key;
        variableInput.classList.add('Checkbox');

        variableInputWrapper.appendChild(variableInput);
        variableInputWrapper.appendChild(variableInputLabel);
        stateVariableSelection.appendChild(variableInputWrapper);
    });


    if (!oldStateVariableSelection) {
        document.getElementById('stateVariablePopup').appendChild(stateVariableSelection);
    }
}

export function getListOfCheckedVariables(listOfNode: NodeListOf<HTMLInputElement>): string[] {
    const checkedVariables: string[] = [];
    listOfNode.forEach((checkbox: HTMLInputElement): void => {
        if (checkbox.checked) {
            checkedVariables.push(checkbox.id);
        }
    });
    return checkedVariables;
}