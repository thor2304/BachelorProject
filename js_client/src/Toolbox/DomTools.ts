export function getChildWithTag(node: HTMLElement, tagName: string): HTMLElement | null {
    const children = node.children;
    for (let i = 0; i < children.length; i++) {
        if (children[i].tagName === tagName) {
            return children[i] as HTMLElement;
        }
    }
    return null;
}


export function getCommandEntry(id: number): HTMLElement | null {
    return document.getElementById(`command-${id}`);
}