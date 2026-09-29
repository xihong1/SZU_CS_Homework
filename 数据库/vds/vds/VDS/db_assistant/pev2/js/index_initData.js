
var top_run_time = document.getElementById('top_run_time');
var topRunTime;
// 定义变量用于记录节点出现顺序
const background_color_20 = 'rgb(102, 193, 10)';
const background_color_40 = 'rgb(157, 193, 10)';
const background_color_60 = 'rgb(193, 193, 10)';
const background_color_80 = 'rgb(193, 113, 10)';
const background_color_99 = 'rgb(193, 79, 10)';
const background_color_100 = 'rgb(193, 10, 10)';
const percentage = 100;
var nodeCount = 1;
var leftTimeCount = 1;
var leftRowsCount = 1;
var leftCostCount = 1;
var plan_content = document.getElementById('plan_content');
var plan_left = document.getElementById('plan_left');
var tipps = document.getElementById('tipps-test');
var maxSelfCost;
var maxSelfRows;
var maxSelfTime;
//网页端直接查看效果解开一下注释
/*var visualExplainData = '{"nodeType":"Nested Loop","children":[{"nodeType":"Nested Loop","children":[{"nodeType":"Nested Loop","children":[{"nodeType":"Index Scan","children":[],"startupCost":0.0,"totalRunTime":0.715,"totalCost":8.28,"planRows":1,"planWidth":215,"actualStartupTime":0.151,"actualTotalTime":0.152,"actualRows":1,"actualLoops":1,"output":["tbl.oid","tbl.relname","tbl.relnamespace","tbl.relpersistence","tbl.reloptions","tbl.reltablespace"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.152,"selfTimeContributionInOverAllPlan":100.0,"selfCost":8.28,"selfCostContributionInOverAllPlan":100.0,"selfRowContributionInOverAllPlan":25.0,"maxSelfRows":0,"maxSelfCost":0.0,"maxSelfTime":0.0},{"nodeType":"Index Scan","children":[],"startupCost":0.0,"totalRunTime":0.715,"totalCost":8.27,"planRows":1,"planWidth":36,"actualStartupTime":0.035,"actualTotalTime":0.035,"actualRows":0,"actualLoops":1,"output":["xctbl.pcrelid","xctbl.pclocatortype","xctbl.pchashalgorithm","xctbl.pchashbuckets","xctbl.pgroup","xctbl.redistributed","xctbl.redis_order","xctbl.pcattnum","xctbl.nodeoids","xctbl.options"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.035,"selfTimeContributionInOverAllPlan":23.02631578947369,"selfCost":8.27,"selfCostContributionInOverAllPlan":99.8792270531401,"selfRowContributionInOverAllPlan":0.0,"maxSelfRows":0,"maxSelfCost":0.0,"maxSelfTime":0.0}],"startupCost":0.0,"totalRunTime":0.715,"totalCost":16.55,"planRows":1,"planWidth":247,"actualStartupTime":0.201,"actualTotalTime":0.204,"actualRows":1,"actualLoops":1,"output":["tbl.oid","tbl.relname","tbl.relnamespace","tbl.relpersistence","tbl.reloptions","tbl.reltablespace","xctbl.nodeoids"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.016999999999999987,"selfTimeContributionInOverAllPlan":11.184210526315782,"selfCost":3.552713678800501E-15,"selfCostContributionInOverAllPlan":4.2907170033822476E-14,"selfRowContributionInOverAllPlan":25.0,"maxSelfRows":0,"maxSelfCost":0.0,"maxSelfTime":0.0},{"nodeType":"Seq Scan","children":[],"startupCost":0.0,"totalRunTime":0.715,"totalCost":1.02,"planRows":2,"planWidth":132,"actualStartupTime":0.017,"actualTotalTime":0.02,"actualRows":4,"actualLoops":1,"output":["ts.spcname","ts.oid"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.02,"selfTimeContributionInOverAllPlan":13.157894736842106,"selfCost":1.02,"selfCostContributionInOverAllPlan":12.318840579710146,"selfRowContributionInOverAllPlan":100.0,"maxSelfRows":0,"maxSelfCost":0.0,"maxSelfTime":0.0}],"startupCost":0.0,"totalRunTime":0.715,"totalCost":17.6,"planRows":1,"planWidth":371,"actualStartupTime":0.239,"actualTotalTime":0.242,"actualRows":1,"actualLoops":1,"output":["tbl.oid","tbl.relname","tbl.relnamespace","tbl.relpersistence","tbl.reloptions","xctbl.nodeoids","ts.spcname"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.018000000000000016,"selfTimeContributionInOverAllPlan":11.842105263157906,"selfCost":0.030000000000001137,"selfCostContributionInOverAllPlan":0.3623188405797239,"selfRowContributionInOverAllPlan":25.0,"maxSelfRows":0,"maxSelfCost":0.0,"maxSelfTime":0.0},{"nodeType":"Index Scan","children":[],"startupCost":0.0,"totalRunTime":0.715,"totalCost":8.27,"planRows":2,"planWidth":31,"actualStartupTime":0.014,"actualTotalTime":0.014,"actualRows":0,"actualLoops":1,"output":["d.objoid","d.classoid","d.objsubid","d.description"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.014,"selfTimeContributionInOverAllPlan":9.210526315789474,"selfCost":8.27,"selfCostContributionInOverAllPlan":99.8792270531401,"selfRowContributionInOverAllPlan":0.0,"maxSelfRows":0,"maxSelfCost":0.0,"maxSelfTime":0.0}],"startupCost":0.0,"totalRunTime":0.715,"totalCost":25.89,"planRows":2,"planWidth":398,"actualStartupTime":0.257,"actualTotalTime":0.26,"actualRows":1,"actualLoops":1,"output":["tbl.oid","tbl.relname","tbl.relnamespace","ts.spcname","tbl.relpersistence","d.description","xctbl.nodeoids","tbl.reloptions"],"sortMethod":"","sortSpaceUsed":0,"sortSpaceType":"","selfTime":0.0040000000000000036,"selfTimeContributionInOverAllPlan":2.6315789473684235,"selfCost":0.019999999999999574,"selfCostContributionInOverAllPlan":0.24154589371980165,"selfRowContributionInOverAllPlan":25.0,"maxSelfRows":4,"maxSelfCost":8.28,"maxSelfTime":0.152}';
(function() {
    // 在这里编写页面初始化的代码
    visualExplainData = JSON.parse(visualExplainData);
    sendToJs();
})();*/

var setting_button = document.getElementById('setting_button');
var setting_div = document.getElementById('setting_div');
setting_button.addEventListener('click', function() {
    if (setting_div.style.display === 'none') {
        setting_div.style.display = 'block';
    } else {
        setting_div.style.display = 'none';
    }
});

var splitter = document.getElementById('splitpanes_self');
var leftPane = document.getElementById('splitpanes_left');
var rightPane = document.getElementById('plan_content');
var isDragging = false;

/*splitter.addEventListener('mousedown', function(e) {
    isDragging = true;
    document.addEventListener('mousemove', resizePanes);
    document.addEventListener('mouseup', stopDragging);
});*/

function resizePanes(e) {
    if (isDragging) {
        var xPos = e.clientX;
        var splitterRect = splitter.getBoundingClientRect();
        var leftWidth = xPos - splitterRect.left;
        var totalWidth = splitter.parentElement.offsetWidth;
        var leftWidthPercentage = (leftWidth / totalWidth) * 100;
        leftPane.style.width = leftWidthPercentage + '%';
        rightPane.style.width = (100 - leftWidthPercentage) + '%';
    }
}

function stopDragging() {
    isDragging = false;
    document.removeEventListener('mousemove', resizePanes);
    document.removeEventListener('mouseup', stopDragging);
}

function sendToJs() {
    //解析json javafx需要在拿到数据后进行JSON.parse  而Browser直接获取到相应的结构 所以注释掉JSON.parse相关部分
    //const data = visualExplainData;
    //var dataJson = JSON.parse(data);
    //直接通过后端 VisualExplainPlanPart类中createPartControlNew 传递visualExplainData的值和调用sendToJs
    var dataJson = visualExplainData;
    topRunTime = dataJson.totalRunTime;
    top_run_time.innerText = topRunTime + 'ms';

    maxSelfCost = dataJson.maxSelfCost;
    maxSelfRows = dataJson.maxSelfRows;
    maxSelfTime = dataJson.maxSelfTime;

    nodeCount = 1;
    leftTimeCount = 1;
    leftRowsCount = 1;
    leftCostCount = 1;
    var htmlContent = analysisNodeAndAssignNumbers(dataJson);
    var htmlLeftPlan = analysisLeftNode(dataJson);
    plan_content.innerHTML = htmlContent;
    //tipps.innerText = htmlContent;
    plan_left.innerHTML = htmlLeftPlan;
    initElementEvents();
}

/**
 * 分析node节点信息，填充左侧树形展示table
 */
function analysisLeftNode(node) {
    var htmlLeftNode = '';
    //左侧time
    var timeLevel = 0;
    var timeLevelStructure = '';
    htmlLeftNode += '<table class="m-1" id="left_table_time" style="display: block"><tbody>';
    htmlLeftNode += initLeftNodeTimeInfo(node, timeLevel, timeLevelStructure);
    htmlLeftNode += '</tbody></table>';
    //左侧rows tips
    var rowsLevel = 0;
    var rowsLevelStructure = '';
    htmlLeftNode += '<table class="m-1" id="left_table_rows" style="display: none"><tbody>';
    htmlLeftNode += initLeftNodeRowsInfo(node, rowsLevel, rowsLevelStructure);
    htmlLeftNode += '</tbody></table>';
    //左侧cost
    var costLevel = 0;
    var costLevelStructure = '';
    htmlLeftNode += '<table class="m-1" id="left_table_cost" style="display: none"><tbody>';
    htmlLeftNode += initLeftNodeCostInfo(node, costLevel, costLevelStructure);
    htmlLeftNode += '</tbody></table>';
    return htmlLeftNode;
}

function initLeftNodeTimeInfo(node, timeLevel, timeLevelStructure) {
    var leftNodeTimeHtml = '';
    //百分比计算 保留四位小数
    const selfTimePercentage = node.selfTimeContributionInOverAllPlan;
    const timeLeftWidth = selfTimePercentage.toFixed(4);
    const timeWidthRight = percentage - timeLeftWidth;
    //左侧节点需要根据上下级以及子节点个数来处理上下级之间的关系 └   &nbsp;├   &nbsp;└   │└
    leftNodeTimeHtml += '<tr data-tippy-content="Time: ' + node.selfTime.toFixed(3) + 'ms"' +
        ' class="no-focus-outline node" >' +
        '   <td class="node-index">' +
        '       <a class="font-weight-normal small">#' + leftTimeCount + '</a>' +
        '   </td>' +
        '   <td class="node-type pr-2"><span class="tree-lines">' + timeLevelStructure + '</span>' + " " + node.nodeType +
        '       </td>' +
        '       <td>' +
        '          <div class="progress rounded-0 align-items-center bg-transparent" style="height: 5px;">' +
        '             <div role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"' +
        '               class="progress-bar border-secondary bg-secondary border-left"' +
        '               style="width: ' + timeLeftWidth + '%; height: 5px;">' +
        '             </div>' +
        '             <div role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"' +
        '                class="progress-bar bg-secondary-light"' +
        '                style="width: ' + timeWidthRight + '%; height: 5px;">' +
        '             </div>' +
        '           </div>' +
        '       </td>' +
        '</tr>';
    leftTimeCount++;
    //拼接子节点
    if (node.children && node.children.length > 0) {
        const childrenSize = node.children.length;
        for (var i = 0; i < node.children.length; i++) {
            if (timeLevel === 0){
                if (childrenSize > 1 && i < (childrenSize - 1)){
                    timeLevelStructure = '├'
                }else {
                    timeLevelStructure = '└'
                }
            }else {
                const nbsp = initNbsp(timeLevel);
                if (childrenSize > 1 && i < (childrenSize - 1)){
                    timeLevelStructure = nbsp + '├'
                }else {
                    timeLevelStructure = nbsp + '└'
                }
            }
            //从li拼接
            leftNodeTimeHtml += initLeftNodeTimeInfo(node.children[i], (timeLevel + 1), timeLevelStructure);
        }
    }
    return leftNodeTimeHtml;
}

function initLeftNodeRowsInfo(node, rowsLevel, rowsLevelStructure) {
    var leftNodeRowsHtml = '';
    //百分比计算 保留四位小数
    const selfRowsPercentage = node.selfRowContributionInOverAllPlan;
    const rowsLeftWidth = selfRowsPercentage.toFixed(4);
    const rowsWidthRight = percentage - rowsLeftWidth;
    leftNodeRowsHtml += '<tr data-tippy-content="Rows: ' + node.actualRows + '"' +
        ' class="no-focus-outline node" >' +
        '   <td class="node-index">' +
        '       <a class="font-weight-normal small">#' + leftRowsCount + '</a>' +
        '   </td>' +
        '   <td class="node-type pr-2"><span class="tree-lines">' + rowsLevelStructure + '</span>' + " " + node.nodeType +
        '   </td>' +
        '   <td>' +
        '      <div class="progress rounded-0 align-items-center bg-transparent" style="height: 5px;">' +
        '         <div role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"' +
        '               class="progress-bar border-secondary bg-secondary border-left"' +
        '               style="width: ' + rowsLeftWidth + '%; height: 5px;">' +
        '         </div>' +
        '         <div role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"' +
        '                class="progress-bar bg-secondary-light"' +
        '                style="width: ' + rowsWidthRight + '%; height: 5px;"></div>' +
        '         </div>' +
        '    </td>' +
        '</tr>';
    leftRowsCount++;
    //拼接子节点
    if (node.children && node.children.length > 0) {
        const childrenSize = node.children.length;
        for (var i = 0; i < node.children.length; i++) {
            if (rowsLevel === 0){
                if (childrenSize > 1 && i < (childrenSize - 1)){
                    rowsLevelStructure = '├'
                }else {
                    rowsLevelStructure = '└'
                }
            }else {
                const nbsp = initNbsp(rowsLevel);
                if (childrenSize > 1 && i < (childrenSize - 1)){
                    rowsLevelStructure = nbsp + '├'
                }else {
                    rowsLevelStructure = nbsp + '└'
                }
            }
            //从li拼接
            leftNodeRowsHtml += initLeftNodeRowsInfo(node.children[i], (rowsLevel + 1), rowsLevelStructure);
        }
    }
    return leftNodeRowsHtml;
}

function initLeftNodeCostInfo(node, costLevel, costLevelStructure) {
    var leftNodeCostHtml = '';
    //百分比计算 保留四位小数
    const selfCostPercentage = node.selfCostContributionInOverAllPlan;
    const costLeftWidth = selfCostPercentage.toFixed(4);
    const costWidthRight = percentage - costLeftWidth;
    leftNodeCostHtml += '<tr data-tippy-content="cost: ' + node.selfCost.toFixed(3) + '"' +
        ' class="no-focus-outline node" >' +
        '   <td class="node-index">' +
        '       <a class="font-weight-normal small">#' + leftCostCount + '</a>' +
        '   </td>' +
        '   <td class="node-type pr-2"><span class="tree-lines">' + costLevelStructure + '</span>' + " " + node.nodeType +
        '   </td>' +
        '   <td>' +
        '      <div class="progress rounded-0 align-items-center bg-transparent" style="height: 5px;">' +
        '         <div role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"' +
        '               class="progress-bar border-secondary bg-secondary border-left"' +
        '               style="width: ' + costLeftWidth + '%; height: 5px;">' +
        '         </div>' +
        '         <div role="progressbar" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"' +
        '                class="progress-bar bg-secondary-light"' +
        '                style="width: ' + costWidthRight + '%; height: 5px;"></div>' +
        '         </div>' +
        '    </td>' +
        '</tr>';
    leftCostCount++;
    //拼接子节点
    if (node.children && node.children.length > 0) {
        const childrenSize = node.children.length;
        for (var i = 0; i < node.children.length; i++) {
            if (costLevel === 0){
                if (childrenSize > 1 && i < (childrenSize - 1)){
                    costLevelStructure = '├'
                }else {
                    costLevelStructure = '└'
                }
            }else {
                const nbsp = initNbsp(costLevel);
                if (childrenSize > 1 && i < (childrenSize - 1)){
                    costLevelStructure = nbsp + '├'
                }else {
                    costLevelStructure = nbsp + '└'
                }
            }
            //从li拼接
            leftNodeCostHtml += initLeftNodeCostInfo(node.children[i], (costLevel + 1), costLevelStructure);
        }
    }
    return leftNodeCostHtml;
}

/**
 * 解析后端获取的数据data,进行解析
 * @param node
 * @param count
 * @returns {*}
 */
function analysisNodeAndAssignNumbers(node) {
    console.log(node);
    //获取node信息 拼接相关html元素
    var htmlString = '';
    //显示内容模块信息
    var showContentHtml = '';
    //卡片详情模块
    var nodeDetail = '';
    var maxIconHtml = '';
    if (maxSelfTime > 0 && node.selfTime === maxSelfTime){
        maxIconHtml += '<span content="最慢" class="p-0  d-inline-block mb-0 ml-1 text-nowrap alert c-2" tabindex="0"><i class="fa fa-fw fa-clock"></i></span>'
    }
    if (maxSelfCost > 0 && node.selfCost === maxSelfCost){
        maxIconHtml += '<span content="开销最大" class="p-0  d-inline-block mb-0 ml-1 text-nowrap alert c-2" tabindex="0"><i class="fa fa-fw fa-dollar-sign"></i></span>';
    }
    //行数不为0
    if (maxSelfRows > 0 && node.actualRows === maxSelfRows){
        maxIconHtml += '<span content="扫描行数最多" class="p-0  d-inline-block mb-0 ml-1 text-nowrap alert c-3" tabindex="0"><i class="fa fa-fw fa-align-justify"></i></span>';
    }
    htmlString += '<ul class="main-plan p-2 mb-0"><li>';
    htmlString += '<div class=""><div class="text-left plan-node">' +
        '<div class="collapse-handle"><i title="Collpase or expand child nodes" class="fa fa-fw fa-compress"></i></div>';
    //填充卡片数据 -----> 卡片编号模块 例如 #1
    htmlString += '<div class="plan-node-body card">' +
        '<div class="card-body header no-focus-outline">' +
        '    <header class="mb-0">' +
        '         <h4 class="text-body">' +
        '             <a class="font-weight-normal small" style="padding-right: 2px;">' + '#' + nodeCount + '</a>' + node.nodeType +
        '         </h4>' +
        '         <div class="float-right">' + maxIconHtml + '</div>' +
        '    </header>' +
        '    <div class="clearfix"></div>';
    //填充卡片数据  -----> 显示内容模块 与右侧显示内容按钮[none|time|cost|row]联动部分
    showContentHtml = initShowContentHtml(node.selfTime, node.selfTimeContributionInOverAllPlan, node.selfCost, node.selfCostContributionInOverAllPlan, node.actualRows, node.selfRowContributionInOverAllPlan);
    htmlString += showContentHtml;
    htmlString += '</div>';
    //填充卡片数据  -----> 卡片详情模块[一般，输出，详情]
    nodeDetail = initNodeDetail(node);
    htmlString += nodeDetail;
    htmlString += '</div></div>'; //plan-node-body card 对应的结尾div text-left plan-node 对应的结尾div
    nodeCount++;
    //拼接子节点
    if (node.children && node.children.length > 0) {
        htmlString += '<ul class="node-children">';
        for (var i = 0; i < node.children.length; i++) {
            //从li拼接
            htmlString += assignNodeNumbers(node.children[i]);
        }
        htmlString += '</ul>';
    }
    htmlString += '</div>' +
        '    </li>' +
        '</ul>';
    return htmlString;
}

/**
 * 设置子节点拼接
 */
function assignNodeNumbers(node) {
    //获取node信息 拼接相关html元素
    var htmlDetail = '';
    //显示内容模块信息
    var showContentHtml = '';
    //卡片详情模块
    var nodeDetail = '';
    var maxIconHtml = '';
    if (maxSelfTime > 0 && node.selfTime === maxSelfTime){
        maxIconHtml += '<span content="最慢" class="p-0  d-inline-block mb-0 ml-1 text-nowrap alert c-2" tabindex="0"><i class="fa fa-fw fa-clock"></i></span>'
    }
    if (maxSelfCost > 0 && node.selfCost === maxSelfCost){
        maxIconHtml += '<span content="开销最大" class="p-0  d-inline-block mb-0 ml-1 text-nowrap alert c-2" tabindex="0"><i class="fa fa-fw fa-dollar-sign"></i></span>';
    }
    if (maxSelfRows !== 0 && node.actualRows === maxSelfRows){
        maxIconHtml += '<span content="扫描行数最多" class="p-0  d-inline-block mb-0 ml-1 text-nowrap alert c-3" tabindex="0"><i class="fa fa-fw fa-align-justify"></i></span>';
    }
    htmlDetail += '<li>' +
        '             <div class="">\n' +
        '                   <div class="text-left plan-node">\n' +
        '                         <div class="collapse-handle">\n' +
        '                               <i title="Collpase or expand child nodes" class="fa fa-fw fa-compress"></i>\n' +
        '                         </div>';
    //填充卡片数据 -----> 卡片编号模块 例如 #2
    htmlDetail += '<div class="plan-node-body card">' +
        '<div class="card-body header no-focus-outline">' +
        '    <header class="mb-0">' +
        '         <h4 class="text-body">' +
        '             <a class="font-weight-normal small" style="padding-right: 2px;">' + '#' + nodeCount + '</a>' + node.nodeType +
        '         </h4>' +
        '         <div class="float-right">' + maxIconHtml + '</div>' +
        '    </header>' +
        '    <div class="clearfix"></div>';
    //填充卡片数据  -----> 显示内容模块 与右侧显示内容按钮[none|time|cost|row]联动部分
    showContentHtml = initShowContentHtml(node.selfTime, node.selfTimeContributionInOverAllPlan, node.selfCost, node.selfCostContributionInOverAllPlan, node.actualRows, node.selfRowContributionInOverAllPlan);
    htmlDetail += showContentHtml;
    htmlDetail += '</div>';
    //填充卡片数据  -----> 卡片详情模块[一般，输出，详情]
    nodeDetail = initNodeDetail(node);
    htmlDetail += nodeDetail;
    htmlDetail += '</div></div>'; //plan-node-body card 对应的结尾div text-left plan-node 对应的结尾div
    nodeCount++;
    //拼接子节点
    if (node.children && node.children.length > 0) {
        htmlDetail += '<ul class="node-children">';
        for (var i = 0; i < node.children.length; i++) {
            //从li拼接
            htmlDetail += assignNodeNumbers(node.children[i]);
        }
        htmlDetail += '</ul>'
    }
    htmlDetail += '</div>' +
        '    </li>';
    return htmlDetail;
}

/**
 * 处理显示内容
 * @param selfTime
 * @param selfTimeContribution
 * @param selfCost
 * @param selfCostContribution
 * @param selfRows
 * @param selfRowContribution
 */
function initShowContentHtml(selfTime, selfTimeContribution, selfCost, selfCostContribution, selfRows, selfRowContribution){
    var showContentHtml = '';
    //time
    var time_width;
    var time_color;
    var time_fixed;
    const selfTimePercentage = selfTimeContribution;
    if (selfTimePercentage <= 20) {
        time_color = background_color_20;
    } else if (selfTimePercentage > 20 && selfTimePercentage <= 40) {
        time_color = background_color_40;
    } else if (selfTimePercentage > 40 && selfTimePercentage <= 60) {
        time_color = background_color_60;
    } else if (selfTimePercentage > 60 && selfTimePercentage <= 80) {
        time_color = background_color_80;
    } else if (selfTimePercentage > 80 && selfTimePercentage < 100) {
        time_color = background_color_99;
    } else {
        time_color = background_color_100;
    }
    time_width = selfTimePercentage.toFixed(4); // 保留四位小数
    //时间-小数点保留3位
    time_fixed = selfTime.toFixed(3);
    console.log("node" + nodeCount + ", time: " + time_fixed + ", timeOver: " + selfTimePercentage + ", time_width: " + time_width);
    showContentHtml += '<div class="node-bar-show-content time" style="display: none" >' +
        '<div class="progress node-bar-container"\ style="height: 5px;">' +
        '    <div role="progressbar" aria-valuenow="0"' +
        '         aria-valuemin="0" aria-valuemax="100"' +
        '         class="progress-bar"' +
        '         style="width: ' + time_width + '%; background-color: ' + time_color + ';"></div>' +
        '    </div>' +
        '    <span class="node-bar-label"><span class="text-muted">time:</span>&nbsp;<span>' + time_fixed + 'ms</span></span>' +
        '</div>';
    //rows
    var rows_width;
    var rows_color;
    var rows_fixed;
    const selfRowPercentage = selfRowContribution;
    if (selfRowPercentage <= 20) {
        rows_color = background_color_20;
    } else if (selfRowPercentage > 20 && selfRowPercentage <= 40) {
        rows_color = background_color_40;
    } else if (selfRowPercentage > 40 && selfRowPercentage <= 60) {
        rows_color = background_color_60;
    } else if (selfRowPercentage > 60 && selfRowPercentage <= 80) {
        rows_color = background_color_80;
    } else if (selfRowPercentage > 80 && selfRowPercentage < 100) {
        rows_color = background_color_99;
    } else {
        rows_color = background_color_100;
    }
    rows_width = selfRowPercentage.toFixed(4);
    //行数 保留整数位
    rows_fixed = selfRows;
    console.log("node" + nodeCount + ", rows: " + rows_fixed + ", rowsOver: " + selfRowPercentage + ", rows_width: " + rows_width);
    showContentHtml += '<div class="node-bar-show-content rows" style="display: none" >\n' +
        '  <div class="progress node-bar-container"\ style="height: 5px;">\n' +
        '    <div role="progressbar" aria-valuenow="0"\n' +
        '         aria-valuemin="0" aria-valuemax="100"\n' +
        '         class="progress-bar"\n' +
        '         style="width: ' + rows_width + '%; background-color: ' + rows_color + ';">' +
        '    </div>' +
        '   </div>\n' +
        '   <span class="node-bar-label"><span class="text-muted">rows:</span>&nbsp;<span>' + rows_fixed + '</span></span>\n' +
        '</div>';
    //cost
    var cost_color;
    var cost_width;
    var cost_fixed;
    const selfCostPercentage = selfCostContribution;
    if (selfCostPercentage <= 20) {
        cost_color = background_color_20;
    } else if (selfCostPercentage > 20 && selfCostPercentage <= 40) {
        cost_color = background_color_40;
    } else if (selfCostPercentage > 40 && selfCostPercentage <= 60) {
        cost_color = background_color_60;
    } else if (selfCostPercentage > 60 && selfCostPercentage <= 80) {
        cost_color = background_color_80;
    } else if (selfCostPercentage > 80 && selfCostPercentage < 100) {
        cost_color = background_color_99;
    } else {
        cost_color = background_color_100;
    }
    cost_width = selfCostPercentage.toFixed(4); // 四舍五入只保留整数位
    //开销 保留3位小数点
    cost_fixed = selfCost.toFixed(3);
    console.log("node" + nodeCount + ", cost: " + cost_fixed + ", costOver: " + selfCostPercentage + ", cost_width: " + cost_width);
    showContentHtml += '<div class="node-bar-show-content cost" style="display: none" >\n' +
        '<div class="progress node-bar-container"\ style="height: 5px;">\n' +
        '    <div role="progressbar" aria-valuenow="0"\n' +
        '         aria-valuemin="0" aria-valuemax="100"\n' +
        '         class="progress-bar"\n' +
        '         style="width: ' + cost_width + '%; background-color: ' + cost_color + ';"></div>\n' +
        '    </div>\n' +
        '    <span class="node-bar-label"><span class="text-muted">cost:</span>&nbsp;<span>' + cost_fixed + '</span></span>\n' +
        '</div>';
    return showContentHtml;
}

function initNodeDetail(node) {
    var nodeDetail = '<div class="card-header border-top" style="display: none">';
    //详情页签头
    const nodeExplain = nodeTypeExplain(node.nodeType);
    if (nodeExplain !== ""){
        nodeDetail += '<div class="node-description">' +
            '               <span class="node-type">' + node.nodeType + '</span>' +
            '&nbsp;<span>' + nodeExplain + '</span>' +
            '           </div>';
    }
    //增加对输出内容的判断
    var outputHeader = '';
    if (node.output && node.output.length > 0) {
        outputHeader = 'nav-link-test';
    }else{
        outputHeader = 'nav-link-test disabled';
    }
    nodeDetail += '   <ul class="nav nav-tabs card-header-tabs">' +
        '                   <li class="nav-item"><a class="nav-link-test active">一般</a></li>';
    nodeDetail +=  '        <li class="nav-item"><a class="' + outputHeader + '">输出</a></li>' +
        '                   <li class="nav-item"><a class="nav-link-test">详情</a></li>' +
        '              </ul>' +
        '         </div>';
    //详情内容
    nodeDetail += '<div class="card-body tab-content" style="display: none">';
    //详情内容 ---> 一般页签内容
    nodeDetail += '<div class="tab-pane  show active">' +
        '              <div><i class="fa fa-fw fa-clock text-muted"></i> <b>Timing:</b>&nbsp;' +
        '                    <span class="p-0 px-1 rounded alert false">' + node.selfTime.toFixed(3) +'ms</span>' +
        '                    |' +
        '                    <strong>' + Math.round(node.selfTimeContributionInOverAllPlan) + '</strong><span class="text-muted">%</span>' +
        '               </div>' +
        '               <div>' +
        '                    <i class="fa fa-fw fa-align-justify text-muted"></i>' +
        '                    <b>Rows:</b>' +
        '                    <span class="px-1">' + node.actualRows + '</span>' +
        '                    <span class="text-muted">(Planned:' + node.planRows + ')</span>' +
        '                </div>' +
        '                <div>' +
        '                     <i class="fa fa-fw fa-dollar-sign text-muted"></i>' +
        '                     <b>Cost:</b> <span class="p-0 px-1 mr-1 alert false">' + node.selfCost.toFixed(3) + '</span>' +
        '                     <span class="text-muted">(Total: ' + node.totalCost.toFixed(2) + ')</span>' +
        '                </div>' +
        '           </div>';
    //详情内容 ---> 输出页签内容
    nodeDetail += '<div class="tab-pane overflow-auto text-monospace" style="max-height: 200px;">' +
        '<ul class="list-unstyled">';
    if (node.output && node.output.length > 0) {
        for (var i = 0; i < node.output.length; i++) {
            //从li拼接
            nodeDetail += '<li>' + node.output[i] + '</li>';
        }
    }
    nodeDetail += '</ul></div>';
    //详情内容 ---> 详情页签内容
    nodeDetail += '<div class="tab-pane">' +
        '              <table class="table table-sm prop-list">' +
        '                  <tr>' +
        '                      <td width="40%">Startup Cost</td>' +
        '                      <td>' + node.startupCost.toFixed(3) + '</td>' +
        '                  </tr>' +
        '                  <tr>' +
        '                      <td width="40%">Plan Width</td>' +
        '                      <td>' + node.planWidth.toFixed(2) + '&nbsp;Bytes</td>' +
        '                  </tr>' +
        '                  <tr>' +
        '                      <td width="40%">Actual Startup Time</td>' +
        '                      <td>' + node.actualStartupTime.toFixed(3) + 'ms</td>' +
        '                  </tr>' +
        '                  <tr>' +
        '                     <td width="40%">Actual Total Time</td>' +
        '                     <td>' +  node.actualTotalTime.toFixed(3) + 'ms</td>' +
        '                  </tr>';

    //新增其他字段拼接 Parent Relationship | Relation Name | Schema | Alias | filter
    if (node.parentRelationship !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Parent Relationship</td>' +
            '<td>' + node.parentRelationship + '</td>' +
            '</tr>';
    }
    if (node.relationName !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Relation Name</td>' +
            '<td>' + node.relationName + '</td>' +
            '</tr>';
    }
    /*if (node.schema !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Schema</td>' +
            '<td>' + node.schema + '</td>' +
            '</tr>';
    }*/
    if (node.alias !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Alias</td>' +
            '<td>' + node.alias + '</td>' +
            '</tr>';
    }
    //排序信息 Sort Key | Sort Method | Sort Space Used | Sort Space Type
    if (node.sortKey !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Sort Key</td>' +
            '<td>' + node.sortKey + '</td>' +
            '</tr>';
    }
    if (node.sortMethod !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Sort Method</td>' +
            '<td>' + node.sortMethod + '</td>' +
            '</tr>';
    }
    if (node.sortSpaceUsed && node.sortSpaceUsed !== 0){
        nodeDetail += '<tr>' +
            '<td width="40%">Sort Space Used</td>' +
            '<td>' + node.sortSpaceUsed + 'KB</td>' +
            '</tr>';
    }
    if (node.sortSpaceType !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Sort Space Type</td>' +
            '<td>' + node.sortSpaceType + '</td>' +
            '</tr>';
    }
    //Index相关 Scan Direction | indexName | Index Cond
    if (node.scanDirection !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Scan Direction</td>' +
            '<td>' + node.scanDirection + '</td>' +
            '</tr>';
    }
    /*if (node.indexName !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Index Name</td>' +
            '<td>' + node.indexName + '</td>' +
            '</tr>';
    }*/
    if (node.indexCond !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Index Cond</td>' +
            '<td>' + node.indexCond + '</td>' +
            '</tr>';
    }

    if (node.filter !== ""){
        nodeDetail += '<tr>' +
            '<td width="40%">Filter</td>' +
            '<td>' + node.filter + '</td>' +
            '</tr>';
    }
    nodeDetail += '   </table>' +
        '         </div>';
    nodeDetail +='</div>';
    return nodeDetail;
}


function initElementEvents() {
    // 获取样式按钮组
    var styleBtnGroup = document.getElementById('btn_style');
    // 获取按钮列表[2D | 经典]
    var stylesButtons = styleBtnGroup.getElementsByTagName('button');
    //获取方位设置模块id
    var orientationDiv = document.getElementById('orientation');
    //中间节点 root节点li下div元素
    var listDiv = document.querySelector('.main-plan li div');
    //中间节点 children节点li下div元素
    var childListDiv = document.querySelector('.node-children li div');

    //-------------------------------右侧设置栏操作与中间模块的联动效果--------------------------------------------
    //为样式按钮添加点击事件
    for (var i = 0; i < stylesButtons.length; i++) {
        stylesButtons[i].addEventListener('click', function() {
            // 切换按钮样式
            for (var j = 0; j < stylesButtons.length; j++) {
                if (stylesButtons[j] === this) {
                    // 添加active样式
                    stylesButtons[j].classList.add('active');
                } else {
                    // 移除active样式
                    stylesButtons[j].classList.remove('active');
                }
            }
            // 判断是2D对应的按钮还是经典按钮
            if (this.id === 'btn_style_2D') {
                // 执行2D按钮对应的处理逻辑
                orientationDiv.classList.add('twod');
                orientationDiv.classList.remove('classic');
                listDiv.setAttribute('style', 'd-flex flex-column align-items-center');
                childListDiv.setAttribute('style', 'd-flex flex-column align-items-center');
            } else if (this.id === 'btn_style_classic') {
                // 执行经典按钮对应的处理逻辑
                orientationDiv.classList.add('classic');
                orientationDiv.classList.remove('twod');
                listDiv.removeAttribute('style');
                childListDiv.removeAttribute('style');
            }
        });
    }
    // 获取展示按钮组
    var btnGroup = document.getElementById('btn_show_content');
    // 获取显示内容按钮列表
    var showContentButtons = btnGroup.getElementsByTagName('button');
    //中间节点部分 显示内容的div
    var planNodeShowContentTime = document.querySelectorAll('.node-bar-show-content.time');
    var planNodeShowContentRows = document.querySelectorAll('.node-bar-show-content.rows');
    var planNodeShowContentCost = document.querySelectorAll('.node-bar-show-content.cost');

    // 为显示内容按钮添加点击事件
    for (var s = 0; s < showContentButtons.length; s++) {
        showContentButtons[s].addEventListener('click', function() {
            for (var t = 0; t < showContentButtons.length; t++) {
                if (showContentButtons[t] === this) {
                    // 添加active样式
                    showContentButtons[t].classList.add('active');
                } else {
                    // 移除active样式
                    showContentButtons[t].classList.remove('active');
                }
            }
            if (this.id === 'show_content_none') {
                for (var showNumber = 0; showNumber < planNodeShowContentTime.length; showNumber++){
                    planNodeShowContentTime[showNumber].style.display = 'none';
                    planNodeShowContentRows[showNumber].style.display = 'none';
                    planNodeShowContentCost[showNumber].style.display = 'none';
                }
            }else if (this.id === 'show_content_time') {
                for (var showNumber = 0; showNumber < planNodeShowContentTime.length; showNumber++){
                    planNodeShowContentTime[showNumber].style.display = 'block';
                    planNodeShowContentRows[showNumber].style.display = 'none';
                    planNodeShowContentCost[showNumber].style.display = 'none';
                }
            }else if (this.id === 'show_content_rows') {
                for (var showNumber = 0; showNumber < planNodeShowContentTime.length; showNumber++){
                    planNodeShowContentTime[showNumber].style.display = 'none';
                    planNodeShowContentRows[showNumber].style.display = 'block';
                    planNodeShowContentCost[showNumber].style.display = 'none';
                }
            }else if (this.id === 'show_content_cost') {
                for (var showNumber = 0; showNumber < planNodeShowContentTime.length; showNumber++){
                    planNodeShowContentTime[showNumber].style.display = 'none';
                    planNodeShowContentRows[showNumber].style.display = 'none';
                    planNodeShowContentCost[showNumber].style.display = 'block';
                }
            }
        });
    }
    //---------------------------------------中间模块联动效果--------------------------------------------------------
    // 获取节点
    var planNodes = document.querySelectorAll('.plan-node');
    for (var j = 0; j < planNodes.length; j++) {
        const planNode = planNodes[j];
        const planBodyHeader = planNode.querySelector('.no-focus-outline');
        // 节点下card-header card-content
        const planCardHeader = planNode.querySelector('.border-top');
        const planCardBody = planNode.querySelector('.tab-content');
        // 找到当前 card-header 下的 tab-links 和 tab-panes
        const tabLinks = planCardHeader.querySelectorAll('.nav-link-test');
        const tabPanes = planCardHeader.nextElementSibling.querySelectorAll('.tab-pane');

        // 添加点击事件处理程序
        planBodyHeader.addEventListener('click', function() {
            // 切换 detail 样式
            // 如果包含 detail 样式，则显示 card-header 和 card-body
            if (planNode.classList.contains('detail')) {
                planNode.classList.remove('detail');
                planCardHeader.style.display = 'none';
                planCardBody.style.display = 'none';
                planNode.style.width = '';
            } else {
                planNode.classList.add('detail');
                planCardHeader.style.display = 'block';
                planCardBody.style.display = 'block';
                //展示卡片详情
                planNode.style.width = '400px';
            }
        });
        //卡片tab
        for (var k = 0; k < tabLinks.length; k++){
            const link = tabLinks[k];
            link.addEventListener('click', function() {
                // 移除其他选项的 active 样式
                for (var m = 0; m < tabLinks.length; m++) {
                    if (tabLinks[m] === this) {
                        // 添加active样式
                        tabLinks[m].classList.add('active');
                        tabPanes[m].classList.add('show', 'active');
                    } else {
                        // 移除active样式
                        tabLinks[m].classList.remove('active');
                        tabPanes[m].classList.remove('show', 'active');
                    }
                }
            });
        }

    }

    //获取所有的no-focus-outline.node样式的tr
    var iconSpans = document.querySelectorAll('div.float-right span');
    // 遍历每一行，并为其添加鼠标进入和离开事件
    for (var icon = 0; icon < iconSpans.length; icon++){
        // 鼠标进入时显示提示信息
        var iconSpan =  iconSpans[icon];
        const tooltipContent = iconSpan.getAttribute('content');
        tippy(iconSpan, {
            content: tooltipContent,
            placement: 'top',
        });
    }

    //----------------------------------------左侧联动JS----------------------------------------------------------

    //获取左侧显示内容按钮组
    var leftButtonGroup = document.getElementById('left-button-group');
    //获取左侧所有按钮
    var leftButtons = leftButtonGroup.querySelectorAll('.btn-outline-secondary');
    //左侧table模块[time | rows | cost]
    var leftTableTime = document.getElementById('left_table_time');
    var leftTableRows = document.getElementById('left_table_rows');
    var leftTableCost = document.getElementById('left_table_cost');
    for (var left = 0; left < leftButtons.length; left++){
        leftButtons[left].addEventListener('click', function() {
            for (var lefts = 0; lefts < leftButtons.length; lefts++) {
                if (leftButtons[lefts] === this) {
                    // 添加active样式
                    leftButtons[lefts].classList.add('active');
                } else {
                    // 移除active样式
                    leftButtons[lefts].classList.remove('active');
                }
            }
            if (this.id === 'left-button-time'){
                leftTableTime.style.display = 'block';
                leftTableRows.style.display = 'none';
                leftTableCost.style.display = 'none';
            }else if(this.id === 'left-button-rows'){
                leftTableTime.style.display = 'none';
                leftTableRows.style.display = 'block';
                leftTableCost.style.display = 'none';
            }else if (this.id === 'left-button-cost'){
                leftTableTime.style.display = 'none';
                leftTableRows.style.display = 'none';
                leftTableCost.style.display = 'block';
            }
        });
    }

    //获取所有的no-focus-outline.node样式的tr
    var tableRows = document.querySelectorAll('tr.no-focus-outline.node');
    // 遍历每一行，并为其添加鼠标进入和离开事件
    for (var row = 0; row < tableRows.length; row++){
        var tableRow =  tableRows[row];
        // 鼠标进入时高亮显示
        var tooltipContent = tableRow.getAttribute('data-tippy-content');
        tippy(tableRow, {
            content: tooltipContent,
            placement: 'top',
        });
        tableRow.addEventListener('mouseenter', function() {
            this.classList.add('highlight');
        });
        // 鼠标离开时去除高亮
        tableRow.addEventListener('mouseleave', function() {
            this.classList.remove('highlight');
        });
    }
}

function initNbsp(level) {
    var nbps = '';
    if (level > 0){
        for (var i=0; i < level; i++){
            nbps +='&nbsp;';
        }
    }
    return nbps;
}
