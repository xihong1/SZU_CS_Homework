% ============================================================
% Van der Pol振子数值求解实验
% 使用四阶Runge-Kutta方法求解Van der Pol振子模型
% d²x/dt² - μ(1-x²)dx/dt + x = 0
% 分别对 μ=0, μ=1, μ=-1 三种情形进行求解
% 并与MATLAB ode45结果进行验证比较
% ============================================================
clear; clc; close all;

% ---------- 参数设置 ----------
mu_values = [0, 1, -1];            % 三种参数情形
tspan_default = [0, 30];           % 默认时间区间
h = 0.05;                           % 固定步长
y0 = [2.0; 0.0];                   % 标准初值 [x(0); x'(0)]

fprintf('========== Van der Pol振子数值求解 ==========\n');
fprintf('方程: d²x/dt² - μ(1-x²)dx/dt + x = 0\n');
fprintf('步长 h = %.3f\n\n', h);

% 遍历三种参数情形
for idx = 1:length(mu_values)
    mu = mu_values(idx);

    % 根据参数设置时间区间
    if mu == -1
        tspan_current = [0, 8];
        y0_current = [1.0; 0.0];   % μ=-1时用小振幅初值
    else
        tspan_current = tspan_default;
        y0_current = y0;
    end

    fprintf('========== μ = %d ==========\n', mu);
    fprintf('时间区间: [%d, %d], 初值: x(0)=%.1f, x''(0)=%.1f\n', ...
            tspan_current(1), tspan_current(2), y0_current(1), y0_current(2));

    % --- 方法1: 显式Euler法 ---
    tic;
    [T_euler, Y_euler] = euler_method(@(t,y) vdp_ode(t,y,mu), ...
                                       tspan_current, y0_current, h);
    time_euler = toc;
    fprintf('Euler法:       步数=%d, 时间=%.4fs\n', length(T_euler)-1, time_euler);

    % --- 方法2: 改进Euler法 ---
    tic;
    [T_imeuler, Y_imeuler] = improved_euler_method(...
        @(t,y) vdp_ode(t,y,mu), tspan_current, y0_current, h);
    time_imeuler = toc;
    fprintf('改进Euler法:   步数=%d, 时间=%.4fs\n', length(T_imeuler)-1, time_imeuler);

    % --- 方法3: 四阶Runge-Kutta法 ---
    tic;
    [T_rk4, Y_rk4] = rk4_method(@(t,y) vdp_ode(t,y,mu), ...
                                 tspan_current, y0_current, h);
    time_rk4 = toc;
    fprintf('RK4法:         步数=%d, 时间=%.4fs\n', length(T_rk4)-1, time_rk4);

    % --- 方法4: MATLAB ode45 (参考解) ---
    options = odeset('RelTol', 1e-8, 'AbsTol', 1e-10);
    tic;
    [T_ode45, Y_ode45] = ode45(@(t,y) vdp_ode(t,y,mu), ...
                                tspan_current, y0_current, options);
    time_ode45 = toc;
    fprintf('ode45:         步数=%d, 时间=%.4fs\n', length(T_ode45)-1, time_ode45);

    % --- 误差分析 ---
    % 将各方法结果插值到ode45的时间点上进行比较
    Y_euler_interp = interp1(T_euler, Y_euler(:,1), T_ode45);
    Y_imeuler_interp = interp1(T_imeuler, Y_imeuler(:,1), T_ode45);
    Y_rk4_interp = interp1(T_rk4, Y_rk4(:,1), T_ode45);

    err_euler = max(abs(Y_euler_interp - Y_ode45(:,1)));
    err_imeuler = max(abs(Y_imeuler_interp - Y_ode45(:,1)));
    err_rk4 = max(abs(Y_rk4_interp - Y_ode45(:,1)));

    fprintf('\n最大绝对误差 (相对于ode45):\n');
    fprintf('  Euler法:      %.6e\n', err_euler);
    fprintf('  改进Euler法:  %.6e\n', err_imeuler);
    fprintf('  RK4法:        %.6e\n\n', err_rk4);

    % --- 详细数据点输出 (用于报告表格) ---
    if mu == 0
        % μ=0 时在特定时间点对比解析解
        t_check = [0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4, 2*pi];
        exact = 2 * cos(t_check);  % x(t) = 2cos(t)
        fprintf('μ=0 时特定时间点数值解与解析解对比:\n');
        fprintf('  t         解析解      Euler      改进Euler   RK4         ode45\n');
        for i = 1:length(t_check)
            t_c = t_check(i);
            if t_c <= tspan_current(2)
                idx_e = find(T_euler <= t_c, 1, 'last');
                idx_ie = find(T_imeuler <= t_c, 1, 'last');
                idx_rk = find(T_rk4 <= t_c, 1, 'last');
                idx_o = find(T_ode45 <= t_c, 1, 'last');
                fprintf('  %.4f    %.6f   %.6f   %.6f   %.6f   %.6f\n', ...
                    t_c, exact(i), Y_euler(idx_e,1), Y_imeuler(idx_ie,1), ...
                    Y_rk4(idx_rk,1), Y_ode45(idx_o,1));
            end
        end
    end

    % 保存指定时间点的数值用于报告表格
    if mu == 1
        t_check = [0, 2, 5, 10, 15, 20, 25, 30];
        fprintf('μ=1 时各方法在特定时间点的 x(t) 值:\n');
        fprintf('  t          Euler      改进Euler   RK4         ode45\n');
        for i = 1:length(t_check)
            t_c = t_check(i);
            if t_c <= tspan_current(2)
                idx_e = find(T_euler <= t_c, 1, 'last');
                idx_ie = find(T_imeuler <= t_c, 1, 'last');
                idx_rk = find(T_rk4 <= t_c, 1, 'last');
                idx_o = find(T_ode45 <= t_c, 1, 'last');
                fprintf('  %.1f       %.6f   %.6f   %.6f   %.6f\n', ...
                    t_c, Y_euler(idx_e,1), Y_imeuler(idx_ie,1), ...
                    Y_rk4(idx_rk,1), Y_ode45(idx_o,1));
            end
        end
    end

    if mu == -1
        t_check = [0, 1, 2, 3, 4, 5, 6, 7, 8];
        fprintf('μ=-1 时各方法在特定时间点的 x(t) 值:\n');
        fprintf('  t          Euler      改进Euler   RK4         ode45\n');
        for i = 1:length(t_check)
            t_c = t_check(i);
            if t_c <= tspan_current(2)
                idx_e = find(T_euler <= t_c, 1, 'last');
                idx_ie = find(T_imeuler <= t_c, 1, 'last');
                idx_rk = find(T_rk4 <= t_c, 1, 'last');
                idx_o = find(T_ode45 <= t_c, 1, 'last');
                fprintf('  %.1f       %.6f   %.6f   %.6f   %.6f\n', ...
                    t_c, Y_euler(idx_e,1), Y_imeuler(idx_ie,1), ...
                    Y_rk4(idx_rk,1), Y_ode45(idx_o,1));
            end
        end
    end

    fprintf('\n');

    % --- 绘图 ---
    figure('Position', [50, 50, 1400, 1000]);

    % 子图1: x(t) 时间序列 - 所有方法对比
    subplot(2,3,1);
    plot(T_euler, Y_euler(:,1), 'b-', 'LineWidth', 0.5); hold on;
    plot(T_imeuler, Y_imeuler(:,1), 'g--', 'LineWidth', 1);
    plot(T_rk4, Y_rk4(:,1), 'r-', 'LineWidth', 1.5);
    plot(T_ode45, Y_ode45(:,1), 'k:', 'LineWidth', 1.5);
    xlabel('t'); ylabel('x(t)');
    title(['x(t)时间序列 - \mu = ' num2str(mu) ' (各方法对比)']);
    legend('Euler', '改进Euler', 'RK4', 'ode45', 'Location', 'best');
    grid on;

    % 子图2: x(t) - RK4与ode45对比
    subplot(2,3,2);
    plot(T_rk4, Y_rk4(:,1), 'r-', 'LineWidth', 1.5); hold on;
    plot(T_ode45, Y_ode45(:,1), 'k:', 'LineWidth', 1.5);
    xlabel('t'); ylabel('x(t)');
    title(['x(t) - \mu = ' num2str(mu) ' (RK4 vs ode45)']);
    legend('RK4', 'ode45', 'Location', 'best');
    grid on;

    % 子图3: 相平面图 (x vs dx/dt)
    subplot(2,3,3);
    plot(Y_euler(:,1), Y_euler(:,2), 'b-', 'LineWidth', 0.3); hold on;
    plot(Y_rk4(:,1), Y_rk4(:,2), 'r-', 'LineWidth', 1.5);
    plot(Y_ode45(:,1), Y_ode45(:,2), 'k:', 'LineWidth', 1.5);
    xlabel('x'); ylabel('dx/dt');
    title(['相平面图 - \mu = ' num2str(mu)]);
    legend('Euler', 'RK4', 'ode45', 'Location', 'best');
    grid on;

    % 子图4: 速度 x'(t)
    subplot(2,3,4);
    plot(T_rk4, Y_rk4(:,2), 'r-', 'LineWidth', 1.5); hold on;
    plot(T_ode45, Y_ode45(:,2), 'k:', 'LineWidth', 1.5);
    xlabel('t'); ylabel('dx/dt');
    title(['速度 x''(t) - \mu = ' num2str(mu)]);
    legend('RK4', 'ode45', 'Location', 'best');
    grid on;

    % 子图5: 误差随时间变化曲线
    subplot(2,3,5);
    % 将ode45解插值到各方法的网格上
    ode45_on_euler = interp1(T_ode45, Y_ode45(:,1), T_euler);
    ode45_on_imeuler = interp1(T_ode45, Y_ode45(:,1), T_imeuler);
    ode45_on_rk4 = interp1(T_ode45, Y_ode45(:,1), T_rk4);

    semilogy(T_euler, abs(Y_euler(:,1) - ode45_on_euler), 'b-', 'LineWidth', 0.5); hold on;
    semilogy(T_imeuler, abs(Y_imeuler(:,1) - ode45_on_imeuler), 'g--', 'LineWidth', 1);
    semilogy(T_rk4, abs(Y_rk4(:,1) - ode45_on_rk4), 'r-', 'LineWidth', 1.5);
    xlabel('t'); ylabel('|Error|');
    title(['误差收敛曲线 - \mu = ' num2str(mu)]);
    legend('Euler', '改进Euler', 'RK4', 'Location', 'best');
    grid on;

    % 子图6: 性能对比柱状图
    subplot(2,3,6);
    methods = {'Euler', '改进Euler', 'RK4', 'ode45'};
    times = [time_euler, time_imeuler, time_rk4, time_ode45];
    steps = [length(T_euler)-1, length(T_imeuler)-1, length(T_rk4)-1, length(T_ode45)-1];

    yyaxis left;
    bar(1:4, times, 'FaceColor', [0.2 0.6 0.8]);
    ylabel('计算时间 (s)');

    yyaxis right;
    plot(1:4, steps, 'ro-', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'r');
    ylabel('步数');
    set(gca, 'XTickLabel', methods);
    title(['性能对比 - \mu = ' num2str(mu)]);
    grid on;

    sgtitle(['Van der Pol振子数值求解 (\mu=' num2str(mu) ...
             ', x(0)=' num2str(y0_current(1)) ', x''(0)=' num2str(y0_current(2)) ')']);

    saveas(gcf, ['vdp_mu_' num2str(mu) '.png']);
    fprintf('图片已保存: vdp_mu_%d.png\n\n', mu);
end

% ============================================================
% μ=0 时与解析解的详细对比
% ============================================================
fprintf('========== μ=0 简谐振子 - 与解析解对比 ==========\n');
mu = 0;
tspan_compare = [0, 4*pi];
y0_comp = [2.0; 0.0];
h_comp = 0.05;

[T_rk4_c, Y_rk4_c] = rk4_method(@(t,y) vdp_ode(t,y,mu), tspan_compare, y0_comp, h_comp);
exact_sol = 2 * cos(T_rk4_c);  % 解析解: x(t) = 2cos(t)

err_vs_exact = abs(Y_rk4_c(:,1) - exact_sol);
fprintf('RK4 vs 解析解 (x(t)=2cos(t)):\n');
fprintf('  最大误差: %.6e\n', max(err_vs_exact));
fprintf('  平均误差: %.6e\n', mean(err_vs_exact));

% 绘图: RK4与解析解对比
figure('Position', [100, 100, 1200, 500]);
subplot(1,2,1);
plot(T_rk4_c, Y_rk4_c(:,1), 'r-', 'LineWidth', 1.5); hold on;
plot(T_rk4_c, exact_sol, 'b--', 'LineWidth', 1.5);
xlabel('t'); ylabel('x(t)');
title('RK4数值解与解析解 x(t)=2cos(t) 对比');
legend('RK4 (h=0.05)', '解析解: 2cos(t)', 'Location', 'best');
grid on;

subplot(1,2,2);
semilogy(T_rk4_c, err_vs_exact, 'r-', 'LineWidth', 1.5);
xlabel('t'); ylabel('|RK4 - 解析解|');
title('RK4误差随时间变化');
grid on;

saveas(gcf, 'vdp_mu0_exact_comparison.png');
fprintf('图片已保存: vdp_mu0_exact_comparison.png\n');

% ============================================================
% 收敛性分析: 验证RK4方法的四阶收敛性
% ============================================================
fprintf('\n========== RK4收敛性验证 ==========\n');
mu_conv = 1;
tspan_conv = [0, 10];
y0_conv = [2.0; 0.0];
h_values = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125];
errors_conv = zeros(length(h_values), 1);

% 使用极高精度的ode45解作为参考
options_ref = odeset('RelTol', 1e-12, 'AbsTol', 1e-14);
[T_ref, Y_ref] = ode45(@(t,y) vdp_ode(t,y,mu_conv), tspan_conv, y0_conv, options_ref);

fprintf('  h         误差          收敛阶\n');
for i = 1:length(h_values)
    h_i = h_values(i);
    [T_i, Y_i] = rk4_method(@(t,y) vdp_ode(t,y,mu_conv), tspan_conv, y0_conv, h_i);
    Y_interp = interp1(T_i, Y_i(:,1), T_ref);
    errors_conv(i) = max(abs(Y_interp - Y_ref(:,1)));

    if i > 1
        order = log(errors_conv(i-1)/errors_conv(i)) / log(h_values(i-1)/h_values(i));
        fprintf('  %.4f     %.2e       %.2f\n', h_i, errors_conv(i), order);
    else
        fprintf('  %.4f     %.2e       ---\n', h_i, errors_conv(i));
    end
end

% 绘制收敛性图
figure('Position', [100, 100, 700, 500]);
loglog(h_values, errors_conv, 'ro-', 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', 'r');
hold on;
% 绘制O(h^4)参考线
loglog(h_values, errors_conv(1)*(h_values/h_values(1)).^4, 'k--', 'LineWidth', 1.5);
xlabel('步长 h');
ylabel('最大绝对误差');
title('RK4方法收敛性验证');
legend('RK4误差', 'O(h^4)参考线', 'Location', 'southeast');
grid on;
saveas(gcf, 'rk4_convergence_verification.png');
fprintf('图片已保存: rk4_convergence_verification.png\n');

% ============================================================
% 不同初值条件下的解 (μ=1 极限环演示)
% ============================================================
fprintf('\n========== μ=1 不同初值条件下的极限环演示 ==========\n');
mu_lc = 1;
tspan_lc = [0, 30];
h_lc = 0.05;
init_conditions = [0.5 0; 1.0 0; 2.0 0; 3.0 0; 0.5 1.0; 2.0 -1.0];

figure('Position', [100, 100, 1000, 800]);
colors = lines(size(init_conditions, 1));

% 相平面子图
subplot(2,1,1);
hold on;
for i = 1:size(init_conditions, 1)
    [~, Y_lc] = rk4_method(@(t,y) vdp_ode(t,y,mu_lc), tspan_lc, init_conditions(i,:)', h_lc);
    plot(Y_lc(:,1), Y_lc(:,2), '-', 'Color', colors(i,:), 'LineWidth', 1.2);
end
xlabel('x'); ylabel('dx/dt');
title('μ=1 不同初值条件下的相平面图 (极限环)');
legend(arrayfun(@(i) sprintf('x_0=%.1f, v_0=%.1f', ...
    init_conditions(i,1), init_conditions(i,2)), 1:6, 'UniformOutput', false), ...
    'Location', 'best');
grid on;

% 时间序列子图
subplot(2,1,2);
hold on;
for i = 1:size(init_conditions, 1)
    [T_lc, Y_lc] = rk4_method(@(t,y) vdp_ode(t,y,mu_lc), tspan_lc, init_conditions(i,:)', h_lc);
    plot(T_lc, Y_lc(:,1), '-', 'Color', colors(i,:), 'LineWidth', 1.2);
end
xlabel('t'); ylabel('x(t)');
title('μ=1 不同初值条件下的x(t)时间序列');
legend(arrayfun(@(i) sprintf('x_0=%.1f, v_0=%.1f', ...
    init_conditions(i,1), init_conditions(i,2)), 1:6, 'UniformOutput', false), ...
    'Location', 'best');
grid on;

saveas(gcf, 'vdp_mu1_limit_cycle.png');
fprintf('图片已保存: vdp_mu1_limit_cycle.png\n');

fprintf('\n========== 全部计算完成 ==========\n');
