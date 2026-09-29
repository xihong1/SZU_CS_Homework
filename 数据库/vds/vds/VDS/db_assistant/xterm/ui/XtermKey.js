var lines = "";
var linesBeforeUpdate = "";
var startY = -1;
var linecount = 1;
var hasChinese = false;
var debounceArr = new Array();

term.onData((data) => {

    if (!allowInput()) {
        return;
    }
    if (passwordGuideFlag) {
        collectionPW(data);
        return;
    }

    if (moreflag) {
        if (data == "q" || data == '\u0003') {
            endMoreIn();
        } else if (data == "\r") {
            readMoreIn();
        }
        return;
    } else if (!moreflag && data == '\u0003') {
        resetEnter();
    }

    //输入防抖处理
    data = inputEnglishDebounce(data);
    //linux环境中文输入防抖
    if (browser == 'swt' && data.charCodeAt(0) > 255) {
        inputChinesDebounce(data);
        return;
    }

    //刷新状态标识
    refreshFlagStatus(data);

    if (data === '\r') {
        // 处理回车键
        enter();
    } else if (data === '\x7F' || data === '\u0008') {
        // 处理退格键
        back();
    } else if (data === '\u001b[D') {
        // 处理向左箭头
        leftArrow(data);
    } else if (data === '\u001b[C') {
        // 处理向右箭头
        rightArrow(data);
    } else if (data === '\u001b[A') {
        // 处理向上箭头
        upArrow();
    } else if (data === '\u001b[B') {
        // 处理向下箭头
        downArrow();
    } else {
        // 处理其他可打印字符
        writePrintToTerm(data);
    }
});

var lastDebounceInput = "";
var lastDebounceInputX = "";

//英文字符防抖
function inputEnglishDebounce(data) {

    if (browser != 'swt') {
        return data;
    }

    if (data === '\r' || data === '\x7F' || data === '\u0008' || data === '\u001b[D' || data === '\u001b[C' || data === '\u001b[A' || data === '\u001b[B') {
        return data;
    }

    if (data.charCodeAt(0) > 255 && data.length > 1) {
        var reg = new RegExp("[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\uff01\u3010\u3011\uffe5]+", "g");
        if (reg.test(data.slice(-1)) || data.slice(-1).trim().length == 0) {
            data = data.slice(-1);
        }
    }

    if (data.indexOf(" ") > -1 && data.length > 1) {
        data = data.slice(-1);
    }

    if (lastDebounceInputX == term.buffer.active.cursorX) {
        if (data.indexOf(lastDebounceInput) > -1) {
            return "";
        }
    } else {
        lastDebounceInputX = term.buffer.active.cursorX
    }

    if (data.length > 1 && lastDebounceInput.length > 0) {
        if (data.indexOf(lastDebounceInput) > -1) {
            data = data.slice(-1);
        }
        lastDebounceInput = data;
    } else {
        lastDebounceInput = data;
    }

    if (data.charCodeAt(0) > 255) {
        lastDebounceInputX = term.buffer.active.cursorX
        return data;
    }

    return data;
}

function inputChinesDebounce(data) {

    debounceArr.unshift(data)
    setTimeout(() => {
        while (debounceArr.length > 1) {
            if (debounceArr.length > 1) {
                debounceArr.pop();
            }
        }
        if (debounceArr.length == 0) {
            return;
        }
        var data_ = debounceArr.pop();
        refreshFlagStatus(data_);
        writePrintToTerm(data_);
    }, 100);
}

/**
 * 输入：回车
 */
function enter() {
    // 处理回车键
    allowWrite = false;
    term.write("\r\n");
    curMaxX = prefix.length;
    term.refresh(0, 0);
    currentLine = getEnterLIne(term);
    clearLine();
    if (mock) {
        mockSendToJava(currentLine);
    } else {
        sendToJava(currentLine);
    }
    charInMiddle = false;
}

function resetEnter() {
    if (allowWrite) {
        term.write("\r\n");
        term.write('\r\x1B[K'); // 将光标移到行首并清空该行
        waitPrint_(prefix);
        curMaxX = prefix.length;
        currentLine = getEnterLIne(term);
        clearLine();
        charInMiddle = false;
    }
}

/**
 * 输入退格
 */
function back() {
    cursorX = term.buffer.active.cursorX;
    var inlinenum = inline(term, lines);
    var deletelast = false;
    var isChinesBefore = false;
    if (cursorX == 0 && !charInMiddle) {
        var cursorY = term.buffer.active.cursorY;
        term.write("\x1b[" + ((cursorY)) + ";" + (termCols + 1) + "H");
        deletelast = true;
    }
    if (inlinenum == 1 && cursorX <= getLength(prefix) && !deletelast) {
        return;
    }
    if (lines.length == 0) {
        return;
    }
    //遇到中文需要两个退格键
    if (hasChinese) {
        isChinesBefore = ifChineseBeforeChar(cursorX, lines);
    }
    var result = refreshLine(getInsertLineParam("", charInMiddle, 8, term.buffer.active.cursorX, getCurrentCursorY()));
    // 处理退格键
    if (deletelast) {
        term.write('\x1b[K');
    } else {
        term.write("\b \b");
    }
    if (isChinesBefore) {
        term.write("\b \b");
    }
    if (curMaxX > prefix.length) {
        curMaxX = curMaxX - 1;
    }
    cmds = cmds.slice(0, -1);
    if (charInMiddle) {
        writeInMiddle(term, "\b \b", 8, result);
    }
}

function leftArrow(keycontent) {

    cursorX = term.buffer.active.cursorX;
    if (lines.length <= prefix.length) {
        return;
    }
    if (cursorX <= getLength(prefix)) {
        var cursorY = getCurrentCursorY();
        var linecontent = getLine(cursorY);
        if (linecontent.startsWith(prefix)) {
            if (cursorX < getLength(prefix)) {
                rightArrow("\u001b[C");
            }
            return;
        }
        if (getLength(lines) < termCols) {
            return;
        }
    }
    if (cursorX == 0) {
        term.write("\x1b[" + (term.buffer.active.cursorY) + ";" + termCols + "H");
    } else {
        term.write(keycontent);
        if (hasChinese && isInChineseChar(lines, cursorX, "", true, false)) {//中文占两个字符
            term.write(keycontent);
        }
    }
    charInMiddle = true;
}

function rightArrow(keycontent) {

    var inlineNum = inline(term, lines);
    cursorX = term.buffer.active.cursorX;
    if (charInMiddle) {
        if (cursorX >= getcurlineMaxX()) {
            charInMiddle = false;
        }
    }
    var hasnext = true;
    if (startY == -1) {
        if (cursorX + 1 >= getLength(lines)) {
            hasnext = false;
        }
    } else {
        var x = (inlineNum - 1) * termCols + cursorX;
        if (x == getLength(lines) - 1) {
            charInMiddle = false;
        }
        if (x >= getLength(lines)) {
            hasnext = false;
        }
    }
    if (!hasnext) {
        charInMiddle = false;
        return;
    }
    if (cursorX == termCols - 1) {
        //光标进入下一行
        term.write("\x1b[" + (term.buffer.active.cursorY + 2) + ";1H");
    } else {
        term.write(keycontent);
    }
    if (hasChinese && isInChineseChar(lines, cursorX, "", false, true)) {//中文占两个字符
        term.write(keycontent);
    }
}

function upArrow() {
    if (historys.length == 0) {
        return;
    }
    var his = readHistory(true);
    clearEnter(term);
    if (his != null) {
        var params = getInsertLineParam(his, false, 38, term.buffer.active.cursorX, getCurrentCursorY());
        params.clear = true;
        refreshLine(params);
        term.write('\r' + prefix + his + '\x1b[K');
        curMaxX = (prefix + his).length;
    }
    return;
}

function downArrow() {
    if (historys.length == 0) {
        return;
    }
    var his = readHistory(false);
    clearEnter(term);
    if (his != null) {
        var params = getInsertLineParam(his, false, 40, term.buffer.active.cursorX, getCurrentCursorY());
        params.clear = true;
        refreshLine(params);
        term.write('\r' + prefix + his + '\x1b[K');
        curMaxX = (prefix + his).length;
    }
    return;
}

function writePrint(e) {

    var content = e.key;
    var params = getInsertLineParam(content, charInMiddle, e.domEvent.keyCode, term.buffer.active.cursorX, getCurrentCursorY());
    if (charInMiddle) {
        if (jugdeContinueInput()) {
            //判断字符连续输入
            content = continueChars;
            params.multiInput = true;
            params.content = content;
        }
        var result = refreshLine(params);
        writeInMiddle(term, content, e.domEvent.keyCode, result);
    } else {
        refreshLine(params);
        term.write(content);
        //光标写至最后一位则换行
        if (term.buffer.active.cursorX == termCols - 1) {
            var nextline = term.buffer.active.cursorY + 2;
            term.write("\x1b[" + nextline + ";0H");
        }
    }
    curMaxX = curMaxX + 1;
}

function writePrintToTerm(data) {

    var content = data;
    var params = getInsertLineParam(content, charInMiddle, 0, term.buffer.active.cursorX, getCurrentCursorY());
    if (charInMiddle) {
        if (jugdeContinueInput()) {
            //判断字符连续输入
            content = continueChars;
            params.multiInput = true;
            params.content = content;
        }
        var result = refreshLine(params);
        writeInMiddle(term, content, 0, result);
    } else {
        refreshLine(params);
        term.write(content);
        //光标写至最后一位则换行
        if (term.buffer.active.cursorX == termCols - 1) {
            var nextline = term.buffer.active.cursorY + 2;
            if (!charInMiddle) {
                term.write("\r\n");
            } else {
                term.write("\x1b[" + nextline + ";0H");
            }
        }
    }
    curMaxX = curMaxX + 1;
}

function inline(term, lineContent) {

    //当cursorY在第1行，则cursorY=0
    var cursorY = getCurrentCursorY();
    var active_ = term.buffer.active;
    var activeY = term.buffer.active.cursorY;
    var min = termRows - activeY;
    var i = 1;
    var linecount_ = Math.ceil(getLength(lineContent) / termCols);

    var lastline = getCurrentCursorY();

    if (linecount_ == 1) {
        return 1;
    }
    var endActiveY = activeY;
    var cursorY = term.buffer.active.cursorY;
    try {
        if (outFullTermRows()) {
            while (true) {
                if (term.buffer.active.getLine(lastline + 1 - i) != undefined) {
                    var curline = term.buffer.active.getLine(lastline + 1 - i).translateToString();
                    if (curline.trim().length > 0) {
                        endActiveY = termRows - (i - 1) - 1;
                        break;
                    }
                    if (lastline + 1 - i < 0) {
                        break;
                    }
                }
                if (lastline + 1 - i < 0) {
                    break;
                }
                i++;
            }
        } else {
            var activeY2 = activeY;
            while (true) {
                if (term.buffer.active.getLine(activeY2 + 1 + i) != undefined) {
                    if ((activeY2 + 1 + i) > termRows) {
                        break;
                    }
                    //getLine(n) n=1 时代表读取第二行内容
                    var curline = term.buffer.active.getLine(activeY2 + i).translateToString();
                    if (curline.trim().length > 0) {
                        if (i > termRows) {
                            break;
                        }
                        i++;
                        continue;
                    } else {
                        //endActiveY = 结束的第n行减1
                        endActiveY = activeY2 + i - 1;
                        break;
                    }
                }
            }
        }
    } catch (e) {
        printContent(e)
    }
    var result = linecount_ - (endActiveY - activeY);
    return result;
}

function copyWrite(content) {

    var param = getInsertLineParam(content, charInMiddle, "", term.buffer.active.cursorX, getCurrentCursorY());
    param.copy = true;
    var result = refreshLine(param);

    if (charInMiddle) {
        writeInMiddle(term, content, "", result);
    } else {
        var arr = content.split("\n");
        for (let i = 0; i < arr.length; i++) {
            if (i > 0) {
                term.write("\r\n");
            }
            term.write(arr[i]);
        }
    }
    if (!hasChinese) {
        hasChinese = hasChineseChar(content);
    }
}

function writeInMiddle(term, keyContent, keycode, result) {

    var cursorX = term.buffer.active.cursorX;
    var cursorY = term.buffer.active.cursorY;

    if (keycode == 8) {
        //退格键
        var secondLine = getHalfLeftLine(cursorX, cursorY, true, linesBeforeUpdate) + " ";
        if (cursorX == 0) {
            var cursorY = term.buffer.active.cursorY;
            term.write("\x1b[" + ((cursorY)) + ";" + (termCols) + "H");
            term.write("\x1b[" + (termCols) + "G" + secondLine);
            term.write("\x1b[" + ((cursorY)) + ";" + (termCols) + "H");
        } else {
            if (hasChinese) {
                var backLength = 1;
                if (ifChineseBeforeChar(cursorX, linesBeforeUpdate)) {
                    backLength = 2;
                    secondLine = secondLine + " ";
                }
                term.write("\x1b[" + (cursorX - backLength + 1) + "G" + secondLine);
                term.write("\x1b[" + ((cursorY + 1)) + ";" + (cursorX - backLength + 1) + "H");
            } else {
                term.write("\x1b[" + (cursorX) + "G" + secondLine);
                term.write("\x1b[" + ((cursorY + 1)) + ";" + (cursorX) + "H");
            }
        }
    } else {
        var secondLine = getHalfLeftLine(cursorX, cursorY, false, linesBeforeUpdate) + " ";
        term.write("\x1b[" + (cursorX + 1) + "G" + (secondLine));

        var xindex = (cursorX + getLength(keyContent)) % termCols;
        var yindex = Math.floor((cursorX + getLength(keyContent)) / termCols);

        var lineoutBefore = Math.ceil((secondLine.length + cursorX - getLength(keyContent)) / termCols);
        var lineoutAfter = Math.ceil((secondLine.length + cursorX - 1) / termCols);
        var lineout = lineoutAfter - lineoutBefore;

        cursorY = term.buffer.active.cursorY;
        if (cursorX + secondLine.length > termCols) {
            if (cursorX + getLength(keyContent) >= termCols) {
                term.write("\x1b[" + (cursorY + 1 + yindex) + ";1H");
            } else {
                //光标进入上n行
                var upline = 0;
                if (lineout > 0) {
                    var lastline = getCurrentCursorY();
                    if (lastline >= termRows - 1) {
                        upline = lineout;
                    }
                }
                if (outFullTermRows() && cursorY == (termRows - 1)) {
                    term.write("\x1b[" + ((cursorY - upline)) + ";" + (xindex + 1) + "H");
                } else {
                    term.write("\x1b[" + ((cursorY + 1 - upline)) + ";" + (xindex + 1) + "H");
                }
            }
        } else {
            //光标定位至当前行(cursorX + 2)位置
            term.write("\x1b[" + (cursorX + getLength(keyContent) + 1) + "G" + "");
        }
    }
}

function outFullTermRows() {
    if (term.buffer.normal.length > termRows) {
        return true;
    }
    return false;
}

function getHalfLeftLine(cursorX, cursorY, backspace, linesContent) {

    var x = 0;
    if (backspace) {
        x = getXWhenHasChinese(linesContent, cursorX) - 1;
    } else {
        x = getXWhenHasChinese(linesContent, cursorX);
    }
    var result = lines.slice(0 - (lines.length - x));
    return result
}

/**
 * @param linesContent
 * @param cursorX 当光标在abc的b后面，则cursorX=2
 * @returns {*} 返回字符下标,从0开始
 */
function getXWhenHasChinese(linesContent, cursorX) {

    var inlineNum = inline(term, linesContent);
    var x = 0;
    if (hasChinese || hasChineseChar(lines)) {
        var arrs = linesToDoubleArray(linesContent, true);
        var array = arrs[inlineNum - 1];
        var xcount = 0;
        var j = 0;
        while (j + 1 < inlineNum) {
            xcount = xcount + arrs[j].length;
            j++;
        }
        var accumulate = 0;
        var xcount2 = 0;
        if (cursorX > 0) {
            for (index in array) {
                accumulate = accumulate + array[index];
                if (accumulate >= cursorX) {
                    xcount2 = index;
                    xcount2++;
                    break;
                }
            }
        }
        x = xcount + xcount2;
    } else {
        x = (inlineNum - 1) * termCols + cursorX;
    }
    return x;
}

function arrcount(array) {
    var account = 0;
    for (index in array) {
        account = account + array[index];
    }
    return account;
}

function getInsertLineParam(inputContent, charInMiddle_, keycode_, inputx_, inputy_) {

    return {
        content: inputContent,
        copy: false,
        clear: false,
        charInMiddle: charInMiddle_,
        keycode: keycode_,
        inputx: inputx_,
        inputy: inputy_,
        //连续输入多个中文字符
        multiInput: false
    };
}

function refreshLine(inputParams) {

    var inputContent = inputParams.content;
    var copy = inputParams.copy;
    var clear = inputParams.clear;
    var inputInMiddle = inputParams.charInMiddle;
    var keycode = inputParams.keycode;
    var inputX = inputParams.inputx;
    var inputY = inputParams.inputy;
    var multiInput = inputParams.multiInput;

    var result = {second: "", x: inputX};

    if (startY == -1) {
        startY = getCurrentCursorY();
    }
    if (lines == "" || clear) {
        lines = prefix;
    }
    linesBeforeUpdate = lines;
    if (!inputInMiddle) {
        if (keycode == 8) {
            lines = lines.slice(0, -1);
            linecount = Math.ceil(lines.length / termCols);
        } else {
            lines = lines + inputContent;
            linecount = Math.ceil(lines.length / termCols);
        }
        return;
    }
    // x是当前插入的位置的字符下标（不是光标下标），例如abcde,例如x在a之后，则x=1
    var x = getXWhenHasChinese(lines, inputX);
    var first = lines.slice(0, x);
    var second = "";
    if (multiInput) {
        if(inputContent.length > 1 && browser == 'swt'){
            second = linesBeforeUpdate.slice(x, lines.length);
        }else{
            var cutX = x + (inputContent.length - 1);
            second = lines.slice(cutX, lines.length);
        }
        result.second = inputContent + second;
    } else {
        var cutX = x;
        second = lines.slice(cutX, lines.length);
        result.second = inputContent + second;
    }

    if (keycode == 8) {
        first = first.slice(0, -1);
        lines = first + second;
    } else {
        lines = first + inputContent + second;
    }
    linecount = Math.ceil(lines.length / termCols);

    return result;
}

function clearLine() {
    lines = "";
    linecount = 1;
    startY = -1;
    hasChinese = "";
}

function clearEnter(term) {

    var lineNum = linecount;
    try {
        var i = 0;
        term.write('\x1b[2K\r');
        if (lineNum > 1) {
            while (i < lineNum - 1) {
                var cursorY = term.buffer.active.cursorY;
                term.write("\x1b[" + (cursorY - i) + ";0H\x1b[2K");
                i++;
            }
        }
    } catch (err) {
        //printContent("err:"+err);
    }
}

/**
 * 获取前一个字符是否是中文
 */
function ifChineseBeforeChar(cursorX, linescontent) {

    if (hasChinese) {
        var inlinenum = inline(term, linescontent);
        var linecount_ = Math.ceil(getLength(linescontent) / termCols);
        var arrs = linesToDoubleArray(linescontent, true);
        var array = arrs[inlinenum - 1];
        var accumulate = 0;
        for (index in array) {
            accumulate = accumulate + array[index];
            if (accumulate == cursorX) {
                var value = array[index];
                if (value == 1) {
                    return false;
                } else if (value == 2) {
                    return true;
                }
                break;
            }
            if (accumulate >= cursorX) {
                var value = array[index];
                if (value == 1) {
                    return false;
                } else if (value == 2) {
                    return true;
                }
                break;
            }
        }
    }
    return false;
}

function getLength(chars) {

    if (hasChinese || judehasChineseInLines(chars)) {
        var chineseCount = 0;
        for (let i = 0; i < chars.length; i++) {
            if (chars.charCodeAt(i) > 255) {
                chineseCount++;
            }
        }
        return chars.length + chineseCount;
    }
    return chars.length
}

function isInChineseChar(lines_, cursorX, inlinenum, left, right) {

    if (inlinenum == null || inlinenum == "") {
        inlinenum = inline(term, lines_);
    }
    var arrs = linesToDoubleArray(lines_, hasChinese);
    var arr = arrs[inlinenum - 1]
    var accumulate = 0;
    for (index in arr) {
        accumulate = accumulate + arr[index];
        if (left) {
            if (accumulate == (cursorX) && arr[index] == 2) {
                return true;
            }
        }
        if (right) {
            if (accumulate == (cursorX)) {
                if (arr[++index] == 2) {
                    return true;
                }
                break;
            }
        }
    }
    return false;
}

function hasChineseChar(chars) {
    let reg = new RegExp("[\\u4E00-\\u9FFF]+", "g")
    if (reg.test(chars)) {
        return true;
    }
    return false;
}

function judehasChineseInLines(linescontent) {

    if (hasChinese != "") {
        return;
    }
    let reg = new RegExp("[\\u4E00-\\u9FFF]+", "g")
    if (reg.test(linescontent)) {
        hasChinese = true;
    } else {
        hasChinese = false;
    }
    return hasChinese;
}

/**
 * 内容转化为二维数组 [[1,1,1,2,1,2],[1,1,1,1,1,1]] 每一个代表一个字符（中文或者非中文字符），2代表中文占据了两个字符，1则代表非中文
 */
function linesToDoubleArray(linescontent, haschinese_) {

    let j = 0;
    var accumulate = 0;
    var all = [];

    if (haschinese_) {
        var arr = [];
        all[all.length] = arr;

        for (let i = 0; i < linescontent.length; i++) {
            if (linescontent.charCodeAt(i) > 255) {
                if (accumulate + 2 > termCols) {
                    arr = [];
                    all[all.length] = arr;
                    j = 0;
                    accumulate = 0;
                    arr[j] = 2;
                    j++;
                    accumulate = accumulate + 2;
                    continue;
                }
                arr[j] = 2;
                accumulate = accumulate + 2;
            } else {
                arr[j] = 1;
                accumulate = accumulate + 1;
            }
            if (accumulate == termCols) {
                j = 0;
                accumulate = 0;
                arr = [];
                all[all.length] = arr;
            } else {
                j++;
            }
        }
    } else {
        var arr = [];
        all[all.length] = arr;
        for (let i = 0; i < linescontent.length; i++) {
            arr[j] = 1;
            accumulate = accumulate + 1;
            if (accumulate == termCols) {
                j = 0;
                accumulate = 0;
                arr = [];
                all[all.length] = arr;
            } else {
                j++;
            }
        }
    }
    return all;
}

//控制连续中文输入字符创
var lastInput = false;
var lastIndexCursorX = -1;
var continueChars = "";

var continueInput = false;

/**
 * 判断是否是连续输入字符
 */
function jugdeContinueInput() {

    if (continueChars.length > 1) {
        return true;
    }
    return false;
}

function getcurlineMaxX() {
    if (!hasChinese) {
        return curMaxX;
    } else {
        var array = linesToDoubleArray(lines, true);
        var linecount_ = array.length;
        if (linecount_ == 1) {
            return getLength(arrcount(array[0]));
        } else {
            var inlines = inline(term, lines);
            return getLength(arrcount(array[inlines - 1]));
        }
    }
}

function refreshFlagStatus(data) {

    var content = data;
    if (data === '\r') {
        lastIndexCursorX = -1;
        lastDebounceInputX = -1;
        continueChars = "";
        hasChinese = false;
        continueInput = false;
    } else if (data === '\x7F' || data === '\u0008') {
        lastIndexCursorX = -1;
        lastDebounceInputX = -1;
        continueChars = "";
        continueInput = false;
    } else if (data === '\u001b[D') {
        lastIndexCursorX = -1;
        lastDebounceInputX = -1;
        continueChars = "";
        continueInput = false;
    } else if (data === '\u001b[C') {
        lastIndexCursorX = -1;
        lastDebounceInputX = -1;
        continueChars = "";
        continueInput = false;
    } else if (data === '\u001b[A') {
        lastIndexCursorX = -1;
        lastDebounceInputX = -1;
        continueChars = "";
        continueInput = false;
    } else if (data === '\u001b[B') {
        lastIndexCursorX = -1;
        lastDebounceInputX = -1;
        continueChars = "";
        continueInput = false;
    } else {
        if (!hasChinese) {
            if (content.charCodeAt(0) > 255) {
                hasChinese = true;
            }
        }
        if (lastIndexCursorX == term.buffer.active.cursorX) {
            continueChars = continueChars + data;
        } else {
            lastIndexCursorX = term.buffer.active.cursorX;
            continueChars = data;
        }
    }
}

function triggerEnter() {
    enter();
}



