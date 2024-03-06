const prefix = 'language-'
const rehypePrefix = "highlight-"

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
export function htmlToElement(html: string): ChildNode {
    const template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;

    const output = template.content.firstElementChild;

    let language = getLanguageFromClasslist(output.classList);

    // if no language is found, then we don't want to add the language class
    if(language === "") {
        // console.warn("No language found in classlist", output.classList)
        return output;
    }

    const preElements = Array.from(output.getElementsByTagName("pre"))

    for (const preElement of preElements) {
        const codeElements = Array.from(preElement.getElementsByTagName("code"))
        if (codeElements.length === 0) {
            // console.warn("No code element found in pre element", preElement)
            continue;
        }
        for (const codeElement of codeElements) {
            codeElement.classList.add(prefix + language)
        }
    }

    return output;
}
