import {EventList} from "./EventList";
import {inputField} from "./InputField";

document.addEventListener(EventList.CommandEntered, function (e: CustomEvent): void {
    lockInputField();
})

document.addEventListener(EventList.CommandFinished, function (e: CustomEvent): void {
    console.log('command finished event received from document', e.detail);
    unlockInputField();
})

function lockInputField(): void {
    inputField.classList.add(lockedClass);
}

function unlockInputField(): void {
    inputField.classList.remove(lockedClass);
}

export function inputFieldIsLocked(): boolean {
    return inputField.classList.contains(lockedClass);
}

export const lockedClass = "locked"

export function indicateToUserThatFieldIsLocked(): void {
    console.log('field is locked');
}
