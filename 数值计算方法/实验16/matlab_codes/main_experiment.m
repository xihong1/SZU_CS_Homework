% ========================================================================
% 实验16：典型混沌系统方程求解  — 主程序
% 数值计算方法：Euler法、改进Euler法、四阶Runge-Kutta法
% 系统：Lorenz、Chen、Lü、Chua电路
% ========================================================================
clc; clear; close all;

% 创建输出目录
output_dir = fullfile('..', 'figures');
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

fprintf('=============================================================\n');
fprintf('实验16：典型混沌系统方程求解\n');
fprintf('=============================================================\n\n');

% ========================================================================
% Step 1: 测试验证 — 使用精确解已知的简单线性算例
% dy/dt = -2y, y(0)=1, t∈[0,2], 精确解: y(t)=exp(-2t)
% ========================================================================
fprintf('>>> Step 1: 方法正确性验证\n');
fprintf('测试算例: dy/dt = -2y, y(0) = 1, t∈[0,2]\n');
fprintf('精确解: y(t) = exp(-2t), y(2) = exp(-4) ≈ 0.0183156389\n\n');

t_span = [0, 2];
y0_test = 1;
h_list = [0.2, 0.1, 0.05, 0.025];
exact_final = exp(-4);

fprintf('%-12s %-12s %-18s %-12s\n', '方法', '步长h', 'y(2)数值解', '终点误差');
fprintf('------------------------------------------------------------------\n');

% 存储验证结果
err_euler = zeros(size(h_list));
err_imeuler = zeros(size(h_list));
err_rk4 = zeros(size(h_list));

for idx = 1:length(h_list)
    h = h_list(idx);

    [~, y_e] = euler_method(@linear_test, t_span, y0_test, h);
    err_euler(idx) = abs(y_e(end) - exact_final);
    fprintf('%-12s %-12.3f %-18.10f %-12.2e\n', 'Euler', h, y_e(end), err_euler(idx));

    [~, y_ie] = improved_euler_method(@linear_test, t_span, y0_test, h);
    err_imeuler(idx) = abs(y_ie(end) - exact_final);
    fprintf('%-12s %-12.3f %-18.10f %-12.2e\n', '改进Euler', h, y_ie(end), err_imeuler(idx));

    [~, y_rk] = rk4_method(@linear_test, t_span, y0_test, h);
    err_rk4(idx) = abs(y_rk(end) - exact_final);
    fprintf('%-12s %-12.3f %-18.10f %-12.2e\n', 'RK4', h, y_rk(end), err_rk4(idx));

    fprintf('\n');
end

% 绘制收敛验证图
figure('Position', [100, 100, 1400, 550]);

subplot(1,2,1);
loglog(h_list, err_euler, 'bo-', 'LineWidth', 2, 'MarkerSize', 8); hold on;
loglog(h_list, err_imeuler, 'rs-', 'LineWidth', 2, 'MarkerSize', 8);
loglog(h_list, err_rk4, 'g^-', 'LineWidth', 2, 'MarkerSize', 8);
% 理论收敛阶参考线
loglog(h_list, h_list.^1, 'k--', 'LineWidth', 1, 'Color', [0.5 0.5 0.5]);
text(h_list(end-1), h_list(end-1)^1*1.5, 'O(h)', 'FontSize', 10);
loglog(h_list, h_list.^2, 'k--', 'LineWidth', 1, 'Color', [0.5 0.5 0.5]);
text(h_list(end-1), h_list(end-1)^2*1.5, 'O(h^2)', 'FontSize', 10);
loglog(h_list, h_list.^4, 'k--', 'LineWidth', 1, 'Color', [0.5 0.5 0.5]);
text(h_list(end-1), h_list(end-1)^4*1.5, 'O(h^4)', 'FontSize', 10);
xlabel('步长 h', 'FontSize', 12);
ylabel('终点绝对误差', 'FontSize', 12);
title('数值方法收敛性验证 (log-log图)', 'FontSize', 14);
legend('Euler (1阶)', '改进Euler (2阶)', 'RK4 (4阶)', 'Location', 'northwest');
grid on;

subplot(1,2,2);
t_exact = linspace(0, 2, 500);
y_exact = exp(-2*t_exact);
plot(t_exact, y_exact, 'k-', 'LineWidth', 2.5); hold on;
h_plot = 0.15;
[te, ye] = euler_method(@linear_test, t_span, y0_test, h_plot);
[tie, yie] = improved_euler_method(@linear_test, t_span, y0_test, h_plot);
[trk, yrk] = rk4_method(@linear_test, t_span, y0_test, h_plot);
plot(te, ye, 'bo-', 'LineWidth', 1.2, 'MarkerSize', 5);
plot(tie, yie, 'rs-', 'LineWidth', 1.2, 'MarkerSize', 5);
plot(trk, yrk, 'g^-', 'LineWidth', 1.2, 'MarkerSize', 5);
xlabel('t', 'FontSize', 12);
ylabel('y(t)', 'FontSize', 12);
title(sprintf('各方法数值解与精确解对比 (h=%.2f)', h_plot), 'FontSize', 14);
legend('精确解 y=e^{-2t}', 'Euler', '改进Euler', 'RK4', 'Location', 'northeast');
grid on;

saveas(gcf, fullfile(output_dir, 'convergence_validation.png'));
fprintf('验证图已保存: figures/convergence_validation.png\n\n');

% ========================================================================
% Step 2: 求解四个典型混沌系统
% ========================================================================
fprintf('>>> Step 2: 求解各混沌系统\n\n');

% 系统配置：{名称, 函数句柄, 初始条件, 时间区间, 步长}
systems = {
    'Lorenz',  @lorenz_system,  [0, 1, 0],    [0, 50],  0.005;
    'Chen',    @chen_system,    [0, 1, 0],    [0, 50],  0.005;
    'Lu',      @lu_system,      [0, 1, 0],    [0, 50],  0.005;
    'Chua',    @chua_system,    [0, 0.5, 0],  [0, 100], 0.01;
};

method_names = {'Euler', '改进Euler', 'RK4'};
all_results = cell(size(systems, 1), 1);

for s = 1:size(systems, 1)
    sys_name = systems{s, 1};
    sys_fun  = systems{s, 2};
    sys_y0   = systems{s, 3};
    sys_tspan = systems{s, 4};
    sys_h    = systems{s, 5};

    fprintf('--- %s系统 ---\n', sys_name);
    fprintf('  初始条件: (%.1f, %.1f, %.1f)\n', sys_y0);
    fprintf('  时间区间: [%.0f, %.0f]\n', sys_tspan(1), sys_tspan(2));
    fprintf('  步长: h = %.4f\n', sys_h);

    sys_results = struct();

    for m = 1:3
        mname = method_names{m};
        tic;
        switch m
            case 1
                [t, y] = euler_method(sys_fun, sys_tspan, sys_y0, sys_h);
            case 2
                [t, y] = improved_euler_method(sys_fun, sys_tspan, sys_y0, sys_h);
            case 3
                [t, y] = rk4_method(sys_fun, sys_tspan, sys_y0, sys_h);
        end
        elapsed = toc;
        n_steps = length(t) - 1;

        sys_results.(strrep(mname, '改进', 'Imp')) = struct(...
            't', t, 'y', y, 'time', elapsed, 'n_steps', n_steps);
        fprintf('  %s: %d步, 耗时 %.4fs\n', mname, n_steps, elapsed);

        % 绘制三维相空间轨迹
        figure('Position', [50, 50, 900, 750]);
        % 使用渐变色显示时间演化
        n_pts = length(t);
        cmap = jet(n_pts);
        for i = 1:n_pts-1
            plot3(y(i:i+1,1), y(i:i+1,2), y(i:i+1,3), ...
                  'Color', cmap(i,:), 'LineWidth', 0.3); hold on;
        end
        xlabel('X', 'FontSize', 12); ylabel('Y', 'FontSize', 12); zlabel('Z', 'FontSize', 12);
        title(sprintf('%s系统 三维相空间轨迹 (%s)', sys_name, mname), 'FontSize', 14);
        view([-35, 25]); grid on; colorbar; colormap jet;
        saveas(gcf, fullfile(output_dir, sprintf('%s_phase3d_%s.png', sys_name, mname)));
        close;

        % 仅为RK4方法绘制更多详细图
        if m == 3
            % 二维相平面投影
            figure('Position', [50, 50, 1500, 450]);
            proj_labels = {'X-Y 平面', 'X-Z 平面', 'Y-Z 平面'};
            proj_pairs = {[1,2], [1,3], [2,3]};
            axis_labels = {'X', 'Y', 'Z'};
            for p_idx = 1:3
                subplot(1,3,p_idx);
                pi = proj_pairs{p_idx};
                for i = 1:n_pts-1
                    plot(y(i:i+1, pi(1)), y(i:i+1, pi(2)), ...
                         'Color', cmap(i,:), 'LineWidth', 0.3); hold on;
                end
                xlabel(axis_labels{pi(1)}, 'FontSize', 10);
                ylabel(axis_labels{pi(2)}, 'FontSize', 10);
                title(proj_labels{p_idx}, 'FontSize', 12);
                grid on;
            end
            sgtitle(sprintf('%s系统 二维相平面投影 (RK4)', sys_name), 'FontSize', 14);
            saveas(gcf, fullfile(output_dir, sprintf('%s_projections_RK4.png', sys_name)));
            close;

            % 时间序列图
            figure('Position', [50, 50, 1200, 700]);
            max_pts = 2000;
            step = max(1, floor(n_pts/max_pts));
            t_plot = t(1:step:end);
            y_plot = y(1:step:end, :);
            subplot(3,1,1);
            plot(t_plot, y_plot(:,1), 'b-', 'LineWidth', 0.5);
            ylabel('X(t)', 'FontSize', 10); grid on;
            title(sprintf('%s系统 时间序列 (RK4)', sys_name), 'FontSize', 13);
            subplot(3,1,2);
            plot(t_plot, y_plot(:,2), 'r-', 'LineWidth', 0.5);
            ylabel('Y(t)', 'FontSize', 10); grid on;
            subplot(3,1,3);
            plot(t_plot, y_plot(:,3), 'Color', [0 0.6 0], 'LineWidth', 0.5);
            ylabel('Z(t)', 'FontSize', 10); xlabel('时间 t', 'FontSize', 12); grid on;
            saveas(gcf, fullfile(output_dir, sprintf('%s_timeseries_RK4.png', sys_name)));
            close;
        end
    end

    % 方法对比图
    figure('Position', [50, 50, 1700, 1000]);
    method_handles = {@euler_method, @improved_euler_method, @rk4_method};
    for m = 1:3
        mname = method_names{m};
        fname = strrep(mname, '改进', 'Imp');
        t_m = sys_results.(fname).t;
        y_m = sys_results.(fname).y;
        n_pts_m = length(t_m);
        cmap_m = jet(n_pts_m);

        % 3D相空间
        subplot(2,3,m);
        for i = 1:n_pts_m-1
            plot3(y_m(i:i+1,1), y_m(i:i+1,2), y_m(i:i+1,3), ...
                  'Color', cmap_m(i,:), 'LineWidth', 0.3); hold on;
        end
        xlabel('X'); ylabel('Y'); zlabel('Z');
        title(sprintf('%s', mname), 'FontSize', 12);
        view([-35, 25]); grid on;

        % 时间序列
        subplot(2,3,m+3);
        step = max(1, floor(n_pts_m/1500));
        t_p = t_m(1:step:end); y_p = y_m(1:step:end, :);
        plot(t_p, y_p(:,1), 'b-', 'LineWidth', 0.5); hold on;
        plot(t_p, y_p(:,2), 'r-', 'LineWidth', 0.5);
        plot(t_p, y_p(:,3), 'Color', [0 0.6 0], 'LineWidth', 0.5);
        xlabel('t'); ylabel('值');
        legend('X(t)', 'Y(t)', 'Z(t)', 'FontSize', 7);
        title(sprintf('%s - 时间序列', mname), 'FontSize', 12);
        grid on;
    end
    sgtitle(sprintf('%s系统 - 三种数值方法对比 (h=%.4f)', sys_name, sys_h), ...
            'FontSize', 16, 'FontWeight', 'bold');
    saveas(gcf, fullfile(output_dir, sprintf('%s_methods_comparison.png', sys_name)));
    close;

    % 初值敏感性分析（蝴蝶效应验证）
    figure('Position', [50, 50, 1200, 750]);
    deltas = [0, 1e-6, 1e-4];
    delta_labels = {'δ=0 (基准)', 'δ=10^{-6}', 'δ=10^{-4}'};
    for d_idx = 1:3
        y0_pert = sys_y0;
        y0_pert(1) = y0_pert(1) + deltas(d_idx);
        [t_sens, y_sens] = rk4_method(sys_fun, sys_tspan, y0_pert, sys_h);

        subplot(3,1,1);
        plot(t_sens, y_sens(:,1), 'LineWidth', 0.8); hold on;
        ylabel('X(t)', 'FontSize', 10);
        if d_idx == 1; title(sprintf('%s系统 初值敏感性分析', sys_name), 'FontSize', 13); end
        grid on;

        subplot(3,1,2);
        plot(t_sens, y_sens(:,2), 'LineWidth', 0.8); hold on;
        ylabel('Y(t)', 'FontSize', 10); grid on;

        subplot(3,1,3);
        plot(t_sens, y_sens(:,3), 'LineWidth', 0.8); hold on;
        ylabel('Z(t)', 'FontSize', 10); xlabel('时间 t', 'FontSize', 12); grid on;
    end
    subplot(3,1,1); legend(delta_labels, 'FontSize', 8);
    saveas(gcf, fullfile(output_dir, sprintf('%s_sensitivity.png', sys_name)));
    close;

    all_results{s} = sys_results;
    fprintf('\n');
end

% ========================================================================
% Step 3: 方法精度对比分析（以RK4小步长解为参考）
% ========================================================================
fprintf('>>> Step 3: 方法精度对比分析\n\n');

for s = 1:size(systems, 1)
    sys_name = systems{s, 1};
    sys_fun  = systems{s, 2};
    sys_y0   = systems{s, 3};
    sys_tspan = systems{s, 4};
    sys_h    = systems{s, 5};

    fprintf('--- %s系统 精度对比 ---\n', sys_name);

    % 参考解（RK4，更小步长）
    h_ref = sys_h / 4;
    [t_ref, y_ref] = rk4_method(sys_fun, sys_tspan, sys_y0, h_ref);

    figure('Position', [50, 50, 1500, 550]);

    subplot(1,2,1);
    for m = 1:3
        mname = method_names{m};
        fname = strrep(mname, '改进', 'Imp');
        t_m = all_results{s}.(fname).t;
        y_m = all_results{s}.(fname).y;

        % 插值到参考时间点
        y_interp = interp1(t_m, y_m, t_ref);
        % 计算每步的2-范数误差
        err_vec = sqrt(sum((y_interp - y_ref).^2, 2));
        semilogy(t_ref, err_vec, 'LineWidth', 1.2); hold on;

        % 终点误差
        y_final_interp = interp1(t_m, y_m, sys_tspan(2));
        y_ref_final = y_ref(end, :);
        final_err = norm(y_final_interp - y_ref_final);
        fprintf('  %s: 终点误差 = %.6e\n', mname, final_err);
    end
    xlabel('时间 t', 'FontSize', 12);
    ylabel('全局误差 (2-范数)', 'FontSize', 12);
    title(sprintf('%s系统 误差演化曲线', sys_name), 'FontSize', 13);
    legend(method_names, 'FontSize', 10);
    grid on;

    subplot(1,2,2);
    plot3(y_ref(:,1), y_ref(:,2), y_ref(:,3), 'b-', 'LineWidth', 0.3);
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title(sprintf('%s系统 RK4参考轨迹 (h=%.5f)', sys_name, h_ref), 'FontSize', 13);
    view([-35, 25]); grid on;

    saveas(gcf, fullfile(output_dir, sprintf('%s_error_analysis.png', sys_name)));
    close;
    fprintf('\n');
end

% ========================================================================
% Step 4: 四种系统吸引子汇总
% ========================================================================
fprintf('>>> Step 4: 生成汇总图表\n');

figure('Position', [50, 50, 1500, 1300]);
for s = 1:4
    sys_name = systems{s, 1};
    sys_fun  = systems{s, 2};
    sys_y0   = systems{s, 3};
    sys_tspan = systems{s, 4};
    sys_h    = systems{s, 5};

    [t_s, y_s] = rk4_method(sys_fun, sys_tspan, sys_y0, sys_h);
    n_pts_s = length(t_s);
    cmap_s = jet(n_pts_s);

    subplot(2,2,s);
    for i = 1:n_pts_s-1
        plot3(y_s(i:i+1,1), y_s(i:i+1,2), y_s(i:i+1,3), ...
              'Color', cmap_s(i,:), 'LineWidth', 0.3); hold on;
    end
    xlabel('X'); ylabel('Y'); zlabel('Z');
    title(sprintf('%s系统 混沌吸引子', sys_name), 'FontSize', 14, 'FontWeight', 'bold');
    view([-35, 25]); grid on;
end
sgtitle('四种典型混沌系统的吸引子结构对比 (RK4方法)', 'FontSize', 16, 'FontWeight', 'bold');
saveas(gcf, fullfile(output_dir, 'all_systems_attractors.png'));
close;
fprintf('  汇总图已保存\n\n');

% ========================================================================
% Step 5: 性能汇总
% ========================================================================
fprintf('>>> Step 5: 性能汇总\n\n');
fprintf('%-8s %-12s %-8s %-14s\n', '系统', '方法', '步数', '计算时间(s)');
fprintf('--------------------------------------------------\n');
for s = 1:4
    sys_name = systems{s, 1};
    for m = 1:3
        mname = method_names{m};
        fname = strrep(mname, '改进', 'Imp');
        r = all_results{s}.(fname);
        fprintf('%-8s %-12s %-8d %-14.4f\n', sys_name, mname, r.n_steps, r.time);
    end
end

fprintf('\n=============================================================\n');
fprintf('所有图表生成完毕！保存在 figures/ 目录下。\n');
fprintf('=============================================================\n');
