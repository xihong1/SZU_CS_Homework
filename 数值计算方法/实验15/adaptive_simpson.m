function [I, n_evals, intervals] = adaptive_simpson(f, a, b, tol)
% 自适应Simpson求积法
% 输入: f - 被积函数句柄
%        a, b - 积分区间
%        tol - 绝对误差限
% 输出: I - 积分近似值
%        n_evals - 函数求值次数
%        intervals - 最终子区间信息 [a_i, b_i, S_i, err_i]

    n_evals = 0;
    intervals = [];

    % 递归调用自适应积分
    [I, n_evals, intervals] = adaptive_simpson_recursive(f, a, b, tol, n_evals, intervals);

    fprintf('自适应Simpson求积法:\n');
    fprintf('  总函数求值次数: %d\n', n_evals);
    fprintf('  最终子区间数: %d\n', size(intervals, 1));
    fprintf('  积分近似值: %.10f\n', I);
end

function [I, n_evals, intervals] = adaptive_simpson_recursive(f, a, b, tol, n_evals, intervals)
    % 计算三点处的函数值
    fa = f(a);
    fb = f(b);
    c = (a + b) / 2;
    fc = f(c);
    n_evals = n_evals + 3;

    h = b - a;

    % Simpson 1/3 公式
    S1 = h / 6 * (fa + 4*fc + fb);

    % 将区间二等分，计算复合Simpson值
    c1 = (a + c) / 2;
    c2 = (c + b) / 2;
    fc1 = f(c1);
    fc2 = f(c2);
    n_evals = n_evals + 2;

    S2 = h / 12 * (fa + 4*fc1 + 2*fc + 4*fc2 + fb);

    % 误差估计 (Richardson外推)
    err = abs(S2 - S1) / 15;

    if err < tol * (h / (b - a)) || (b - a) < 1e-12
        I = S2 + (S2 - S1) / 15;  % 误差修正
        intervals = [intervals; a, b, I, err];
    else
        % 递归细分
        [I_left, n_evals, intervals] = adaptive_simpson_recursive(f, a, c, tol/2, n_evals, intervals);
        [I_right, n_evals, intervals] = adaptive_simpson_recursive(f, c, b, tol/2, n_evals, intervals);
        I = I_left + I_right;
    end
end
