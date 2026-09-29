var dbversion = "g100"
var grammerJson = []

function getSuggesion(commandID) {

    if (commandID == "" || commandID == undefined) {
        return "";
    }
    commandID = commandID.toUpperCase()
    var Gjson = getJson();
    for (i in Gjson) {
        if (commandID == Gjson[i].alias) {
            return Gjson[i].suggestion;
        }
    }
    return "";
}

function getSuggesionWithKeyWord(keyword) {

    var result = "";
    keyword = keyword.toUpperCase();
    var count = 0;
    var res = {
        result: "",
        count: 18
    };
    var Gjson = getJson();
    for (i in grammerJson) {
        if (grammerJson[i].alias.indexOf(keyword) == 0) {
            var append = "<tr><td align='left' onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);hideKeyWordList(this.innerText);'>" + grammerJson[i].alias + "</td></tr>";
            result = result + append;
            count++;
        }
    }
    res.result = result;
    res.count = count;
    return res;
}

function getGramList() {

    var result = "";
    var Gjson = getJson();
    var i = 0;
    for (json_ in Gjson) {
        if (i > 0) {
            var append = "· <a href='#'onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);goBack(\"block\");'class='linkText'>" + Gjson[json_].alias + "</a></br>\n";
        } else {
            var append = "\t\t\t\t\t· <a href='#'onclick='selectedCmdAlias=this.innerText;processInput(this.innerText);goBack(\"block\");'class='linkText'>" + Gjson[json_].alias + "</a></br>\n";
        }
        i++;
        result = result + append;
    }
    return result;
}

function getJson() {
    if (dbversion == "g100") {
        grammerJson = json_g100_2210;
    }
    return grammerJson;
}

