import {common, createStarryNight} from '@wooorm/starry-night'
import {toHtml} from 'hast-util-to-html'

import urscript from "./URScript_TextMate"

export async function highlightCommand(command: string, wrap_in_pre: boolean = true): Promise<ChildNode> {
    const starryNight = await createStarryNight(common)
    await starryNight.register([urscript])

    const tree = starryNight.highlight(command, 'source.urscript')


    let htmlString = toHtml(tree)
    if (!(htmlString.toLowerCase().startsWith("<code>") || htmlString.toLowerCase().startsWith("<pre>"))){
        htmlString = `<code>${htmlString}</code>`
        htmlString = wrap_in_pre ? `<pre>${htmlString}</pre>` : htmlString
    }

    return htmlToElement(htmlString)
}

export function highlightCommandIntoElement(command: string, element: HTMLElement): void {
    if (command.startsWith("\n")){
        command = command.substring(1)
    }

    highlightCommand(command).then((highlighted) => {

        element.appendChild(highlighted)
    })
}

/**
 * Starting copied from: https://stackoverflow.com/a/35385518
 *<br>
 * But modified by me, to inject the language class into the code tag.<br>
 * This is done to comply with best practices for accessibility on the web.
 *
 * @param {String} html representing a single element
 * @return {Element}
 */
export function htmlToElement(html: string): ChildNode {
    const template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;

    return template.content.firstElementChild;
}
