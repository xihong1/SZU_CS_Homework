#include <algorithm>
#include <cctype>
#include <deque>
#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace
{

    struct Production
    {
        std::vector<std::string> lhs;
        std::vector<std::vector<std::string>> rhsAlternatives;
        int lineNo = 0;
    };

    struct ErrorItem
    {
        std::string type;
        std::string symbol;
        std::string location;
    };

    struct Grammar
    {
        std::set<std::string> nonterminals;
        std::set<std::string> terminals;
        std::vector<Production> productions;
        std::string start;
    };

    struct ParseResult
    {
        bool formatOk = true;
        Grammar grammar;
        std::vector<ErrorItem> errors;
    };

    std::string trim(const std::string &s)
    {
        size_t l = 0;
        size_t r = s.size();
        while (l < r && std::isspace(static_cast<unsigned char>(s[l])))
        {
            ++l;
        }
        while (r > l && std::isspace(static_cast<unsigned char>(s[r - 1])))
        {
            --r;
        }
        return s.substr(l, r - l);
    }

    bool startsWith(const std::string &s, const std::string &prefix)
    {
        return s.rfind(prefix, 0) == 0;
    }

    std::vector<std::string> splitBySpace(const std::string &s)
    {
        std::vector<std::string> out;
        std::istringstream iss(s);
        std::string tok;
        while (iss >> tok)
        {
            out.push_back(tok);
        }
        return out;
    }

    std::vector<std::string> splitByChar(const std::string &s, char ch)
    {
        std::vector<std::string> out;
        std::string cur;
        for (char c : s)
        {
            if (c == ch)
            {
                out.push_back(cur);
                cur.clear();
            }
            else
            {
                cur.push_back(c);
            }
        }
        out.push_back(cur);
        return out;
    }

    bool isEpsilonToken(const std::string &s)
    {
        return s == "epsilon" || s == "EPSILON" || s == "$\\varepsilon$";
    }

    bool appendUniqueError(std::vector<ErrorItem> &errors, const ErrorItem &e)
    {
        for (const auto &ex : errors)
        {
            if (ex.type == e.type && ex.symbol == e.symbol && ex.location == e.location)
            {
                return false;
            }
        }
        errors.push_back(e);
        return true;
    }

    std::vector<std::string> parseSymbolSeq(
        const std::string &raw,
        const std::set<std::string> &nonterminals,
        const std::set<std::string> &terminals,
        bool *ok)
    {
        std::string t = trim(raw);
        if (t.empty())
        {
            *ok = false;
            return {};
        }

        auto spaced = splitBySpace(t);
        if (spaced.size() > 1)
        {
            if (spaced.size() == 1 && isEpsilonToken(spaced[0]))
            {
                *ok = true;
                return {};
            }
            if (spaced.size() == 1 && trim(spaced[0]).empty())
            {
                *ok = false;
                return {};
            }
            if (spaced.size() == 1 && isEpsilonToken(spaced[0]))
            {
                *ok = true;
                return {};
            }
            bool allEmpty = true;
            for (const auto &x : spaced)
            {
                if (!trim(x).empty())
                {
                    allEmpty = false;
                    break;
                }
            }
            if (allEmpty)
            {
                *ok = false;
                return {};
            }
            std::vector<std::string> tokens;
            for (const auto &x : spaced)
            {
                if (trim(x).empty())
                {
                    continue;
                }
                if (isEpsilonToken(x))
                {
                    if (spaced.size() == 1)
                    {
                        *ok = true;
                        return {};
                    }
                    *ok = false;
                    return {};
                }
                tokens.push_back(x);
            }
            *ok = !tokens.empty();
            return tokens;
        }

        if (spaced.size() == 1 && isEpsilonToken(spaced[0]))
        {
            *ok = true;
            return {};
        }

        std::vector<std::string> symbols;
        size_t i = 0;
        while (i < t.size())
        {
            if (std::isspace(static_cast<unsigned char>(t[i])))
            {
                ++i;
                continue;
            }
            std::string best;
            for (const auto &nt : nonterminals)
            {
                if (nt.empty())
                {
                    continue;
                }
                if (i + nt.size() <= t.size() && t.compare(i, nt.size(), nt) == 0)
                {
                    if (nt.size() > best.size())
                    {
                        best = nt;
                    }
                }
            }
            for (const auto &tt : terminals)
            {
                if (tt.empty())
                {
                    continue;
                }
                if (i + tt.size() <= t.size() && t.compare(i, tt.size(), tt) == 0)
                {
                    if (tt.size() > best.size())
                    {
                        best = tt;
                    }
                }
            }
            if (best.empty())
            {
                symbols.push_back(std::string(1, t[i]));
                ++i;
            }
            else
            {
                symbols.push_back(best);
                i += best.size();
            }
        }

        *ok = !symbols.empty();
        return symbols;
    }

    ParseResult parseGrammarFile(const std::string &path)
    {
        ParseResult result;
        std::ifstream in(path);
        if (!in)
        {
            result.formatOk = false;
            appendUniqueError(result.errors, {"FORMAT_ERROR", "", "cannot open file"});
            return result;
        }

        bool seenN = false;
        bool seenT = false;
        bool seenP = false;
        bool seenSTART = false;

        bool inProductionBlock = false;
        std::string line;
        int lineNo = 0;

        while (std::getline(in, line))
        {
            ++lineNo;
            std::string t = trim(line);
            if (t.empty() || startsWith(t, "#"))
            {
                continue;
            }

            if (startsWith(t, "N:"))
            {
                seenN = true;
                inProductionBlock = false;
                auto symbols = splitBySpace(trim(t.substr(2)));
                if (symbols.empty())
                {
                    result.formatOk = false;
                    appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                }
                for (const auto &s : symbols)
                {
                    if (!s.empty())
                    {
                        result.grammar.nonterminals.insert(s);
                    }
                }
                continue;
            }

            if (startsWith(t, "T:"))
            {
                seenT = true;
                inProductionBlock = false;
                auto symbols = splitBySpace(trim(t.substr(2)));
                for (const auto &s : symbols)
                {
                    if (!s.empty())
                    {
                        result.grammar.terminals.insert(s);
                    }
                }
                continue;
            }

            if (startsWith(t, "P:"))
            {
                seenP = true;
                inProductionBlock = true;
                continue;
            }

            if (startsWith(t, "START:"))
            {
                seenSTART = true;
                inProductionBlock = false;
                result.grammar.start = trim(t.substr(6));
                if (result.grammar.start.empty())
                {
                    result.formatOk = false;
                    appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                }
                continue;
            }

            if (!inProductionBlock)
            {
                result.formatOk = false;
                appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                continue;
            }

            auto pos = t.find("->");
            if (pos == std::string::npos)
            {
                result.formatOk = false;
                appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                continue;
            }

            std::string lhsRaw = trim(t.substr(0, pos));
            std::string rhsRaw = trim(t.substr(pos + 2));
            if (lhsRaw.empty() || rhsRaw.empty())
            {
                result.formatOk = false;
                appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                continue;
            }

            bool lhsOk = true;
            auto lhsSymbols = parseSymbolSeq(lhsRaw, result.grammar.nonterminals, result.grammar.terminals, &lhsOk);
            if (!lhsOk || lhsSymbols.empty())
            {
                result.formatOk = false;
                appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                continue;
            }

            Production p;
            p.lhs = std::move(lhsSymbols);
            p.lineNo = lineNo;

            auto alts = splitByChar(rhsRaw, '|');
            bool rhsHasAtLeastOne = false;
            for (const auto &altRaw : alts)
            {
                bool rhsOk = true;
                auto rhsSymbols = parseSymbolSeq(altRaw, result.grammar.nonterminals, result.grammar.terminals, &rhsOk);
                if (!rhsOk && !isEpsilonToken(trim(altRaw)))
                {
                    result.formatOk = false;
                    appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                    continue;
                }
                if (isEpsilonToken(trim(altRaw)))
                {
                    rhsSymbols.clear();
                }
                p.rhsAlternatives.push_back(std::move(rhsSymbols));
                rhsHasAtLeastOne = true;
            }

            if (!rhsHasAtLeastOne)
            {
                result.formatOk = false;
                appendUniqueError(result.errors, {"FORMAT_ERROR", "", "line " + std::to_string(lineNo)});
                continue;
            }

            result.grammar.productions.push_back(std::move(p));
        }

        if (!seenN || !seenT || !seenP || !seenSTART)
        {
            result.formatOk = false;
            appendUniqueError(result.errors, {"FORMAT_ERROR", "", "missing required sections"});
        }

        if (result.grammar.nonterminals.empty())
        {
            result.formatOk = false;
            appendUniqueError(result.errors, {"FORMAT_ERROR", "", "N is empty"});
        }

        if (result.grammar.productions.empty())
        {
            result.formatOk = false;
            appendUniqueError(result.errors, {"FORMAT_ERROR", "", "P is empty"});
        }

        return result;
    }

    std::vector<ErrorItem> validateGrammar(const ParseResult &parsed)
    {
        std::vector<ErrorItem> errors = parsed.errors;
        const Grammar &g = parsed.grammar;

        if (g.nonterminals.find(g.start) == g.nonterminals.end())
        {
            appendUniqueError(errors, {"START_NOT_IN_N", g.start, ""});
        }

        int prodIndex = 0;
        for (const auto &p : g.productions)
        {
            ++prodIndex;
            for (const auto &sym : p.lhs)
            {
                if (g.nonterminals.find(sym) == g.nonterminals.end() && g.terminals.find(sym) == g.terminals.end())
                {
                    appendUniqueError(errors, {"UNDEFINED_SYMBOL", sym, "production " + std::to_string(prodIndex)});
                }
            }
            for (const auto &rhs : p.rhsAlternatives)
            {
                for (const auto &sym : rhs)
                {
                    if (g.nonterminals.find(sym) == g.nonterminals.end() && g.terminals.find(sym) == g.terminals.end())
                    {
                        appendUniqueError(errors, {"UNDEFINED_SYMBOL", sym, "production " + std::to_string(prodIndex)});
                    }
                }
            }
        }

        if (g.nonterminals.find(g.start) != g.nonterminals.end())
        {
            std::set<std::string> reachable;
            std::queue<std::string> q;
            reachable.insert(g.start);
            q.push(g.start);

            while (!q.empty())
            {
                auto cur = q.front();
                q.pop();
                for (const auto &p : g.productions)
                {
                    if (p.lhs.size() == 1 && p.lhs[0] == cur)
                    {
                        for (const auto &rhs : p.rhsAlternatives)
                        {
                            for (const auto &sym : rhs)
                            {
                                if (g.nonterminals.find(sym) != g.nonterminals.end() && reachable.find(sym) == reachable.end())
                                {
                                    reachable.insert(sym);
                                    q.push(sym);
                                }
                            }
                        }
                    }
                }
            }

            for (const auto &nt : g.nonterminals)
            {
                if (reachable.find(nt) == reachable.end())
                {
                    appendUniqueError(errors, {"UNREACHABLE", nt, ""});
                }
            }
        }

        std::set<std::string> generating;
        bool changed = true;
        while (changed)
        {
            changed = false;
            for (const auto &p : g.productions)
            {
                if (p.lhs.size() != 1 || g.nonterminals.find(p.lhs[0]) == g.nonterminals.end())
                {
                    continue;
                }
                const auto &A = p.lhs[0];
                for (const auto &rhs : p.rhsAlternatives)
                {
                    bool good = true;
                    for (const auto &sym : rhs)
                    {
                        if (g.nonterminals.find(sym) != g.nonterminals.end())
                        {
                            if (generating.find(sym) == generating.end())
                            {
                                good = false;
                                break;
                            }
                        }
                        else if (g.terminals.find(sym) == g.terminals.end())
                        {
                            good = false;
                            break;
                        }
                    }
                    if (good)
                    {
                        if (generating.insert(A).second)
                        {
                            changed = true;
                        }
                    }
                }
            }
        }

        for (const auto &nt : g.nonterminals)
        {
            if (generating.find(nt) == generating.end())
            {
                appendUniqueError(errors, {"NON_GENERATING", nt, ""});
            }
        }

        return errors;
    }

    bool isValidGrammar(const std::vector<ErrorItem> &errors)
    {
        return errors.empty();
    }

    bool allLhsSingleNonterminal(const Grammar &g)
    {
        for (const auto &p : g.productions)
        {
            if (p.lhs.size() != 1)
            {
                return false;
            }
            if (g.nonterminals.find(p.lhs[0]) == g.nonterminals.end())
            {
                return false;
            }
        }
        return true;
    }

    bool isOnlyTerminals(const Grammar &g, const std::vector<std::string> &rhs)
    {
        for (const auto &s : rhs)
        {
            if (g.terminals.find(s) == g.terminals.end())
            {
                return false;
            }
        }
        return true;
    }

    bool isRightLinearRule(const Grammar &g, const std::vector<std::string> &rhs)
    {
        if (rhs.empty())
        {
            return true;
        }
        int nonterminalPos = -1;
        for (int i = 0; i < static_cast<int>(rhs.size()); ++i)
        {
            if (g.nonterminals.find(rhs[i]) != g.nonterminals.end())
            {
                if (nonterminalPos != -1)
                {
                    return false;
                }
                nonterminalPos = i;
            }
            else if (g.terminals.find(rhs[i]) == g.terminals.end())
            {
                return false;
            }
        }
        if (nonterminalPos == -1)
        {
            return isOnlyTerminals(g, rhs);
        }
        if (nonterminalPos != static_cast<int>(rhs.size()) - 1)
        {
            return false;
        }
        if (rhs.size() == 1)
        {
            return false;
        }
        for (int i = 0; i < nonterminalPos; ++i)
        {
            if (g.terminals.find(rhs[i]) == g.terminals.end())
            {
                return false;
            }
        }
        return true;
    }

    bool isLeftLinearRule(const Grammar &g, const std::vector<std::string> &rhs)
    {
        if (rhs.empty())
        {
            return true;
        }
        int nonterminalPos = -1;
        for (int i = 0; i < static_cast<int>(rhs.size()); ++i)
        {
            if (g.nonterminals.find(rhs[i]) != g.nonterminals.end())
            {
                if (nonterminalPos != -1)
                {
                    return false;
                }
                nonterminalPos = i;
            }
            else if (g.terminals.find(rhs[i]) == g.terminals.end())
            {
                return false;
            }
        }
        if (nonterminalPos == -1)
        {
            return isOnlyTerminals(g, rhs);
        }
        if (nonterminalPos != 0)
        {
            return false;
        }
        if (rhs.size() == 1)
        {
            return false;
        }
        for (size_t i = 1; i < rhs.size(); ++i)
        {
            if (g.terminals.find(rhs[i]) == g.terminals.end())
            {
                return false;
            }
        }
        return true;
    }

    int symbolLength(const std::vector<std::string> &symbols)
    {
        return static_cast<int>(symbols.size());
    }

    std::string classifyType(const Grammar &g)
    {
        bool type2 = allLhsSingleNonterminal(g);

        if (type2)
        {
            bool rightLinear = true;
            bool leftLinear = true;
            for (const auto &p : g.productions)
            {
                for (const auto &rhs : p.rhsAlternatives)
                {
                    rightLinear = rightLinear && isRightLinearRule(g, rhs);
                    leftLinear = leftLinear && isLeftLinearRule(g, rhs);
                }
            }
            if (rightLinear && !leftLinear)
            {
                return "TYPE_3_RIGHT";
            }
            if (!rightLinear && leftLinear)
            {
                return "TYPE_3_LEFT";
            }
            if (rightLinear && leftLinear)
            {
                return "TYPE_3_RIGHT";
            }
            return "TYPE_2";
        }

        bool startAppearsInRhs = false;
        for (const auto &p : g.productions)
        {
            for (const auto &rhs : p.rhsAlternatives)
            {
                for (const auto &sym : rhs)
                {
                    if (sym == g.start)
                    {
                        startAppearsInRhs = true;
                    }
                }
            }
        }

        bool type1 = true;
        for (const auto &p : g.productions)
        {
            for (const auto &rhs : p.rhsAlternatives)
            {
                int l = symbolLength(p.lhs);
                int r = symbolLength(rhs);
                if (l <= r)
                {
                    continue;
                }
                bool isS2Eps = (p.lhs.size() == 1 && p.lhs[0] == g.start && rhs.empty() && !startAppearsInRhs);
                if (!isS2Eps)
                {
                    type1 = false;
                }
            }
        }
        if (type1)
        {
            return "TYPE_1";
        }

        return "TYPE_0";
    }

    std::string jsonEscape(const std::string &s)
    {
        std::string out;
        for (char c : s)
        {
            switch (c)
            {
            case '\\':
                out += "\\\\";
                break;
            case '"':
                out += "\\\"";
                break;
            case '\n':
                out += "\\n";
                break;
            case '\r':
                out += "\\r";
                break;
            case '\t':
                out += "\\t";
                break;
            default:
                out.push_back(c);
                break;
            }
        }
        return out;
    }

    void printValidateJson(const std::vector<ErrorItem> &errors)
    {
        if (errors.empty())
        {
            std::cout << "{\"valid\": true}";
            return;
        }

        std::cout << "{\"valid\": false, \"errors\": [\n";
        for (size_t i = 0; i < errors.size(); ++i)
        {
            std::cout << "  {\"type\": \"" << jsonEscape(errors[i].type) << "\"";
            if (!errors[i].symbol.empty())
            {
                std::cout << ", \"symbol\": \"" << jsonEscape(errors[i].symbol) << "\"";
            }
            if (!errors[i].location.empty())
            {
                std::cout << ", \"location\": \"" << jsonEscape(errors[i].location) << "\"";
            }
            std::cout << "}";
            if (i + 1 < errors.size())
            {
                std::cout << ",";
            }
            std::cout << "\n";
        }
        std::cout << "]}";
    }

    void printStatsJson(const Grammar &g)
    {
        int numProductions = 0;
        bool hasEpsilon = false;
        for (const auto &p : g.productions)
        {
            numProductions += static_cast<int>(p.rhsAlternatives.size());
            for (const auto &rhs : p.rhsAlternatives)
            {
                if (rhs.empty())
                {
                    hasEpsilon = true;
                }
            }
        }

        std::cout << "{\n";
        std::cout << "  \"num_nonterminals\": " << g.nonterminals.size() << ",\n";
        std::cout << "  \"num_terminals\": " << g.terminals.size() << ",\n";
        std::cout << "  \"num_productions\": " << numProductions << ", \n";
        std::cout << "  \"has_epsilon\": " << (hasEpsilon ? "true" : "false") << ",\n";
        std::cout << "  \"start_symbol\": \"" << jsonEscape(g.start) << "\"\n";
        std::cout << "}";
    }

    std::string joinWithSpace(const std::vector<std::string> &tokens)
    {
        if (tokens.empty())
        {
            return "";
        }
        std::ostringstream oss;
        for (size_t i = 0; i < tokens.size(); ++i)
        {
            if (i)
            {
                oss << ' ';
            }
            oss << tokens[i];
        }
        return oss.str();
    }

    std::unordered_map<std::string, int> minTerminalLength(const Grammar &g)
    {
        const int INF = 1e9;
        std::unordered_map<std::string, int> minLen;
        for (const auto &nt : g.nonterminals)
        {
            minLen[nt] = INF;
        }

        bool changed = true;
        while (changed)
        {
            changed = false;
            for (const auto &p : g.productions)
            {
                if (p.lhs.size() != 1 || g.nonterminals.find(p.lhs[0]) == g.nonterminals.end())
                {
                    continue;
                }
                const std::string &A = p.lhs[0];
                for (const auto &rhs : p.rhsAlternatives)
                {
                    int cur = 0;
                    bool ok = true;
                    for (const auto &sym : rhs)
                    {
                        if (g.terminals.find(sym) != g.terminals.end())
                        {
                            cur += 1;
                        }
                        else if (g.nonterminals.find(sym) != g.nonterminals.end())
                        {
                            if (minLen[sym] >= INF)
                            {
                                ok = false;
                                break;
                            }
                            cur += minLen[sym];
                        }
                        else
                        {
                            ok = false;
                            break;
                        }
                    }
                    if (ok && cur < minLen[A])
                    {
                        minLen[A] = cur;
                        changed = true;
                    }
                }
            }
        }

        return minLen;
    }

    int lowerBoundTerminals(
        const std::vector<std::string> &form,
        const Grammar &g,
        const std::unordered_map<std::string, int> &minLen)
    {
        const int INF = 1e9;
        int lb = 0;
        for (const auto &sym : form)
        {
            if (g.terminals.find(sym) != g.terminals.end())
            {
                lb += 1;
            }
            else if (g.nonterminals.find(sym) != g.nonterminals.end())
            {
                auto it = minLen.find(sym);
                if (it == minLen.end() || it->second >= INF)
                {
                    return INF;
                }
                lb += it->second;
            }
            else
            {
                return INF;
            }
        }
        return lb;
    }

    int countTerminalsInForm(const std::vector<std::string> &form, const Grammar &g)
    {
        int count = 0;
        for (const auto &sym : form)
        {
            if (g.terminals.find(sym) != g.terminals.end())
            {
                ++count;
            }
        }
        return count;
    }

    int leftmostNonterminalPos(const std::vector<std::string> &form, const Grammar &g)
    {
        for (int i = 0; i < static_cast<int>(form.size()); ++i)
        {
            if (g.nonterminals.find(form[i]) != g.nonterminals.end())
            {
                return i;
            }
        }
        return -1;
    }

    std::string encodeForm(const std::vector<std::string> &form)
    {
        std::ostringstream oss;
        for (size_t i = 0; i < form.size(); ++i)
        {
            if (i)
            {
                oss << '\x1f';
            }
            oss << form[i];
        }
        return oss.str();
    }

    struct AmbiguityResult
    {
        bool ambiguous = false;
        std::vector<std::string> witness;
        int parseCount = 0;
    };

    AmbiguityResult ambiguityCheck(const Grammar &g, int maxLen)
    {
        AmbiguityResult out;

        if (!allLhsSingleNonterminal(g))
        {
            return out;
        }

        auto minLen = minTerminalLength(g);
        const int INF = 1e9;
        if (!minLen.count(g.start) || minLen[g.start] >= INF)
        {
            return out;
        }

        std::unordered_map<std::string, std::vector<std::vector<std::string>>> byLhs;
        for (const auto &p : g.productions)
        {
            if (p.lhs.size() == 1 && g.nonterminals.find(p.lhs[0]) != g.nonterminals.end())
            {
                for (const auto &rhs : p.rhsAlternatives)
                {
                    byLhs[p.lhs[0]].push_back(rhs);
                }
            }
        }

        struct Node
        {
            std::vector<std::string> form;
            int steps;
        };

        int depthLimit = std::max(12, maxLen * 4 + 10);

        std::deque<Node> q;
        q.push_back({{g.start}, 0});

        std::unordered_map<std::string, int> statePushCount;
        statePushCount[encodeForm({g.start}) + "#0"] = 1;

        std::unordered_map<std::string, int> terminalStringCount;

        while (!q.empty())
        {
            Node cur = q.front();
            q.pop_front();
            int curTerminals = countTerminalsInForm(cur.form, g);
            if (curTerminals > maxLen)
                continue;
            int lb = lowerBoundTerminals(cur.form, g, minLen);
            if (lb == INF || lb > maxLen)
                continue;

            int pos = leftmostNonterminalPos(cur.form, g);
            if (pos == -1)
            {
                std::string key = joinWithSpace(cur.form);
                int &cnt = terminalStringCount[key];
                cnt += 1;
                if (cnt >= 2)
                {
                    out.ambiguous = true;
                    out.witness = cur.form;
                    out.parseCount = cnt;
                    return out;
                }
                continue;
            }
            if (cur.steps >= depthLimit)
                continue;
            const std::string &A = cur.form[pos];
            auto it = byLhs.find(A);
            if (it == byLhs.end())
                continue;
            for (const auto &rhs : it->second)
            {
                std::vector<std::string> next;
                next.reserve(cur.form.size() - 1 + rhs.size());
                for (int i = 0; i < pos; ++i)
                {
                    next.push_back(cur.form[i]);
                }
                for (const auto &x : rhs)
                {
                    next.push_back(x);
                }
                for (size_t i = pos + 1; i < cur.form.size(); ++i)
                {
                    next.push_back(cur.form[i]);
                }

                int nextTerminals = countTerminalsInForm(next, g);
                if (nextTerminals > maxLen)
                {
                    continue;
                }
                int nextLb = lowerBoundTerminals(next, g, minLen);
                if (nextLb == INF || nextLb > maxLen)
                {
                    continue;
                }

                std::string key = encodeForm(next) + "#" + std::to_string(cur.steps + 1);
                int &pushes = statePushCount[key];
                if (pushes >= 2)
                {
                    continue;
                }
                pushes += 1;

                q.push_back({std::move(next), cur.steps + 1});
            }
        }

        return out;
    }

} // namespace

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cerr << "Usage: ./grammar_analyzer <input_file> [--check-type|--validate|--stats|--ambiguity-check --max-length N]\n";
        return 1;
    }

    std::string inputPath = argv[1];
    std::string mode = argv[2];

    int maxLength = 8;
    if (mode == "--ambiguity-check")
    {
        for (int i = 3; i < argc; ++i)
        {
            std::string arg = argv[i];
            if (arg == "--max-length" && i + 1 < argc)
            {
                maxLength = std::stoi(argv[i + 1]);
                ++i;
            }
        }
        if (maxLength < 0)
        {
            maxLength = 0;
        }
    }

    ParseResult parsed = parseGrammarFile(inputPath);
    std::vector<ErrorItem> validationErrors = validateGrammar(parsed);

    if (mode == "--validate")
    {
        printValidateJson(validationErrors);
        return 0;
    }

    if (mode == "--check-type")
    {
        if (!isValidGrammar(validationErrors))
        {
            std::cout << "INVALID";
            return 0;
        }
        std::cout << classifyType(parsed.grammar);
        return 0;
    }

    if (mode == "--stats")
    {
        printStatsJson(parsed.grammar);
        return 0;
    }

    if (mode == "--ambiguity-check")
    {
        if (!isValidGrammar(validationErrors))
        {
            std::cout << "{\"ambiguous\": false, \"max_length_checked\": " << maxLength << "}";
            return 0;
        }
        AmbiguityResult r = ambiguityCheck(parsed.grammar, maxLength);
        if (r.ambiguous)
        {
            std::cout << "{\"ambiguous\": true, \"witness\": \"" << jsonEscape(joinWithSpace(r.witness))
                      << "\", \"parse_count\": " << r.parseCount << "}";
        }
        else
        {
            std::cout << "{\"ambiguous\": false, \"max_length_checked\": " << maxLength << "}";
        }
        return 0;
    }

    std::cerr << "Unknown option: " << mode << "\n";
    return 1;
}
