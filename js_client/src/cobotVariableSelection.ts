import {RobotStateMessageData} from "./messageHandling/messageDefinitions";

const listId: 'stateVariableSelection' = "stateVariableSelection";
const stateVariableSelectionList: HTMLElement = document.getElementById(listId);

const checkboxes: NodeListOf<HTMLInputElement> = stateVariableSelectionList.querySelectorAll('.dropdown-item input[type="checkbox"]');

export function generateVariableSelection(data: RobotStateMessageData, callback: () => void): void {
    if (isVariableSelectionGenerated()) {
        return;
    }

    const fragment: DocumentFragment = document.createDocumentFragment();

    const startLiElement: HTMLLIElement = stateVariableSelectionList.firstElementChild as HTMLLIElement;
    const clonedLiElement: HTMLLIElement = startLiElement.cloneNode(true) as HTMLLIElement;

    const handleChange = (): void  => {
        callback();
    };

    Object.entries(data).forEach(([key]): void => {
        const clone: HTMLLIElement = clonedLiElement.cloneNode(true) as HTMLLIElement;
        const label: HTMLLabelElement = clone.querySelector('label');
        const input: HTMLInputElement = clone.querySelector('input');
        label.htmlFor = key;
        label.textContent = key;
        input.id = key;
        input.checked = true;
        input.disabled = false;
        input.addEventListener('change', handleChange);
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
    return getListOfCheckedVariables(checkboxes);

}

function isVariableSelectionGenerated(): boolean {
    return !stateVariableSelectionList.firstElementChild.isSameNode(stateVariableSelectionList.lastElementChild);
}