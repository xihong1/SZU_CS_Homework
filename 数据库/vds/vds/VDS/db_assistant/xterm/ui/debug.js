var paramValues = getParameterByName(window.location.href);
var mockParam = paramValues["mock"];//mock = false

window.onload = function () {

    if (mockParam != "false") {
        term.onKey((e) => {
            allowWrite = true;
        });
        allowWrite = true;
        term.write(prefix);
    }
/*
    document.addEventListener('input', function (e) {
        //printContentPlus2(e.data)
    })*/
};

function mockSendToJava(content) {
    defaultMode = 0;
    if (content == "\\q") {
//        inputCmd_("host='172.16.100.13' port='10902' dbname='vastbase' user='test' sslmode='prefer' sslcompression='False' password='Aa123456'");
        return;
    }
    coverWrite_("this is mock output.");
    waitPrint_(prefix);
}

/*
term.onKey((e) => {

    if (!allowInput()) {
        return;
    }
    if (moreflag) {
        if (e.key == "q" || (e.domEvent.ctrlKey && e.domEvent.keyCode === 67)) {
            endMoreIn();
        } else if (e.domEvent.key === "Enter" || e.key == "\r") {
            readMoreIn();
        }
        return;
    }
    var printable = !e.altKey && !e.ctrlKey && !e.metaKey;
    //刷新状态标识
    refreshStatus(e);

    if (e.domEvent.key === "Enter" || e.key == "\r") {
        // 处理回车键
        enter();
    } else if (e.domEvent.key === "Backspace" || e.key == "\b" || e.domEvent.keyCode == 8) {//可以使用判断逻辑：e.domEvent.keyCode == 8
        // 处理退格键
        back();
    } else if (e.domEvent.keyCode == 37) {//箭头向左
        // 处理向左箭头
        leftArrow(e.key);
    } else if (e.domEvent.keyCode == 39 && e.key != "'") {//箭头向右
        // 处理向右箭头
        rightArrow(e.key);
    } else if (e.domEvent.keyCode == 38) {//箭头向上
        // 处理向上箭头
        upArrow();
    } else if (e.domEvent.keyCode == 40 && e.key != "(") {//箭头向下
        // 处理向下箭头
        downArrow();
    } else if (printable) {
        if(data.charCodeAt(0) > 255){
            return;
        }
        // 处理其他可打印字符
        writePrint(e);
    }
});*/

function refreshStatus(e) {

    var content = e.key;
    if (e.domEvent.key === "Enter" || e.key == "\r") {
        lastIndexCursorX = -1;
        continueChars = "";
        hasChinese = false;
        continueInput = false;
    } else if (e.domEvent.key === "Backspace" || e.key == "\b" || e.domEvent.keyCode == 8) {
        lastIndexCursorX = -1;
        continueChars = "";
        continueInput = false;
    } else if (e.domEvent.keyCode == 37) {
        lastIndexCursorX = -1;
        continueChars = "";
        continueInput = false;
    } else if (e.domEvent.keyCode == 39 && e.key != "'") {
        lastIndexCursorX = -1;
        continueChars = "";
        continueInput = false;
    } else if (e.domEvent.keyCode == 38) {
        lastIndexCursorX = -1;
        continueChars = "";
        continueInput = false;
    } else if (e.domEvent.keyCode == 40 && e.key != "(") {
        lastIndexCursorX = -1;
        continueChars = "";
        continueInput = false;
    } else {
        if (!hasChinese) {
            if (content.charCodeAt(0) > 255) {
                hasChinese = true;
            }
        }
        if (lastIndexCursorX == term.buffer.active.cursorX) {
            continueChars = continueChars + e.key;
        } else {
            lastIndexCursorX = term.buffer.active.cursorX;
            continueChars = e.key;
        }
    }
}


