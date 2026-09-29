window.addEventListener('contextmenu', event => {
    event.preventDefault();
});

function enterWithChangLine(copyContent) {
    if (/\r|\n/.test(copyContent)) {
        triggerEnter(copyContent);
    }
}

window.addEventListener('mousedown', event => {

    event.preventDefault();
    if (event.button === 2) {
        if (moreflag || browser == 'javafx') {
            return;
        }
        var sel = term.getSelection();
        if (sel == "" || sel == undefined) {
            var pasteContent = getPasteContent();
            if (pasteContent == "" || pasteContent == undefined) {
                return;
            }
            paste(pasteContent);
            enterWithChangLine(pasteContent);
            return;
        } else {
            paste(sel);
            copyToClipbord(sel);
            enterWithChangLine(content);
            return;
        }
    }
});







