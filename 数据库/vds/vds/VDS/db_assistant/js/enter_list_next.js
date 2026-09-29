var recordpath = getCookie("recordDataPath");
var datajspath = "<script language=javascript src='Vastbase G100/zh/data.js'></script>"
document.write(datajspath);
//document.write("<script language=javascript src='Gauss200 OLAP V100R007C10/zh/data.js'></script>");
var isNotSingle = true;
var selectedCmdAlias = "temp";
var formerCmd = "";
var cur_cmd = "";
var NameSnext;

//读取cookies
function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");

    if (arr = document.cookie.match(reg))

        return unescape(arr[2]);
    else
        return null;
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

function LoadSuggestion(recordpath) {
    //commands = new Commands();
    //var xml = new ActiveXObject("Microsoft.XMLDOM");
    //var xml = document.implementation.createDocument("", "", null);
    //xml.async = false;
    //xml.load(recordpath + "/suggestion.xml");
    //txt = "<commands></command>";
    //txt = $('#xmlContent').html();
    //txt = "<commands><command id='SELECT' alias='SELECT'><div><suggestion>hhhhhhhh</suggestion></div></command></commands>";
    //parser = new DOMParser();
    //xml = parser.parseFromString(txt, "text/xml");
    //commands.load(xml);
    //getSQLHtmlForConent(commands.cmds);
    processInput(NameSnext);
}

function getSQLHtmlForConent(tempValues) {

    //编辑sugesion.xml所有command，查找对应的command
    processInput(NameSnext);
}

function processInput(tempId) {
    tempId = $.trim(tempId); //trim（）方法从字符串的两边删除空格
    tempCmds = tempId;
    if ("" != tempId) {
        if (tempCmds.length > 0) {

            var suggesion = getSuggesion(tempId);

            if (suggesion == "undefined" || suggesion == undefined) {
                return;
            }

            if (suggesion != "") {
                tempSuggestion = "<h4 class='sectionCmdTitle'>" + tempId + "</h4>" + suggesion;
            }

            if (cur_cmd != "" && formerCmd == "") {
                tempSuggestion = "<h4 class='sectionCmdTitle'>" + tempId + "</h4>" + getSuggesion(tempId);
                $('#divSuggestion').html(tempSuggestion);
                $(document).scrollTop(0);
                assistantHighlight("assistantExamples");
                formerCmd = cur_cmd;
            } else if (cur_cmd != "" && formerCmd != "" && cur_cmd.alias != formerCmd.alias) {
                $('#divSuggestion').html(tempSuggestion);
                $(document).scrollTop(0);
                assistantHighlight("assistantExamples");
                formerCmd = cur_cmd;
            } else if (formerCmd == "") {
                $('#divSuggestion').html(tempSuggestion);
                $(document).scrollTop(0);
            }
        }
    }
}

function getParams(key) {
    var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return unescape(r[2]);
    }
    return null;
};
$(function () {
    $("#grammarNext").click(function () {
        location.href = "index_zh.html";
        $(this).addClass("active");
        $("#operationListNext").removeClass("active");
        $("#beginnerGuideNext").removeClass("active");
        $("#caseNext").removeClass("active");
    });
    $("#beginnerGuideNext").click(function () {
        $(this).addClass("active");
        $("#operationListNext").removeClass("active");
        $("#grammarNext").removeClass("active");
        $("#caseNext").removeClass("active");
    });

    $("#caseNext").click(function () {
        $(this).addClass("active");
        $("#operationListNext").removeClass("active");
        $("#beginnerGuideNext").removeClass("active");
        $("#grammarNext").removeClass("active");
    });
    var heroes = db['sheet1'];
    var mun = getParams("param1");
    NameS = heroes[mun].分类名称;
    NameSnext = getParams("param2");
    $("#operNameSnext").text(">"+NameSnext);
    var operNameNext = "<a class='button-item-A' href='enter_list.html?param3=true&param4=" + mun + "'>" + ">" + NameS + "</a>"

    $("#operNameS").append(operNameNext);
    // $("#operNameB").append(recordpath);
    recordpath = "openGauss 1.0.0/zh";
    LoadSuggestion(recordpath);

});