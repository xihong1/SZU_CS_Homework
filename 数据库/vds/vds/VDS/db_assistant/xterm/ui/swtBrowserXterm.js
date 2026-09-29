var base = new Base64(); 

function pasteWithConvert(content) {

	if (moreflag || browser == 'javafx') {
        return;
    }
    var sel = term.getSelection();
    if (sel != undefined && sel != null && sel.length > 0) {
        paste(sel);
        copyToClipbord(sel);
        enterWithChangLine(content);
        return;
    }
    
    const utf8 = atob(content);  
	content = decodeURIComponent(escape(utf8));  
    
    if (content.length > 0) {
        paste(content);
        enterWithChangLine(content);
    }
}

