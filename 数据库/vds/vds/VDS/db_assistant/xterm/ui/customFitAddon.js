function addon(_terminal) {

    if (_terminal && _terminal.element && _terminal.element.parentElement) {
        var e = _terminal._core;
        if (0 !== e._renderService.dimensions.actualCellWidth && 0 !== e._renderService.dimensions.actualCellHeight) {
            var t = window.getComputedStyle(_terminal.element.parentElement),
                r = parseInt(t.getPropertyValue("height")),
                i = Math.max(0, parseInt(t.getPropertyValue("width"))),
                n = window.getComputedStyle(_terminal.element),
                o = r - (parseInt(n.getPropertyValue("padding-top")) + parseInt(n.getPropertyValue("padding-bottom"))),
                a = i - (parseInt(n.getPropertyValue("padding-right")) + parseInt(n.getPropertyValue("padding-left"))) - e.viewport.scrollBarWidth;

            var geometry = new Object();
            geometry.cols = Math.max(2, Math.floor(a / e._renderService.dimensions.actualCellWidth));
            geometry.rows = Math.max(1, Math.floor(o / e._renderService.dimensions.actualCellHeight));
            return geometry;
        }
    }
}

function addonHighVersion(_terminal) {

    if (!_terminal) {
        return undefined;
    }
    if (!_terminal.element || !_terminal.element.parentElement) {
        return undefined;
    }
    var core = _terminal._core;
    if (core._renderService.dimensions.actualCellWidth === 0 || core._renderService.dimensions.actualCellHeight === 0) {
        return undefined;
    }
    var parentElementStyle = window.getComputedStyle(_terminal.element.parentElement);
    var parentElementHeight = parseInt(parentElementStyle.getPropertyValue('height'));
    var parentElementWidth = Math.max(0, parseInt(parentElementStyle.getPropertyValue('width')));
    var elementStyle = window.getComputedStyle(_terminal.element);
    var elementPadding = {
        top: parseInt(elementStyle.getPropertyValue('padding-top')),
        bottom: parseInt(elementStyle.getPropertyValue('padding-bottom')),
        right: parseInt(elementStyle.getPropertyValue('padding-right')),
        left: parseInt(elementStyle.getPropertyValue('padding-left'))
    };
    var elementPaddingVer = elementPadding.top + elementPadding.bottom;
    var elementPaddingHor = elementPadding.right + elementPadding.left;
    var availableHeight = parentElementHeight - elementPaddingVer;
    var availableWidth = parentElementWidth - elementPaddingHor - core.viewport.scrollBarWidth;
    var geometry = {
        cols: Math.max(MINIMUM_COLS, Math.floor(availableWidth / core._renderService.dimensions.actualCellWidth)),
        rows: Math.max(MINIMUM_ROWS, Math.floor(availableHeight / core._renderService.dimensions.actualCellHeight))
    };
    return geometry;
}