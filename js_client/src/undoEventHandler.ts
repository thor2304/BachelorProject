import {EventList} from "./interaction/EventList";
import {getCommandEntry} from "./Toolbox/DomTools";


document.addEventListener(EventList.UndoEvent, function (e: CustomEvent): void {
    markCommandElementsWithUndo(e.detail.id);
});


function markCommandElementsWithUndo(id: number): void {
    let running = true;
    while (running) {
        const element = getCommandEntry(id++)
        if (element) {
            element.classList.add('undone');
        } else {
            running = false;
        }
    }
}


