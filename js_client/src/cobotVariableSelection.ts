import {RobotStateMessageData} from "./messageHandling/messageDefinitions";

const listId: 'stateVariableSelection' = "stateVariableSelection";
const stateVariableSelectionList: HTMLElement = document.getElementById(listId);

export function generateVariableSelection(data: RobotStateMessageData, handleCheckboxChange: () => void): void {
    if (isVariableSelectionGenerated()) {
        return;
    }

    const fragment: DocumentFragment = document.createDocumentFragment();

    const startLiElement: HTMLLIElement = stateVariableSelectionList.firstElementChild as HTMLLIElement;
    const clonedLiElement: HTMLLIElement = startLiElement.cloneNode(true) as HTMLLIElement;

    Object.entries(data).forEach(([key]): void => {
        const clone: HTMLLIElement = clonedLiElement.cloneNode(true) as HTMLLIElement;
        const label: HTMLLabelElement = clone.querySelector('label');
        const input: HTMLInputElement = clone.querySelector('input');
        label.htmlFor = key;
        label.textContent = key;
        input.id = key;
        input.checked = true;
        input.disabled = false;
        input.addEventListener('change', handleCheckboxChange);
        fragment.appendChild(clone);
    });

    stateVariableSelectionList.replaceChildren(fragment);
}

function getListOfCheckedVariables(listOfNode: NodeListOf<HTMLInputElement>): string[] {
    const checkedVariables: string[] = [];
    listOfNode.forEach((checkbox: HTMLInputElement): void => {
        if (checkbox.checked) {
            checkedVariables.push(checkbox.id);
        }
    });
    return checkedVariables;
}

export function listOfVariablesToDisplay(): string[] {
    const checkboxes: NodeListOf<HTMLInputElement> = stateVariableSelectionList.querySelectorAll('.dropdown-item input[type="checkbox"]');
    return getListOfCheckedVariables(checkboxes);

}

function isVariableSelectionGenerated(): boolean {
    return !stateVariableSelectionList.firstElementChild.isSameNode(stateVariableSelectionList.lastElementChild);
}