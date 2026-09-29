var jsConnector = {
    pressKey: function (result) {
        if ("Backspace" == result) {
        }
    },

    writeToXterm: function (content) {
        writeToXterm_(content);
    },

    inputCmd: function (content) {
        inputCmd_(content);
    },

    waitPrint: function (prefix_) {
        waitPrint_(prefix_);
    },

    xtermInit: function (browserM) {
        xtermInit_(browserM);
    },

    moreTip: function () {
        moreTip_();
    },

    endMoreOut: function () {
        endMoreOut_();
    },

    coverWrite: function (content) {
        coverWrite_(content);
    },

    resetFontAndBgColor: function (fontSize, fontColor, bgColor) {
        resetFontAndBgColor_(fontSize, fontColor, bgColor);
    },

    updatePrefix: function (content) {
        updatePrefix_(content);
    },

    passwordGuide: function (prefix_) {
        passwordGuide_(prefix_);
    },

    pasteClipboard: function (content) {

        var sel = term.getSelection();
        if (sel != undefined && sel != null && sel.length > 0) {
            paste(sel);
            javaConnector.copyToClipbord(sel);
            enterWithChangLine(content);
            return;
        }
        paste(content);
        enterWithChangLine(content);
    },

};