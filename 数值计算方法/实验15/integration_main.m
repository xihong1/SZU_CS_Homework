% ============================================================
% 数值积分方法比较实验
% 计算积分 ∫_0^(π/2) cos(x) dx
% 精确值 = 1
% 方法: 变步长梯形求积、自适应Simpson求积、Romberg求积
% 绝对误差要求: 0.5 × 10^(-6)
% ============================================================
clear; clc; close all;

% 定义被积函数和积分区间
f = @(x) cos(x);
a = 0;
b = pi/2;
exact_value = 1.0;  % ∫_0^(π/2) cos(x)dx = sin(π/2) - sin(0) = 1
tol = 0.5e-6;

fprintf('============================================\n');
fprintf('数值积分实验: ∫_0^(π/2) cos(x) dx\n');
fprintf('精确值: %.10f\n', exact_value);
fprintf('误差要求: %.2e\n\n', tol);

% 存储结果
results = cell(4, 6);
results(1,:) = {'方法', '计算结果', '绝对误差', '误差限达标', '迭代/细分次数', '函数求值次数'};

% ============================================================
% 方法1: 变步长梯形求积法
% ============================================================
fprintf('========== 方法1: 变步长梯形求积法 ==========\n');
tic;
[I_trap, n_trap, errors_trap] = var_step_trapezoidal(f, a, b, tol);
time_trap = toc;
err_trap = abs(I_trap - exact_value);
fprintf('计算结果: %.10f, 绝对误差: %.2e, 子区间数: %d, 时间: %.4fs\n\n', ...
        I_trap, err_trap, n_trap, time_trap);
results(2,:) = {'变步长梯形法', I_trap, err_trap, err_trap < tol, n_trap, n_trap+1};

% ============================================================
% 方法2: 自适应Simpson求积法
% ============================================================
fprintf('========== 方法2: 自适应Simpson求积法 ==========\n');
tic;
[I_simp, n_evals_simp, intervals_simp] = adaptive_simpson(f, a, b, tol);
time_simp = toc;
err_simp = abs(I_simp - exact_value);
n_simp = size(intervals_simp, 1);
fprintf('计算结果: %.10f, 绝对误差: %.2e, 子区间数: %d, 时间: %.4fs\n\n', ...
        I_simp, err_simp, n_simp, time_simp);
results(3,:) = {'自适应Simpson法', I_simp, err_simp, err_simp < tol, n_simp, n_evals_simp};

% ============================================================
% 方法3: Romberg求积法
% ============================================================
fprintf('========== 方法3: Romberg求积法 ==========\n');
tic;
[I_romb, T_table, n_evals_romb] = romberg(f, a, b, tol);
time_romb = toc;
err_romb = abs(I_romb - exact_value);
fprintf('计算结果: %.10f, 绝对误差: %.2e, 外推次数: %d, 时间: %.4fs\n\n', ...
        I_romb, err_romb, size(T_table,1)-1, time_romb);
results(4,:) = {'Romberg法', I_romb, err_romb, err_romb < tol, size(T_table,1)-1, n_evals_romb};

% ============================================================
% 结果汇总
% ============================================================
fprintf('========== 结果汇总 ==========\n');
fprintf('%-20s %-14s %-14s %-10s %-12s %-12s\n', results{1,:});
fprintf('%-20s %-14.10f %-14.2e %-10s %-12d %-12d\n', results{2,:});
fprintf('%-20s %-14.10f %-14.2e %-10s %-12d %-12d\n', results{3,:});
fprintf('%-20s %-14.10f %-14.2e %-10s %-12d %-12d\n', results{4,:});

% ============================================================
% 绘图: 收敛性分析
% ============================================================

% 图1: 变步长梯形法误差收敛曲线
figure('Position', [100, 100, 900, 600]);
semilogy(1:length(errors_trap), errors_trap, 'b-o', 'LineWidth', 1.5, 'MarkerSize', 6);
hold on;
yline(tol, 'r--', 'LineWidth', 1.5);
xlabel('迭代次数 k');
ylabel('误差估计 |T_{2n} - T_n|/3');
title('变步长梯形求积法 - 误差收敛曲线');
legend('误差估计', ['目标精度 = ' num2str(tol)], 'Location', 'northeast');
grid on;
saveas(gcf, 'trapezoidal_convergence.png');
fprintf('\n图1已保存: trapezoidal_convergence.png\n');

% 图2: Romberg外推表可视化
figure('Position', [100, 100, 900, 600]);
semilogy(0:size(T_table,1)-1, abs(diag(T_table) - exact_value), 'r-s', ...
         'LineWidth', 1.5, 'MarkerSize', 8, 'MarkerFaceColor', 'r');
hold on;
yline(tol, 'b--', 'LineWidth', 1.5);
xlabel('外推次数 k');
ylabel('|T_{k,k} - 精确值|');
title('Romberg求积法 - 对角元误差收敛曲线');
legend('|T_{k,k} - 1|', ['目标精度 = ' num2str(tol)], 'Location', 'northeast');
grid on;
saveas(gcf, 'romberg_convergence.png');
fprintf('图2已保存: romberg_convergence.png\n');

% 图3: 各方法精度对比柱状图
figure('Position', [100, 100, 700, 500]);
methods = {'变步长梯形', '自适应Simpson', 'Romberg'};
errors_all = [err_trap, err_simp, err_romb];
bar(errors_all);
set(gca, 'XTickLabel', methods);
ylabel('绝对误差');
title('三种求积方法精度对比');
hold on;
yline(tol, 'r--', 'LineWidth', 1.5);
text(0.5, tol*2, ['目标精度 = ' num2str(tol)], 'Color', 'red');
set(gca, 'YScale', 'log');
grid on;
for i = 1:3
    text(i, errors_all(i)*1.5, sprintf('%.2e', errors_all(i)), ...
         'HorizontalAlignment', 'center', 'FontSize', 10);
end
saveas(gcf, 'methods_comparison.png');
fprintf('图3已保存: methods_comparison.png\n');

% 图4: 自适应Simpson子区间分布
figure('Position', [100, 100, 900, 500]);
subplot(2,1,1);
x_plot = linspace(a, b, 1000);
plot(x_plot, f(x_plot), 'b-', 'LineWidth', 1.5);
hold on;
% 标记子区间边界
for i = 1:size(intervals_simp, 1)
    xline(intervals_simp(i,1), 'r--', 'Alpha', 0.3);
end
xline(b, 'r--', 'Alpha', 0.3);
xlabel('x'); ylabel('f(x) = cos(x)');
title('自适应Simpson求积法 - 子区间划分');
grid on;

subplot(2,1,2);
bar_widths = intervals_simp(:,2) - intervals_simp(:,1);
bar(1:length(bar_widths), bar_widths, 'FaceColor', [0.2 0.6 0.8]);
xlabel('子区间编号'); ylabel('子区间宽度');
title('各子区间宽度分布');
grid on;
saveas(gcf, 'adaptive_simpson_intervals.png');
fprintf('图4已保存: adaptive_simpson_intervals.png\n');

fprintf('\n========== 计算完成 ==========\n');
