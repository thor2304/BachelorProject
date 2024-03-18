import {RobotStateMessageData} from "./messageHandling/messageDefinitions";
import {iterateMessageData, savedRobotStateMessage} from "./messageHandling/RobotStateMessageHandler";

const listId: 'stateVariableSelection' = "stateVariableSelection";
const stateVariableSelectionList: HTMLElement = document.getElementById(listId);

export function generateVariableSelection(data: RobotStateMessageData): void {
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
        input.addEventListener('change', checkboxChanged);
        fragment.appendChild(clone);
    });

    if(!isVariableSelectionGenerated()){
        stateVariableSelectionList.replaceChildren(fragment);
        return;
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

function isVariableSelectionGenerated(): boolean {
    return !stateVariableSelectionList.firstElementChild.isSameNode(stateVariableSelectionList.lastElementChild);
}

function checkboxChanged(): void {
    iterateMessageData(savedRobotStateMessage.data);
}