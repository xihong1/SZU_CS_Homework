(function (t) {
    function e(e) {
        for (var a, r, i = e[0], l = e[1], c = e[2], u = 0, d = []; u < i.length; u++) r = i[u], Object.prototype.hasOwnProperty.call(o, r) && o[r] && d.push(o[r][0]), o[r] = 0;
        for (a in l) Object.prototype.hasOwnProperty.call(l, a) && (t[a] = l[a]);
        p && p(e);
        while (d.length) d.shift()();
        return s.push.apply(s, c || []), n()
    }

    function n() {
        for (var t, e = 0; e < s.length; e++) {
            for (var n = s[e], a = !0, r = 1; r < n.length; r++) {
                var l = n[r];
                0 !== o[l] && (a = !1)
            }
            a && (s.splice(e--, 1), t = i(i.s = n[0]))
        }
        return t
    }

    var a = {}, o = {index: 0}, s = [];

    function r(t) {
        return i.p + "js/" + ({}[t] || t) + "." + {
            "chunk-2d0a3abc": "bf57648b",
            "chunk-2d0a3cca": "be22d60f",
            "chunk-2d0b5e13": "26cf3328",
            "chunk-2d0b8eae": "a739dd68",
            "chunk-2d0b9432": "47df4291",
            "chunk-2d0b9fd3": "1d97f4de",
            "chunk-2d0cf715": "d0d91b81",
            "chunk-2d0de754": "34dcecb7",
            "chunk-2d0e4fb4": "9c27cda1",
            "chunk-2d0e6ca3": "ed9891fa",
            "chunk-2d208143": "dc6a665b",
            "chunk-2d20935b": "cd160e4f",
            "chunk-2d21d7f9": "47de21d4",
            "chunk-2d225642": "c050b224",
            "chunk-2d2290b1": "d7910a3f",
            "chunk-2d22bf8b": "7f9c8f96",
            "chunk-2d2304f6": "c0330358",
            "chunk-2d237163": "a091eff5",
            "chunk-2d23756e": "30e2d570",
            "chunk-2d237b34": "cdc7bb70"
        }[t] + ".js"
    }

    function i(e) {
        if (a[e]) return a[e].exports;
        var n = a[e] = {i: e, l: !1, exports: {}};
        return t[e].call(n.exports, n, n.exports, i), n.l = !0, n.exports
    }

    i.e = function (t) {
        var e = [], n = o[t];
        if (0 !== n) if (n) e.push(n[2]); else {
            var a = new Promise((function (e, a) {
                n = o[t] = [e, a]
            }));
            e.push(n[2] = a);
            var s, l = document.createElement("script");
            l.charset = "utf-8", l.timeout = 120, i.nc && l.setAttribute("nonce", i.nc), l.src = r(t);
            var c = new Error;
            s = function (e) {
                l.onerror = l.onload = null, clearTimeout(u);
                var n = o[t];
                if (0 !== n) {
                    if (n) {
                        var a = e && ("load" === e.type ? "missing" : e.type), s = e && e.target && e.target.src;
                        c.message = "Loading chunk " + t + " failed.\n(" + a + ": " + s + ")", c.name = "ChunkLoadError", c.type = a, c.request = s, n[1](c)
                    }
                    o[t] = void 0
                }
            };
            var u = setTimeout((function () {
                s({type: "timeout", target: l})
            }), 12e4);
            l.onerror = l.onload = s, document.head.appendChild(l)
        }
        return Promise.all(e)
    }, i.m = t, i.c = a, i.d = function (t, e, n) {
        i.o(t, e) || Object.defineProperty(t, e, {enumerable: !0, get: n})
    }, i.r = function (t) {
        "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {value: "Module"}), Object.defineProperty(t, "__esModule", {value: !0})
    }, i.t = function (t, e) {
        if (1 & e && (t = i(t)), 8 & e) return t;
        if (4 & e && "object" === typeof t && t && t.__esModule) return t;
        var n = Object.create(null);
        if (i.r(n), Object.defineProperty(n, "default", {
            enumerable: !0,
            value: t
        }), 2 & e && "string" != typeof t) for (var a in t) i.d(n, a, function (e) {
            return t[e]
        }.bind(null, a));
        return n
    }, i.n = function (t) {
        var e = t && t.__esModule ? function () {
            return t["default"]
        } : function () {
            return t
        };
        return i.d(e, "a", e), e
    }, i.o = function (t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, i.p = "", i.oe = function (t) {
        throw console.error(t), t
    };
    var l = window["webpackJsonp"] = window["webpackJsonp"] || [], c = l.push.bind(l);
    l.push = e, l = l.slice();
    for (var u = 0; u < l.length; u++) e(l[u]);
    var p = c;
    s.push([0, "chunk-vendors"]), n()
})({
    0: function (t, e, n) {
        t.exports = n("c605")
    }, "0624": function (t, e, n) {
        "use strict";
        var a = n("416c"), o = n.n(a);
        o.a
    }, 1: function (t, e) {
    }, "1dfb": function (t, e, n) {
        var a = n("24fb");
        e = a(!1), e.push([t.i, ".dropzone-over{-webkit-box-shadow:0 0 5px #51cbee;box-shadow:0 0 5px #51cbee;border:1px solid #51cbee}", ""]), t.exports = e
    }, 2: function (t, e) {
    }, 2883: function (t, e, n) {
        var a = n("7617");
        "string" === typeof a && (a = [[t.i, a, ""]]), a.locals && (t.exports = a.locals);
        var o = n("499e").default;
        o("5da5e98c", a, !0, {sourceMap: !1, shadowMode: !1})
    }, "30b8": function (t, e, n) {
        "use strict";
        var a = function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("main-layout", [n("div", {staticClass: "container"}, [n("div", {staticClass: "alert alert-warning"}, [t._v("\n    This is the demo application for "), n("a", {attrs: {href: "https://github.com/dalibo/pev2"}}, [t._v("PEV2")]), t._v(". It is serverless and doesn't store your plans.\n    "), n("br"), t._v("\n    Please consider using "), n("a", {attrs: {href: "https://explain.dalibo.com"}}, [t._v("explain.dalibo.com")]), t._v(" instead if you want to save or share your plans.\n  ")]), t._v(" "), n("div", {staticClass: "row"}, [n("div", {staticClass: "col d-flex"}, [n("div", {staticClass: "text-muted"}, [t._v("\n        For best results, use "), n("code", [t._v("EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)")]), t._v(" "), n("br"), t._v(" "), n("em", [t._v("psql")]), t._v(" users can export the plan to a file using "), n("code", [t._v("psql -XqAt -f explain.sql > analyze.json")])]), t._v(" "), n("div", {staticClass: "dropdown ml-auto"}, [n("button", {
                staticClass: "btn btn-secondary dropdown-toggle",
                attrs: {
                    type: "button",
                    id: "dropdownMenuButton",
                    "data-toggle": "dropdown",
                    "aria-haspopup": "true",
                    "aria-expanded": "false"
                }
            }, [t._v("\n          Sample Plans\n        ")]), t._v(" "), n("div", {
                staticClass: "dropdown-menu",
                attrs: {"aria-labelledby": "dropdownMenuButton"}
            }, t._l(t.samples, (function (e, a) {
                return n("a", {
                    staticClass: "dropdown-item", attrs: {href: ""}, on: {
                        click: function (n) {
                            return n.preventDefault(), t.loadSample(e)
                        }
                    }
                }, [t._v("\n            " + t._s(e[0]) + "\n          ")])
            })), 0)])])]), t._v(" "), n("form", {
                on: {
                    submit: function (e) {
                        return e.preventDefault(), t.submitPlan.apply(null, arguments)
                    }
                }
            }, [n("div", {staticClass: "form-group"}, [n("label", {attrs: {for: "planInput"}}, [t._v("Plan "), n("span", {staticClass: "small text-muted"}, [t._v("(text or JSON)")])]), t._v(" "), n("textarea", {
                directives: [{
                    name: "model",
                    rawName: "v-model",
                    value: t.planInput,
                    expression: "planInput"
                }],
                class: ["form-control", t.draggingPlan ? "dropzone-over" : ""],
                attrs: {id: "planInput", rows: "8", placeholder: "Paste execution plan\\nOr drop a file"},
                domProps: {value: t.planInput},
                on: {
                    dragenter: function (e) {
                        t.draggingPlan = !0
                    }, dragleave: function (e) {
                        t.draggingPlan = !1
                    }, drop: function (e) {
                        return e.preventDefault(), t.handleDrop.apply(null, arguments)
                    }, input: function (e) {
                        e.target.composing || (t.planInput = e.target.value)
                    }
                }
            })]), t._v(" "), n("div", {staticClass: "form-group"}, [n("label", {attrs: {for: "queryInput"}}, [t._v("Query "), n("span", {staticClass: "small text-muted"}, [t._v("(optional)")])]), t._v(" "), n("textarea", {
                directives: [{
                    name: "model",
                    rawName: "v-model",
                    value: t.queryInput,
                    expression: "queryInput"
                }],
                class: ["form-control", t.draggingQuery ? "dropzone-over" : ""],
                attrs: {id: "queryInput", rows: "8", placeholder: "Paste corresponding SQL query\\nOr drop a file"},
                domProps: {value: t.queryInput},
                on: {
                    dragenter: function (e) {
                        t.draggingQuery = !0
                    }, dragleave: function (e) {
                        t.draggingQuery = !1
                    }, drop: function (e) {
                        return e.preventDefault(), t.handleDrop.apply(null, arguments)
                    }, input: function (e) {
                        e.target.composing || (t.queryInput = e.target.value)
                    }
                }
            })]), t._v(" "), n("button", {
                staticClass: "btn btn-primary",
                attrs: {type: "submit"}
            }, [t._v("Submit")])])])])
        }, o = [], s = n("9ab4"), r = n("60a3"), i = n("4f32"), l = n("c605");

        function c(t) {
            return c = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, c(t)
        }

        function u(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function p(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function d(t, e, n) {
            return e && p(t.prototype, e), n && p(t, n), t
        }

        function f(t, e) {
            return !e || "object" !== c(e) && "function" !== typeof e ? _(t) : e
        }

        function _(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function h(t) {
            return h = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, h(t)
        }

        function v(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && b(t, e)
        }

        function b(t, e) {
            return b = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, b(t, e)
        }

        var m = function (t) {
            function e() {
                var t;
                return u(this, e), t = f(this, h(e).apply(this, arguments)), t.samples = [["Example 1 (JSON)", "plan_1_.txt", "plan_1.sql"], ["Example 1 (plain text)", "plan_1.txt", "plan_1.sql"], ["Example 2", "plan_2.txt", "plan_2.sql"], ["Example 3", "plan_3.txt", "plan_3.sql"], ["Example 4", "plan_4.txt"], ["Example 5", "plan_5.txt", "plan_5.sql"], ["With subplan", "plan_6.txt"], ["With CTE", "plan_7.txt"], ["Very large plan", "plan_8.txt"], ["With trigger", "plan_trigger_.txt", "plan_trigger.sql"], ["With trigger (plain text)", "plan_trigger.txt", "plan_trigger_2.sql"], ["Parallel (verbose)", "plan_parallel.txt"], ["Parallel (4 workers)", "plan_parallel2.txt", "plan_parallel2.sql"]], t.planInput = "", t.queryInput = "", t.draggingPlan = !1, t.draggingQuery = !1, t
            }

            return v(e, t), d(e, [{
                key: "mounted", value: function () {
                    var t = document.getElementsByTagName("textarea");
                    Array.prototype.forEach.call(t, (function (t) {
                        t.placeholder = t.placeholder.replace(/\\n/g, "\n")
                    }));
                    var e = window.location.href.replace(/#.*$/, "");
                    window.history.replaceState("", document.title, e)
                }
            }, {
                key: "submitPlan", value: function () {
                    Object(l["setPlanData"])(this.planInput, this.queryInput)
                }
            }, {
                key: "loadSample", value: function (t) {
                    var e = this;
                    n("4ba5")("./" + t[1]).then((function (t) {
                        e.planInput = t.default
                    })), t[2] ? n("4ba5")("./" + t[2]).then((function (t) {
                        e.queryInput = t.default
                    })) : this.queryInput = ""
                }
            }, {
                key: "handleDrop", value: function (t) {
                    var e = t.srcElement;
                    if (e instanceof HTMLTextAreaElement && (this.draggingPlan = !1, this.draggingQuery = !1, t.dataTransfer)) {
                        var n = t.dataTransfer.files[0], a = new FileReader;
                        a.onload = function (t) {
                            a.result instanceof ArrayBuffer || (e.value = a.result || "", e.dispatchEvent(new Event("input")))
                        }, a.readAsText(n)
                    }
                }
            }]), e
        }(r["c"]);
        m = Object(s["a"])([Object(r["a"])({components: {MainLayout: i["a"]}})], m);
        var E = m, g = E, S = (n("0624"), n("2877")), T = Object(S["a"])(g, a, o, !1, null, null, null);
        e["a"] = T.exports
    }, "416c": function (t, e, n) {
        var a = n("1dfb");
        "string" === typeof a && (a = [[t.i, a, ""]]), a.locals && (t.exports = a.locals);
        var o = n("499e").default;
        o("b9a20a5e", a, !0, {sourceMap: !1, shadowMode: !1})
    }, "44bc": function (t, e, n) {
        "use strict";
        var a = n("2883"), o = n.n(a);
        o.a
    }, "4ba5": function (t, e, n) {
        var a = {
            "./plan_1.sql": ["fa2d", "chunk-2d237163"],
            "./plan_1.txt": ["1b7c", "chunk-2d0b5e13"],
            "./plan_1_.txt": ["31ca", "chunk-2d0b9432"],
            "./plan_2.sql": ["02bf", "chunk-2d0a3abc"],
            "./plan_2.txt": ["3171", "chunk-2d0b8eae"],
            "./plan_3.sql": ["a7a0", "chunk-2d20935b"],
            "./plan_3.txt": ["e3ca", "chunk-2d225642"],
            "./plan_4.txt": ["d20e", "chunk-2d21d7f9"],
            "./plan_5.sql": ["f0f1", "chunk-2d22bf8b"],
            "./plan_5.txt": ["8677", "chunk-2d0de754"],
            "./plan_6.txt": ["045e", "chunk-2d0a3cca"],
            "./plan_7.txt": ["dc84", "chunk-2d2290b1"],
            "./plan_8.txt": ["fb62", "chunk-2d23756e"],
            "./plan_parallel.txt": ["ec79", "chunk-2d2304f6"],
            "./plan_parallel2.sql": ["9315", "chunk-2d0e4fb4"],
            "./plan_parallel2.txt": ["6478", "chunk-2d0cf715"],
            "./plan_trigger.sql": ["fbdf", "chunk-2d237b34"],
            "./plan_trigger.txt": ["99f3", "chunk-2d0e6ca3"],
            "./plan_trigger_.txt": ["a2ea", "chunk-2d208143"],
            "./plan_trigger_2.sql": ["34fb", "chunk-2d0b9fd3"]
        };

        function o(t) {
            if (!n.o(a, t)) return Promise.resolve().then((function () {
                var e = new Error("Cannot find module '" + t + "'");
                throw e.code = "MODULE_NOT_FOUND", e
            }));
            var e = a[t], o = e[0];
            return n.e(e[1]).then((function () {
                return n(o)
            }))
        }

        o.keys = function () {
            return Object.keys(a)
        }, o.id = "4ba5", t.exports = o
    }, "4f32": function (t, e, n) {
        "use strict";
        var a = function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("div", {staticClass: "d-flex flex-column vh-100"}, [n("div", {staticClass: "navbar container flex-shrink-0"}, [n("v-link", {
                    staticClass: "btn btn-secondary ml-auto",
                    attrs: {to: "/"}
                }, [t._v("New Plan")]), t._v(" "), n("v-link", {
                    staticClass: "btn btn-link",
                    attrs: {to: "/about"}
                }, [t._v("About")])], 1), t._v(" "), t._t("default")], 2)
            }, o = [], s = function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("a", {attrs: {to: t.to, href: ""}, on: {click: t.go}}, [t._t("default")], 2)
            }, r = [], i = {
                props: {to: {type: String, required: !0}}, methods: {
                    go: function (t) {
                        t.preventDefault(), this.$root.currentRoute = this.to
                    }
                }
            }, l = i, c = n("2877"), u = Object(c["a"])(l, s, r, !1, null, null, null), p = u.exports,
            d = {components: {VLink: p}}, f = d, _ = Object(c["a"])(f, a, o, !1, null, null, null);
        e["a"] = _.exports
    }, 7617: function (t, e, n) {
        var a = n("24fb"), o = n("dda2"), s = n("2e6f"), r = n("54c0");
        e = a(!1), e.i(o), e.i(s), e.i(r), e.push([t.i, '.alert.c-1{background-color:#ccc;color:#454545;font-weight:700}.alert.c-1 .text-muted{color:#454545!important;font-weight:400}.progress-bar.c-1{background-color:#ccc;border-color:#ccc!important}.text-c-1{color:#ccc}.alert.c-2{background-color:#fddb61;color:#454545;font-weight:700}.alert.c-2 .text-muted{color:#454545!important;font-weight:400}.progress-bar.c-2{background-color:#fddb61;border-color:#fddb61!important}.text-c-2{color:#fddb61}.alert.c-3{background-color:#e80;color:#454545;font-weight:700}.alert.c-3 .text-muted{color:#454545!important;font-weight:400}.progress-bar.c-3{background-color:#e80;border-color:#e80!important}.text-c-3{color:#e80}.alert.c-4{background-color:#800;color:#fff;font-weight:700}.alert.c-4 .text-muted{color:#fff!important;font-weight:400}.progress-bar.c-4{background-color:#800;border-color:#800!important}.text-c-4{color:#800}.bg-hit{background-color:#ccc}.bg-read{background-color:#fddb61}.bg-dirtied{background-color:#e80}.bg-written{background-color:#800}.btn-group-xs>.btn,.btn-xs{padding:.25rem .4rem;font-size:12px;border-radius:.2rem}.btn-group-xs>.btn,.btn-group-xs>.btn .fa,.btn-xs,.btn-xs .fa{line-height:1.0}@-webkit-keyframes flash{0%{background:#fff}20%{background:#ffb}to{background:#fff}}@keyframes flash{0%{background:#fff}20%{background:#ffb}to{background:#fff}}.bg-hatched,.plan-node.never-executed .plan-node-body{background-image:linear-gradient(45deg,#f7f7f7 25%,transparent 0,transparent 50%,#f7f7f7 0,#f7f7f7 75%,transparent 0,transparent);background-size:1rem 1rem}.border-dashed{border-style:dashed!important;background-color:transparent!important}.line-clamp-2{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;text-overflow:ellipsis;overflow:hidden}*>.copy{display:none}:hover>.copy{display:block}.bg-secondary-light{background-color:#dedede!important}.plan-container{font-family:Noto Sans,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}.plan-container .menu{position:absolute;z-index:1;right:0}.plan-container .menu-hidden h3,.plan-container .menu-hidden ul{display:none}.plan-container .grab-bing{cursor:-webkit-grab;cursor:-o-grab;cursor:grab}.plan-container .grab-bing:active{cursor:-webkit-grabbing;cursor:-o-grabbing;cursor:grabbing}.plan-container .text-muted{color:#ababab!important}.plan-container .cursor-help{cursor:help}.plan-container pre{overflow:initial}.plan ol,.plan ul{list-style:none}.twod .plan ol,.twod .plan ul{padding:0}.twod .plan ul.main-plan,.twod .plan ul.node-children{margin-left:auto;margin-right:auto;text-align:center}.twod .plan ul.node-children{display:-webkit-box;display:-ms-flexbox;display:flex;padding-top:12px;margin-top:-5px}.plan ul.init-plans{-webkit-flex:none}.classic .plan ul:first-child{padding-left:0}.classic .plan ul:first-child>li:after,.classic .plan ul:first-child>li:before{display:none}.plan ul.node-children{position:relative;-webkit-transition:all .5s;transition:all .5s}.twod .plan ul.node-children:before{content:"";position:absolute;top:0;left:50%;border-left:2px solid #c4c4c4;height:12px;width:0}.plan ul.node-children>li{list-style-type:none;position:relative;-webkit-transition:all .5s;transition:all .5s}.twod .plan ul.node-children>li:not(:first-child){padding-left:10px}.twod .plan ul.node-children>li{padding-top:12px}.twod .plan ul.node-children>li:after,.twod .plan ul.node-children>li:before{content:"";position:absolute;top:0;right:50%;border-top:2px solid #c4c4c4;width:50%;height:12px}.twod .plan ul.node-children>li:after{right:auto;left:50%;border-left:2px solid #c4c4c4}.twod .plan ul.node-children>li:only-child{padding-top:0}.twod .plan ul.node-children>li:only-child:after,.twod .plan ul.node-children>li:only-child:before{display:none}.twod .plan ul.node-children>li:first-child:before,.twod .plan ul.node-children>li:last-child:after{border:0 none}.twod .plan ul.node-children>li:last-child:before{border-right:2px solid #c4c4c4;border-radius:0 6px 0 0}.twod .plan ul.node-children>li:first-child:after{border-radius:6px 0 0 0}.classic .plan ul.node-children>li:after,.classic .plan ul.node-children>li:before{content:"";position:absolute;left:-10px}.classic .plan ul.node-children>li:before{border-top:2px solid #c4c4c4;top:22px;width:11px;left:-10px}.classic .plan ul.node-children>li:after{border-left:2px solid #c4c4c4;height:calc(100% + 4px);width:6px;top:-5px}.classic .plan ul.node-children>li:last-child:after{height:29px;border-bottom:2px solid #c4c4c4;border-radius:0 0 0 6px}.classic .plan ul.node-children>li:last-child:before{left:-4px;width:5px}.plan ul.node-children>li .plan-node:hover+ul:before{border-color:#00b5e2}.plan ul.node-children>li .plan-node:hover+ul li:after,.plan ul.node-children>li .plan-node:hover+ul li:before,.plan ul.node-children>li .plan-node:hover+ul ul:before{border-color:#008caf}.plan ul.init-plans{padding-left:0;display:block}.twod .plan ul.init-plans{display:-webkit-box;display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.twod .plan ul.init-plans>li{margin-left:3px;margin-right:3px;margin-bottom:10px}.plan .subplan{border:1px solid #dedede;border-radius:3px;background-color:#fcfcfc;-webkit-box-shadow:1px 1px 3px 0 rgba(0,0,0,.1);box-shadow:1px 1px 3px 0 rgba(0,0,0,.1);padding:0 10px 6px 10px}.plan .subplan>h4{font-size:12px;margin-top:.5rem;font-weight:600;font-style:italic}.classic .plan .subplan{margin-bottom:3px;display:inline-block}.twod .plan .subplan{display:-webkit-inline-box;display:-ms-inline-flexbox;display:inline-flex;-webkit-box-orient:vertical;-webkit-box-direction:normal;-ms-flex-direction:column;flex-direction:column;-webkit-box-align:center;-ms-flex-align:center;align-items:center}.plan .subplan.flash{-webkit-animation:flash 1s;animation:flash 1s}.plan .btn-close{border-radius:50%;-webkit-box-shadow:0;box-shadow:0;line-height:1.5;border:1px solid #dedede;background-color:#fff;font-size:12px}.plan button .fa-chevron-right{display:inline-block}.plan button .fa-chevron-down{display:none}.plan button[aria-expanded=true] .fa-chevron-right{display:none!important}.plan button[aria-expanded=true] .fa-chevron-down{display:inline-block!important}.plan-stats{font-size:13px}.plan-stats .stat-dropdown-container{border:1px solid #dedede;padding:18px;background-color:#fff;position:absolute;-webkit-box-shadow:0 0 10px 2px rgba(0,0,0,.3);box-shadow:0 0 10px 2px rgba(0,0,0,.3);border-radius:3px;margin-bottom:18px;z-index:6;right:0;width:300px;max-height:70vh;overflow:auto}.plan-stats .stat-dropdown-container .btn-close{border-radius:50%;-webkit-box-shadow:0;box-shadow:0;line-height:1.5;border:1px solid #dedede;background-color:#fff;font-size:12px}.plan-stats .stat-dropdown-container h3{font-size:17px;width:93%;text-align:left;border-bottom:1px solid #dedede;padding-bottom:6px;margin-bottom:10px}.tippy-popper .tippy-tooltip{text-align:left}.tippy-popper .text-muted{color:inherit!important}.splitpanes__pane{-webkit-transition:none!important;transition:none!important}.no-focus-outline:focus{outline:none}.table-nonfluid{width:auto!important}.more-info[title]{-webkit-text-decoration-line:underline;text-decoration-line:underline;-webkit-text-decoration-style:dotted;text-decoration-style:dotted;-webkit-text-decoration-color:#ababab;text-decoration-color:#ababab;cursor:help}.plan-diagram{line-height:1.00em;font-family:Noto Sans,sans-serif}.plan-diagram.plan-diagram-top{max-height:30%}.plan-diagram table tr td:nth-child(3){width:90%}.plan-diagram .legend ul li{font-size:13px}.plan-diagram .legend ul li span{display:inline-block;width:8px;height:8px;border-radius:50%}.plan-diagram tbody:after{content:"";display:block;height:10px}.plan-diagram td,.plan-diagram th{margin:0;color:#4d525a;white-space:nowrap}.plan-diagram td.node-index,.plan-diagram td.node-type,.plan-diagram td.subplan,.plan-diagram th.node-index,.plan-diagram th.node-type,.plan-diagram th.subplan{font-size:13px}.plan-diagram td.node-type,.plan-diagram th.node-type{font-weight:700}.plan-diagram th{font-size:13px}.plan-diagram tr.highlight{-webkit-box-shadow:1px 1px 5px 0 rgba(0,0,0,.4);box-shadow:1px 1px 5px 0 rgba(0,0,0,.4)}.plan-diagram tr.selected{outline:1px solid #00b5e2;-webkit-box-shadow:0 0 5px 2px rgba(0,181,226,.4);box-shadow:0 0 5px 2px rgba(0,181,226,.4)}.plan-diagram tr.highlight,.plan-diagram tr.selected{background-color:#fff}.plan-diagram .tree-lines{font-family:"monospace"}.plan-node{text-decoration:none;color:#4d525a;display:inline-block;-webkit-transition:all .1s;transition:all .1s;position:relative;font-size:12px;margin-bottom:4px;overflow-wrap:break-word;word-wrap:break-word;width:400px}.twod .plan-node{width:240px}.twod.compact .plan-node{width:140px}.twod.dot .plan-node{width:50px}.plan-node .plan-node-body{position:relative;border:1px solid #dedede;border-radius:3px;background-color:#fff;-webkit-box-shadow:1px 1px 3px 0 rgba(0,0,0,.1);box-shadow:1px 1px 3px 0 rgba(0,0,0,.1);cursor:auto}.plan-node .plan-node-body .header.card-body{cursor:pointer}.plan-node .plan-node-body .header.card-body:hover{background-color:#f7f7f7}.plan-node .plan-node-body.card .card-body,.plan-node .plan-node-body.card .card-header{padding:6px 10px}.plan-node .plan-node-body.card .card-header .card-header-tabs{margin-right:0;margin-left:0;margin-bottom:-6px;margin-top:6px}.plan-node .plan-node-body.card .card-header .card-header-tabs .nav-link{padding:3px 10px}.plan-node.parallel .plan-node-body{-webkit-box-shadow:none;box-shadow:none}.plan-node header{margin-bottom:6px;overflow:hidden}.plan-node header h4{font-size:14px;float:left;font-weight:600;margin:0;line-height:inherit;color:#000!important}.plan-node header .node-duration{float:right;margin-left:10px;font-size:13px}.plan-node .prop-list{color:inherit;table-layout:fixed}.plan-node.highlight .plan-node-body,.plan-node:hover .plan-node-body{-webkit-box-shadow:1px 1px 5px 0 rgba(0,0,0,.4);box-shadow:1px 1px 5px 0 rgba(0,0,0,.4)}.plan-node.highlight .workers>div,.plan-node:hover .workers>div{border-color:rgba(0,0,0,.2)}.plan-node.selected .plan-node-body{border-color:#00b5e2;-webkit-box-shadow:0 0 5px 2px rgba(0,181,226,.4);box-shadow:0 0 5px 2px rgba(0,181,226,.4)}.plan-node.selected .workers>div{border-color:rgba(0,181,226,.2)}.plan-node .node-description{text-align:left;font-style:italic;word-break:normal}.plan-node .node-description .node-type{font-weight:600;background-color:#00b5e2;color:#fff;padding:0 6px}.plan-node .btn-default{border:0}.plan-node .text-muted{color:#999ea7}.plan-node .plan-query-container{border:1px solid #dedede;padding:18px;background-color:#fff;position:absolute;-webkit-box-shadow:0 0 10px 2px rgba(0,0,0,.3);box-shadow:0 0 10px 2px rgba(0,0,0,.3);border-radius:3px;margin-bottom:18px;z-index:1;left:0}.plan-node .plan-query-container h3{font-size:17px;width:93%;text-align:left;border-bottom:1px solid #dedede;padding-bottom:6px;margin-bottom:10px}.plan-node .collapse-handle{cursor:pointer;position:absolute;z-index:1;bottom:0;right:0;display:none;background-color:hsla(0,0%,100%,.7)}.plan-node:hover .collapse-handle{display:block}.plan-node.flash .plan-node-body{-webkit-animation:flash 1s;animation:flash 1s}.plan-node .workers{position:absolute;left:-1px;top:1px;width:100%;height:100%;cursor:pointer}.plan-node .workers>div{border:1px solid #dedede;border-radius:3px;background-color:#fff;width:100%;height:100%;position:absolute}.plan-node .workers-handle{cursor:pointer;position:absolute;top:0;right:-5px}.plan-node .workers-handle>div{position:absolute;top:0;background-color:#fff;border:1px solid #efefef;border-radius:3px}.plan-node .workers-handle>div:hover{background-color:#f7f7f7;border-color:#dedede}.node-bar-container{height:5px;margin-top:10px;margin-bottom:3px;border-radius:6px;background-color:#dedede;position:relative}.node-bar-container .node-bar{border-radius:6px;height:100%;text-align:left;position:absolute;left:0;top:0}.node-bar-label{text-align:left;display:block}.detailed{width:400px!important}ul.node-children.collapsed .plan-node,ul.node-children.collapsed .plan-node-body{width:50px!important}ul.node-children.collapsed .plan-node{display:block}ul.node-children.collapsed .plan-node .plan-node-body{height:16.66667px}ul.node-children.collapsed .plan-node .plan-node-body *,ul.node-children.collapsed .plan-node:hover .collapse-handle{display:none}.classic .plan ul.node-children.collapsed li:before{top:7px}.classic .plan ul.node-children.collapsed li:last-child:after{height:14px}', ""]), t.exports = e
    }, "77d1": function (t, e, n) {
        "use strict";
        var a = function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("main-layout", [t.planSource ? n("plan", {
                ref: "plan",
                attrs: {"plan-source": t.planSource, "plan-query": t.planQuery}
            }) : t._e()], 1)
        }, o = [], s = n("9ab4"), r = n("60a3"), i = function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("div", {staticClass: "plan-container d-flex flex-column overflow-hidden flex-grow-1 bg-light"}, [n("div", [n("ul", {staticClass: "nav nav-pills"}, [n("li", {staticClass: "nav-item p-1"}, [n("a", {
                staticClass: "nav-link px-2 py-0",
                class: {active: "plan" === t.activeTab},
                attrs: {href: "#plan"}
            }, [t._v("Plan")])]), t._v(" "), n("li", {staticClass: "nav-item p-1"}, [n("a", {
                staticClass: "nav-link px-2 py-0",
                class: {active: "raw" === t.activeTab},
                attrs: {href: "#raw"}
            }, [t._v("Raw")])]), t._v(" "), n("li", {staticClass: "nav-item p-1"}, [n("a", {
                staticClass: "nav-link px-2 py-0",
                class: {active: "query" === t.activeTab, disabled: !t.queryText},
                attrs: {href: "#query"}
            }, [t._v("Query")])]), t._v(" "), n("li", {staticClass: "nav-item p-1"}, [n("a", {
                staticClass: "nav-link px-2 py-0",
                class: {active: "stats" === t.activeTab},
                attrs: {href: "#stats"}
            }, [t._v("Stats")])])])]), t._v(" "), n("div", {staticClass: "tab-content flex-grow-1 d-flex overflow-hidden"}, [t.validationMessage ? n("div", {staticClass: "flex-grow-1 d-flex justify-content-center"}, [n("div", {staticClass: "alert alert-danger align-self-center"}, [t._v(t._s(t.validationMessage))])]) : t._e(), t._v(" "), t.validationMessage ? t._e() : n("div", {
                staticClass: "tab-pane flex-grow-1 overflow-hidden",
                class: {"show active d-flex": "plan" === t.activeTab}
            }, [n("div", {
                staticClass: "d-flex flex-column flex-grow-1 overflow-hidden",
                class: [t.viewOptions.viewMode, t.viewOptions.orientation]
            }, [t.plan ? n("div", {staticClass: "plan-stats flex-shrink-0 d-flex border-bottom border-top form-inline"}, [n("div", {staticClass: "d-inline-block px-2"}, [t._v("\n            Execution time:\n            "), t.plan.planStats.executionTime ? [n("span", {
                staticClass: "stat-value",
                domProps: {innerHTML: t._s(t.$options.filters.duration(t.plan.planStats.executionTime))}
            })] : [n("span", {staticClass: "text-muted"}, [t._v("\n                N/A\n                "), n("i", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                staticClass: "fa fa-info-circle cursor-help",
                attrs: {content: t.getHelpMessage("missing execution time")}
            })])]], 2), t._v(" "), n("div", {staticClass: "d-inline-block border-left px-2"}, [t._v("\n            Planning time:\n            "), t.plan.planStats.planningTime ? [n("span", {staticClass: "stat-value"}, [n("span", {
                class: "mb-0 p-0 px-1 alert " + t.planningTimeClass(t.plan.planStats.planningTime / t.plan.planStats.executionTime * 100),
                domProps: {innerHTML: t._s(t.$options.filters.duration(t.plan.planStats.planningTime))}
            })])] : [n("span", {staticClass: "text-muted"}, [t._v("\n                N/A\n                "), n("i", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                staticClass: "fa fa-info-circle cursor-help",
                attrs: {content: t.getHelpMessage("missing planning time")}
            })])]], 2), t._v(" "), t.plan.planStats.jitTime ? n("div", {staticClass: "d-inline-block border-left px-2"}, [t._v("\n            JIT:\n            "), n("span", {staticClass: "stat-value"}, [n("span", {
                class: "mb-0 p-0 px-1 alert " + t.planningTimeClass(t.plan.planStats.jitTime / t.plan.planStats.executionTime * 100),
                domProps: {innerHTML: t._s(t.$options.filters.duration(t.plan.planStats.jitTime))}
            })])]) : t._e(), t._v(" "), n("div", {staticClass: "d-inline-block border-left px-2 position-relative"}, [n("span", {staticClass: "stat-label"}, [t._v("Triggers: ")]), t._v(" "), t.plan.planStats.triggers.length ? [n("span", {staticClass: "stat-value"}, [n("span", {
                class: "mb-0 p-0 px-1 alert " + t.$options.filters.durationClass(t.totalTriggerDurationPercent),
                domProps: {innerHTML: t._s(t.$options.filters.duration(t.triggersTotalDuration))}
            })]), t._v(" "), n("button", {
                staticClass: "bg-transparent border-0 p-0 m-0 pl-1",
                on: {
                    click: function (e) {
                        e.preventDefault(), t.showTriggers = !t.showTriggers
                    }
                }
            }, [n("i", {staticClass: "fa fa-caret-down text-muted"})]), t._v(" "), t.showTriggers ? n("div", {staticClass: "stat-dropdown-container text-left"}, [n("button", {
                staticClass: "btn btn-close float-right",
                on: {
                    click: function (e) {
                        t.showTriggers = !1
                    }
                }
            }, [n("i", {staticClass: "fa fa-times"})]), t._v(" "), n("h3", [t._v("Triggers")]), t._v(" "), t._l(t.plan.planStats.triggers, (function (e, a) {
                return n("div", [t._v("\n                  " + t._s(e["Trigger Name"]) + "\n                  "), n("br"), t._v(" "), n("span", {staticClass: "text-muted"}, [t._v("Called")]), t._v(" " + t._s(e["Calls"])), n("span", {staticClass: "text-muted"}, [t._v("×")]), t._v(" "), n("span", {staticClass: "float-right"}, [n("span", {
                    class: "p-0 px-1 alert " + t.$options.filters.durationClass(t.triggerDurationPercent(e)),
                    domProps: {innerHTML: t._s(t.$options.filters.duration(e.Time))}
                }), t._v("\n                    | " + t._s(t.triggerDurationPercent(e))), n("span", {staticClass: "text-muted"}, [t._v("%")])]), t._v(" "), n("br"), t._v(" "), e.Relation ? n("span", {staticClass: "text-muted"}, [t._v("on")]) : t._e(), t._v("\n                  " + t._s(e.Relation) + "\n                  "), n("div", {staticClass: "clearfix"}), t._v(" "), a != t.plan.planStats.triggers.length - 1 ? n("hr", {staticClass: "my-2"}) : t._e()])
            }))], 2) : t._e()] : n("span", {staticClass: "text-muted"}, [t._v("\n              N/A\n            ")])], 2), t._v(" "), t.plan.planStats.settings ? n("div", {staticClass: "d-inline-block border-left px-2 position-relative"}, [n("span", {staticClass: "stat-label"}, [t._v("Settings: "), n("span", {staticClass: "badge badge-secondary"}, [t._v(t._s(t.lodash.keys(t.plan.planStats.settings).length))])]), t._v(" "), n("button", {
                staticClass: "bg-transparent border-0 p-0 m-0 pl-1",
                on: {
                    click: function (e) {
                        e.preventDefault(), t.showSettings = !t.showSettings
                    }
                }
            }, [n("i", {staticClass: "fa fa-caret-down text-muted"})]), t._v(" "), t.showSettings ? n("div", {staticClass: "stat-dropdown-container text-left"}, [n("button", {
                staticClass: "btn btn-close float-right",
                on: {
                    click: function (e) {
                        t.showSettings = !1
                    }
                }
            }, [n("i", {staticClass: "fa fa-times"})]), t._v(" "), n("h3", [t._v("PG Settings")]), t._v(" "), n("em", {staticClass: "text-muted d-block pb-2"}, [t._v("\n              Configuration parameters affecting query planning with value different from the built-in default value.\n              ")]), t._v(" "), n("table", {staticClass: "table table-sm table-striped mb-0"}, [n("tbody", t._l(t.plan.planStats.settings, (function (e, a) {
                return n("tr", [n("td", [t._v(t._s(a))]), t._v(" "), n("td", [t._v(t._s(e))])])
            })), 0)])]) : t._e()]) : t._e(), t._v(" "), n("button", {
                class: ["border-left btn btn-sm p-0 px-2 ml-auto", {"text-primary": !t.viewOptions.menuHidden}],
                on: {click: t.showHideMenu}
            }, [n("i", {staticClass: "fa fa-cog p-0"}), t._v(" Settings\n          ")])]) : t._e(), t._v(" "), n("div", {staticClass: "flex-grow-1 d-flex overflow-hidden"}, [n("div", {staticClass: "flex-grow-1 overflow-hidden"}, [n("splitpanes", {
                staticClass: "default-theme",
                on: {
                    resize: function (e) {
                        t.viewOptions.diagramWidth = e[0].size
                    }
                }
            }, [t.viewOptions.showDiagram ? n("pane", {
                staticClass: "d-flex",
                attrs: {size: t.viewOptions.diagramWidth}
            }, [n("diagram", {
                ref: "diagram",
                staticClass: "d-flex flex-column flex-grow-1 overflow-hidden plan-diagram",
                attrs: {plan: t.plan, eventBus: t.eventBus},
                scopedSlots: t._u([{
                    key: "nodeindex", fn: function (e) {
                        var n = e.node;
                        return [t._t("nodeindex", null, {node: n})]
                    }
                }], null, !0)
            })], 1) : t._e(), t._v(" "), n("pane", {
                ref: "plan",
                staticClass: "plan d-flex flex-column flex-grow-1 grab-bing overflow-auto"
            }, [n("ul", {staticClass: "main-plan p-2 mb-0"}, [n("li", [n("plan-node", {
                ref: "root",
                attrs: {node: t.rootNode, plan: t.plan, viewOptions: t.viewOptions, eventBus: t.eventBus},
                scopedSlots: t._u([{
                    key: "nodeindex", fn: function (e) {
                        var n = e.node;
                        return [t._t("nodeindex", null, {node: n})]
                    }
                }], null, !0)
            })], 1)]), t._v(" "), t.plan.ctes.length ? n("ul", {staticClass: "init-plans p-2 mb-0"}, t._l(t.plan.ctes, (function (e) {
                return n("li", [n("plan-node", {
                    ref: "root",
                    refInFor: !0,
                    attrs: {node: e, plan: t.plan, viewOptions: t.viewOptions, eventBus: t.eventBus},
                    scopedSlots: t._u([{
                        key: "nodeindex", fn: function (e) {
                            var n = e.node;
                            return [t._t("nodeindex", null, {node: n})]
                        }
                    }], null, !0)
                })], 1)
            })), 0) : t._e()])], 1)], 1), t._v(" "), t.plan && !t.viewOptions.menuHidden ? n("div", {staticClass: "small p-2 border-left"}, [n("div", {staticClass: "text-right clearfix"}, [n("button", {
                staticClass: "close",
                attrs: {type: "button", "aria-label": "Close"},
                on: {
                    click: function (e) {
                        t.viewOptions.menuHidden = !0
                    }
                }
            }, [n("span", {attrs: {"aria-hidden": "true"}}, [t._v("×")])])]), t._v(" "), n("div", {staticClass: "form-check"}, [n("input", {
                directives: [{
                    name: "model",
                    rawName: "v-model",
                    value: t.viewOptions.showDiagram,
                    expression: "viewOptions.showDiagram"
                }],
                staticClass: "form-check-input",
                attrs: {id: "showDiagram", type: "checkbox"},
                domProps: {checked: Array.isArray(t.viewOptions.showDiagram) ? t._i(t.viewOptions.showDiagram, null) > -1 : t.viewOptions.showDiagram},
                on: {
                    change: function (e) {
                        var n = t.viewOptions.showDiagram, a = e.target, o = !!a.checked;
                        if (Array.isArray(n)) {
                            var s = null, r = t._i(n, s);
                            a.checked ? r < 0 && t.$set(t.viewOptions, "showDiagram", n.concat([s])) : r > -1 && t.$set(t.viewOptions, "showDiagram", n.slice(0, r).concat(n.slice(r + 1)))
                        } else t.$set(t.viewOptions, "showDiagram", o)
                    }
                }
            }), t._v(" "), t._m(0)]), t._v(" "), n("hr"), t._v(" "), n("label", {staticClass: "text-uppercase"}, [t._v("Density")]), t._v(" "), n("div", {staticClass: "form-group"}, [n("div", {staticClass: "btn-group btn-group-sm"}, [n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.viewMode == t.viewModes.FULL},
                on: {
                    click: function (e) {
                        t.viewOptions.viewMode = t.viewModes.FULL
                    }
                }
            }, [t._v("full")]), t._v(" "), n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.viewMode == t.viewModes.COMPACT},
                on: {
                    click: function (e) {
                        t.viewOptions.viewMode = t.viewModes.COMPACT
                    }
                }
            }, [t._v("compact")]), t._v(" "), n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.viewMode == t.viewModes.DOT},
                on: {
                    click: function (e) {
                        t.viewOptions.viewMode = t.viewModes.DOT
                    }
                }
            }, [t._v("dot")])])]), t._v(" "), n("hr"), t._v(" "), n("label", {staticClass: "text-uppercase"}, [t._v("Orientation")]), t._v(" "), n("div", {staticClass: "form-group"}, [n("div", {staticClass: "btn-group btn-group-sm"}, [n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.orientation == t.orientations.TWOD},
                on: {
                    click: function (e) {
                        t.viewOptions.orientation = t.orientations.TWOD
                    }
                }
            }, [n("i", {staticClass: "fa fa-sitemap"}), t._v("\n                  2D\n                ")]), t._v(" "), n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.orientation == t.orientations.CLASSIC},
                on: {
                    click: function (e) {
                        t.viewOptions.orientation = t.orientations.CLASSIC
                    }
                }
            }, [n("i", {staticClass: "fa fa-list"}), t._v("\n                  classic\n                ")])])]), t._v(" "), n("hr"), t._v(" "), n("label", {staticClass: "text-uppercase"}, [t._v("Graph metric")]), t._v(" "), n("div", {staticClass: "form-group"}, [n("div", {staticClass: "btn-group btn-group-sm"}, [n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.highlightType === t.highlightTypes.NONE},
                on: {
                    click: function (e) {
                        t.viewOptions.highlightType = t.highlightTypes.NONE
                    }
                }
            }, [t._v("none")]), t._v(" "), n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.highlightType === t.highlightTypes.DURATION},
                attrs: {disabled: !t.plan.isAnalyze},
                on: {
                    click: function (e) {
                        t.viewOptions.highlightType = t.highlightTypes.DURATION
                    }
                }
            }, [t._v("duration")]), t._v(" "), n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.highlightType === t.highlightTypes.ROWS},
                attrs: {disabled: void 0 === t.rootNode[t.nodeProps.ACTUAL_ROWS]},
                on: {
                    click: function (e) {
                        t.viewOptions.highlightType = t.highlightTypes.ROWS
                    }
                }
            }, [t._v("rows")]), t._v(" "), n("button", {
                staticClass: "btn btn-outline-secondary",
                class: {active: t.viewOptions.highlightType === t.highlightTypes.COST},
                on: {
                    click: function (e) {
                        t.viewOptions.highlightType = t.highlightTypes.COST
                    }
                }
            }, [t._v("cost")])])])]) : t._e()])])]), t._v(" "), n("div", {
                staticClass: "tab-pane flex-grow-1 overflow-hidden position-relative",
                class: {"show active": "raw" === t.activeTab}
            }, [n("div", {staticClass: "overflow-hidden d-flex w-100 h-100"}, [n("div", {staticClass: "overflow-auto flex-grow-1"}, [n("pre", {staticClass: "small p-2 mb-0"}, [n("code", {domProps: {innerHTML: t._s(t.$options.filters.json(t.planSource))}})])]), t._v(" "), n("copy", {attrs: {content: t.planSource}})], 1)]), t._v(" "), t.queryText ? n("div", {
                staticClass: "tab-pane flex-grow-1 overflow-hidden position-relative",
                class: {"show active": "query" === t.activeTab}
            }, [n("div", {staticClass: "overflow-hidden d-flex w-100 h-100"}, [n("div", {staticClass: "overflow-auto flex-grow-1"}, [n("pre", {staticClass: "small p-2 mb-0"}, [n("code", {domProps: {innerHTML: t._s(t.$options.filters.pgsql(t.queryText))}})])])]), t._v(" "), n("copy", {attrs: {content: t.queryText}})], 1) : t._e(), t._v(" "), n("div", {
                staticClass: "tab-pane flex-grow-1 overflow-auto",
                class: {"show active": "stats" === t.activeTab}
            }, [n("stats", {attrs: {plan: t.plan}})], 1)])])
        }, l = [function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("label", {
                staticClass: "form-check-label",
                attrs: {for: "showDiagram"}
            }, [n("i", {staticClass: "fa fa-align-left"}), t._v(" Diagram")])
        }], c = n("2ef0"), u = n("512e"), p = function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("div", {
                class: {
                    subplan: t.node[t.nodeProps.SUBPLAN_NAME],
                    "d-flex flex-column align-items-center": t.viewOptions.orientation == t.orientations.TWOD
                }
            }, [t.node[t.nodeProps.SUBPLAN_NAME] ? n("h4", [t._v(t._s(t.node[t.nodeProps.SUBPLAN_NAME]))]) : t._e(), t._v(" "), n("div", {
                class: ["text-left plan-node", {
                    detailed: t.showDetails,
                    "never-executed": t.isNeverExecuted,
                    parallel: t.workersPlannedCount,
                    selected: t.selected
                }]
            }, [t.workersPlannedCount ? n("div", {staticClass: "workers text-muted py-0 px-1"}, t._l(t.workersPlannedCountReversed, (function (e) {
                return n("div", {
                    class: {"border-dashed": e >= t.workersLaunchedCount},
                    style: "top: " + (1 + 2 * e) + "px; left: " + (1 + 3 * (e + 1)) + "px;"
                }, [t._v("\n        " + t._s(e) + "\n      ")])
            })), 0) : t._e(), t._v(" "), t.hasChildren ? n("div", {staticClass: "collapse-handle"}, [n("i", {
                class: ["fa fa-fw", {
                    "fa-compress": !t.collapsed,
                    "fa-expand": t.collapsed
                }], attrs: {title: "Collpase or expand child nodes"}, on: {
                    click: function (e) {
                        return e.stopPropagation(), t.toggleCollapsed()
                    }
                }
            })]) : t._e(), t._v(" "), n("div", {
                staticClass: "plan-node-body card", on: {
                    mouseenter: function (e) {
                        return t.eventBus.$emit("mouseovernode", t.node.nodeId)
                    }, mouseleave: function (e) {
                        return t.eventBus.$emit("mouseoutnode", t.node.nodeId)
                    }
                }
            }, [n("div", {
                staticClass: "card-body header no-focus-outline", on: {
                    click: function (e) {
                        e.stopPropagation(), t.showDetails = !t.showDetails
                    }
                }
            }, [n("header", {staticClass: "mb-0"}, [n("h4", {staticClass: "text-body"}, [n("a", {
                staticClass: "font-weight-normal small",
                attrs: {href: "#plan/node/" + t.node.nodeId},
                on: {
                    click: function (t) {
                        t.stopPropagation()
                    }
                }
            }, [t._v("#" + t._s(t.node.nodeId))]), t._v("\n            " + t._s(t.getNodeName()) + "\n          ")]), t._v(" "), n("div", {staticClass: "float-right"}, [t.durationClass ? n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                class: "p-0  d-inline-block mb-0 ml-1 text-nowrap alert " + t.durationClass,
                attrs: {content: "Slow"}
            }, [n("i", {staticClass: "fa fa-fw fa-clock"})]) : t._e(), t._v(" "), t.costClass ? n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                class: "p-0  d-inline-block mb-0 ml-1 text-nowrap alert " + t.costClass,
                attrs: {content: "Cost is high"}
            }, [n("i", {staticClass: "fa fa-fw fa-dollar-sign"})]) : t._e(), t._v(" "), t.estimationClass ? n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                class: "p-0  d-inline-block mb-0 ml-1 text-nowrap alert " + t.estimationClass,
                attrs: {content: "Bad estimation for number of rows"}
            }, [n("i", {staticClass: "fa fa-fw fa-thumbs-down"})]) : t._e(), t._v(" "), t.rowsRemovedClass ? n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                class: "p-0  d-inline-block mb-0 ml-1 text-nowrap alert " + t.rowsRemovedClass,
                attrs: {content: t.filterTooltip}
            }, [n("i", {staticClass: "fa fa-fw fa-filter"})]) : t._e(), t._v(" "), t.heapFetchesClass ? n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy",
                    value: {arrow: !0},
                    expression: "{arrow: true}"
                }],
                class: "p-0  d-inline-block mb-0 ml-1 text-nowrap alert " + t.heapFetchesClass,
                attrs: {content: "Heap Fetches number is high"}
            }, [n("i", {staticClass: "fa fa-fw fa-exchange-alt"})]) : t._e(), t._v(" "), t.rowsRemoved && !t.rowsRemovedClass ? n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }], staticClass: "p-0  d-inline-block mb-0 ml-1 text-nowrap", attrs: {content: t.filterTooltip}
            }, [n("i", {staticClass: "fa fa-fw fa-filter text-muted"})]) : t._e()]), t._v(" "), t.viewOptions.viewMode === t.viewModes.FULL ? n("span", [t.isNeverExecuted ? n("span", {staticClass: "node-duration text-warning"}, [t._v("\n              Never executed\n            ")]) : t._e()]) : t._e()]), t._v(" "), t.viewOptions.viewMode === t.viewModes.FULL ? n("div", {staticClass: "text-left text-monospace"}, [t.node[t.nodeProps.RELATION_NAME] ? n("div", {class: {"line-clamp-2": !t.showDetails}}, [n("span", {staticClass: "text-muted"}, [t._v("on ")]), t.node[t.nodeProps.SCHEMA] ? n("span", [t._v(t._s(t.node[t.nodeProps.SCHEMA]) + ".")]) : t._e(), t._v(t._s(t.node[t.nodeProps.RELATION_NAME]) + "\n            "), t.node[t.nodeProps.ALIAS] ? n("span", [n("span", {staticClass: "text-muted"}, [t._v("as")]), t._v("\n              " + t._s(t.node[t.nodeProps.ALIAS]) + "\n            ")]) : t._e()]) : t._e(), t._v(" "), t.node[t.nodeProps.GROUP_KEY] ? n("div", {class: {"line-clamp-2": !t.showDetails}}, [n("span", {staticClass: "text-muted"}, [t._v("by")]), t._v(" "), n("span", {domProps: {innerHTML: t._s(t.$options.filters.keysToString(t.node[t.nodeProps.GROUP_KEY]))}})]) : t._e(), t._v(" "), t.node[t.nodeProps.SORT_KEY] ? n("div", {class: {"line-clamp-2": !t.showDetails}}, [n("span", {staticClass: "text-muted"}, [t._v("by")]), t._v(" "), n("span", {domProps: {innerHTML: t._s(t.$options.filters.sortKeys(t.node[t.nodeProps.SORT_KEY], t.node[t.nodeProps.PRESORTED_KEY]))}})]) : t._e(), t._v(" "), t.node[t.nodeProps.JOIN_TYPE] ? n("div", [t._v(t._s(t.node[t.nodeProps.JOIN_TYPE]) + "\n            "), n("span", {staticClass: "text-muted"}, [t._v("join")])]) : t._e(), t._v(" "), t.node[t.nodeProps.INDEX_NAME] ? n("div", {class: {"line-clamp-2": !t.showDetails}}, [n("span", {staticClass: "text-muted"}, [t._v("using")]), t._v(" "), n("span", {domProps: {innerHTML: t._s(t.$options.filters.keysToString(t.node[t.nodeProps.INDEX_NAME]))}})]) : t._e(), t._v(" "), t.node[t.nodeProps.HASH_CONDITION] ? n("div", {class: {"line-clamp-2": !t.showDetails}}, [n("span", {staticClass: "text-muted"}, [t._v("on")]), t._v(" "), n("span", {domProps: {innerHTML: t._s(t.$options.filters.keysToString(t.node[t.nodeProps.HASH_CONDITION]))}})]) : t._e(), t._v(" "), t.node[t.nodeProps.CTE_NAME] ? n("div", [n("a", {
                staticClass: "text-reset",
                attrs: {href: ""},
                on: {
                    click: function (e) {
                        return e.stopPropagation(), e.preventDefault(), t.eventBus.$emit("clickcte", "CTE " + t.node[t.nodeProps.CTE_NAME])
                    }
                }
            }, [n("i", {staticClass: "fa fa-search text-muted"}), t._v(" "), n("span", {staticClass: "text-muted"}, [t._v("CTE")]), t._v(" " + t._s(t.node[t.nodeProps.CTE_NAME]) + "\n            ")])]) : t._e()]) : t._e(), t._v(" "), t.allWorkersLaunched || t.viewOptions.viewMode !== t.viewModes.FULL ? t._e() : n("div", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                staticClass: "text-c-3 cursor-help",
                attrs: {content: t.getHelpMessage("workers planned not launched")}
            }, [n("i", {staticClass: "fa fa-exclamation-triangle"}), t._v(" \n          "), n("span", [t._v("Not all workers launched")])]), t._v(" "), n("div", {staticClass: "clearfix"}), t._v(" "), t.viewOptions.highlightType !== t.highlightTypes.NONE && null !== t.highlightValue ? n("div", [n("div", {
                staticClass: "progress node-bar-container",
                staticStyle: {height: "5px"}
            }, [n("div", {
                staticClass: "progress-bar",
                style: {width: t.barWidth + "%", "background-color": t.getBarColor(t.barWidth)},
                attrs: {role: "progressbar", "aria-valuenow": "0", "aria-valuemin": "0", "aria-valuemax": "100"}
            })]), t._v(" "), t.shouldShowNodeBarLabel() ? n("span", {staticClass: "node-bar-label"}, [n("span", {staticClass: "text-muted"}, [t._v(t._s(t.viewOptions.highlightType) + ":")]), t._v(" \n            "), n("span", {domProps: {innerHTML: t._s(t.highlightValue)}})]) : t._e()]) : t._e()]), t._v(" "), t.showDetails ? n("div", {staticClass: "card-header border-top"}, [t.getNodeTypeDescription() ? n("div", {staticClass: "node-description"}, [n("span", {staticClass: "node-type"}, [t._v(t._s(t.node[t.nodeProps.NODE_TYPE]) + " Node")]), t._v(" "), n("span", {domProps: {innerHTML: t._s(t.getNodeTypeDescription())}})]) : t._e(), t._v(" "), n("ul", {staticClass: "nav nav-tabs card-header-tabs"}, [n("li", {staticClass: "nav-item"}, [n("a", {
                staticClass: "nav-link",
                class: {active: "general" === t.activeTab},
                attrs: {href: ""},
                on: {
                    click: function (e) {
                        return e.preventDefault(), t.setActiveTab("general")
                    }
                }
            }, [t._v("General")])]), t._v(" "), n("li", {staticClass: "nav-item"}, [n("a", {
                staticClass: "nav-link text-nowrap",
                class: {active: "iobuffer" === t.activeTab, disabled: !t.shouldShowIoBuffers},
                attrs: {href: ""},
                on: {
                    click: function (e) {
                        return e.preventDefault(), t.setActiveTab("iobuffer")
                    }
                }
            }, [t._v("IO & Buffers")])]), t._v(" "), n("li", {staticClass: "nav-item"}, [n("a", {
                staticClass: "nav-link",
                class: {active: "output" === t.activeTab, disabled: !t.node[t.nodeProps.OUTPUT]},
                attrs: {href: ""},
                on: {
                    click: function (e) {
                        return e.preventDefault(), t.setActiveTab("output")
                    }
                }
            }, [t._v("Output")])]), t._v(" "), n("li", {staticClass: "nav-item"}, [n("a", {
                staticClass: "nav-link",
                class: {
                    active: "workers" === t.activeTab,
                    disabled: !(t.node[t.nodeProps.WORKERS_PLANNED] || t.node[t.nodeProps.WORKERS_PLANNED_BY_GATHER])
                },
                attrs: {href: ""},
                on: {
                    click: function (e) {
                        return e.preventDefault(), t.setActiveTab("workers")
                    }
                }
            }, [t._v("Workers")])]), t._v(" "), n("li", {staticClass: "nav-item"}, [n("a", {
                staticClass: "nav-link",
                class: {active: "misc" === t.activeTab},
                attrs: {href: ""},
                on: {
                    click: function (e) {
                        return e.preventDefault(), t.setActiveTab("misc")
                    }
                }
            }, [t._v("Misc")])])])]) : t._e(), t._v(" "), t.showDetails ? n("div", {staticClass: "card-body tab-content"}, [n("div", {
                staticClass: "tab-pane",
                class: {"show active": "general" === t.activeTab}
            }, [t.plan.isAnalyze ? n("div", [n("i", {staticClass: "fa fa-fw fa-clock text-muted"}), t._v(" "), n("b", [t._v("Timing:")]), t._v(" \n            "), n("span", {
                class: "p-0 px-1 rounded alert " + t.durationClass,
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_DURATION"))}
            }), t._v(" "), t.executionTimePercent !== 1 / 0 ? [t._v("\n              |\n              "), n("strong", [t._v(t._s(t.executionTimePercent))]), n("span", {staticClass: "text-muted"}, [t._v("%")])] : t._e()], 2) : t._e(), t._v(" "), n("div", [n("i", {staticClass: "fa fa-fw fa-align-justify text-muted"}), t._v(" "), n("b", [t._v("Rows:")]), t._v(" "), n("span", {staticClass: "px-1"}, [t._v(t._s(t.tilde + t.formattedProp("ACTUAL_ROWS_REVISED")))]), t._v(" "), t.node[t.nodeProps.PLAN_ROWS] ? n("span", {staticClass: "text-muted"}, [t._v("(Planned: " + t._s(t.tilde + t.formattedProp("PLAN_ROWS_REVISED")) + ")")]) : t._e(), t._v(" "), t.plannerRowEstimateDirection !== t.estimateDirections.none && t.shouldShowPlannerEstimate ? n("span", [t._v("\n              |\n              "), t.plannerRowEstimateDirection === t.estimateDirections.over ? n("span", [n("i", {staticClass: "fa fa-arrow-up"}), t._v(" over")]) : t._e(), t._v(" "), t.plannerRowEstimateDirection === t.estimateDirections.under ? n("span", [n("i", {staticClass: "fa fa-arrow-down"}), t._v(" under")]) : t._e(), t._v("\n              estimated\n              "), t.plannerRowEstimateValue != 1 / 0 ? n("span", [t._v(" by\n                "), n("span", {
                class: "p-0 px-1 alert " + t.estimationClass,
                domProps: {innerHTML: t._s(t.formattedProp("PLANNER_ESTIMATE_FACTOR"))}
            })]) : t._e()]) : t._e()]), t._v(" "), t.rowsRemoved ? n("div", [n("i", {staticClass: "fa fa-fw fa-filter text-muted"}), t._v(" "), n("b", [t._v("\n              " + t._s(t.nodeProps[t.rowsRemovedProp]) + ":\n            ")]), t._v(" "), n("span", [n("span", {staticClass: "px-1"}, [t._v(t._s(t.tilde + t.formattedProp(t.rowsRemovedProp)))]), t._v("|\n              "), n("span", {class: "p-0 px-1 alert " + t.rowsRemovedClass}, [t._v(t._s(t.rowsRemovedPercentString) + "%")])])]) : t._e(), t._v(" "), t.node[t.nodeProps.HEAP_FETCHES] ? n("div", [n("i", {staticClass: "fa fa-fw fa-exchange-alt text-muted"}), t._v(" "), n("b", [t._v("Heap Fetches:")]), t._v(" \n            "), n("span", {
                class: "p-0 px-1 rounded alert " + t.heapFetchesClass,
                domProps: {innerHTML: t._s(t.formattedProp("HEAP_FETCHES"))}
            }), t._v("\n             \n            "), t.heapFetchesClass ? n("i", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy",
                    value: {arrow: !0},
                    expression: "{arrow: true}"
                }],
                staticClass: "fa fa-fw fa-info-circle text-muted",
                attrs: {content: "Visibility map may be out-of-date. Consider using VACUUM or change autovacuum settings."}
            }) : t._e()]) : t._e(), t._v(" "), t.node[t.nodeProps.EXCLUSIVE_COST] ? n("div", [n("i", {staticClass: "fa fa-fw fa-dollar-sign text-muted"}), t._v(" "), n("b", [t._v("Cost:")]), t._v(" "), n("span", {class: "p-0 px-1 mr-1 alert " + t.costClass}, [t._v(t._s(t.formattedProp("EXCLUSIVE_COST")))]), t._v(" "), n("span", {staticClass: "text-muted"}, [t._v("(Total: " + t._s(t.formattedProp("TOTAL_COST")) + ")")])]) : t._e(), t._v(" "), t.node[t.nodeProps.ACTUAL_LOOPS] > 1 ? n("div", [n("i", {staticClass: "fa fa-fw fa-undo text-muted"}), t._v(" "), n("b", [t._v("Loops:")]), t._v(" "), n("span", {staticClass: "px-1"}, [t._v(t._s(t.formattedProp("ACTUAL_LOOPS")) + "\n            ")])]) : t._e()]), t._v(" "), n("div", {
                staticClass: "tab-pane",
                class: {"show active": "iobuffer" === t.activeTab}
            }, [t.node[t.nodeProps.EXCLUSIVE_IO_READ_TIME] || t.node[t.nodeProps.EXCLUSIVE_IO_WRITE_TIME] ? n("div", {staticClass: "mb-2"}, [n("b", [t._v("\n              I/O Timings:\n            ")]), t._v(" "), t.node[t.nodeProps.EXCLUSIVE_IO_READ_TIME] ? n("span", {staticClass: "ml-2"}, [n("b", [t._v("Read: ")]), t._v("\n              " + t._s(t.formattedProp("EXCLUSIVE_IO_READ_TIME")) + "\n            ")]) : t._e(), t._v(" "), t.node[t.nodeProps.EXCLUSIVE_IO_WRITE_TIME] ? n("span", {staticClass: "ml-2"}, [n("b", [t._v("Write: ")]), t._v("\n              " + t._s(t.formattedProp("EXCLUSIVE_IO_WRITE_TIME")) + "\n            ")]) : t._e()]) : t._e(), t._v(" "), n("b", [t._v("\n            Blocks:\n          ")]), t._v(" "), n("table", {staticClass: "table table-sm"}, [t._m(0), t._v(" "), n("tr", [n("th", [t._v("Shared")]), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_SHARED_HIT_BLOCKS") || "-")}
            }), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_SHARED_READ_BLOCKS") || "-")}
            }), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_SHARED_DIRTIED_BLOCKS") || "-")}
            }), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_SHARED_WRITTEN_BLOCKS") || "-")}
            })]), t._v(" "), n("tr", [n("th", [t._v("Temp")]), t._v(" "), n("td", {staticClass: "text-right bg-hatched"}), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_TEMP_READ_BLOCKS") || "-")}
            }), t._v(" "), n("td", {staticClass: "text-right bg-hatched"}), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_TEMP_WRITTEN_BLOCKS") || "-")}
            })]), t._v(" "), n("tr", [n("th", [t._v("Local")]), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_LOCAL_HIT_BLOCKS") || "-")}
            }), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_LOCAL_READ_BLOCKS") || "-")}
            }), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_LOCAL_DIRTIED_BLOCKS") || "-")}
            }), t._v(" "), n("td", {
                staticClass: "text-right",
                domProps: {innerHTML: t._s(t.formattedProp("EXCLUSIVE_LOCAL_WRITTEN_BLOCKS") || "-")}
            })])]), t._v(" "), t.node[t.nodeProps.WAL_RECORDS] || t.node[t.nodeProps.WAL_BYTES] ? n("div", {staticClass: "mb-2"}, [n("b", [n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }], staticClass: "more-info", attrs: {content: "Write-Ahead Logging"}
            }, [t._v("WAL")]), t._v(":\n            ")]), t._v("\n            " + t._s(t.formattedProp("WAL_RECORDS")) + " records "), n("small", [t._v("(" + t._s(t.formattedProp("WAL_BYTES")) + ")")]), t._v(" "), t.node[t.nodeProps.WAL_FPI] ? n("span", [t._v(" -\n            "), n("span", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }], staticClass: "more-info", attrs: {content: "WAL Full Page Images"}
            }, [t._v("FPI")]), t._v(": " + t._s(t.formattedProp("WAL_FPI")) + "\n            ")]) : t._e()]) : t._e()]), t._v(" "), n("div", {
                staticClass: "tab-pane overflow-auto text-monospace",
                class: {"show active": "output" === t.activeTab},
                staticStyle: {"max-height": "200px"},
                domProps: {innerHTML: t._s(t.formattedProp("OUTPUT"))}
            }), t._v(" "), t.node[t.nodeProps.WORKERS_PLANNED] || t.node[t.nodeProps.WORKERS_PLANNED_BY_GATHER] ? n("div", {
                staticClass: "tab-pane",
                class: {"show active": "workers" === t.activeTab}
            }, [(t.node[t.nodeProps.WORKERS_PLANNED] || t.node[t.nodeProps.WORKERS_PLANNED_BY_GATHER]) && t.viewOptions.viewMode === t.viewModes.FULL ? n("div", [n("b", [t._v("Workers planned: ")]), t._v(" "), n("span", {staticClass: "px-1"}, [t._v(t._s(t.node[t.nodeProps.WORKERS_PLANNED] || t.node[t.nodeProps.WORKERS_PLANNED_BY_GATHER]))]), t._v(" "), t.node[t.nodeProps.WORKERS_PLANNED] || t.node[t.nodeProps.WORKERS] || t.plan.isVerbose && t.plan.isAnalyze ? t._e() : n("em", {staticClass: "text-warning"}, [n("i", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                staticClass: "fa fa-exclamation-triangle cursor-help",
                attrs: {content: t.getHelpMessage("fuzzy needs verbose")}
            })])]) : t._e(), t._v(" "), t.node[t.nodeProps.WORKERS_LAUNCHED] && t.viewOptions.viewMode === t.viewModes.FULL ? n("div", [n("b", [t._v("Workers launched: ")]), t._v(" "), n("span", {staticClass: "px-1"}, [t._v(t._s(t.node[t.nodeProps.WORKERS_LAUNCHED]))])]) : t._e(), t._v(" "), !t.workersLaunchedCount && t.node[t.nodeProps.WORKERS_PLANNED_BY_GATHER] ? n("div", {staticClass: "text-muted"}, [n("em", [t._v("\n              Detailed information is not available.\n                "), n("i", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy"
                }],
                staticClass: "fa fa-info-circle cursor-help",
                attrs: {content: t.getHelpMessage("workers detailed info missing")}
            })])]) : t._e(), t._v(" "), t.lodash.isArray(t.node[t.nodeProps.WORKERS]) ? n("div", {staticClass: "accordion"}, [t._l(t.node[t.nodeProps.WORKERS], (function (e, a) {
                return [n("div", {staticClass: "card"}, [n("div", {staticClass: "card-header p-0"}, [n("button", {
                    staticClass: "btn btn-link btn-sm text-secondary",
                    staticStyle: {"font-size": "inherit"},
                    attrs: {type: "button", "data-toggle": "collapse", "data-target": "#collapse-" + t._uid + "-" + a}
                }, [n("i", {staticClass: "fa fa-chevron-right fa-fw"}), t._v(" "), n("i", {staticClass: "fa fa-chevron-down fa-fw"}), t._v("\n                    Worker " + t._s(e[t.workerProps.WORKER_NUMBER]) + "\n                  ")])]), t._v(" "), n("div", {
                    staticClass: "collapse",
                    attrs: {id: "collapse-" + t._uid + "-" + a}
                }, [n("div", {staticClass: "card-body p-0"}, [n("table", {staticClass: "table table-sm prop-list mb-0"}, t._l(e, (function (e, a) {
                    return t.shouldShowProp(a, e) ? n("tr", [n("td", {attrs: {width: "40%"}}, [t._v(t._s(a))]), t._v(" "), n("td", {domProps: {innerHTML: t._s(t.$options.filters.formatNodeProp(a, e, !0))}})]) : t._e()
                })), 0)])])])]
            }))], 2) : t._e()]) : t._e(), t._v(" "), n("div", {
                staticClass: "tab-pane",
                class: {"show active": "misc" === t.activeTab}
            }, [n("table", {staticClass: "table table-sm prop-list"}, t._l(t.props, (function (e) {
                return t.shouldShowProp(e.key, e.value) ? n("tr", [n("td", {attrs: {width: "40%"}}, [t._v(t._s(e.key))]), t._v(" "), n("td", {domProps: {innerHTML: t._s(t.$options.filters.formatNodeProp(e.key, e.value, !0))}})]) : t._e()
            })), 0), t._v(" "), t._m(1)])]) : t._e()])]), t._v(" "), t.plans ? n("ul", {class: ["node-children", {collapsed: t.collapsed}]}, t._l(t.plans, (function (e) {
                return n("li", [n("plan-node", {
                    attrs: {
                        node: e,
                        plan: t.plan,
                        viewOptions: t.viewOptions,
                        eventBus: t.eventBus
                    }, scopedSlots: t._u([{
                        key: "nodeindex", fn: function (e) {
                            var n = e.node;
                            return [t._t("nodeindex", null, {node: n})]
                        }
                    }], null, !0)
                })], 1)
            })), 0) : t._e()])
        }, d = [function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("tr", [n("td"), t._v(" "), n("th", {
                staticClass: "text-right",
                attrs: {width: "25%"}
            }, [t._v("Hit")]), t._v(" "), n("th", {
                staticClass: "text-right",
                attrs: {width: "25%"}
            }, [t._v("Read")]), t._v(" "), n("th", {
                staticClass: "text-right",
                attrs: {width: "25%"}
            }, [t._v("Dirtied")]), t._v(" "), n("th", {
                staticClass: "text-right",
                attrs: {width: "25%"}
            }, [t._v("Written")])])
        }, function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("div", {staticClass: "text-muted text-right"}, [n("em", [t._v("* Calculated value")])])
        }];

        function f(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function _(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function h(t, e, n) {
            return e && _(t.prototype, e), n && _(t, n), t
        }

        var v = function () {
            function t() {
                f(this, t), this.nodeId = 0
            }

            return h(t, [{
                key: "getNodeTypeDescription", value: function (t) {
                    return b[t.toUpperCase()]
                }
            }, {
                key: "getHelpMessage", value: function (t) {
                    return m[t.toUpperCase()]
                }
            }]), t
        }(), b = {
            LIMIT: "returns a specified number of rows from a record set.",
            SORT: "sorts a record set based on the specified sort key.",
            "NESTED LOOP": "merges two record sets by looping through every record in the first set and\n   trying to find a match in the second set. All matching records are returned.",
            "MERGE JOIN": "merges two record sets by first sorting them on a <strong>join key</strong>.",
            HASH: "generates a hash table from the records in the input recordset. Hash is used by\n   <strong>Hash Join</strong>.",
            "HASH JOIN": "joins two record sets by hashing one of them (using a <strong>Hash Scan</strong>).",
            AGGREGATE: "groups records together based on a GROUP BY or aggregate function (like <code>sum()</code>).",
            HASHAGGREGATE: "groups records together based on a GROUP BY or aggregate function (like sum()). Hash Aggregate uses\n   a hash to first organize the records by a key.",
            "SEQ SCAN": "finds relevant records by sequentially scanning the input record set. When reading from a table,\n   Seq Scans (unlike Index Scans) perform a single read operation (only the table is read).",
            "INDEX SCAN": "finds relevant records based on an <strong>Index</strong>.\n    Index Scans perform 2 read operations: one to\n    read the index and another to read the actual value from the table.",
            "INDEX ONLY SCAN": "finds relevant records based on an <strong>Index</strong>.\n    Index Only Scans perform a single read operation\n    from the index and do not read from the corresponding table.",
            "BITMAP HEAP SCAN": "searches through the pages returned by the <strong>Bitmap Index Scan</strong>\n    for relevant rows.",
            "BITMAP INDEX SCAN": "uses a <strong>Bitmap Index</strong> (index which uses 1 bit per page)\n    to find all relevant pages.\n    Results of this node are fed to the <strong>Bitmap Heap Scan</strong>.",
            "CTE SCAN": "performs a sequential scan of <strong>Common Table Expression (CTE) query</strong> results. Note that\n    results of a CTE are materialized (calculated and temporarily stored).",
            MEMOIZE: "is used to cache the results of the inner side of a nested loop. It avoids executing underlying nodes when the results for the current parameters are already in the cache."
        }, m = {
            "MISSING EXECUTION TIME": "Execution time (or Total runtime) not available for this plan. Make sure you\n    use EXPLAIN ANALYZE.",
            "MISSING PLANNING TIME": "Planning time not available for this plan.",
            "WORKERS PLANNED NOT LAUNCHED": "Less workers than planned were launched.\nConsider modifying max_parallel_workers or max_parallel_workers_per_gather.",
            "WORKERS DETAILED INFO MISSING": "Consider using EXPLAIN (ANALYZE, VERBOSE)",
            "FUZZY NEEDS VERBOSE": "Information may not be accurate. Use EXPLAIN VERBOSE mode."
        };

        function E(t, e, n, a) {
            var o = t.getBoundingClientRect(), s = e.getBoundingClientRect(), r = t.scrollLeft,
                i = s.left >= o.left && s.left <= o.right && s.right <= o.right, l = t.scrollTop,
                c = s.top >= o.top && s.top <= o.bottom && s.bottom <= o.bottom;
            !n && i && c ? a && a() : (r = s.left + t.scrollLeft - o.left - o.width / 2 + s.width / 2, l = s.top + t.scrollTop - o.top - o.height / 2 + s.height / 2, T({
                element: t,
                to: {scrollTop: l, scrollLeft: r},
                duration: 400,
                done: a
            }))
        }

        var g, S = function (t) {
            var e = t.currentTime, n = t.start, a = t.change, o = t.duration, s = e;
            return s /= o / 2, s < 1 ? a / 2 * s * s + n : (s -= 1, -a / 2 * (s * (s - 2) - 1) + n)
        };

        function T(t) {
            var e = t.duration, n = t.element, a = t.to, o = t.done, s = n.scrollTop, r = n.scrollLeft,
                i = a.scrollTop - s, l = a.scrollLeft - r, c = (new Date).getTime(), u = function t() {
                    var u = (new Date).getTime(), p = u - c;
                    n.scrollTop = S({currentTime: p, start: s, change: i, duration: e}), n.scrollLeft = S({
                        currentTime: p,
                        start: r,
                        change: l,
                        duration: e
                    }), p < e ? requestAnimationFrame(t) : (n.scrollTop = a.scrollTop, n.scrollLeft = a.scrollLeft, o && o())
                };
            u()
        }

        function C(t, e) {
            var n = "([\\s\\S]*?)(e)?(?:(o)|(c)|(t)|(sp)|$)".replace("sp", e).replace("o", "[\\(\\{\\[]").replace("c", "[\\)\\}\\]]").replace("t", "['\"]").replace("e", "[\\\\]"),
                a = new RegExp(n, "gi"), o = [], s = [], r = [];
            return t.replace(a, (function (t, e, n, a, i, l, c, u) {
                if (n) return s.push(e, c || a || i || l), "";
                if (a) o.push(a); else if (i) o.pop(); else if (l) o[o.length - 1] !== l ? o.push(l) : o.pop(); else if (c ? !o.length : !e) return s.push(e), r.push(s.join("")), s = [], "";
                return s.push(t), ""
            })), r
        }

        function O(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function y(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function w(t, e, n) {
            return e && y(t.prototype, e), n && y(t, n), t
        }

        (function (t) {
            t[t["scrollTop"] = 0] = "scrollTop", t[t["scrollLeft"] = 1] = "scrollLeft"
        })(g || (g = {})), Element.prototype.matches || (Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector), Element.prototype.closest || (Element.prototype.closest = function (t) {
            var e = this;
            if (!document.documentElement.contains(e)) return null;
            do {
                if (e.matches(t)) return e;
                e = e.parentElement || e.parentNode
            } while (null !== e && 1 === e.nodeType);
            return null
        });
        var x, L, A, R = function () {
            function t() {
                O(this, t)
            }

            return w(t, [{
                key: "hslToRgb", value: function (t, e, n) {
                    var a, o, s;
                    if (0 === e) a = o = s = n; else {
                        var r = n < .5 ? n * (1 + e) : n + e - n * e, i = 2 * n - r;
                        a = this.hue2rgb(i, r, t + 1 / 3), o = this.hue2rgb(i, r, t), s = this.hue2rgb(i, r, t - 1 / 3)
                    }
                    return [Math.floor(255 * a), Math.floor(255 * o), Math.floor(255 * s)]
                }
            }, {
                key: "numberToColorHsl", value: function (t) {
                    var e = 1.2 * (100 - t) / 360, n = this.hslToRgb(e, .9, .4);
                    return "rgb(" + n[0] + "," + n[1] + "," + n[2] + ")"
                }
            }, {
                key: "durationPercentToClass", value: function (t) {
                    return t > 90 ? 4 : t > 40 ? 3 : t > 10 ? 2 : 1
                }
            }, {
                key: "hue2rgb", value: function (t, e, n) {
                    return n < 0 && (n += 1), n > 1 && (n -= 1), n < 1 / 6 ? t + 6 * (e - t) * n : n < .5 ? e : n < 2 / 3 ? t + (e - t) * (2 / 3 - n) * 6 : t
                }
            }]), t
        }(), I = n("c1df"), P = n.n(I), k = n("4623"), N = n.n(k);

        function D(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        (function (t) {
            t[t["time"] = 0] = "time", t[t["rows"] = 1] = "rows", t[t["cost"] = 2] = "cost", t[t["buffers"] = 3] = "buffers", t[t["estimate_factor"] = 4] = "estimate_factor"
        })(x || (x = {})), function (t) {
            t["shared"] = "Shared", t["temp"] = "Temp", t["local"] = "Local"
        }(L || (L = {})), function (t) {
            t["hit"] = "Hit", t["read"] = "Read", t["written"] = "Written", t["dirtied"] = "Dirtied"
        }(A || (A = {}));
        var M, U = function t() {
            D(this, t)
        };
        U.NONE = "none", U.DURATION = "duration", U.ROWS = "rows", U.COST = "cost", function (t) {
            t[t["over"] = 1] = "over", t[t["under"] = 2] = "under", t[t["none"] = 3] = "none"
        }(M || (M = {}));
        var B = function t() {
            D(this, t)
        };
        B.FULL = "full", B.COMPACT = "compact", B.DOT = "dot";
        var W, V, H, j, K = function t() {
            D(this, t)
        };
        K.TWOD = "twod", K.CLASSIC = "classic", function (t) {
            t[t["center"] = 0] = "center", t[t["visible"] = 1] = "visible", t[t["none"] = 2] = "none"
        }(W || (W = {})), function (t) {
            t[t["flash"] = 1] = "flash", t[t["highlight"] = 2] = "highlight", t[t["showdetails"] = 4] = "showdetails"
        }(V || (V = {})), function (t) {
            t["NODE_TYPE"] = "Node Type", t["ACTUAL_ROWS"] = "Actual Rows", t["PLAN_ROWS"] = "Plan Rows", t["PLAN_WIDTH"] = "Plan Width", t["ROWS_REMOVED_BY_FILTER"] = "Rows Removed by Filter", t["ROWS_REMOVED_BY_JOIN_FILTER"] = "Rows Removed by Join Filter", t["ACTUAL_STARTUP_TIME"] = "Actual Startup Time", t["ACTUAL_TOTAL_TIME"] = "Actual Total Time", t["ACTUAL_LOOPS"] = "Actual Loops", t["STARTUP_COST"] = "Startup Cost", t["TOTAL_COST"] = "Total Cost", t["PLANS"] = "Plans", t["RELATION_NAME"] = "Relation Name", t["SCHEMA"] = "Schema", t["ALIAS"] = "Alias", t["GROUP_KEY"] = "Group Key", t["SORT_KEY"] = "Sort Key", t["SORT_METHOD"] = "Sort Method", t["SORT_SPACE_TYPE"] = "Sort Space Type", t["SORT_SPACE_USED"] = "Sort Space Used", t["JOIN_TYPE"] = "Join Type", t["INDEX_NAME"] = "Index Name", t["HASH_CONDITION"] = "Hash Cond", t["PARENT_RELATIONSHIP"] = "Parent Relationship", t["SUBPLAN_NAME"] = "Subplan Name", t["PARALLEL_AWARE"] = "Parallel Aware", t["WORKERS"] = "Workers", t["WORKERS_PLANNED"] = "Workers Planned", t["WORKERS_LAUNCHED"] = "Workers Launched", t["SHARED_HIT_BLOCKS"] = "Shared Hit Blocks", t["SHARED_READ_BLOCKS"] = "Shared Read Blocks", t["SHARED_DIRTIED_BLOCKS"] = "Shared Dirtied Blocks", t["SHARED_WRITTEN_BLOCKS"] = "Shared Written Blocks", t["TEMP_READ_BLOCKS"] = "Temp Read Blocks", t["TEMP_WRITTEN_BLOCKS"] = "Temp Written Blocks", t["LOCAL_HIT_BLOCKS"] = "Local Hit Blocks", t["LOCAL_READ_BLOCKS"] = "Local Read Blocks", t["LOCAL_DIRTIED_BLOCKS"] = "Local Dirtied Blocks", t["LOCAL_WRITTEN_BLOCKS"] = "Local Written Blocks", t["IO_READ_TIME"] = "I/O Read Time", t["IO_WRITE_TIME"] = "I/O Write Time", t["OUTPUT"] = "Output", t["HEAP_FETCHES"] = "Heap Fetches", t["WAL_RECORDS"] = "WAL Records", t["WAL_BYTES"] = "WAL Bytes", t["WAL_FPI"] = "WAL FPI", t["FULL_SORT_GROUPS"] = "Full-sort Groups", t["PRE_SORTED_GROUPS"] = "Pre-sorted Groups", t["PRESORTED_KEY"] = "Presorted Key", t["NODE_ID"] = "nodeId", t["EXCLUSIVE_DURATION"] = "*Duration (exclusive)", t["EXCLUSIVE_COST"] = "*Cost (exclusive)", t["ACTUAL_ROWS_REVISED"] = "*Actual Rows Revised", t["PLAN_ROWS_REVISED"] = "*Plan Rows Revised", t["ROWS_REMOVED_BY_FILTER_REVISED"] = "*Rows Removed by Filter", t["ROWS_REMOVED_BY_JOIN_FILTER_REVISED"] = "*Rows Removed by Join Filter", t["PLANNER_ESTIMATE_FACTOR"] = "*Planner Row Estimate Factor", t["PLANNER_ESTIMATE_DIRECTION"] = "*Planner Row Estimate Direction", t["EXCLUSIVE_SHARED_HIT_BLOCKS"] = "*Shared Hit Blocks (exclusive)", t["EXCLUSIVE_SHARED_READ_BLOCKS"] = "*Shared Read Blocks (exclusive)", t["EXCLUSIVE_SHARED_DIRTIED_BLOCKS"] = "*Shared Dirtied Blocks (exclusive)", t["EXCLUSIVE_SHARED_WRITTEN_BLOCKS"] = "*Shared Written Blocks (exclusive)", t["EXCLUSIVE_TEMP_READ_BLOCKS"] = "*Temp Read Blocks (exclusive)", t["EXCLUSIVE_TEMP_WRITTEN_BLOCKS"] = "*Temp Written Blocks (exclusive)", t["EXCLUSIVE_LOCAL_HIT_BLOCKS"] = "*Local Hit Blocks (exclusive)", t["EXCLUSIVE_LOCAL_READ_BLOCKS"] = "*Local Read Blocks (exclusive)", t["EXCLUSIVE_LOCAL_DIRTIED_BLOCKS"] = "*Local Dirtied Blocks (exclusive)", t["EXCLUSIVE_LOCAL_WRITTEN_BLOCKS"] = "*Local Written Blocks (exclusive)", t["EXCLUSIVE_IO_READ_TIME"] = "*I/O Read Time (exclusive)", t["EXCLUSIVE_IO_WRITE_TIME"] = "*I/O Write Time (exclusive)", t["WORKERS_PLANNED_BY_GATHER"] = "*Workers Planned By Gather", t["CTE_SCAN"] = "CTE Scan", t["CTE_NAME"] = "CTE Name", t["FUNCTION_NAME"] = "Function Name", t["ARRAY_INDEX_KEY"] = "arrayIndex", t["PEV_PLAN_TAG"] = "plan_"
        }(H || (H = {})), function (t) {
            t[t["blocks"] = 0] = "blocks", t[t["boolean"] = 1] = "boolean", t[t["bytes"] = 2] = "bytes", t[t["cost"] = 3] = "cost", t[t["duration"] = 4] = "duration", t[t["estimateDirection"] = 5] = "estimateDirection", t[t["factor"] = 6] = "factor", t[t["increment"] = 7] = "increment", t[t["json"] = 8] = "json", t[t["kilobytes"] = 9] = "kilobytes", t[t["list"] = 10] = "list", t[t["loops"] = 11] = "loops", t[t["rows"] = 12] = "rows", t[t["sortGroups"] = 13] = "sortGroups"
        }(j || (j = {}));
        var X = {};
        X[H.ACTUAL_ROWS] = j.rows, X[H.ACTUAL_LOOPS] = j.loops, X[H.PLAN_ROWS] = j.rows, X[H.PLAN_WIDTH] = j.bytes, X[H.ACTUAL_ROWS_REVISED] = j.rows, X[H.PLAN_ROWS_REVISED] = j.rows, X[H.ACTUAL_TOTAL_TIME] = j.duration, X[H.ACTUAL_STARTUP_TIME] = j.duration, X[H.STARTUP_COST] = j.cost, X[H.TOTAL_COST] = j.cost, X[H.PARALLEL_AWARE] = j.boolean, X[H.WORKERS] = j.json, X[H.SORT_SPACE_USED] = j.kilobytes, X[H.ROWS_REMOVED_BY_FILTER] = j.rows, X[H.ROWS_REMOVED_BY_JOIN_FILTER] = j.rows, X[H.ROWS_REMOVED_BY_FILTER_REVISED] = j.rows, X[H.ROWS_REMOVED_BY_JOIN_FILTER_REVISED] = j.rows, X[H.HEAP_FETCHES] = j.rows, X[H.OUTPUT] = j.list, X[H.SORT_KEY] = j.list, X[H.PRESORTED_KEY] = j.list, X[H.WAL_RECORDS] = j.rows, X[H.WAL_BYTES] = j.bytes, X[H.WAL_FPI] = j.rows, X[H.EXCLUSIVE_DURATION] = j.duration, X[H.EXCLUSIVE_COST] = j.cost, X[H.PLANNER_ESTIMATE_FACTOR] = j.factor, X[H.PLANNER_ESTIMATE_DIRECTION] = j.estimateDirection, X[H.IO_READ_TIME] = j.duration, X[H.IO_WRITE_TIME] = j.duration, X[H.EXCLUSIVE_IO_READ_TIME] = j.duration, X[H.EXCLUSIVE_IO_WRITE_TIME] = j.duration, X[H.EXCLUSIVE_SHARED_HIT_BLOCKS] = j.blocks, X[H.EXCLUSIVE_SHARED_READ_BLOCKS] = j.blocks, X[H.EXCLUSIVE_SHARED_DIRTIED_BLOCKS] = j.blocks, X[H.EXCLUSIVE_SHARED_WRITTEN_BLOCKS] = j.blocks, X[H.EXCLUSIVE_TEMP_READ_BLOCKS] = j.blocks, X[H.EXCLUSIVE_TEMP_WRITTEN_BLOCKS] = j.blocks, X[H.EXCLUSIVE_LOCAL_HIT_BLOCKS] = j.blocks, X[H.EXCLUSIVE_LOCAL_READ_BLOCKS] = j.blocks, X[H.EXCLUSIVE_LOCAL_DIRTIED_BLOCKS] = j.blocks, X[H.EXCLUSIVE_LOCAL_WRITTEN_BLOCKS] = j.blocks, X[H.FULL_SORT_GROUPS] = j.sortGroups, X[H.PRE_SORTED_GROUPS] = j.sortGroups;
        var F, $, Y = function t() {
            D(this, t)
        };
        Y.WORKER_NUMBER = "Worker Number", X[Y.WORKER_NUMBER] = j.increment, function (t) {
            t["GROUP_COUNT"] = "Group Count", t["SORT_METHODS_USED"] = "Sort Methods Used", t["SORT_SPACE_MEMORY"] = "Sort Space Memory"
        }(F || (F = {})), function (t) {
            t["AVERAGE_SORT_SPACE_USED"] = "Average Sort Space Used", t["PEAK_SORT_SPACE_USED"] = "Peak Sort Space Used"
        }($ || ($ = {}));
        var G = n("1020"), q = n.n(G), J = n("f851"), z = n("5ad2"), Q = function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("div", [t._v("\n  Count: " + t._s(t.sortGroup["Group Count"]) + "\n  "), n("br"), t._v(" "), n("table", {staticClass: "table-borderless"}, [n("tr", [n("td", {staticClass: "text-nowrap p-0"}, [t._v("\n        Sort Method"), t.sortGroup["Sort Methods Used"].length > 1 ? [t._v("s")] : t._e(), t._v(":\n      ")], 2), t._v(" "), n("td", {staticClass: "p-0 pl-1"}, [t._v("\n        " + t._s(t._f("keysToString")(t.sortGroup["Sort Methods Used"])) + "\n      ")])])]), t._v(" "), n("table", {staticClass: "table-borderless"}, [n("tr", [n("td", {staticClass: "p-0"}, [t._v("\n        Memory:\n      ")]), t._v(" "), n("td", {staticClass: "p-0 pl-1"}, [t._v("\n        Average: " + t._s(t._f("kilobytes")(t.sortGroup["Sort Space Memory"]["Average Sort Space Used"])) + "\n        "), n("br"), t._v("\n        Peak: " + t._s(t._f("kilobytes")(t.sortGroup["Sort Space Memory"]["Peak Sort Space Used"])) + "\n      ")])])])])
            }, Z = [], tt = {props: ["sortGroup"], filters: {keysToString: ft, kilobytes: vt}}, et = tt, nt = n("2877"),
            at = Object(nt["a"])(et, Q, Z, !1, null, null, null), ot = at.exports;

        function st(t, e) {
            var n = Object.keys(t);
            if (Object.getOwnPropertySymbols) {
                var a = Object.getOwnPropertySymbols(t);
                e && (a = a.filter((function (e) {
                    return Object.getOwnPropertyDescriptor(t, e).enumerable
                }))), n.push.apply(n, a)
            }
            return n
        }

        function rt(t) {
            for (var e = 1; e < arguments.length; e++) {
                var n = null != arguments[e] ? arguments[e] : {};
                e % 2 ? st(Object(n), !0).forEach((function (e) {
                    it(t, e, n[e])
                })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : st(Object(n)).forEach((function (e) {
                    Object.defineProperty(t, e, Object.getOwnPropertyDescriptor(n, e))
                }))
            }
            return t
        }

        function it(t, e, n) {
            return e in t ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0
            }) : t[e] = n, t
        }

        function lt(t) {
            return void 0 === t ? "N/A" : t < 1e3 ? parseFloat(t.toPrecision(3)).toLocaleString() + "ms" : I["duration"](t).format("w[w] d[d] h[h] m[m] s[s] SSS[ms]", {largest: 2})
        }

        function ct(t) {
            return t ? (t = parseFloat(t.toPrecision(3)), t.toLocaleString()) : "N/A"
        }

        function ut(t) {
            return void 0 === t ? "N/A" : t.toLocaleString()
        }

        function pt(t) {
            return void 0 === t ? "N/A" : t.toLocaleString()
        }

        function dt(t) {
            var e = parseFloat(t.toPrecision(2)).toLocaleString(),
                n = c["template"]('${f}&nbsp;<span class="text-muted">&times;</span>');
            return n({f: e})
        }

        function ft(t) {
            return t instanceof Array || (t = [t]), t = c["map"](t, (function (t) {
                return c["escape"](t.replace(/(^\(|\)$)/g, ""))
            })), t.join(", ")
        }

        function _t(t, e) {
            return c["map"](t, (function (t) {
                var n = c["escape"](t);
                return e && (n += -1 !== e.indexOf(t) ? '&nbsp;<span class="text-muted">(presort)</span>' : ""), n
            })).join(", ")
        }

        function ht(t, e, n) {
            return n = n || "...", t.length > e ? t.slice(0, e) + n : t
        }

        function vt(t) {
            return mt(1024 * t)
        }

        function bt(t) {
            return mt(t)
        }

        function mt(t) {
            var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 2, n = 1024, a = e < 0 ? 0 : e,
                o = ["Bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"],
                s = Math.floor(Math.log(t) / Math.log(n)), r = c["template"]("${value} ${unit}"),
                i = parseFloat((t / Math.pow(n, s)).toFixed(a)).toLocaleString();
            return r({value: i, unit: o[s]})
        }

        function Et(t) {
            return t ? t.toLocaleString() + "<br><small>" + mt(8 * t * 1024) + "</small>" : ""
        }

        function gt(t) {
            return isNaN(t) ? "-" : c["round"](100 * t) + "%"
        }

        function St(t) {
            "string" === typeof t && (t = c["escape"](t).split(/\s*,\s*/));
            var e = c["template"]("<% _.forEach(lines, function(line) { %><li><%- line %></li><% }); %>");
            return '<ul class="list-unstyled">' + e({lines: t}) + "</ul>"
        }

        function Tt(t) {
            var e = new r["c"](rt({}, ot, {propsData: {sortGroup: t}}));
            return e.$mount().$el.outerHTML
        }

        function Ct(t, e) {
            if (c["has"](X, t)) {
                if (X[t] === j.duration) return lt(e);
                if (X[t] === j.boolean) return e ? "yes" : "no";
                if (X[t] === j.cost) return ct(e);
                if (X[t] === j.rows) return ut(e);
                if (X[t] === j.loops) return pt(e);
                if (X[t] === j.factor) return dt(e);
                if (X[t] === j.estimateDirection) switch (e) {
                    case M.over:
                        return '<i class="fa fa-arrow-up"></i> over';
                    case M.under:
                        return '<i class="fa fa-arrow-down"></i> under';
                    default:
                        return "-"
                } else {
                    if (X[t] === j.json) return JSON.stringify(e, null, 2);
                    if (X[t] === j.bytes) return bt(e);
                    if (X[t] === j.kilobytes) return vt(e);
                    if (X[t] === j.blocks) return Et(e);
                    if (X[t] === j.list) return St(e);
                    if (X[t] === j.sortGroups) return Tt(e)
                }
            }
            return c["escape"](e)
        }

        function Ot(t) {
            var e;
            return t > 90 ? e = 4 : t > 40 ? e = 3 : t > 10 && (e = 2), e ? "c-" + e : ""
        }

        function yt(t) {
            return q.a.highlight(t, {language: "pgsql"}).value
        }

        function wt(t) {
            return q.a.highlight(t, {language: "json"}).value
        }

        function xt(t) {
            return xt = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, xt(t)
        }

        function Lt(t) {
            return It(t) || Rt(t) || At()
        }

        function At() {
            throw new TypeError("Invalid attempt to spread non-iterable instance")
        }

        function Rt(t) {
            if (Symbol.iterator in Object(t) || "[object Arguments]" === Object.prototype.toString.call(t)) return Array.from(t)
        }

        function It(t) {
            if (Array.isArray(t)) {
                for (var e = 0, n = new Array(t.length); e < t.length; e++) n[e] = t[e];
                return n
            }
        }

        function Pt(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function kt(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function Nt(t, e, n) {
            return e && kt(t.prototype, e), n && kt(t, n), t
        }

        function Dt(t, e) {
            return !e || "object" !== xt(e) && "function" !== typeof e ? Mt(t) : e
        }

        function Mt(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function Ut(t) {
            return Ut = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, Ut(t)
        }

        function Bt(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && Wt(t, e)
        }

        function Wt(t, e) {
            return Wt = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, Wt(t, e)
        }

        N()(I), q.a.registerLanguage("pgsql", J), q.a.registerLanguage("json", z);
        var Vt = function (t) {
            function e() {
                var t;
                return Pt(this, e), t = Dt(this, Ut(e).apply(this, arguments)), t.executionTimePercent = NaN, t.selected = !1, t.showDetails = !1, t.collapsed = !1, t.activeTab = "general", t.costPercent = NaN, t.barWidth = 0, t.props = [], t.plans = [], t.rowsRemoved = NaN, t.rowsRemovedPercent = NaN, t.estimateDirections = M, t.highlightTypes = U, t.viewModes = B, t.orientations = K, t.nodeProps = H, t.workerProps = Y, t.helpService = new v, t.colorService = new R, t.lodash = c, t.notMiscProperties = [H.NODE_TYPE, H.CTE_NAME, H.EXCLUSIVE_DURATION, H.EXCLUSIVE_COST, H.TOTAL_COST, H.PLAN_ROWS, H.ACTUAL_ROWS, H.ACTUAL_LOOPS, H.OUTPUT, H.WORKERS, H.WORKERS_PLANNED, H.WORKERS_LAUNCHED, H.EXCLUSIVE_SHARED_HIT_BLOCKS, H.EXCLUSIVE_SHARED_READ_BLOCKS, H.EXCLUSIVE_SHARED_DIRTIED_BLOCKS, H.EXCLUSIVE_SHARED_WRITTEN_BLOCKS, H.EXCLUSIVE_TEMP_READ_BLOCKS, H.EXCLUSIVE_TEMP_WRITTEN_BLOCKS, H.EXCLUSIVE_LOCAL_HIT_BLOCKS, H.EXCLUSIVE_LOCAL_READ_BLOCKS, H.EXCLUSIVE_LOCAL_DIRTIED_BLOCKS, H.EXCLUSIVE_LOCAL_WRITTEN_BLOCKS, H.SHARED_HIT_BLOCKS, H.SHARED_READ_BLOCKS, H.SHARED_DIRTIED_BLOCKS, H.SHARED_WRITTEN_BLOCKS, H.TEMP_READ_BLOCKS, H.TEMP_WRITTEN_BLOCKS, H.LOCAL_HIT_BLOCKS, H.LOCAL_READ_BLOCKS, H.LOCAL_DIRTIED_BLOCKS, H.LOCAL_WRITTEN_BLOCKS, H.PLANNER_ESTIMATE_FACTOR, H.PLANNER_ESTIMATE_DIRECTION, H.SUBPLAN_NAME, H.GROUP_KEY, H.HASH_CONDITION, H.JOIN_TYPE, H.INDEX_NAME, H.HASH_CONDITION, H.EXCLUSIVE_IO_READ_TIME, H.EXCLUSIVE_IO_WRITE_TIME, H.IO_READ_TIME, H.IO_WRITE_TIME, H.HEAP_FETCHES, H.WAL_RECORDS, H.WAL_BYTES, H.WAL_FPI, H.NODE_ID, H.ROWS_REMOVED_BY_FILTER, H.ROWS_REMOVED_BY_JOIN_FILTER, H.ACTUAL_ROWS_REVISED, H.PLAN_ROWS_REVISED, H.ROWS_REMOVED_BY_FILTER_REVISED, H.ROWS_REMOVED_BY_JOIN_FILTER_REVISED], t
            }

            return Bt(e, t), Nt(e, [{
                key: "setShowDetails", value: function (t) {
                    this.showDetails = t
                }
            }, {
                key: "created", value: function () {
                    this.calculateProps(), this.calculateBar(), this.calculateDuration(), this.calculateCost(), this.calculateRowsRemoved(), this.plans = this.node[H.PLANS], this.plannerRowEstimateDirection = this.node[H.PLANNER_ESTIMATE_DIRECTION], this.plannerRowEstimateValue = this.node[H.PLANNER_ESTIMATE_FACTOR]
                }
            }, {
                key: "calculateDuration", value: function () {
                    var t = this.plan.planStats.executionTime || this.plan.content.Plan[H.ACTUAL_TOTAL_TIME];
                    this.executionTimePercent = c["round"](this.node[H.EXCLUSIVE_DURATION] / t * 100)
                }
            }, {
                key: "calculateCost", value: function () {
                    var t = this.plan.content.maxTotalCost;
                    this.costPercent = c["round"](this.node[H.EXCLUSIVE_COST] / t * 100)
                }
            }, {
                key: "calculateRowsRemoved", value: function () {
                    var t = this.rowsRemovedProp;
                    if (t) {
                        var e = this.node[H[t]];
                        this.rowsRemoved = e;
                        var n = this.node[H.ACTUAL_ROWS];
                        this.rowsRemovedPercent = c["floor"](e / (e + n) * 100), 100 === this.rowsRemovedPercent ? this.rowsRemovedPercentString = ">99" : 0 === this.rowsRemovedPercent ? this.rowsRemovedPercentString = "<1" : this.rowsRemovedPercentString = this.rowsRemovedPercent.toString()
                    }
                }
            }, {
                key: "calculateProps", value: function () {
                    this.props = c["chain"](this.node).omit(H.PLANS).omit(H.WORKERS).map((function (t, e) {
                        return {key: e, value: t}
                    })).value()
                }
            }, {
                key: "getNodeTypeDescription", value: function () {
                    return this.helpService.getNodeTypeDescription(this.node[H.NODE_TYPE])
                }
            }, {
                key: "getNodeName", value: function () {
                    var t = this.isParallelAware ? "Parallel " : "";
                    return t += this.node[H.NODE_TYPE], this.viewOptions.viewMode !== B.DOT || this.showDetails ? t : t.replace(/[^A-Z]/g, "")
                }
            }, {
                key: "shouldShowNodeBarLabel", value: function () {
                    return !!this.showDetails || !this.collapsed && this.viewOptions.viewMode !== B.DOT
                }
            }, {
                key: "calculateBar", value: function () {
                    var t;
                    if (this.$options && this.$options.filters) switch (this.viewOptions.highlightType) {
                        case U.DURATION:
                            if (t = this.node[H.EXCLUSIVE_DURATION], void 0 === t) {
                                this.highlightValue = null;
                                break
                            }
                            this.barWidth = Math.round(t / this.plan.planStats.maxDuration * 100), this.highlightValue = this.$options.filters.duration(t);
                            break;
                        case U.ROWS:
                            if (t = this.node[H.ACTUAL_ROWS], void 0 === t) {
                                this.highlightValue = null;
                                break
                            }
                            this.barWidth = Math.round(t / this.plan.planStats.maxRows * 100) || 0, this.highlightValue = this.$options.filters.rows(t);
                            break;
                        case U.COST:
                            if (t = this.node[H.EXCLUSIVE_COST], void 0 === t) {
                                this.highlightValue = null;
                                break
                            }
                            this.barWidth = Math.round(t / this.plan.planStats.maxCost * 100), this.highlightValue = this.$options.filters.cost(t);
                            break
                    }
                }
            }, {
                key: "getBarColor", value: function (t) {
                    return this.colorService.numberToColorHsl(t)
                }
            }, {
                key: "toggleCollapsed", value: function () {
                    this.collapsed = !this.collapsed
                }
            }, {
                key: "getHelpMessage", value: function (t) {
                    return this.helpService.getHelpMessage(t)
                }
            }, {
                key: "shouldShowProp", value: function (t, e) {
                    return (e || X[t] === j.increment || t === H.ACTUAL_ROWS) && -1 === this.notMiscProperties.indexOf(t)
                }
            }, {
                key: "setActiveTab", value: function (t) {
                    this.activeTab = t
                }
            }, {
                key: "formattedProp", value: function (t) {
                    var e = H[t], n = this.node[e];
                    return this.$options.filters.formatNodeProp(e, n)
                }
            }, {
                key: "rowsRemovedProp", get: function () {
                    var t = Object.keys(this.node).find((function (t) {
                        return t === H.ROWS_REMOVED_BY_FILTER_REVISED || t === H.ROWS_REMOVED_BY_JOIN_FILTER_REVISED
                    }));
                    return Object.keys(H).find((function (e) {
                        return H[e] === t
                    }))
                }
            }, {
                key: "shouldShowPlannerEstimate", get: function () {
                    return !(this.collapsed && !this.showDetails || this.viewOptions.viewMode === B.DOT) && ((this.estimationClass || this.showDetails) && this.plannerRowEstimateDirection !== M.none && this.plannerRowEstimateValue)
                }
            }, {
                key: "shouldShowCost", get: function () {
                    return !(this.collapsed && !this.showDetails || this.viewOptions.viewMode === B.DOT) && (this.node[H.EXCLUSIVE_COST] && (this.costClass || this.showDetails))
                }
            }, {
                key: "shouldShowRowsRemoved", get: function () {
                    return !!this.rowsRemovedClass && this.viewOptions.viewMode === B.FULL && !this.collapsed
                }
            }, {
                key: "durationClass", get: function () {
                    var t, e = this.executionTimePercent;
                    return e > 90 ? t = 4 : e > 40 ? t = 3 : e > 10 && (t = 2), !!t && "c-" + t
                }
            }, {
                key: "estimationClass", get: function () {
                    var t, e = this.node[H.PLANNER_ESTIMATE_FACTOR];
                    return e > 1e3 ? t = 4 : e > 100 ? t = 3 : e > 10 && (t = 2), !!t && "c-" + t
                }
            }, {
                key: "costClass", get: function () {
                    var t, e = this.costPercent;
                    return e > 90 ? t = 4 : e > 40 ? t = 3 : e > 10 && (t = 2), !!t && "c-" + t
                }
            }, {
                key: "rowsRemovedClass", get: function () {
                    var t, e = this.rowsRemovedPercent * this.executionTimePercent;
                    return e > 2e3 ? t = 4 : e > 500 && (t = 3), !!t && "c-" + t
                }
            }, {
                key: "heapFetchesClass", get: function () {
                    var t,
                        e = this.node[H.HEAP_FETCHES] / (this.node[H.ACTUAL_ROWS] + (this.node[H.ROWS_REMOVED_BY_FILTER] || 0) + (this.node[H.ROWS_REMOVED_BY_JOIN_FILTER] || 0)) * 100;
                    return e > 90 ? t = 4 : e > 40 ? t = 3 : e > 10 && (t = 2), !!t && "c-" + t
                }
            }, {
                key: "hasChildren", get: function () {
                    return !!this.plans
                }
            }, {
                key: "filterTooltip", get: function () {
                    return this.rowsRemovedPercentString + "% of rows removed by filter"
                }
            }, {
                key: "workersLaunchedCount", get: function () {
                    return c["isArray"](this.node[H.WORKERS]) ? this.node[H.WORKERS].length : parseInt(this.node[H.WORKERS], 0)
                }
            }, {
                key: "workersPlannedCount", get: function () {
                    return this.node[H.WORKERS_PLANNED_BY_GATHER]
                }
            }, {
                key: "workersPlannedCountReversed", get: function () {
                    var t = this.node[H.WORKERS_PLANNED_BY_GATHER];
                    return Lt(Array(t).keys()).slice().reverse()
                }
            }, {
                key: "isParallelAware", get: function () {
                    return this.node[H.PARALLEL_AWARE]
                }
            }, {
                key: "allWorkersLaunched", get: function () {
                    return !this.node[H.WORKERS_LAUNCHED] || this.node[H.WORKERS_PLANNED] === this.node[H.WORKERS_LAUNCHED]
                }
            }, {
                key: "shouldShowIoBuffers", get: function () {
                    var t = this,
                        e = ["EXCLUSIVE_SHARED_HIT_BLOCKS", "EXCLUSIVE_SHARED_READ_BLOCKS", "EXCLUSIVE_SHARED_DIRTIED_BLOCKS", "EXCLUSIVE_SHARED_WRITTEN_BLOCKS", "EXCLUSIVE_TEMP_READ_BLOCKS", "EXCLUSIVE_TEMP_WRITTEN_BLOCKS", "EXCLUSIVE_LOCAL_HIT_BLOCKS", "EXCLUSIVE_LOCAL_READ_BLOCKS", "EXCLUSIVE_LOCAL_DIRTIED_BLOCKS", "EXCLUSIVE_LOCAL_WRITTEN_BLOCKS", "EXCLUSIVE_IO_READ_TIME", "EXCLUSIVE_IO_WRITE_TIME"],
                        n = c["map"](e, (function (e) {
                            var n = t.node[H[e]];
                            return c["isNaN"](n) ? 0 : n
                        })), a = c["sum"](n);
                    return a > 0
                }
            }, {
                key: "isNeverExecuted", get: function () {
                    return this.plan.planStats.executionTime && !this.node[H.ACTUAL_LOOPS]
                }
            }, {
                key: "hasSeveralLoops", get: function () {
                    return this.node[H.ACTUAL_LOOPS] > 1
                }
            }, {
                key: "tilde", get: function () {
                    return this.hasSeveralLoops ? "~" : ""
                }
            }]), e
        }(r["c"]);
        Object(s["a"])([Object(r["b"])(Object)], Vt.prototype, "node", void 0), Object(s["a"])([Object(r["b"])(Object)], Vt.prototype, "plan", void 0), Object(s["a"])([Object(r["b"])(Object)], Vt.prototype, "viewOptions", void 0), Object(s["a"])([Object(r["b"])()], Vt.prototype, "eventBus", void 0), Object(s["a"])([Object(r["d"])("viewOptions.highlightType")], Vt.prototype, "calculateBar", null), Vt = Object(s["a"])([Object(r["a"])({
            name: "plan-node",
            filters: {
                cost: ct,
                duration: lt,
                factor: dt,
                formatNodeProp: Ct,
                keysToString: ft,
                sortKeys: _t,
                truncate: ht,
                rows: ut
            }
        })], Vt);
        var Ht = Vt, jt = Ht, Kt = Object(nt["a"])(jt, p, d, !1, null, null, null), Xt = Kt.exports, Ft = function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("div", {
                staticClass: "copy position-absolute",
                staticStyle: {top: "0", right: "0"}
            }, [n("button", {
                staticClass: "btn btn-outline-secondary bg-light btn-sm m-2",
                class: t.copied ? "d-none" : "d-block",
                attrs: {name: "copyRawButton"},
                on: {click: t.copyRaw}
            }, [n("i", {staticClass: "far fa-clipboard fa-fw"})]), t._v(" "), n("button", {
                directives: [{
                    name: "tippy",
                    rawName: "v-tippy",
                    value: {placement: "left", arrow: !0},
                    expression: "{ placement: 'left', arrow: true }"
                }],
                staticClass: "btn btn-outline-secondary bg-light btn-sm m-2",
                class: t.copied ? "d-block" : "d-none",
                attrs: {content: "copied"},
                on: {click: t.copyRaw}
            }, [n("i", {staticClass: "fa fa-check fa-fw text-success"})])])
        }, $t = [], Yt = n("e6a9"), Gt = n.n(Yt);

        function qt(t) {
            return qt = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, qt(t)
        }

        function Jt(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function zt(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function Qt(t, e, n) {
            return e && zt(t.prototype, e), n && zt(t, n), t
        }

        function Zt(t, e) {
            return !e || "object" !== qt(e) && "function" !== typeof e ? te(t) : e
        }

        function te(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function ee(t) {
            return ee = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, ee(t)
        }

        function ne(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && ae(t, e)
        }

        function ae(t, e) {
            return ae = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, ae(t, e)
        }

        var oe = function (t) {
            function e() {
                var t;
                return Jt(this, e), t = Zt(this, ee(e).apply(this, arguments)), t.copied = !1, t
            }

            return ne(e, t), Qt(e, [{
                key: "copyRaw", value: function () {
                    var t = this, e = Gt()(), n = e.toClipboard;
                    n(this.content), this.copied = !0, window.setTimeout((function () {
                        t.copied = !1
                    }), 2e3)
                }
            }]), e
        }(r["c"]);
        Object(s["a"])([Object(r["b"])(String)], oe.prototype, "content", void 0), oe = Object(s["a"])([Object(r["a"])({})], oe);
        var se = oe, re = se, ie = Object(nt["a"])(re, Ft, $t, !1, null, null, null), le = ie.exports,
            ce = function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("div", {staticClass: "diagram"}, [n("div", {staticClass: "flex-shrink-0"}, [n("div", {staticClass: "form-group text-center my-1"}, [n("div", {staticClass: "btn-group btn-group-xs"}, [n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.metric === t.metrics.time},
                    on: {
                        click: function (e) {
                            t.viewOptions.metric = t.metrics.time
                        }
                    }
                }, [t._v("time")]), t._v(" "), n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.metric === t.metrics.rows},
                    on: {
                        click: function (e) {
                            t.viewOptions.metric = t.metrics.rows
                        }
                    }
                }, [t._v("rows")]), t._v(" "), n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.metric === t.metrics.estimate_factor},
                    on: {
                        click: function (e) {
                            t.viewOptions.metric = t.metrics.estimate_factor
                        }
                    }
                }, [t._v("estimation")]), t._v(" "), n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.metric === t.metrics.cost},
                    on: {
                        click: function (e) {
                            t.viewOptions.metric = t.metrics.cost
                        }
                    }
                }, [t._v("cost")]), t._v(" "), n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.metric === t.metrics.buffers},
                    on: {
                        click: function (e) {
                            t.viewOptions.metric = t.metrics.buffers
                        }
                    }
                }, [t._v("buffers")])])]), t._v(" "), t.viewOptions.metric == t.metrics.buffers ? n("div", {staticClass: "form-group text-center my-1"}, [n("div", {staticClass: "btn-group btn-group-xs"}, [n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.buffersMetric === t.bufferLocations.shared},
                    attrs: {disabled: !t.plan.planStats.maxBlocks[t.bufferLocations.shared]},
                    on: {
                        click: function (e) {
                            t.viewOptions.buffersMetric = t.bufferLocations.shared
                        }
                    }
                }, [t._v("\n          shared")]), t._v(" "), n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.buffersMetric === t.bufferLocations.temp},
                    attrs: {disabled: !t.plan.planStats.maxBlocks[t.bufferLocations.temp]},
                    on: {
                        click: function (e) {
                            t.viewOptions.buffersMetric = t.bufferLocations.temp
                        }
                    }
                }, [t._v("\n          temp\n        ")]), t._v(" "), n("button", {
                    staticClass: "btn btn-outline-secondary",
                    class: {active: t.viewOptions.buffersMetric === t.bufferLocations.local},
                    attrs: {disabled: !t.plan.planStats.maxBlocks[t.bufferLocations.local]},
                    on: {
                        click: function (e) {
                            t.viewOptions.buffersMetric = t.bufferLocations.local
                        }
                    }
                }, [t._v("\n          local\n        ")])])]) : t._e(), t._v(" "), n("div", {staticClass: "legend text-center"}, [t.viewOptions.metric == t.metrics.buffers ? n("ul", {staticClass: "list-unstyled list-inline mb-0"}, [t.viewOptions.buffersMetric != t.bufferLocations.temp ? n("li", {staticClass: "list-inline-item"}, [n("span", {staticClass: "bg-hit rounded"}), t._v("\n          Hit\n        ")]) : t._e(), t._v(" "), t._m(0), t._v(" "), t.viewOptions.buffersMetric != t.bufferLocations.temp ? n("li", {staticClass: "list-inline-item"}, [n("span", {staticClass: "bg-dirtied"}), t._v("\n          Dirtied\n        ")]) : t._e(), t._v(" "), t._m(1)]) : t._e()])]), t._v(" "), n("div", {
                    ref: "container",
                    staticClass: "overflow-auto flex-grow-1"
                }, [t.dataAvailable ? n("table", {staticClass: "m-1"}, t._l(t.plans, (function (e, a) {
                    return n("tbody", [0 === a && t.plans.length > 1 ? n("tr", [n("th", {
                        staticClass: "subplan",
                        attrs: {colspan: "3"}
                    }, [t._v("\n            Main Query Plan\n          ")])]) : t._e(), t._v(" "), t._l(e, (function (e, a) {
                        return [e[1][t.nodeProps.SUBPLAN_NAME] ? n("tr", [t.isCTE(e[1]) ? t._e() : n("td"), t._v(" "), n("td", {
                            staticClass: "subplan pr-2",
                            class: {"font-weight-bold": t.isCTE(e[1])},
                            attrs: {colspan: t.isCTE(e[1]) ? 3 : 2}
                        }, [n("span", {staticClass: "tree-lines"}, [t._l(t.lodash.range(e[0]), (function (n) {
                            return [-1 != t.lodash.indexOf(e[3], n) ? [t._v("│")] : 0 !== n ? [t._v(" ")] : t._e()]
                        })), 0 !== a ? [t._v(t._s(e[2] ? "└" : "├"))] : t._e()], 2), t._v(" "), n("a", {
                            staticClass: "font-italic text-reset",
                            attrs: {href: ""},
                            on: {
                                click: function (n) {
                                    return n.preventDefault(), t.eventBus.$emit("clickcte", e[1][t.nodeProps.SUBPLAN_NAME])
                                }
                            }
                        }, [t._v("\n                " + t._s(e[1][t.nodeProps.SUBPLAN_NAME]) + "\n              ")])])]) : t._e(), t._v(" "), n("tr", {
                            ref: "node_" + e[1].nodeId,
                            refInFor: !0,
                            staticClass: "no-focus-outline node",
                            class: {selected: e[1].nodeId === t.selected, highlight: e[1].nodeId === t.highlightedNode},
                            attrs: {"data-tippy-content": t.getTooltipContent(e[1])},
                            on: {
                                mouseenter: function (n) {
                                    return t.eventBus.$emit("mouseovernode", e[1].nodeId)
                                }, mouseleave: function (n) {
                                    return t.eventBus.$emit("mouseoutnode", e[1].nodeId)
                                }
                            }
                        }, [n("td", {staticClass: "node-index"}, [n("a", {
                            staticClass: "font-weight-normal small",
                            attrs: {href: "#plan/node/" + e[1].nodeId},
                            on: {
                                click: function (t) {
                                }
                            }
                        }, [t._v("#" + t._s(e[1].nodeId))])]), t._v(" "), n("td", {staticClass: "node-type pr-2"}, [n("span", {staticClass: "tree-lines"}, [t._l(t.lodash.range(e[0]), (function (n) {
                            return [-1 != t.lodash.indexOf(e[3], n) ? [t._v("│")] : 0 !== n ? [t._v(" ")] : t._e()]
                        })), 0 !== a ? [e[1][t.nodeProps.SUBPLAN_NAME] ? [e[2] ? [t._v(" ")] : [t._v("│")]] : [t._v(t._s(e[2] ? "└" : "├"))]] : t._e()], 2), t._v("\n              " + t._s(t.nodeType(e)) + "\n            ")]), t._v(" "), n("td", [t.viewOptions.metric == t.metrics.time ? n("div", {
                            key: "node" + a + "time",
                            staticClass: "progress rounded-0 align-items-center bg-transparent",
                            staticStyle: {height: "5px"}
                        }, [n("div", {
                            staticClass: "progress-bar border-secondary bg-secondary",
                            class: {"border-left": e[1][t.nodeProps.EXCLUSIVE_DURATION] > 0},
                            style: "width: " + e[1][t.nodeProps.EXCLUSIVE_DURATION] / (t.plan.planStats.executionTime || t.plan.content.Plan[t.nodeProps.ACTUAL_TOTAL_TIME]) * 100 + "%; height:5px;",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "progress-bar bg-secondary-light",
                            style: "width: " + (e[1][t.nodeProps.ACTUAL_TOTAL_TIME] - e[1][t.nodeProps.EXCLUSIVE_DURATION]) / (t.plan.planStats.executionTime || t.plan.content.Plan[t.nodeProps.ACTUAL_TOTAL_TIME]) * 100 + "%; height:5px;",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        })]) : t.viewOptions.metric == t.metrics.rows ? n("div", {
                            key: "node" + a + "rows",
                            staticClass: "progress rounded-0 align-items-center bg-transparent",
                            staticStyle: {height: "5px"}
                        }, [n("div", {
                            staticClass: "bg-secondary",
                            staticStyle: {height: "5px"},
                            style: "width: " + Math.round(e[1][t.nodeProps.ACTUAL_ROWS_REVISED] / t.plan.planStats.maxRows * 100) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        })]) : t.viewOptions.metric == t.metrics.estimate_factor ? n("div", {
                            key: "node" + a + "estimation",
                            staticClass: "progress rounded-0 align-items-center bg-transparent justify-content-center",
                            staticStyle: {height: "10px"}
                        }, [n("span", {staticClass: "text-muted small"}, [n("i", {
                            staticClass: "fa fa-fw",
                            class: {"fa-arrow-down": e[1][t.nodeProps.PLANNER_ESTIMATE_DIRECTION] === t.estimateDirections.under}
                        })]), t._v(" "), n("div", {
                            staticClass: "progress-bar",
                            class: [e[1][t.nodeProps.PLANNER_ESTIMATE_DIRECTION] === t.estimateDirections.under ? "bg-secondary" : "bg-transparent"],
                            style: "width: " + t.estimateFactorPercent(e) + "%; height:5px;",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "progress-bar border-left",
                            staticStyle: {width: "1px", height: "5px"},
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "progress-bar",
                            class: [e[1][t.nodeProps.PLANNER_ESTIMATE_DIRECTION] === t.estimateDirections.over ? "bg-secondary" : "bg-transparent"],
                            style: "width: " + t.estimateFactorPercent(e) + "%; height:5px;",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("span", {staticClass: "text-muted small"}, [n("i", {
                            staticClass: "fa fa-fw",
                            class: {"fa-arrow-up": e[1][t.nodeProps.PLANNER_ESTIMATE_DIRECTION] === t.estimateDirections.over}
                        })])]) : t.viewOptions.metric == t.metrics.cost ? n("div", {
                            key: "node" + a + "cost",
                            staticClass: "progress rounded-0 align-items-center bg-transparent",
                            staticStyle: {height: "5px"}
                        }, [n("div", {
                            staticClass: "bg-secondary",
                            staticStyle: {height: "5px"},
                            style: "width: " + Math.round(e[1][t.nodeProps.EXCLUSIVE_COST] / t.plan.planStats.maxCost * 100) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        })]) : t.viewOptions.metric == t.metrics.buffers && t.viewOptions.buffersMetric == t.bufferLocations.shared && t.plan.planStats.maxBlocks[t.bufferLocations.shared] ? n("div", {
                            key: "node" + a + "buffers_shared",
                            staticClass: "progress rounded-0 align-items-center bg-transparent",
                            staticStyle: {height: "5px"}
                        }, [n("div", {
                            staticClass: "bg-hit",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_SHARED_HIT_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.shared] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-read",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_SHARED_READ_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.shared] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-dirtied",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_SHARED_DIRTIED_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.shared] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-written",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_SHARED_WRITTEN_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.shared] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        })]) : t.viewOptions.metric == t.metrics.buffers && t.viewOptions.buffersMetric == t.bufferLocations.temp && t.plan.planStats.maxBlocks[t.bufferLocations.temp] ? n("div", {
                            key: "node" + a + "buffers_temp",
                            staticClass: "progress rounded-0 align-items-center bg-transparent",
                            staticStyle: {height: "5px"}
                        }, [n("div", {
                            staticClass: "bg-read",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_TEMP_READ_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.temp] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-written",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_TEMP_WRITTEN_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.temp] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        })]) : t.viewOptions.metric == t.metrics.buffers && t.viewOptions.buffersMetric == t.bufferLocations.local && t.plan.planStats.maxBlocks[t.bufferLocations.local] ? n("div", {
                            key: "node" + a + "buffers_local",
                            staticClass: "progress rounded-0 align-items-center bg-transparent",
                            staticStyle: {height: "5px"}
                        }, [n("div", {
                            staticClass: "bg-hit",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_LOCAL_HIT_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.local] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-read",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_LOCAL_READ_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.local] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-dirtied",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_LOCAL_DIRTIED_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.local] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        }), t._v(" "), n("div", {
                            staticClass: "bg-written",
                            staticStyle: {height: "5px"},
                            style: "width: " + (Math.round(e[1][t.nodeProps.EXCLUSIVE_LOCAL_WRITTEN_BLOCKS] / t.plan.planStats.maxBlocks[t.bufferLocations.local] * 100) || 0) + "%",
                            attrs: {
                                role: "progressbar",
                                "aria-valuenow": "15",
                                "aria-valuemin": "0",
                                "aria-valuemax": "100"
                            }
                        })]) : t._e()])])]
                    }))], 2)
                })), 0) : n("div", {staticClass: "p-2 text-center text-muted"}, [n("em", [t._v("\n        No data available\n      ")])])])])
            }, ue = [function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("li", {staticClass: "list-inline-item"}, [n("span", {staticClass: "bg-read"}), t._v("\n          Read\n        ")])
            }, function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("li", {staticClass: "list-inline-item"}, [n("span", {staticClass: "bg-written"}), t._v("\n          Written\n        ")])
            }], pe = n("6f9a");

        function de(t) {
            return de = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, de(t)
        }

        function fe(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function _e(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function he(t, e, n) {
            return e && _e(t.prototype, e), n && _e(t, n), t
        }

        function ve(t, e) {
            return !e || "object" !== de(e) && "function" !== typeof e ? be(t) : e
        }

        function be(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function me(t) {
            return me = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, me(t)
        }

        function Ee(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && ge(t, e)
        }

        function ge(t, e) {
            return ge = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, ge(t, e)
        }

        var Se = function (t) {
            function e() {
                var t;
                return fe(this, e), t = ve(this, me(e).apply(this, arguments)), t.selected = null, t.plans = [[]], t.lodash = c, t.nodeProps = H, t.metrics = x, t.bufferLocations = L, t.estimateDirections = M, t.centerModes = W, t.highlightModes = V, t.highlightedNode = null, t.tippyInstances = [], t.viewOptions = {
                    metric: x.time,
                    buffersMetric: L.shared
                }, t
            }

            return Ee(e, t), he(e, [{
                key: "created", value: function () {
                    var t = this, e = localStorage.getItem("diagramViewOptions");
                    e && c["assignIn"](this.viewOptions, JSON.parse(e)), this.flatten(this.plans[0], 0, this.plan.content.Plan, !0, []), c["each"](this.plan.ctes, (function (e) {
                        var n = [];
                        t.flatten(n, 0, e, !0, []), t.plans.push(n)
                    })), this.eventBus.$on("mouseovernode", (function (e) {
                        t.highlightedNode = e
                    })), this.eventBus.$on("mouseoutnode", (function () {
                        t.highlightedNode = null
                    }));
                    var n = c["keys"](this.plan.planStats.maxBlocks);
                    -1 === c["indexOf"](n, this.viewOptions.buffersMetric) && (this.viewOptions.buffersMetric = c["min"](n))
                }
            }, {
                key: "mounted", value: function () {
                    this.loadTooltips()
                }
            }, {
                key: "onViewOptionsChanged", value: function (t, e) {
                    localStorage.setItem("diagramViewOptions", JSON.stringify(this.viewOptions)), r["c"].nextTick(this.loadTooltips)
                }
            }, {
                key: "loadTooltips", value: function () {
                    this.tippySingleton && this.tippySingleton.destroy(), c["each"](this.tippyInstances, (function (t) {
                        t.destroy()
                    })), this.tippyInstances = Object(pe["b"])(".diagram tr.node"), this.tippySingleton = Object(pe["a"])(this.tippyInstances, {
                        delay: 100,
                        allowHTML: !0
                    })
                }
            }, {
                key: "getTooltipContent", value: function (t) {
                    var e = "";
                    switch (this.viewOptions.metric) {
                        case x.time:
                            e += this.timeTooltip(t);
                            break;
                        case x.rows:
                            e += this.rowsTooltip(t);
                            break;
                        case x.estimate_factor:
                            e += this.estimateFactorTooltip(t);
                            break;
                        case x.cost:
                            e += this.costTooltip(t);
                            break;
                        case x.buffers:
                            e += this.buffersTooltip(t);
                            break
                    }
                    return t[H.CTE_NAME] && (e += "<br><em>CTE " + t[H.CTE_NAME] + "</em>"), e
                }
            }, {
                key: "timeTooltip", value: function (t) {
                    return ["Duration: <br>Exclusive: ", lt(t[H.EXCLUSIVE_DURATION]), ", Total: ", lt(t[H.ACTUAL_TOTAL_TIME])].join("")
                }
            }, {
                key: "rowsTooltip", value: function (t) {
                    return ["Rows: ", ut(t[H.ACTUAL_ROWS_REVISED])].join("")
                }
            }, {
                key: "estimateFactorTooltip", value: function (t) {
                    var e = t[H.PLANNER_ESTIMATE_FACTOR], n = t[H.PLANNER_ESTIMATE_DIRECTION], a = "";
                    if (void 0 === e || void 0 === n) return "N/A";
                    switch (n) {
                        case M.over:
                            a += '<i class="fa fa-arrow-up"></i> over';
                            break;
                        case M.under:
                            a += '<i class="fa fa-arrow-down"></i> under';
                            break;
                        default:
                            a += "Correctly"
                    }
                    return a += " estimated", a += 1 !== e ? " by <b>" + dt(e) + "</b>" : "", a += "<br>", a += "Planned: " + t[H.PLAN_ROWS_REVISED], a += " 🡒 Actual: " + t[H.ACTUAL_ROWS_REVISED], a
                }
            }, {
                key: "costTooltip", value: function (t) {
                    return ["Cost: ", ut(t[H.EXCLUSIVE_COST])].join("")
                }
            }, {
                key: "buffersTooltip", value: function (t) {
                    var e, n, a, o, s = "";
                    switch (this.viewOptions.buffersMetric) {
                        case L.shared:
                            e = t[H.EXCLUSIVE_SHARED_HIT_BLOCKS], n = t[H.EXCLUSIVE_SHARED_READ_BLOCKS], o = t[H.EXCLUSIVE_SHARED_DIRTIED_BLOCKS], a = t[H.EXCLUSIVE_SHARED_WRITTEN_BLOCKS];
                            break;
                        case L.temp:
                            n = t[H.EXCLUSIVE_TEMP_READ_BLOCKS], a = t[H.EXCLUSIVE_TEMP_WRITTEN_BLOCKS];
                            break;
                        case L.local:
                            e = t[H.EXCLUSIVE_LOCAL_HIT_BLOCKS], n = t[H.EXCLUSIVE_LOCAL_READ_BLOCKS], o = t[H.EXCLUSIVE_LOCAL_DIRTIED_BLOCKS], a = t[H.EXCLUSIVE_LOCAL_WRITTEN_BLOCKS];
                            break
                    }
                    switch (s += '<table class="table text-white table-sm table-borderless mb-0">', s += e ? '<tr><td>Hit:</td><td class="text-right">' + Et(e) + "</td></tr>" : "", s += n ? '<tr><td>Read:</td><td class="text-right">' + Et(n) + "</td></tr>" : "", s += o ? '<tr><td>Dirtied:</td><td class="text-right">' + Et(o) + "</td></tr>" : "", s += a ? '<tr><td>Written:</td><td class="text-right">' + Et(a) + "</td></tr>" : "", s += "</table>", e || n || o || a || (s = " N/A"), this.viewOptions.buffersMetric) {
                        case L.shared:
                            s = "Shared Blocks:" + s;
                            break;
                        case L.temp:
                            s = "Temp Blocks:" + s;
                            break;
                        case L.local:
                            s = "Local Blocks:" + s;
                            break
                    }
                    return s
                }
            }, {
                key: "nodeType", value: function (t) {
                    return t[1][H.NODE_TYPE]
                }
            }, {
                key: "flatten", value: function (t, e, n, a, o) {
                    var s = this;
                    t.push([e, n, a, c["concat"]([], o)]), a || o.push(e), c["each"](n.Plans, (function (a) {
                        s.flatten(t, e + 1, a, a === c["last"](n.Plans), o)
                    })), a || o.pop()
                }
            }, {
                key: "estimateFactorPercent", value: function (t) {
                    var e = t[1];
                    return e[H.PLANNER_ESTIMATE_FACTOR] === 1 / 0 ? 100 : (e[H.PLANNER_ESTIMATE_FACTOR] || 0) / this.maxEstimateFactor * 100
                }
            }, {
                key: "isCTE", value: function (t) {
                    return c["startsWith"](t[H.SUBPLAN_NAME], "CTE")
                }
            }, {
                key: "onSelectedNodeChange", value: function (t) {
                    var e = this.$refs["node_" + t][0], n = this.$refs.container;
                    E(n, e, !1)
                }
            }, {
                key: "maxEstimateFactor", get: function () {
                    var t = c["max"](c["map"](this.plans, (function (t) {
                        return c["max"](c["map"](t, (function (t) {
                            var e = t[1][H.PLANNER_ESTIMATE_FACTOR];
                            if (e !== 1 / 0) return e
                        })))
                    })));
                    return 2 * t || 1
                }
            }, {
                key: "dataAvailable", get: function () {
                    return this.viewOptions.metric !== this.metrics.buffers || this.viewOptions.buffersMetric
                }
            }]), e
        }(r["c"]);
        Object(s["a"])([Object(r["b"])()], Se.prototype, "plan", void 0), Object(s["a"])([Object(r["b"])()], Se.prototype, "eventBus", void 0), Object(s["a"])([Object(r["d"])("viewOptions", {deep: !0})], Se.prototype, "onViewOptionsChanged", null), Object(s["a"])([Object(r["d"])("selected")], Se.prototype, "onSelectedNodeChange", null), Se = Object(s["a"])([Object(r["a"])({filters: {durationClass: Ot}})], Se);
        var Te = Se, Ce = Te, Oe = Object(nt["a"])(Ce, ce, ue, !1, null, null, null), ye = Oe.exports,
            we = function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("div", {staticClass: "p-2 small stats"}, [n("h6", {staticClass: "mt-2"}, [t._v("Per table stats")]), t._v(" "), n("sorted-table", {
                    ref: "table",
                    staticClass: "table table-nonfluid table-sm table-bordered align-top",
                    attrs: {
                        values: t.perTable,
                        ascIcon: "<span> ▲</span>",
                        descIcon: "<span> ▼</span>",
                        sort: "time",
                        dir: "desc"
                    },
                    scopedSlots: t._u([{
                        key: "body", fn: function (e) {
                            return [t._l(e.values, (function (e) {
                                return [n("stats-table-item", {attrs: {value: e, executionTime: t.executionTime}})]
                            }))]
                        }
                    }])
                }, [n("thead", {staticClass: "thead-dark"}, [n("tr", [n("th", {attrs: {scope: "col"}}, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "name"}
                }, [t._v("Table")])], 1), t._v(" "), n("th", {
                    staticClass: "text-right",
                    attrs: {scope: "col"}
                }, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "count"}
                }, [t._v("Count")])], 1), t._v(" "), n("th", {
                    staticClass: "text-right",
                    attrs: {scope: "col", colspan: "2"}
                }, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "time"}
                }, [t._v("Time")])], 1)])]), t._v(" "), t._v(" "), t.perTable.length ? t._e() : n("tbody", [n("tr", [n("td", {
                    staticClass: "text-center font-italic",
                    attrs: {colspan: "3"}
                }, [t._v("No tables used")])])])]), t._v(" "), n("h6", [t._v("Per node type stats")]), t._v(" "), n("sorted-table", {
                    staticClass: "table table-nonfluid table-sm table-bordered align-top",
                    attrs: {
                        values: t.perNodeType,
                        ascIcon: "<span> ▲</span>",
                        descIcon: "<span> ▼</span>",
                        sort: "time",
                        dir: "desc"
                    },
                    scopedSlots: t._u([{
                        key: "body", fn: function (e) {
                            return [t._l(e.values, (function (e) {
                                return [n("stats-table-item", {attrs: {value: e, executionTime: t.executionTime}})]
                            }))]
                        }
                    }])
                }, [n("thead", {staticClass: "thead-dark"}, [n("tr", [n("th", {attrs: {scope: "col"}}, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "name"}
                }, [t._v("Node Type")])], 1), t._v(" "), n("th", {
                    staticClass: "text-right",
                    attrs: {scope: "col"}
                }, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "count"}
                }, [t._v("Count")])], 1), t._v(" "), n("th", {
                    staticClass: "text-right",
                    attrs: {scope: "col", colspan: "2"}
                }, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "time"}
                }, [t._v("Time")])], 1)])])]), t._v(" "), n("h6", [t._v("Per index stats")]), t._v(" "), n("sorted-table", {
                    staticClass: "table table-nonfluid table-sm table-bordered align-top",
                    attrs: {
                        values: t.perIndex,
                        ascIcon: "<span> ▲</span>",
                        descIcon: "<span> ▼</span>",
                        sort: "time",
                        dir: "desc"
                    },
                    scopedSlots: t._u([{
                        key: "body", fn: function (e) {
                            return [t._l(e.values, (function (e) {
                                return [n("stats-table-item", {attrs: {value: e, executionTime: t.executionTime}})]
                            }))]
                        }
                    }])
                }, [n("thead", {staticClass: "thead-dark"}, [n("tr", [n("th", {attrs: {scope: "col"}}, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "name"}
                }, [t._v("Index Name")])], 1), t._v(" "), n("th", {
                    staticClass: "text-right",
                    attrs: {scope: "col"}
                }, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "count"}
                }, [t._v("Count")])], 1), t._v(" "), n("th", {
                    staticClass: "text-right",
                    attrs: {scope: "col", colspan: "2"}
                }, [n("sort-link", {
                    staticClass: "text-white",
                    attrs: {name: "time"}
                }, [t._v("Time")])], 1)])]), t._v(" "), t._v(" "), t.perIndex.length ? t._e() : n("tbody", [n("tr", [n("td", {
                    staticClass: "text-center font-italic",
                    attrs: {colspan: "3"}
                }, [t._v("No index used")])])])])], 1)
            }, xe = [], Le = n("9871"), Ae = function () {
                var t = this, e = t.$createElement, n = t._self._c || e;
                return n("fragment", [n("thead", {staticClass: "thead-light"}, [n("tr", {
                    staticClass: "user-select-none",
                    attrs: {role: "button"},
                    on: {
                        click: function (e) {
                            e.preventDefault(), t.expanded = !t.expanded
                        }
                    }
                }, [n("th", [n("i", {
                    staticClass: "fa fa-fw",
                    class: {"fa-chevron-right": !t.expanded, "fa-chevron-down": t.expanded}
                }), t._v("\n        " + t._s(t.value.name) + "\n      ")]), t._v(" "), n("th", {staticClass: "text-right"}, [t._v(t._s(t.value.count))]), t._v(" "), n("th", {staticClass: "text-right"}, [n("span", {
                    staticClass: "alert p-0 px-1",
                    class: t.$options.filters.durationClass(100 * t.value.timePercent)
                }, [t._v("\n          " + t._s(t._f("duration")(t.value.time, !0)) + "\n        ")])]), t._v(" "), n("th", {staticClass: "text-right"}, [t._v(t._s(t._f("percent")(t.value.timePercent)))])])]), t._v(" "), n("tbody", {class: t.expanded ? "" : "d-none"}, t._l(t.lodash.reverse(t.lodash.sortBy(t.value.nodes, t.nodeProps.EXCLUSIVE_DURATION)), (function (e) {
                    return n("tr", {staticStyle: {"font-size": "smaller"}}, [n("td", {staticClass: "pl-3"}, [n("a", {
                        staticClass: "mr-1",
                        attrs: {href: "#plan/node/" + e.nodeId}
                    }, [t._v("#" + t._s(e.nodeId))]), t._v(" " + t._s(e[t.nodeProps.NODE_TYPE]) + "\n      ")]), t._v(" "), n("td", {staticClass: "text-right"}), t._v(" "), n("td", {staticClass: "text-right"}, [n("span", {staticClass: "px-1"}, [t._v("\n          " + t._s(t._f("duration")(e[t.nodeProps.EXCLUSIVE_DURATION], !0)) + "\n        ")])]), t._v(" "), n("td", {staticClass: "text-right"}, [t._v("\n        " + t._s(t._f("percent")(t.durationPercent(e))) + "\n      ")])])
                })), 0)])
            }, Re = [], Ie = n("3f08");

        function Pe(t) {
            return Pe = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, Pe(t)
        }

        function ke(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function Ne(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function De(t, e, n) {
            return e && Ne(t.prototype, e), n && Ne(t, n), t
        }

        function Me(t, e) {
            return !e || "object" !== Pe(e) && "function" !== typeof e ? Ue(t) : e
        }

        function Ue(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function Be(t) {
            return Be = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, Be(t)
        }

        function We(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && Ve(t, e)
        }

        function Ve(t, e) {
            return Ve = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, Ve(t, e)
        }

        var He = function (t) {
            function e() {
                var t;
                return ke(this, e), t = Me(this, Be(e).apply(this, arguments)), t.expanded = !1, t.lodash = c, t.nodeProps = H, t
            }

            return We(e, t), De(e, [{
                key: "durationPercent", value: function (t) {
                    return t[H.EXCLUSIVE_DURATION] / this.executionTime
                }
            }]), e
        }(r["c"]);
        Object(s["a"])([Object(r["b"])()], He.prototype, "value", void 0), Object(s["a"])([Object(r["b"])()], He.prototype, "executionTime", void 0), He = Object(s["a"])([Object(r["a"])({
            filters: {
                duration: lt,
                durationClass: Ot,
                percent: gt
            }, components: {Fragment: Ie["a"]}
        })], He);
        var je = He, Ke = je, Xe = Object(nt["a"])(Ke, Ae, Re, !1, null, null, null), Fe = Xe.exports;

        function $e(t) {
            return $e = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, $e(t)
        }

        function Ye(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function Ge(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function qe(t, e, n) {
            return e && Ge(t.prototype, e), n && Ge(t, n), t
        }

        function Je(t, e) {
            return !e || "object" !== $e(e) && "function" !== typeof e ? ze(t) : e
        }

        function ze(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function Qe(t) {
            return Qe = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, Qe(t)
        }

        function Ze(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && tn(t, e)
        }

        function tn(t, e) {
            return tn = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, tn(t, e)
        }

        var en = function (t) {
            function e() {
                var t;
                return Ye(this, e), t = Je(this, Qe(e).apply(this, arguments)), t.nodes = [], t.nodeProps = H, t.executionTime = 0, t
            }

            return Ze(e, t), qe(e, [{
                key: "created", value: function () {
                    var t = this;
                    this.executionTime = this.plan.planStats.executionTime || this.plan.content.Plan[H.ACTUAL_TOTAL_TIME];
                    var e = this.plan.content.Plan;
                    this.flatten(this.nodes, e), c["each"](this.plan.ctes, (function (e) {
                        t.flatten(t.nodes, e)
                    }))
                }
            }, {
                key: "flatten", value: function (t, e) {
                    var n = this;
                    t.push(e), c["each"](e.Plans, (function (e) {
                        n.flatten(t, e)
                    }))
                }
            }, {
                key: "durationPercent", value: function (t) {
                    return c["sumBy"](t, H.EXCLUSIVE_DURATION) / this.executionTime
                }
            }, {
                key: "perTable", get: function () {
                    var t = this, e = c["groupBy"](c["filter"](this.nodes, (function (t) {
                        return void 0 !== t[H.RELATION_NAME]
                    })), H.RELATION_NAME), n = [];
                    return c["each"](e, (function (e, a) {
                        n.push({
                            name: a,
                            count: e.length,
                            time: c["sumBy"](e, H.EXCLUSIVE_DURATION),
                            timePercent: t.durationPercent(e),
                            nodes: e
                        })
                    })), n
                }
            }, {
                key: "perNodeType", get: function () {
                    var t = this, e = c["groupBy"](this.nodes, H.NODE_TYPE), n = [];
                    return c["each"](e, (function (e, a) {
                        n.push({
                            name: a,
                            count: e.length,
                            time: c["sumBy"](e, H.EXCLUSIVE_DURATION),
                            timePercent: t.durationPercent(e),
                            nodes: e
                        })
                    })), n
                }
            }, {
                key: "perIndex", get: function () {
                    var t = this, e = c["groupBy"](c["filter"](this.nodes, (function (t) {
                        return void 0 !== t[H.INDEX_NAME]
                    })), H.INDEX_NAME), n = [];
                    return c["each"](e, (function (e, a) {
                        n.push({
                            name: a,
                            count: e.length,
                            time: c["sumBy"](e, H.EXCLUSIVE_DURATION),
                            timePercent: t.durationPercent(e),
                            nodes: e
                        })
                    })), n
                }
            }]), e
        }(r["c"]);
        Object(s["a"])([Object(r["b"])()], en.prototype, "plan", void 0), en = Object(s["a"])([Object(r["a"])({
            components: {
                SortedTable: Le["SortedTable"],
                SortLink: Le["SortLink"],
                StatsTableItem: Fe
            }
        })], en);
        var nn = en, an = nn, on = Object(nt["a"])(an, we, xe, !1, null, null, null), sn = on.exports;

        function rn(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        var ln = function t(e) {
            rn(this, t), this[H.NODE_TYPE] = e;
            var n = /^((?:Parallel\s+)?(?:Seq\sScan|Tid.*Scan|Bitmap\s+Heap\s+Scan|(?:Async\s+)?Foreign\s+Scan|Update|Insert|Delete))\son\s(\S+)(?:\s+(\S+))?$/.exec(e),
                a = /^(Bitmap\s+Index\s+Scan)\son\s(\S+)$/.exec(e),
                o = /^((?:Parallel\s+)?Index(?:\sOnly)?\sScan(?:\sBackward)?)\susing\s(\S+)\son\s(\S+)(?:\s+(\S+))?$/.exec(e),
                s = /^(CTE\sScan)\son\s(\S+)(?:\s+(\S+))?$/.exec(e),
                r = /^(Function\sScan)\son\s(\S+)(?:\s+(\S+))?$/.exec(e), i = /^(Subquery\sScan)\son\s(.+)$/.exec(e);
            n ? (this[H.NODE_TYPE] = n[1], this[H.RELATION_NAME] = n[2], n[3] && (this[H.ALIAS] = n[3])) : a ? (this[H.NODE_TYPE] = a[1], this[H.INDEX_NAME] = a[2]) : o ? (this[H.NODE_TYPE] = o[1], this[H.INDEX_NAME] = o[2], this[H.RELATION_NAME] = o[3], o[4] && (this[H.ALIAS] = o[4])) : s ? (this[H.NODE_TYPE] = s[1], this[H.CTE_NAME] = s[2], s[3] && (this[H.ALIAS] = s[3])) : r ? (this[H.NODE_TYPE] = r[1], this[H.FUNCTION_NAME] = r[2], r[3] && (this[H.ALIAS] = r[3])) : i && (this[H.NODE_TYPE] = i[1]);
            var l = /^(Parallel\s+)(.*)/.exec(this[H.NODE_TYPE]);
            l && (this[H.NODE_TYPE] = l[2], this[H.PARALLEL_AWARE] = !0);
            var c = /(.*)\sJoin$/.exec(this[H.NODE_TYPE]), u = /(.*)\s+(Full|Left|Right|Anti)/.exec(this[H.NODE_TYPE]);
            c && (this[H.NODE_TYPE] = c[1], u && (this[H.NODE_TYPE] = u[1], this[H.JOIN_TYPE] = u[2]), this[H.NODE_TYPE] += " Join")
        };

        function cn(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        var un = function t(e) {
            cn(this, t), this[Y.WORKER_NUMBER] = e
        }, pn = n("3c66"), dn = n.n(pn);

        function fn(t, e, n) {
            return e in t ? Object.defineProperty(t, e, {
                value: n,
                enumerable: !0,
                configurable: !0,
                writable: !0
            }) : t[e] = n, t
        }

        function _n(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function hn(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function vn(t, e, n) {
            return e && hn(t.prototype, e), n && hn(t, n), t
        }

        var bn = function () {
            function t() {
                _n(this, t), this.nodeId = 0
            }

            return vn(t, [{
                key: "createPlan", value: function (t, e, n) {
                    n = n.replace(/(\S)(?!$)(\s{2,})/gm, "$1 ");
                    var a = {
                        id: H.PEV_PLAN_TAG + (new Date).getTime().toString(),
                        name: t || "plan created on " + P()().format("LLL"),
                        createdOn: new Date,
                        content: e,
                        query: n,
                        planStats: {},
                        ctes: [],
                        isAnalyze: c["has"](e.Plan, H.ACTUAL_ROWS),
                        isVerbose: this.findOutputProperty(e.Plan)
                    };
                    return this.nodeId = 1, this.processNode(a.content.Plan, a), this.calculateMaximums(a.content), a
                }
            }, {
                key: "isCTE", value: function (t) {
                    return "InitPlan" === t[H.PARENT_RELATIONSHIP] && c["startsWith"](t[H.SUBPLAN_NAME], "CTE")
                }
            }, {
                key: "processNode", value: function (t, e) {
                    var n = this;
                    t.nodeId = this.nodeId++, this.calculatePlannerEstimate(t), c["each"](t[H.PLANS], (function (a) {
                        n.isCTE(a) || "InitPlan" === a[H.PARENT_RELATIONSHIP] || "SubPlan" === a[H.PARENT_RELATIONSHIP] || (a[H.WORKERS_PLANNED_BY_GATHER] = t[H.WORKERS_PLANNED] || t[H.WORKERS_PLANNED_BY_GATHER]), n.isCTE(a) && e.ctes.push(a), n.processNode(a, e)
                    })), c["remove"](t[H.PLANS], (function (t) {
                        return n.isCTE(t)
                    })), this.calculateActuals(t), this.calculateExclusives(t)
                }
            }, {
                key: "calculateMaximums", value: function (t) {
                    function e(t) {
                        return c["map"](t, (function (t) {
                            return [t, e(t[H.PLANS])]
                        }))
                    }

                    var n = c["flattenDeep"](e([t.Plan])), a = c["maxBy"](n, H.ACTUAL_ROWS);
                    a && (t.maxRows = a[H.ACTUAL_ROWS]);
                    var o = c["maxBy"](n, H.EXCLUSIVE_COST);
                    o && (t.maxCost = o[H.EXCLUSIVE_COST]);
                    var s = c["maxBy"](n, H.TOTAL_COST);
                    s && (t.maxTotalCost = s[H.TOTAL_COST]);
                    var r = c["maxBy"](n, H.EXCLUSIVE_DURATION);

                    function i(t) {
                        return t[H.EXCLUSIVE_SHARED_HIT_BLOCKS] + t[H.EXCLUSIVE_SHARED_READ_BLOCKS] + t[H.EXCLUSIVE_SHARED_DIRTIED_BLOCKS] + t[H.EXCLUSIVE_SHARED_WRITTEN_BLOCKS]
                    }

                    r && (t.maxDuration = r[H.EXCLUSIVE_DURATION]), t.maxBlocks || (t.maxBlocks = {});
                    var l = c["maxBy"](n, (function (t) {
                        return i(t)
                    }));

                    function u(t) {
                        return t[H.EXCLUSIVE_TEMP_READ_BLOCKS] + t[H.EXCLUSIVE_TEMP_WRITTEN_BLOCKS]
                    }

                    l && i(l) && (t.maxBlocks[L.shared] = i(l));
                    var p = c["maxBy"](n, (function (t) {
                        return u(t)
                    }));

                    function d(t) {
                        return t[H.EXCLUSIVE_LOCAL_HIT_BLOCKS] + t[H.EXCLUSIVE_LOCAL_READ_BLOCKS] + t[H.EXCLUSIVE_LOCAL_DIRTIED_BLOCKS] + t[H.EXCLUSIVE_LOCAL_WRITTEN_BLOCKS]
                    }

                    p && u(p) && (t.maxBlocks[L.temp] = u(p));
                    var f = c["maxBy"](n, (function (t) {
                        return d(t)
                    }));
                    f && d(f) && (t.maxBlocks[L.local] = d(f))
                }
            }, {
                key: "calculateActuals", value: function (t) {
                    if (!c["isUndefined"](t[H.ACTUAL_TOTAL_TIME])) {
                        var e = (t[H.WORKERS_PLANNED_BY_GATHER] || 0) + 1;
                        t[H.ACTUAL_TOTAL_TIME] = t[H.ACTUAL_TOTAL_TIME] * t[H.ACTUAL_LOOPS] / e, t[H.ACTUAL_STARTUP_TIME] = t[H.ACTUAL_STARTUP_TIME] * t[H.ACTUAL_LOOPS] / e, t[H.EXCLUSIVE_DURATION] = t[H.ACTUAL_TOTAL_TIME];
                        var n = t[H.EXCLUSIVE_DURATION] - this.childrenDuration(t, 0);
                        t[H.EXCLUSIVE_DURATION] = n > 0 ? n : 0
                    }
                    t[H.TOTAL_COST] && (t[H.EXCLUSIVE_COST] = t[H.TOTAL_COST]), c["each"](t[H.PLANS], (function (e) {
                        "InitPlan" !== e[H.PARENT_RELATIONSHIP] && e[H.TOTAL_COST] && (t[H.EXCLUSIVE_COST] = t[H.EXCLUSIVE_COST] - e[H.TOTAL_COST])
                    })), t[H.EXCLUSIVE_COST] < 0 && (t[H.EXCLUSIVE_COST] = 0), c["each"](["ACTUAL_ROWS", "PLAN_ROWS", "ROWS_REMOVED_BY_FILTER", "ROWS_REMOVED_BY_JOIN_FILTER"], (function (e) {
                        if (!c["isUndefined"](t[H[e]])) {
                            var n = e + "_REVISED", a = t[H.ACTUAL_LOOPS] || 1;
                            t[H[n]] = t[H[e]] * a
                        }
                    }))
                }
            }, {
                key: "childrenDuration", value: function (t, e) {
                    var n = this;
                    return c["each"](t[H.PLANS], (function (t) {
                        "InitPlan" !== t[H.PARENT_RELATIONSHIP] && (e += t[H.EXCLUSIVE_DURATION] || 0, e = n.childrenDuration(t, e))
                    })), e
                }
            }, {
                key: "calculatePlannerEstimate", value: function (t) {
                    void 0 !== t[H.ACTUAL_ROWS] && (t[H.PLANNER_ESTIMATE_FACTOR] = t[H.ACTUAL_ROWS] / t[H.PLAN_ROWS], t[H.PLANNER_ESTIMATE_DIRECTION] = M.none, t[H.ACTUAL_ROWS] > t[H.PLAN_ROWS] && (t[H.PLANNER_ESTIMATE_DIRECTION] = M.under), t[H.ACTUAL_ROWS] < t[H.PLAN_ROWS] && (t[H.PLANNER_ESTIMATE_DIRECTION] = M.over, t[H.PLANNER_ESTIMATE_FACTOR] = t[H.PLAN_ROWS] / t[H.ACTUAL_ROWS]))
                }
            }, {
                key: "cleanupSource", value: function (t) {
                    return t = t.replace(/^(\||║|│)(.*)\1\r?\n/gm, "$2\n"), t = t.replace(/^\+-+\+\r?\n/gm, ""), t = t.replace(/^(-|─|═)\1+\r?\n/gm, ""), t = t.replace(/^(├|╟|╠|╞)(─|═)\2*(┤|╢|╣|╡)\r?\n/gm, ""), t = t.replace(/^\+-+\+\r?\n/gm, ""), t = t.replace(/^└(─)+┘\r?\n/gm, ""), t = t.replace(/^╚(═)+╝\r?\n/gm, ""), t = t.replace(/^┌(─)+┐\r?\n/gm, ""), t = t.replace(/^╔(═)+╗\r?\n/gm, ""), t = t.replace(/^(["'])(.*)\1\r?\n/gm, "$2\n"), t = t.replace(/\s*\+\r?\n/g, "\n"), t = t.replace(/↵\r?/gm, "\n"), t = t.replace(/^\s*QUERY PLAN\s*\r?\n/m, ""), t = t.replace(/^\(\d+\s+[a-z]*s?\)(\r?\n|$)/gm, "\n"), t
                }
            }, {
                key: "fromSource", value: function (t) {
                    t = this.cleanupSource(t);
                    var e = !1;
                    try {
                        e = JSON.parse(t)
                    } catch (n) {
                    }
                    return e ? this.parseJson(t) : /^([\t-\r \xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF]*)(\[|\{)[\t-\r \xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF]*\n[\s\S]*?\1(\]|\})[\t-\r \xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF]*/gm.exec(t) ? this.fromJson(t) : this.fromText(t)
                }
            }, {
                key: "fromJson", value: function (t) {
                    var e = t.split(/[\r\n]+/), n = "", a = 0;
                    c["each"](e, (function (t, e) {
                        var o = /^(\s*)(\[|\{)\s*$/.exec(t);
                        if (o) return n = o[1], a = e, !1
                    }));
                    var o = 0;
                    c["each"](e, (function (t, e) {
                        var a = new RegExp("^" + n + "(]|})s*$").exec(t);
                        if (a) return o = e, !1
                    }));
                    var s = e.slice(a, o + 1).join("\n");
                    return this.parseJson(s)
                }
            }, {
                key: "parseJson", value: function (t) {
                    var e = dn.a.parser(), n = [], a = null, o = null;
                    return e.onvalue = function (t) {
                        var e = n[n.length - 1];
                        if (c["isArray"](e)) e.push(t); else {
                            var a = Object.keys(e), o = a[a.length - 1];
                            e[o] = t
                        }
                    }, e.onopenobject = function (t) {
                        var e = {};
                        e[t] = null, n.push(e)
                    }, e.onkey = function (t) {
                        var e = n[n.length - 1], a = Object.keys(e);
                        -1 !== a.indexOf(t) ? o = [n.length - 1, e[t]] : e[t] = null
                    }, e.onopenarray = function () {
                        n.push([])
                    }, e.oncloseobject = e.onclosearray = function () {
                        var t = n.pop();
                        if (n.length) {
                            var e = n[n.length - 1];
                            if (o && o[0] === n.length - 1) c["merge"](o[1], t), o = null; else if (c["isArray"](e)) e.push(t); else {
                                var s = Object.keys(e), r = s[s.length - 1];
                                e[r] = t
                            }
                        } else a = t
                    }, e.write(t).close(), a instanceof Array && (a = a[0]), a
                }
            }, {
                key: "splitIntoLines", value: function (t) {
                    var e = [], n = t.split(/\r?\n/), a = function (t, e) {
                        return (t.match(e) || []).length
                    };
                    return c["each"](n, (function (t) {
                        a(t, /\)/g) > a(t, /\(/g) ? e[e.length - 1] += t : t.match(/^(?:Total\s+runtime|Planning\s+time|Execution\s+time|Time|Filter|Output|JIT)/i) ? e.push(t) : (t.match(/^\S/) || t.match(/^\s*\(/)) && 0 < e.length ? e[e.length - 1] += t : e.push(t)
                    })), e
                }
            }, {
                key: "fromText", value: function (t) {
                    var e = this, n = this.splitIntoLines(t), a = {Plan: null}, o = [];
                    if (c["each"](n, (function (t) {
                        t = t.replace(/"\s*$/, ""), t = t.replace(/^\s*"/, ""), t = t.replace(/\t/gm, "    ");
                        var n = /^\s*/, s = t.match(n)[0].length;
                        t = t.replace(n, "");
                        var r = "^s*$", i = "^\\s*(QUERY|---|#).*$", l = "^(\\s*->\\s*|\\s*)",
                            u = "([^\\r\\n\\t\\f\\v\\:\\(]*?)",
                            p = "\\(cost=(\\d+\\.\\d+)\\.\\.(\\d+\\.\\d+)\\s+rows=(\\d+)\\s+width=(\\d+)\\)", d = "(?:",
                            f = ")", _ = "\\(", h = "\\)",
                            v = "(?:actual\\stime=(\\d+\\.\\d+)\\.\\.(\\d+\\.\\d+)\\srows=(\\d+)\\sloops=(\\d+)|actual\\srows=(\\d+)\\sloops=(\\d+)|(never\\s+executed))",
                            b = "?", m = new RegExp(r).exec(t), E = new RegExp(i).exec(t),
                            g = new RegExp(l + u + "\\s*" + d + (d + p) + "\\s+" + _ + v + h + f + "|" + d + p + f + "|" + d + _ + v + h + f + f + "\\s*$", "gm"),
                            S = g.exec(t), T = /^(\s*)((?:Sub|Init)Plan)\s*(?:\d+\s*)?\s*(?:\(returns.*\)\s*)?$/gm,
                            C = T.exec(t), O = /^(\s*)CTE\s+(\S+)\s*$/g, y = O.exec(t),
                            w = /^(\s*)Trigger\s+(.*):\s+time=(\d+\.\d+)\s+calls=(\d+)\s*$/g, x = w.exec(t),
                            L = new RegExp(/^(\s*)Worker\s+(\d+):\s+/.source + d + v + f + b + "(.*)\\s*$", "g"),
                            A = L.exec(t), R = /^(\s*)JIT:\s*$/g, I = R.exec(t), P = /^(\s*)(\S.*\S)\s*$/g,
                            k = P.exec(t);
                        if (!m && !E) if (!S || y || C) {
                            if (C) {
                                C[1];
                                var N = C[2];
                                c["remove"](o, (function (t) {
                                    return t[0] >= s
                                }));
                                var D = c["last"](o)[1],
                                    M = {node: D.node, subelementType: N.toLowerCase(), name: C[0]};
                                o.push([s, M])
                            } else if (y) {
                                y[1];
                                var U = y[2];
                                c["remove"](o, (function (t) {
                                    return t[0] >= s
                                }));
                                var B = c["last"](o)[1],
                                    W = {node: B.node, subelementType: "initplan", name: "CTE " + U};
                                o.push([s, W])
                            } else if (A) {
                                A[1];
                                var V = parseInt(A[2], 0), j = c["last"](o)[1];
                                j.node[H.WORKERS] || (j.node[H.WORKERS] = []);
                                var K = e.getWorker(j.node, V);
                                if (K || (K = new un(V), j.node[H.WORKERS].push(K)), A[3] && A[4] && (K[H.ACTUAL_STARTUP_TIME] = parseFloat(A[3]), K[H.ACTUAL_TOTAL_TIME] = parseFloat(A[4]), K[H.ACTUAL_ROWS] = parseInt(A[5], 0), K[H.ACTUAL_LOOPS] = parseInt(A[6], 0)), e.parseSort(A[10], K)) return;
                                var X = A[10].split(/: (.+)/).filter((function (t) {
                                    return t
                                }));
                                if (A[10]) {
                                    if (!X[1]) return;
                                    var F = c["startCase"](X[0]);
                                    K[F] = X[1]
                                }
                            } else if (x) {
                                x[1];
                                c["remove"](o, (function (t) {
                                    return t[0] >= s
                                })), a.Triggers = a.Triggers || [], a.Triggers.push({
                                    "Trigger Name": x[2],
                                    Time: e.parseTime(x[3]),
                                    Calls: x[4]
                                })
                            } else if (I) {
                                var $;
                                if (0 === o.length) a.JIT = {}, $ = {node: a.JIT}, o.push([1, $]); else {
                                    var Y = c["last"](o)[1];
                                    if (c["last"](Y.node[H.WORKERS])) {
                                        var G = c["last"](Y.node[H.WORKERS]);
                                        G.JIT = {}, $ = {node: G.JIT}, o.push([s, $])
                                    }
                                }
                            } else if (k) {
                                var q;
                                k[1];
                                if (c["remove"](o, (function (t) {
                                    return t[0] >= s
                                })), q = 0 === o.length ? a : c["last"](o)[1].node, !q.Plan && q["Query Text"]) return void (q["Query Text"] += "\n" + t);
                                var J = k[2].split(/: (.+)/).filter((function (t) {
                                    return t
                                }));
                                if (!J[1]) return;
                                if (e.parseSort(k[2], q)) return;
                                if (e.parseBuffers(k[2], q)) return;
                                if (e.parseWAL(k[2], q)) return;
                                if (e.parseIOTimings(k[2], q)) return;
                                if (e.parseOptions(k[2], q)) return;
                                if (e.parseTiming(k[2], q)) return;
                                if (e.parseSettings(k[2], q)) return;
                                if (e.parseSortGroups(k[2], q)) return;
                                if (e.parseSortKey(k[2], q)) return;
                                var z = J[1].replace(/(\s*ms)$/, "");
                                parseFloat(z) && (z = parseFloat(z));
                                var Q = J[0];
                                -1 === Q.indexOf(" runtime") && -1 === Q.indexOf(" time") || (Q = c["startCase"](Q)), q[Q] = z
                            }
                        } else {
                            S[1];
                            var Z = S[13], tt = new ln(S[2]);
                            (S[3] && S[4] || S[14] && S[15]) && (tt[H.STARTUP_COST] = parseFloat(S[3] || S[14]), tt[H.TOTAL_COST] = parseFloat(S[4] || S[15]), tt[H.PLAN_ROWS] = parseInt(S[5] || S[16], 0), tt[H.PLAN_WIDTH] = parseInt(S[6] || S[17], 0)), (S[7] && S[8] || S[18] && S[19]) && (tt[H.ACTUAL_STARTUP_TIME] = parseFloat(S[7] || S[18]), tt[H.ACTUAL_TOTAL_TIME] = parseFloat(S[8] || S[19])), (S[9] && S[10] || S[11] && S[12] || S[20] && S[21]) && (tt[H.ACTUAL_ROWS] = parseInt(S[9] || S[11] || S[20], 0), tt[H.ACTUAL_LOOPS] = parseInt(S[10] || S[12] || S[21], 0)), Z && (tt[H.ACTUAL_LOOPS] = 0, tt[H.ACTUAL_ROWS] = 0, tt[H.ACTUAL_TOTAL_TIME] = 0);
                            var et = {node: tt, subelementType: "subnode"};
                            if (0 === o.length) return o.push([s, et]), void (a.Plan = tt);
                            c["remove"](o, (function (t) {
                                return t[0] >= s
                            }));
                            var nt = c["last"](o)[1];
                            o.push([s, et]), nt.node[H.PLANS] || (nt.node[H.PLANS] = []), "initplan" === nt.subelementType ? (tt[H.PARENT_RELATIONSHIP] = "InitPlan", tt[H.SUBPLAN_NAME] = nt.name) : "subplan" === nt.subelementType && (tt[H.PARENT_RELATIONSHIP] = "SubPlan", tt[H.SUBPLAN_NAME] = nt.name), nt.node.Plans.push(tt)
                        }
                    })), !a.Plan) throw new Error("Unable to parse plan");
                    return a
                }
            }, {
                key: "parseSortKey", value: function (t, e) {
                    var n = /^\s*((?:Sort|Presorted) Key):\s+(.*)/g, a = n.exec(t);
                    return !!a && (e[a[1]] = c["map"](C(a[2], ","), c["trim"]), !0)
                }
            }, {
                key: "parseSort", value: function (t, e) {
                    var n = /^(\s*)Sort Method:\s+(.*)\s+(Memory|Disk):\s+(?:(\S*)kB)\s*$/g, a = n.exec(t);
                    return !!a && (e[H.SORT_METHOD] = a[2].trim(), e[H.SORT_SPACE_USED] = a[4], e[H.SORT_SPACE_TYPE] = a[3], !0)
                }
            }, {
                key: "parseBuffers", value: function (t, e) {
                    var n = this, a = /Buffers:\s+(.*)\s*$/g, o = a.exec(t);
                    return !!o && (c["each"](o[1].split(/,\s+/), (function (t) {
                        var a = /(shared|temp|local)\s+(.*)$/g, o = a.exec(t);
                        if (o) {
                            var s = o[1];
                            c["each"](["hit", "read", "written", "dirtied"], (function (t) {
                                e[c["map"]([s, t, "blocks"], c["capitalize"]).join(" ")] = 0
                            })), c["each"](o[2].split(/\s+/), (function (t) {
                                n.parseBuffer(t, s, e)
                            }))
                        }
                    })), !0)
                }
            }, {
                key: "parseBuffer", value: function (t, e, n) {
                    var a = t.split(/=/), o = a[0], s = parseInt(a[1], 0);
                    n[c["map"]([e, o, "blocks"], c["capitalize"]).join(" ")] = s
                }
            }, {
                key: "getWorker", value: function (t, e) {
                    return c["find"](t[H.WORKERS], (function (t) {
                        return t[Y.WORKER_NUMBER] === e
                    }))
                }
            }, {
                key: "parseWAL", value: function (t, e) {
                    var n = /WAL:\s+(.*)\s*$/g, a = n.exec(t);
                    return !!a && (c["each"](["Records", "Bytes", "FPI"], (function (t) {
                        e["WAL " + t] = 0
                    })), c["each"](a[1].split(/\s+/), (function (t) {
                        var n, a = t.split(/=/), o = a[0], s = parseInt(a[1], 0);
                        switch (o) {
                            case"fpi":
                                n = "FPI";
                                break;
                            default:
                                n = c["capitalize"](o)
                        }
                        e["WAL " + n] = s
                    })), !0)
                }
            }, {
                key: "parseIOTimings", value: function (t, e) {
                    var n = /I\/O Timings:\s+(.*)\s*$/g, a = n.exec(t);
                    return !!a && (e[H.IO_READ_TIME] = 0, e[H.IO_WRITE_TIME] = 0, c["each"](a[1].split(/\s+/), (function (t) {
                        var n = t.split(/=/), a = n[0], o = parseFloat(n[1]), s = "IO_" + c["upperCase"](a) + "_TIME";
                        e[H[s]] = o
                    })), !0)
                }
            }, {
                key: "parseOptions", value: function (t, e) {
                    var n = /^(\s*)Options:\s+(.*)$/g, a = n.exec(t);
                    if (a) {
                        e.Options = {};
                        var o, s = a[2].split(/\s*,\s*/);
                        return c["each"](s, (function (t) {
                            var n = /^(\S*)\s+(.*)$/g;
                            o = n.exec(t), e.Options[o[1]] = JSON.parse(o[2])
                        })), !0
                    }
                    return !1
                }
            }, {
                key: "parseTiming", value: function (t, e) {
                    var n = this, a = /^(\s*)Timing:\s+(.*)$/g, o = a.exec(t);
                    if (o) {
                        e.Timing = {};
                        var s, r = o[2].split(/\s*,\s*/);
                        return c["each"](r, (function (t) {
                            var a = /^(\S*)\s+(.*)$/g;
                            s = a.exec(t), e.Timing[s[1]] = n.parseTime(s[2])
                        })), !0
                    }
                    return !1
                }
            }, {
                key: "parseTime", value: function (t) {
                    return parseFloat(t.replace(/(\s*ms)$/, ""))
                }
            }, {
                key: "parseSettings", value: function (t, e) {
                    var n = /^(\s*)Settings:\s*(.*)$/g, a = n.exec(t);
                    if (a) {
                        e.Settings = {};
                        var o, s = C(a[2], ",");
                        return c["each"](s, (function (t) {
                            var n = /^(\S*)\s+=\s+(.*)$/g;
                            o = n.exec(c["trim"](t)), e.Settings[o[1]] = o[2].replace(/'/g, "")
                        })), !0
                    }
                    return !1
                }
            }, {
                key: "parseSortGroups", value: function (t, e) {
                    var n = /^\s*(Full-sort|Pre-sorted) Groups:\s+([0-9]*)\s+Sort Method[s]*:\s+(.*)\s+Average Memory:\s+(\S*)kB\s+Peak Memory:\s+(\S*)kB.*$/g,
                        a = n.exec(t);
                    if (a) {
                        var o, s,
                            r = (s = {}, fn(s, F.GROUP_COUNT, parseInt(a[2], 0)), fn(s, F.SORT_METHODS_USED, c["map"](a[3].split(","), c["trim"])), fn(s, F.SORT_SPACE_MEMORY, (o = {}, fn(o, $.AVERAGE_SORT_SPACE_USED, parseInt(a[4], 0)), fn(o, $.PEAK_SORT_SPACE_USED, parseInt(a[5], 0)), o)), s);
                        if ("Full-sort" === a[1]) e[H.FULL_SORT_GROUPS] = r; else {
                            if ("Pre-sorted" !== a[1]) throw new Error("Unsupported sort groups method");
                            e[H.PRE_SORTED_GROUPS] = r
                        }
                        return !0
                    }
                    return !1
                }
            }, {
                key: "calculateExclusives", value: function (t) {
                    var e = ["SHARED_HIT_BLOCKS", "SHARED_READ_BLOCKS", "SHARED_DIRTIED_BLOCKS", "SHARED_WRITTEN_BLOCKS", "TEMP_READ_BLOCKS", "TEMP_WRITTEN_BLOCKS", "LOCAL_HIT_BLOCKS", "LOCAL_READ_BLOCKS", "LOCAL_DIRTIED_BLOCKS", "LOCAL_WRITTEN_BLOCKS", "IO_READ_TIME", "IO_WRITE_TIME"];
                    c["each"](e, (function (e) {
                        var n = c["sumBy"](t[H.PLANS], (function (t) {
                            return t[H[e]] || 0
                        })), a = "EXCLUSIVE_" + e;
                        t[H[a]] = t[H[e]] - n
                    }))
                }
            }, {
                key: "findOutputProperty", value: function (t) {
                    var e = this, n = t.Plans;
                    return !!n && c["some"](n, (function (t) {
                        return c["has"](t, H.OUTPUT) || e.findOutputProperty(t)
                    }))
                }
            }]), t
        }();

        function mn(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function En(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function gn(t, e, n) {
            return e && En(t.prototype, e), n && En(t, n), t
        }

        var Sn = function () {
            function t(e) {
                var n = this;
                mn(this, t), this.element = e, this.listener = !0, this.start = !1, this.startMousePositionX = 0, this.startMousePositionY = 0, this.startScrollPositionX = 0, this.startScrollPositionY = 0, this.element.addEventListener("mousedown", (function (t) {
                    t.target.closest(".plan-node-body") || (t.preventDefault(), n.clearSelection(), n.startMousePositionX = t.screenX, n.startMousePositionY = t.screenY, n.startScrollPositionX = n.element.scrollLeft, n.startScrollPositionY = n.element.scrollTop, n.start = !0)
                })), document.documentElement.addEventListener("mouseup", (function (t) {
                    t.preventDefault(), n.startMousePositionX = 0, n.startMousePositionY = 0, n.startScrollPositionX = 0, n.startScrollPositionY = 0, n.start = !1
                })), this.element.addEventListener("mousemove", (function (t) {
                    n.listener && n.start && (t.preventDefault(), n.element.scrollTo(n.startScrollPositionX + (n.startMousePositionX - t.screenX), n.startScrollPositionY + (n.startMousePositionY - t.screenY)))
                }))
            }

            return gn(t, [{
                key: "clearSelection", value: function () {
                    if (window.getSelection) {
                        var t = window.getSelection();
                        t && t.removeAllRanges()
                    }
                }
            }]), t
        }(), Tn = n("6018");

        function Cn(t) {
            return Cn = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, Cn(t)
        }

        function On(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function yn(t, e) {
            for (var n = 0; n < e.length; n++) {
                var a = e[n];
                a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
            }
        }

        function wn(t, e, n) {
            return e && yn(t.prototype, e), n && yn(t, n), t
        }

        function xn(t, e) {
            return !e || "object" !== Cn(e) && "function" !== typeof e ? Ln(t) : e
        }

        function Ln(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function An(t) {
            return An = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, An(t)
        }

        function Rn(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && In(t, e)
        }

        function In(t, e) {
            return In = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, In(t, e)
        }

        r["c"].use(Tn["b"]), r["c"].component("tippy", Tn["a"]);
        var Pn = function (t) {
            function e() {
                var t;
                return On(this, e), t = xn(this, An(e).apply(this, arguments)), t.flat = [], t.menuHidden = !0, t.validationMessage = "", t.showTriggers = !1, t.showSettings = !1, t.activeTab = "", t.rawCopied = !1, t.helpService = new v, t.lodash = c, t.eventBus = new r["c"], t.viewOptions = {
                    menuHidden: !0,
                    showHighlightBar: !1,
                    showPlanStats: !0,
                    highlightType: U.NONE,
                    viewMode: B.FULL,
                    orientation: K.TWOD,
                    showDiagram: !0,
                    diagramWidth: 20
                }, t.highlightTypes = U, t.viewModes = B, t.orientations = K, t.planService = new bn, t.nodeProps = H, t.selectedNode = null, t
            }

            return Rn(e, t), wn(e, [{
                key: "selectNode", value: function (t) {
                    this.selectedNode = t, this.centerNode(t, W.visible, V.highlight)
                }
            }, {
                key: "mounted", value: function () {
                    this.handleScroll(), this.eventBus.$on("mouseovernode", this.onMouseOverNode), this.eventBus.$on("mouseoutnode", this.onMouseOutNode), this.eventBus.$on("clickcte", this.centerCTE)
                }
            }, {
                key: "handleScroll", value: function () {
                    var t = this.$refs.plan.$el;
                    new Sn(t)
                }
            }, {
                key: "created", value: function () {
                    var t, e = this, n = localStorage.getItem("viewOptions");
                    n && c["assignIn"](this.viewOptions, JSON.parse(n));
                    try {
                        t = this.planService.fromSource(this.planSource), this.validationMessage = "", this.setActiveTab("plan")
                    } catch (o) {
                        return this.validationMessage = "Couldn't parse plan", void (this.plan = null)
                    }
                    this.rootNode = t.Plan, this.queryText = t["Query Text"] || this.planQuery, this.plan = this.planService.createPlan("", t, this.queryText);
                    var a = this.plan.content;
                    this.plan.planStats = {
                        executionTime: a["Execution Time"] || a["Total Runtime"] || null,
                        planningTime: a["Planning Time"] || null,
                        maxRows: a.maxRows || null,
                        maxCost: a.maxCost || null,
                        maxDuration: a.maxDuration || null,
                        maxBlocks: a.maxBlocks || null,
                        triggers: a.Triggers || [],
                        jitTime: a.JIT && a.JIT.Timing && a.JIT.Timing.Total || null,
                        settings: a.Settings
                    }, r["c"].nextTick((function () {
                        var t = 1, n = V.flash;
                        e.zoomTo && (t = e.zoomTo, n = V.highlight | V.showdetails), e.centerNode(t, W.visible, n), e.plan && e.onHashChange()
                    })), window.addEventListener("hashchange", this.onHashChange)
                }
            }, {
                key: "beforeDestroy", value: function () {
                    window.removeEventListener("hashchange", this.onHashChange)
                }
            }, {
                key: "onHashChange", value: function () {
                    var t = this, e = /#([a-zA-Z]*)(\/node\/([0-9]*))*/, n = e.exec(window.location.hash);
                    if (n) {
                        var a = n[1] || "plan";
                        this.setActiveTab(a);
                        var o = n[3];
                        void 0 !== o && setTimeout((function () {
                            t.selectNode(parseInt(o, 0))
                        }), 1)
                    }
                }
            }, {
                key: "onViewOptionsChanged", value: function (t, e) {
                    localStorage.setItem("viewOptions", JSON.stringify(this.viewOptions))
                }
            }, {
                key: "showHideMenu", value: function () {
                    this.viewOptions.menuHidden = !this.viewOptions.menuHidden
                }
            }, {
                key: "getHelpMessage", value: function (t) {
                    return this.helpService.getHelpMessage(t)
                }
            }, {
                key: "centerNode", value: function (t, e, n) {
                    var a = this.findPlanNode((function (e) {
                        return e.node.nodeId === t
                    }));
                    a && (this.highlightEl(a.$el.querySelector(".plan-node"), e, n), n & V.showdetails && a.setShowDetails(!0))
                }
            }, {
                key: "highlightEl", value: function (t, e, n) {
                    if (t) {
                        var a = this.$refs.plan.$el;
                        e !== W.none && E(a, t, e === W.center, (function () {
                            n & V.flash && (t.classList.add("flash"), setTimeout((function () {
                                t.classList.remove("flash")
                            }), 1e3)), n & V.highlight && t.classList.add("highlight")
                        }))
                    }
                }
            }, {
                key: "highlightNode", value: function (t, e) {
                    var n = this, a = this.$el.querySelector(".plan-node.highlight");
                    a && a.classList.remove("highlight"), window.clearTimeout(this.highlightTimeout), this.highlightTimeout = window.setTimeout(function () {
                        var a = n.findPlanNode((function (e) {
                            return e.node.nodeId === t
                        }));
                        if (a) {
                            var o = a.$el.querySelector(".plan-node");
                            o.classList.toggle("highlight", e)
                        }
                    }.bind(this), 50)
                }
            }, {
                key: "centerCTE", value: function (t) {
                    var e = this.findPlanNode((function (e) {
                        return e.node[H.SUBPLAN_NAME] === t
                    }));
                    e && this.highlightEl(e.$el, W.visible, V.flash)
                }
            }, {
                key: "triggerDurationPercent", value: function (t) {
                    this.plan, this.plan && this.plan.planStats;
                    var e = this.plan && this.plan.planStats.executionTime || 0, n = t.Time;
                    return c["round"](n / e * 100)
                }
            }, {
                key: "toggleDiagram", value: function () {
                    this.viewOptions.showDiagram = !this.viewOptions.showDiagram
                }
            }, {
                key: "planningTimeClass", value: function (t) {
                    var e;
                    return t > 90 ? e = 4 : t > 40 ? e = 3 : t > 10 && (e = 2), !!e && "c-" + e
                }
            }, {
                key: "onMouseOverNode", value: function (t) {
                    this.highlightNode(t, !0)
                }
            }, {
                key: "onMouseOutNode", value: function (t) {
                    this.highlightNode(t, !1)
                }
            }, {
                key: "setActiveTab", value: function (t) {
                    this.activeTab = t
                }
            }, {
                key: "findPlanNode", value: function (t) {
                    var e = null;
                    return this.$refs.plan.$children.some((function n(a) {
                        if (a instanceof Xt) return t(a) ? (e = a, !0) : a.$children.some(n)
                    })), e
                }
            }, {
                key: "onSelectedNodeChange", value: function (t, e) {
                    var n = this.findPlanNode((function (e) {
                        return e.node.nodeId === t
                    }));
                    n && (n.selected = !0), this.$refs.diagram.selected = t, n = this.findPlanNode((function (t) {
                        return t.node.nodeId === e
                    })), n && (n.selected = !1)
                }
            }, {
                key: "totalTriggerDurationPercent", get: function () {
                    this.plan, this.plan && this.plan.planStats;
                    var t = this.plan && this.plan.planStats.executionTime || 0, e = this.triggersTotalDuration || 0;
                    return c["round"](e / t * 100)
                }
            }, {
                key: "triggersTotalDuration", get: function () {
                    if (this.plan) return c["sumBy"](this.plan.planStats.triggers, (function (t) {
                        return t.Time
                    }))
                }
            }]), e
        }(r["c"]);
        Object(s["a"])([Object(r["b"])(String)], Pn.prototype, "planSource", void 0), Object(s["a"])([Object(r["b"])(String)], Pn.prototype, "planQuery", void 0), Object(s["a"])([Object(r["b"])(Number)], Pn.prototype, "zoomTo", void 0), Object(s["a"])([Object(r["d"])("viewOptions", {deep: !0})], Pn.prototype, "onViewOptionsChanged", null), Object(s["a"])([Object(r["d"])("selectedNode")], Pn.prototype, "onSelectedNodeChange", null), Pn = Object(s["a"])([Object(r["a"])({
            name: "plan",
            components: {Copy: le, Diagram: ye, Pane: u["Pane"], PlanNode: Xt, Splitpanes: u["Splitpanes"], Stats: sn},
            directives: {},
            filters: {cost: ct, duration: lt, durationClass: Ot, json: wt, pgsql: yt, rows: ut}
        })], Pn);
        var kn = Pn, Nn = kn, Dn = (n("44bc"), Object(nt["a"])(Nn, i, l, !1, null, null, null)), Mn = Dn.exports,
            Un = n("4f32"), Bn = n("c605");

        function Wn(t) {
            return Wn = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, Wn(t)
        }

        function Vn(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function Hn(t, e) {
            return !e || "object" !== Wn(e) && "function" !== typeof e ? jn(t) : e
        }

        function jn(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function Kn(t) {
            return Kn = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, Kn(t)
        }

        function Xn(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && Fn(t, e)
        }

        function Fn(t, e) {
            return Fn = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, Fn(t, e)
        }

        var $n = function (t) {
            function e() {
                var t;
                return Vn(this, e), t = Hn(this, Kn(e).apply(this, arguments)), t.planSource = Bn["planData"][0], t.planQuery = Bn["planData"][1], t
            }

            return Xn(e, t), e
        }(r["c"]);
        $n = Object(s["a"])([Object(r["a"])({components: {MainLayout: Un["a"], Plan: Mn}})], $n);
        var Yn = $n, Gn = Yn, qn = Object(nt["a"])(Gn, a, o, !1, null, null, null);
        e["a"] = qn.exports
    }, c605: function (t, e, n) {
        "use strict";
        n.r(e), function (t) {
            n.d(e, "planData", (function () {
                return l
            })), n.d(e, "setPlanData", (function () {
                return c
            }));
            var a = n("2b0e"), o = (n("4989"), n("ab8b"), n("15f5"), n("30b8")), s = n("77d1"), r = n("d3fc"),
                i = {"/": o["a"], "/plan": s["a"], "/about": r["a"]}, l = ["", ""];

            function c(t, e) {
                l[0] = t, l[1] = e, u.currentRoute = "/plan"
            }

            a["a"].config.productionTip = !1, t.setPlanData = c;
            var u = new a["a"]({
                data: {currentRoute: "/"}, computed: {
                    ViewComponent: function () {
                        return i[this.currentRoute]
                    }
                }, render: function (t) {
                    return t(this.ViewComponent)
                }
            }).$mount("#app")
        }.call(this, n("c8ba"))
    }, d3fc: function (t, e, n) {
        "use strict";
        var a = function () {
            var t = this, e = t.$createElement, n = t._self._c || e;
            return n("main-layout", [n("div", {staticClass: "container"}, [n("h2", [t._v("\n    Disclaimer\n  ")]), t._v(" "), n("p", [t._v("\n    This project is a rewrite of the excellent "), n("a", {attrs: {href: "https://github.com/AlexTatiyants/pev"}}, [t._v("Postgres Explain Visualizer (pev)")]), t._v(". Kudos go to Alex Tatiyants.\n  ")]), t._v(" "), n("p", [t._v("\n  The pev project was initialy written in early 2016 but seem to be abandonned since then. There was no activity at all for more than "), n("a", {attrs: {href: "https://github.com/AlexTatiyants/pev/issues/42"}}, [t._v("3 years and counting")]), t._v(" though there are "), n("a", {attrs: {href: "https://github.com/AlexTatiyants/pev/issues"}}, [t._v("several issues open")]), t._v(" and relevant pull requests pending.\n  ")]), t._v(" "), n("p", [t._v("\n  The current project has several goals:\n  "), n("ul", [n("li", [t._v("\n      isolate the plan view component and its dependencies in order to use it in\n      any web app "), n("i", {staticClass: "fa fa-check text-success"})]), t._v(" "), n("li", [t._v("\n      make it work with recent version of JS frameworks "), n("i", {staticClass: "fa fa-check text-success"})]), t._v(" "), n("li", [t._v("\n      upgrade Bootstrap to a more recent version "), n("i", {staticClass: "fa fa-check text-success"})]), t._v(" "), n("li", [t._v("\n      use VueJS just for a matter of taste "), n("i", {staticClass: "fa fa-check text-success"})]), t._v(" "), n("li", [t._v("\n      add ability to parse text format "), n("i", {staticClass: "fa fa-check text-success"})]), t._v(" "), n("li", [t._v("\n      add support for new features (parallelism, triggers, disk usage, …)\n    ")]), t._v(" "), n("li", [t._v("\n      maintain the project to match upgrades in PostgreSQL.\n    ")])])]), t._v(" "), n("h2", [t._v("\n    Usage tips\n  ")]), t._v(" "), n("p", [t._v("\n  To get the most out of it, we recommend generating a query plan using the following line: "), n("code", [t._v("EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)")]), t._v(". It is recommend submitting a (decently formatted) SQL query that generated the plan.\n  ")]), t._v(" "), n("p", [t._v("\n    PEV2 can also parse text although the JSON format usually has better support.\n  ")]), t._v(" "), n("h2", [t._v("\n    Help improve PEV2\n  ")]), t._v(" "), n("p", [t._v("\n  You can help us.\n  ")]), t._v(" "), n("p", [t._v("\n  Report issues or contribute to the code on "), n("a", {attrs: {href: "https://github.com/dalibo/pev2"}}, [t._v("Github")]), t._v(".\n  ")]), t._v(" "), n("hr"), t._v(" "), n("div", {staticClass: "text-center text-muted"}, [n("b", [t._v("pev2")]), t._v(" is brought to you by "), n("a", {attrs: {href: "https://dalibo.com"}}, [t._v("Dalibo")])])])])
        }, o = [], s = n("9ab4"), r = n("60a3"), i = n("4f32");

        function l(t) {
            return l = "function" === typeof Symbol && "symbol" === typeof Symbol.iterator ? function (t) {
                return typeof t
            } : function (t) {
                return t && "function" === typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
            }, l(t)
        }

        function c(t, e) {
            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
        }

        function u(t, e) {
            return !e || "object" !== l(e) && "function" !== typeof e ? p(t) : e
        }

        function p(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }

        function d(t) {
            return d = Object.setPrototypeOf ? Object.getPrototypeOf : function (t) {
                return t.__proto__ || Object.getPrototypeOf(t)
            }, d(t)
        }

        function f(t, e) {
            if ("function" !== typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && _(t, e)
        }

        function _(t, e) {
            return _ = Object.setPrototypeOf || function (t, e) {
                return t.__proto__ = e, t
            }, _(t, e)
        }

        var h = function (t) {
            function e() {
                return c(this, e), u(this, d(e).apply(this, arguments))
            }

            return f(e, t), e
        }(r["c"]);
        h = Object(s["a"])([Object(r["a"])({components: {MainLayout: i["a"]}})], h);
        var v = h, b = v, m = n("2877"), E = Object(m["a"])(b, a, o, !1, null, null, null);
        e["a"] = E.exports
    }
});