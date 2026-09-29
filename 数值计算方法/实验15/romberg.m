function [I, T_table, n_evals] = romberg(f, a, b, tol)
% Romberg求积法
% 输入: f - 被积函数句柄
%        a, b - 积分区间
%        tol - 绝对误差限
% 输出: I - 积分近似值
%        T_table - Romberg外推表
%        n_evals - 函数求值次数

    max_k = 20;  % 最大外推次数
    T_table = zeros(max_k, max_k);
    n_evals = 0;

    % 第一步: 计算 T(1,1)
    T_table(1,1) = (b - a) / 2 * (f(a) + f(b));
    n_evals = n_evals + 2;

    fprintf('Romberg求积法迭代过程:\n');
    fprintf('  k      T_{k,1}          T_{k,2}          T_{k,3}          T_{k,4}          T_{k,5}\n');
    fprintf('  %d      %.10f\n', 0, T_table(1,1));

    for k = 2:max_k
        % 计算梯形序列 T(k,1) 使用递推公式
        n_sub = 2^(k-2);  % 新增分点数
        h = (b - a) / n_sub;
        x_new = a + h/2 : h : b - h/2;
        sum_new = sum(f(x_new));
        n_evals = n_evals + length(x_new);

        T_table(k,1) = T_table(k-1,1) / 2 + h/2 * sum_new;

        % Richardson外推
        for j = 2:k
            T_table(k,j) = (4^(j-1) * T_table(k,j-1) - T_table(k-1,j-1)) / (4^(j-1) - 1);
        end

        % 打印当前行
        fprintf('  %d      ', k-1);
        for j = 1:min(5, k)
            fprintf('%.10f    ', T_table(k,j));
        end
        fprintf('\n');

        % 检查收敛: |T(k,k) - T(k-1,k-1)| < tol
        if k > 2 && abs(T_table(k,k) - T_table(k-1,k-1)) < tol
            I = T_table(k,k);
            T_table = T_table(1:k, 1:k);
            fprintf('\nRomberg积分结果: %.10f\n', I);
            fprintf('外推次数: %d, 函数求值次数: %d\n', k-1, n_evals);
            return;
        end
    end

    I = T_table(max_k, max_k);
    T_table = T_table(1:max_k, 1:max_k);
    fprintf('警告: 达到最大外推次数\n');
end
