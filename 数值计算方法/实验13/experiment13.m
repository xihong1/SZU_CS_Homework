%% 实验13：机械求积、Newton-Cotes求积与复合求积
% 被积函数：f(x) = sin(x^2)，积分区间：[0, 1]
clc; clear; close all;

%% ===================== 实验1：基本机械求积 =====================
fprintf('========== 实验1：基本机械求积 ==========\n\n');
a = 0; b = 1;
f = @(x) sin(x.^2);
exact_val = integral(f, a, b);
fprintf('精确值 (MATLAB integral): %.10f\n\n', exact_val);

% 左矩形积分
I_left = (b - a) * f(a);
err_left = abs(I_left - exact_val);

% 中矩形积分
I_mid = (b - a) * f((a + b) / 2);
err_mid = abs(I_mid - exact_val);

% 右矩形积分
I_right = (b - a) * f(b);
err_right = abs(I_right - exact_val);

% 梯形积分
I_trap = (b - a) / 2 * (f(a) + f(b));
err_trap = abs(I_trap - exact_val);

% Simpson积分
I_simp = (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b));
err_simp = abs(I_simp - exact_val);

fprintf('左矩形积分: %.10f, 误差: %.2e\n', I_left, err_left);
fprintf('中矩形积分: %.10f, 误差: %.2e\n', I_mid, err_mid);
fprintf('右矩形积分: %.10f, 误差: %.2e\n', I_right, err_right);
fprintf('梯形积分:   %.10f, 误差: %.2e\n', I_trap, err_trap);
fprintf('Simpson积分: %.10f, 误差: %.2e\n\n', I_simp, err_simp);

% 绘制被积函数图像
figure(1);
x_plot = linspace(a, b, 200);
y_plot = f(x_plot);
plot(x_plot, y_plot, 'b-', 'LineWidth', 2);
hold on;
fill([x_plot, fliplr(x_plot)], [y_plot, zeros(size(y_plot))], 'b', 'FaceAlpha', 0.2);
xlabel('x'); ylabel('y');
title('f(x) = sin(x^2) 在 [0, 1] 上的图像与积分区域');
legend('f(x) = sin(x^2)', '积分区域');
grid on; hold off;
saveas(gcf, 'fig1_integrand.png');

%% ===================== 实验2：Newton-Cotes与复合求积 =====================
fprintf('========== 实验2：Newton-Cotes与复合求积 ==========\n\n');
n_values = [2, 4, 6, 8, 10];
num_n = length(n_values);

results_nc = zeros(num_n, 1); errors_nc = zeros(num_n, 1); times_nc = zeros(num_n, 1);
results_trap = zeros(num_n, 1); errors_trap = zeros(num_n, 1); times_trap = zeros(num_n, 1);
results_simp = zeros(num_n, 1); errors_simp = zeros(num_n, 1); times_simp = zeros(num_n, 1);
bounds_trap = zeros(num_n, 1); bounds_simp = zeros(num_n, 1);
weights_all = cell(num_n, 1);

for k = 1:num_n
    n = n_values(k);
    h = (b - a) / n;
    
    % Newton-Cotes求积
    tic;
    [I_nc, w] = my_newton_cotes(f, a, b, n);
    times_nc(k) = toc;
    errors_nc(k) = abs(I_nc - exact_val);
    results_nc(k) = I_nc;
    weights_all{k} = w;
    
    % 复合梯形
    tic;
    I_ct = my_composite_trapezoid(f, a, b, n);
    times_trap(k) = toc;
    errors_trap(k) = abs(I_ct - exact_val);
    results_trap(k) = I_ct;
    
    % 复合Simpson
    tic;
    I_cs = my_composite_simpson(f, a, b, n);
    times_simp(k) = toc;
    errors_simp(k) = abs(I_cs - exact_val);
    results_simp(k) = I_cs;
    
    % 理论误差界
    M2 = max(abs(2*cos(linspace(a,b,2000).^2) - 4*linspace(a,b,2000).^2.*sin(linspace(a,b,2000).^2)));
    bounds_trap(k) = (b-a)/12 * h^2 * M2;
    
    xt = linspace(a, b, 2000);
    f4v = abs(-12*cos(xt.^2) + 48*xt.^2.*sin(xt.^2) + 16*xt.^4.*cos(xt.^2) - 16*xt.^2.*sin(xt.^2));
    M4 = max(f4v);
    bounds_simp(k) = (b-a)/2880 * h^4 * M4;
    
    fprintf('n=%2d: NC=%.10f (err=%.2e), CT=%.10f (err=%.2e), CS=%.10f (err=%.2e)\n', ...
        n, I_nc, errors_nc(k), I_ct, errors_trap(k), I_cs, errors_simp(k));
end

%% 打印Newton-Cotes系数
fprintf('\n===== Newton-Cotes求积系数 =====\n');
for k = 1:num_n
    n = n_values(k);
    w = weights_all{k};
    has_neg = any(w < 0);
    neg_str = '';
    if has_neg
        neg_str = ' (出现负值!)';
    end
    fprintf('n=%d: ', n);
    fprintf('%.6f ', w);
    fprintf('%s\n', neg_str);
end

%% 图2：误差对比
figure(2);
subplot(1,2,1);
semilogy(n_values, errors_trap, 'ro-', 'LineWidth', 1.5, 'MarkerSize', 8); hold on;
semilogy(n_values, bounds_trap, 'r--', 'LineWidth', 1.5);
semilogy(n_values, errors_simp, 'bs-', 'LineWidth', 1.5, 'MarkerSize', 8);
semilogy(n_values, bounds_simp, 'b--', 'LineWidth', 1.5);
semilogy(n_values, errors_nc, 'g^-', 'LineWidth', 1.5, 'MarkerSize', 8);
xlabel('n'); ylabel('误差');
title('实际误差与截断误差界对比');
legend('复合梯形实际误差', '复合梯形误差界', '复合Simpson实际误差', ...
    '复合Simpson误差界', 'Newton-Cotes实际误差', 'Location', 'best');
grid on; hold off;

subplot(1,2,2);
bar(n_values, [times_trap, times_simp, times_nc]);
xlabel('n'); ylabel('时间(秒)');
title('各方法计算时间对比');
legend('复合梯形', '复合Simpson', 'Newton-Cotes', 'Location', 'best');
grid on;
saveas(gcf, 'fig2_error_time.png');

%% 图3：各方法收敛对比
figure(3);
plot(n_values, errors_trap, 'ro-', 'LineWidth', 1.5, 'MarkerSize', 8); hold on;
plot(n_values, errors_simp, 'bs-', 'LineWidth', 1.5, 'MarkerSize', 8);
plot(n_values, errors_nc, 'g^-', 'LineWidth', 1.5, 'MarkerSize', 8);
set(gca, 'YScale', 'log');
xlabel('n'); ylabel('误差');
title('三种方法的收敛性对比');
legend('复合梯形', '复合Simpson', 'Newton-Cotes', 'Location', 'best');
grid on; hold off;
saveas(gcf, 'fig3_convergence.png');

%% ===================== 函数定义 =====================
function [I, weights] = my_newton_cotes(f, a, b, n)
    h = (b - a) / n;
    x = linspace(a, b, n+1)';
    t = linspace(0, 1, n+1);
    weights = zeros(n+1, 1);
    for i = 0:n
        L = @(tv) ones(size(tv));
        for j = 0:n
            if j ~= i
                L = L .* (tv - t(j+1)) / (t(i+1) - t(j+1));
            end
        end
        weights(i+1) = integral(@(tv) arrayfun(@(v) L(v), tv), 0, 1);
    end
    weights = weights * (b - a);
    I = weights' * f(x);
end

function I = my_composite_trapezoid(f, a, b, n)
    h = (b - a) / n;
    x = linspace(a, b, n+1);
    fx = f(x);
    I = h * (sum(fx) - 0.5*(fx(1)+fx(end)));
end

function I = my_composite_simpson(f, a, b, n)
    if mod(n,2) ~= 0, n = n+1; end
    h = (b - a) / n;
    x = linspace(a, b, n+1);
    fx = f(x);
    I = h/3 * (fx(1) + fx(end) + 4*sum(fx(2:2:end-1)) + 2*sum(fx(3:2:end-2)));
end
