import {unified} from 'https://esm.sh/unified@10.1.2?bundle'
import remarkParse from "https://esm.sh/remark-parse@10.0.2?bundle"
import remarkRehype from "https://esm.sh/remark-rehype@10.1.0?bundle"
import rehypeStringify from 'https://esm.sh/rehype-stringify@9.0.3?bundle'
import rehypeStarryNight from "https://esm.sh/@microflash/rehype-starry-night@2.1.0?bundle"

import urscript from "./URScript_TextMate"

const prefix = 'language-'
const rehypePrefix = "highlight-"

export async function renderMarkDownToHTML(markdown: string): Promise<ChildNode> {
    const file = await unified()
        .use(remarkParse)
        .use(remarkRehype, {allowDangerousHtml: true})
        .use(rehypeStarryNight, {aliases: {script: "urscript"}, grammars: [urscript]})
        .use(rehypeStringify, {allowDangerousHtml: true})
        .process(markdown).catch((error: Error) => {
            console.error(error, markdown)
        })

    return htmlToElement(String(file))
}

function getLanguageFromClasslist(classlist: DOMTokenList) {

    let language = "";

    const list = Array.from(classlist);

    for (const classIn of list) {
        if (classIn.startsWith(rehypePrefix)) {
            language = classIn.substring(rehypePrefix.length)
            break;
        }
    }
    return language;
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
function htmlToElement(html: string): ChildNode {
    const template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;

    const output = template.content.firstElementChild;


    let language = getLanguageFromClasslist(output.classList);

    // if no language is found, then we don't want to add the language class
    if(language === "") {
        console.warn("No language found in classlist", output.classList)
        return output;
    }

    const preElements = Array.from(output.getElementsByTagName("pre"))

    for (const preElement of preElements) {
        const codeElements = Array.from(preElement.getElementsByTagName("code"))
        if (codeElements.length === 0) {
            console.warn("No code element found in pre element", preElement)
            continue;
        }
        for (const codeElement of codeElements) {
            codeElement.classList.add(prefix + language)
        }
    }

    return output;
}

export function highlightCommand(command: string): string {
    return renderMarkDownToHTML("```urscript\n" + command + "\n```");
}