function [I, n_intervals, errors] = var_step_trapezoidal(f, a, b, tol)
% 变步长梯形求积法
% 输入: f - 被积函数句柄
%        a, b - 积分区间
%        tol - 绝对误差限
% 输出: I - 积分近似值
%        n_intervals - 最终子区间数
%        errors - 每次迭代的误差估计

    max_iter = 30;          % 最大迭代次数
    n = 1;                  % 初始等分数
    h = b - a;              % 初始步长

    % 首次计算
    T1 = h / 2 * (f(a) + f(b));

    errors = [];
    fprintf('变步长梯形求积法迭代过程:\n');
    fprintf('  k      n         T_n             误差估计\n');
    fprintf('  %d      %d      %.10f        ---\n', 0, n, T1);

    for k = 1:max_iter
        % 计算新增分点的函数值之和
        h = (b - a) / n;
        x_new = a + h/2 : h : b - h/2;
        sum_new = sum(f(x_new));

        % 递推计算新的梯形值
        T2 = T1 / 2 + h/2 * sum_new;

        % 误差估计
        err = abs(T2 - T1) / 3;
        errors = [errors; err];

        fprintf('  %d      %d      %.10f       %.2e\n', k, 2*n, T2, err);

        % 检查收敛
        if err < tol
            I = T2;
            n_intervals = 2 * n;
            return;
        end

        % 更新
        T1 = T2;
        n = 2 * n;
    end

    I = T2;
    n_intervals = 2 * n;
    fprintf('警告: 达到最大迭代次数，可能未满足精度要求\n');
end
