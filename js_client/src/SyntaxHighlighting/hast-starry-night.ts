import {common, createStarryNight} from '@wooorm/starry-night'
import {toHtml} from 'hast-util-to-html'
import {htmlToElement} from "./HighlightHistory";

import urscript from "./URScript_TextMate"

export async function highlightCommand(command: string): Promise<ChildNode> {
    const starryNight = await createStarryNight(common)
    await starryNight.register([urscript])

    const tree = starryNight.highlight(command, 'source.urscript')
    console.log(tree, toHtml(tree))

    let htmlString = toHtml(tree)
    if (!htmlString.toLowerCase().startsWith("<code>")){
        htmlString = `<code>${htmlString}</code>`
    }

    return htmlToElement(htmlString)
}

export function highlightCommandIntoElement(command: string, element: HTMLElement): void {
    if (command.startsWith("\n")){
        command = command.substring(1)
    }

    highlightCommand(command).then((highlighted) => {
        console.log(highlighted)
        element.appendChild(highlighted)
    })
}