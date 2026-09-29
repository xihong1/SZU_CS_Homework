// var data = require('../js/operationList');
var commands;
var errorcodes;
var selectedCmdAlias = "temp";
var isNotSingle = true;
var oTextSelection = "";
var currentSQL = "";
var backString = "";
var rightMenu = "";
var divDefault = "";
var divGoBack = "";
var formerCmd = "";
var cur_cmd = "";

function getSQLHtml(tempValues) {
    var tempSuggestion = "<pre>";
    $.each(tempValues, function (n, v) {
        if (v.alias.indexOf('|') > -1) {
            tempSuggestion = tempSuggestion + "· <a href='#' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);goBack(\"block\");' class='linkText'>" + v.id + "</a>\r\n";
        } else {
            tempSuggestion = tempSuggestion + "· <a href='#' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);goBack(\"block\");' class='linkText'>" + v.alias + "</a>\r\n";
        }
    });
    tempSuggestion = tempSuggestion + "</pre>";
    return tempSuggestion;
}

function hideKeyWord(needHide) {
    if (needHide) {
        $('#keywordInfo').hide();
        $("#listStatus").removeClass("hideList").addClass("showList");
    } else {
        $('#keywordInfo').show();
        $("#listStatus").removeClass("showList").addClass("hideList");
    }
}

function hideOrShowKeyWord() {
    if ($("#keywordInfo").is(':visible')) {
        hideKeyWord(true);
    } else {
        hideKeyWord(false);
    }
}

function hideKeyWordList(str) {
    $('#keyword').val(str);
    hideKeyWord(true);
}

function getSQLHtmlForList(tempValues, recordPath) {
    var tempSuggestion = "";
    $.each(tempValues, function (n, v) {
        if (v.alias.indexOf('|') > -1) {
            tempSuggestion = tempSuggestion + "<tr><td align='left' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);hideKeyWordList(this.innerText);'>" + v.id + "</td></tr>";
        } else {
            tempSuggestion = tempSuggestion + "<tr><td align='left' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);hideKeyWordList(this.innerText);'>" + v.alias + "</td></tr>";
        }
    });
    $('#keywordInfo').css("height", "300px");
    $('#keywordInfoBody').html(tempSuggestion);
    setCookie("recordDataPath", recordPath);
}

function checkField(keyword) {
    var temStr = keyword.toUpperCase();
    var rowCount = 0;
    var tempSuggestion = getSuggesionWithKeyWord(keyword);
    rowCount = tempSuggestion.count;
    if (rowCount < 16) {
        $('#keywordInfo').css("height", (14 * rowCount) + "px");
    } else {
        $('#keywordInfo').css("height", "300px");
    }
    $('#keywordInfoBody').html(tempSuggestion.result);
    hideKeyWord(false);
    renderKeywordEvent();
    if (keyword == '') {
        $('#removeinput').hide();
    } else {
        removeIconShow();
    }
}

var needShowIcon = false;

function removeIconShow() {
    if (document.documentMode) {
        if (document.documentMode > 8) {
            $('#removeinput').hide();
        } else {
            $('#removeinput').show();
        }
    } else {
        $('#removeinput').show();
    }
}

function renderKeywordEvent() {
    $('#keywordInfoBody').children().children().bind("click", function () {
        selectedCmdAlias = this.innerText;
        processInput(this.innerText);
        hideKeyWordList(this.innerText);
    });
}

function processInput(tempId) {

    if ("hideAssistant" == tempId) {
        myCallDBAssistant('hide');
        return;
    }
    if (document.selection) {
        document.selection.empty();
    } else {
        window.getSelection().removeAllRanges();
    }
    if (divGoBack != "") {
        divGoBack.remove ? divGoBack.remove() : divGoBack.removeNode(true);
    }
    if (rightMenu != "") {
        rightMenu.remove ? rightMenu.remove() : rightMenu.removeNode(true);
    }
    tempId = $.trim(tempId);

    if (tempId != "") {
        var suggesion = getSuggesion(tempId);
        if (suggesion == "") {
            return;
        }
        $('#keyword').val(tempId.toUpperCase());
        suggesion = "<h4 class='sectionCmdTitle'>" + tempId.toUpperCase() + "</h4>" + suggesion;
        $('#divSuggestion').html(suggesion);
        $('#removeinput').show();
    } else {
        var suggesion = getGramList();
        $('#divSuggestion').html(suggesion);
    }
    hideKeyWord(true);
}

function processErrorCode(errorCode) {
    var err = errorcodes.find($.trim(errorCode));
    if (err != "") {
        var tempHtml = "<p class=\"sectionCmdTitle\">" + errorCode + "</p><p><span class=\"sectionTitle\">Descrition</span></p><p><span class=\"sectionText\">" + err.description + "</span></p><p><span class=\"sectionTitle\">SQLSTATE</span></p><p><span class=\"sectionText\">" + err.sqlstate + "</span></p><p><span class=\"sectionTitle\">Possible Causes</span></p><p><span class=\"sectionText\">" + err.cause + "</span></p><p ><span class=\"sectionTitle\">Solution</span</p><p><span class=\"sectionText\">" + err.solution + "</span></p>";
        $('#divSuggestion').html(tempHtml);
        if (isNotSingle) myCallDBAssistant('show');
    }
}

function processSelection1() {
    if (oTextSelection != "") {
        myCallDBAssistantProcessSelection(oTextSelection);
    }
}

function processSelection2() {
    if (oTextSelection != "") {
        myCallDBAssistantProcessSelection2(oTextSelection);
    }
}

function displayVersionNote(curVersion) {
    var divVersionNote = $('<div style="display:none;line-height:22px;background-color:#fefce8;position:fixed;top:10px;margin:2 0 0 2;padding-left:6px;padding-right:6px;border-radius:4px;border:1px solid;border-color:#aaa9a9;"></div>');
    var p1 = $('<p style="margin-top:5px;">请从华为Support上下载FusionInsight LibrA对应版本的知识库。</p>');
    divVersionNote.append(p1);
    $('body').append(divVersionNote);
}

function disableNote(disable) {
    if (disable) {
        if (divDefault != "") {
            divDefault.remove();
            divDefault = "";
        }
    } else {
        divDefault = $('<div style="line-height:22px;background-color:#fefce8;position:fixed;bottom:0px;margin:10 0 0 2;padding-left:6px;padding-right:6px;border-radius:4px;border:1px solid;border-color:#aaa9a9;">');
        var p1 = $('<p style="margin-bottom:0px;">在中间窗口中，<span style="color:#ed6b44">选中SQL语句或错误码</span>，SQL助手会显示对应的<span style="color:#ed6b44">说明信息</span>。</p>');
        var p2 = $('<p align="right" style="margin-top:-5px;margin-bottom:5px;color:#016bd8;"><span style="cursor:hand;" onclick="disableNote(true);myCallDBAssistantDisableNote(\'\');">我知道了</span></p>');
        divDefault.append(p1);
        divDefault.append(p2);
        $('body').append(divDefault);
    }
}

function setCurrentSQL(sql) {
    currentSQL = sql;
}

function setCookie(name, value) {
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

function loadSuggestion(docRealPath) {

    grammerJson = json_g100_2210;
    var tempSuggestion = "";
    for (json_ in grammerJson) {
        var sugess = "· <a href='#' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);goBack(\"block\");'\n" +
            "                     class='linkText'>" + grammerJson[json_].alias + "</a></br>";
        tempSuggestion = tempSuggestion + sugess;
    }
    $('#divSuggestion').html(tempSuggestion);
    loadKeyWords(grammerJson);
}

function loadKeyWords(gjson) {
    var tempSuggestion = "";
    for (i in gjson) {
        var append = "<tr><td align='left' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);hideKeyWordList(this.innerText);'>" + gjson[i].alias + "</td></tr>";
        tempSuggestion = tempSuggestion + append;
    }
    $('#keywordInfo').css("height", "300px");
    $('#keywordInfoBody').html(tempSuggestion);
    //setCookie("recordDataPath", recordPath);
}

function resetKeyword() {
    loadKeyWords(grammerJson);
}

function loadErrorcode(docRealPath) {
    errorcodes = new ErrorCodes();
    //var xml = new ActiveXObject("Microsoft.XMLDOM");
    //xml.async = false;
    //xml.load(docRealPath+"/errorcode.xml");
    //errorcodes.load(xml);
    processInput(currentSQL);
    myCallDBAssistant('show');
}

function isHidden(oDiv) {
    var vDiv = oDiv.nextSibling;
    while (vDiv.nodeType == 3) {
        vDiv = vDiv.nextSibling;
    }
    vDiv.style.display = (vDiv.style.display == 'none') ? 'block' : 'none';
    var pngs = oDiv.getElementsByTagName("img");
    switch (pngs[1].style.display) {
        case 'none':
            pngs[0].style.display = 'none';
            pngs[1].style.display = 'inline';
            break;
        case 'inline':
            pngs[0].style.display = 'inline';
            pngs[1].style.display = 'none';
            break;
    }
}

function goBack(display) {
    if (display == "none") {
        //divGoBack.remove ? divGoBack.remove() : divGoBack.removeNode(true);
        divGoBack.remove ? divGoBack.remove() : $('#divGoBack').remove();
        divGoBack = "";
        processInput(backString);
    } else {
        divGoBack = $('<div class="grammar-item-goback center" id="divGoBack"></div>');
        var img1 = $('<img src="img/goback.png" id="gobackid" border="0" title="返回" onClick="javascript:goBack(\'none\');">');
        divGoBack.append(img1);
        $(".grammar-item-one").append(divGoBack);
        $(document).on('click', '#gobackid', function () {
            goBack('none');
        });
    }
}

function readWorkbookFromRemoteFile(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('get', url, true);
    xhr.responseType = 'arraybuffer';
    xhr.onload = function (e) {
        if (xhr.status == 200) {
            var data = new Uint8Array(xhr.response)
            var workbook = XLSX.read(data, {type: 'array'});
            if (callback) callback(workbook);
        }
    };
    xhr.send();
}

$(function () {
    loadSuggestion("g100");
    $("#keywordInfo").scrollBar({
        width: 252
    });
    setTimeout(function () { //用于在指定的毫秒数后调用函数或计算表达式
        //myCallDBAssistantLoad('');
        //console.log("myCallDBAssistantLoad")
    }, 1000);
    $('body').contextmenu(function (event) {
        //hideKeyWordList();
        if (document.selection) {
            oTextSelection = document.selection.createRange().text;
        } else {
            oTextSelection = window.getSelection().toString();
        }
        //var event = event || window.event;
        var leftX = event.pageX;
        var topY = event.pageY;

        if (oTextSelection != "" && rightMenu == "") {
            var bodyW = $('body').width();
            if (bodyW <= leftX + 130) {
                leftX = bodyW - 130;
            }
            rightMenu = $('<div style="box-shadow:-10px 0 10px rgba(255,255,255,0.01),2px 0 3px gray,0 -10px 10px rgba(255,255,255,0.01),2px 2px 3px gray;width:118px;top:' + topY + 'px;left:' + leftX + 'px;padding:2px 2px 2px 2px;position:absolute;background-image:url(img/assistantCopy.png);border: 1px solid gray;font-size:10px;"></div>');
            var span1 = $('<div style="padding-left:30px;margin:0 0 0 0;border:1px solid #F0F0F0;font-size:12px;line-height:22px;cursor:pointer;" onclick="javascript:processSelection1();" onmouseover="this.style.borderColor=\'#AECFF7\'" onmouseout="this.style.borderColor=\'#F0F0F0\'">拷贝</div>');
            //var br1 =$('<br>');
            var span2 = $('<div style="padding-left:30px;margin:0 0 0 0;border:1px solid #F0F0F0;font-size:12px;line-height:22px;cursor:pointer;" onclick="javascript:processSelection2();" onmouseover="this.style.borderColor=\'#AECFF7\'" onmouseout="this.style.borderColor=\'#F0F0F0\'">拷贝到编辑区</div>');
            rightMenu.append(span1);
            //rightMenu.append(br1);
            rightMenu.append(span2);
            $('body').append(rightMenu);
        } else if (oTextSelection != "" && rightMenu != "") {
            var bodyW = $('body').width();
            if (bodyW <= leftX + 130) {
                leftX = bodyW - 130;
            }
            rightMenu.css('left', leftX);
            rightMenu.css('top', topY);
        } else if (rightMenu != "") {
            rightMenu.remove ? rightMenu.remove() : rightMenu.removeNode(true);
            rightMenu = "";
        }
        return false;
    });
    document.onclick = function () {
        if (rightMenu != "") {
            rightMenu.remove ? rightMenu.remove() : rightMenu.removeNode(true);
            rightMenu = "";
        }
    };
    document.onkeydown = function (e) {
        var e = window.event ? window.event : e;
        if (e.ctrlKey && e.keyCode == 67) {
            if (document.selection) {
                oTextSelection = document.selection.createRange().text;
            } else {
                oTextSelection = window.getSelection().toString();
            }
            if (oTextSelection != "") {
                processSelection1();
                return false;
            }
        }
    };
    $("#grammar").click(function () {
        $(this).addClass("active");
        $("#operationList").removeClass("active");
        $("#beginnerGuide").removeClass("active");
        $("#case").removeClass("active");
        location.href = "index_zh.html";
    });

    $("#operationList").click(function () {
        $(this).addClass("active");
        $("#grammar").removeClass("active");
        $("#beginnerGuide").removeClass("active");
        $("#case").removeClass("active");
        location.href = "operationList.html";
    });

    $("#beginnerGuide").click(function () {
        $(this).addClass("active");
        $("#operationList").removeClass("active");
        $("#grammar").removeClass("active");
        $("#case").removeClass("active");
        location.href = "beginnerGuide.html";
    });

    $("#case").click(function () {
        $(this).addClass("active");
        $("#operationList").removeClass("active");
        $("#beginnerGuide").removeClass("active");
        $("#grammar").removeClass("active");
        location.href = "case.html";
    });

    if (document.documentMode) {
        if (document.documentMode <= 8) {
            $('#removeinput').hide();
            needShowIcon = true;
        } else {
            $('#removeinput').remove();
        }
    }
});

$(window).load(function(){
	if (document.documentMode) {
        if (document.documentMode <= 8) {
			//IE8以下，输入框内容改变事件不生效，需特殊处理
            document.getElementById("keyword").onpropertychange = function () {
                checkField(document.getElementById("keyword").value);
            };
			hideKeyWord(true);
        } 
    }
});