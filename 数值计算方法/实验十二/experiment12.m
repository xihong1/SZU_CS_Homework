clc; clear; close all;
format long;

xi = [-1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0];
fi = [-4.447, -0.452, 0.551, 0.048, -0.447, 0.549, 4.552];
n = length(xi);
m = 3;

%% ===== 1. 一般多项式最小二乘拟合 =====
fprintf('===== 1. 一般多项式最小二乘拟合 =====\n');
A1 = zeros(n, m+1);
for k = 0:m
    A1(:, k+1) = xi.^k;
end
c1 = (A1' * A1) \ (A1' * fi');
fprintf('p(x) = %.10f + %.10f*x + %.10f*x^2 + %.10f*x^3\n', c1(1), c1(2), c1(3), c1(4));
y1_all = A1 * c1;
sse1 = sum((fi' - y1_all).^2);
fprintf('SSE = %.15f\n', sse1);

%% ===== 2. 正交多项式拟合 (Legendre) =====
fprintf('\n===== 2. 正交多项式拟合 (Legendre) =====\n');
a_int = -1; b_int = 2;
t = (2*xi - (a_int+b_int)) / (b_int - a_int);

A2 = zeros(n, m+1);
A2(:,1) = 1;
A2(:,2) = t';
A2(:,3) = (3*t'.^2 - 1) / 2;
A2(:,4) = (5*t'.^3 - 3*t') / 2;

alpha2 = (A2' * A2) \ (A2' * fi');

at = 2/3; bt = -1/3;
ct = zeros(1, 4);
ct(1) = alpha2(1) - alpha2(3)/2;
ct(2) = alpha2(2) - 3*alpha2(4)/2;
ct(3) = 3*alpha2(3)/2;
ct(4) = 5*alpha2(4)/2;
c2 = zeros(4,1);
c2(1) = ct(1) + ct(2)*bt + ct(3)*bt^2 + ct(4)*bt^3;
c2(2) = ct(2)*at + 2*ct(3)*at*bt + 3*ct(4)*at*bt^2;
c2(3) = ct(3)*at^2 + 3*ct(4)*at^2*bt;
c2(4) = ct(4)*at^3;

fprintf('p(x) = %.10f + %.10f*x + %.10f*x^2 + %.10f*x^3\n', c2(1), c2(2), c2(3), c2(4));
y2_all = A2 * alpha2;
sse2 = sum((fi' - y2_all).^2);
fprintf('SSE = %.15f\n', sse2);

%% ===== 3. 离散正交多项式拟合 (修正版) =====
fprintf('\n===== 3. 离散正交多项式拟合 =====\n');

% 三项递推公式:
% phi_0(x) = 1
% phi_1(x) = (x - alpha_1) * phi_0(x)
% phi_{k+1}(x) = (x - alpha_{k+1}) * phi_k(x) - beta_k * phi_{k-1}(x)
%
% 关键修正: alpha_{k+1} = <x*phi_k, phi_k> / <phi_k, phi_k>
%                              ^^^^^^^^^^^^
% 分子是 x*phi_k^2，不是 x*phi_k！

phi = zeros(n, m+1);
phi(:, 1) = ones(n, 1);

d = zeros(m+1, 1);
alpha_d = zeros(m+1, 1);
beta_d = zeros(m+1, 1);

d(1) = sum(phi(:,1).^2);  % <phi_0, phi_0> = 7

% alpha_1 = <x*phi_0, phi_0> / <phi_0, phi_0> = sum(x*1*1)/sum(1*1) = sum(x)/7
alpha_d(1) = sum(xi' .* phi(:,1) .* phi(:,1)) / d(1);
phi(:, 2) = (xi' - alpha_d(1)) .* phi(:, 1);

d(2) = sum(phi(:,2).^2);
beta_d(1) = d(2) / d(1);

for k = 2:m
    % 关键修正: 分子是 sum(x * phi_k^2)，不是 sum(x * phi_k)
    alpha_d(k) = sum(xi' .* phi(:,k) .* phi(:,k)) / d(k);
    phi(:, k+1) = (xi' - alpha_d(k)) .* phi(:, k) - beta_d(k-1) .* phi(:, k-1);
    d(k+1) = sum(phi(:,k+1).^2);
    beta_d(k) = d(k+1) / d(k);
end

fprintf('递推系数:\n');
for k = 1:m
    fprintf('  alpha(%d) = %.10f\n', k, alpha_d(k));
end
for k = 1:m
    fprintf('  beta(%d) = %.10f\n', k, beta_d(k));
end

% 验证正交性
fprintf('\n正交性验证 <phi_i, phi_j>:\n');
for i = 0:m
    for j = 0:m
        val = sum(phi(:,i+1) .* phi(:,j+1));
        if abs(val) > 1e-8
            fprintf('  <phi_%d, phi_%d> = %.10f\n', i, j, val);
        end
    end
end

% 计算gamma系数
gamma_d = zeros(m+1, 1);
for k = 0:m
    gamma_d(k+1) = sum(fi' .* phi(:,k+1)) / d(k+1);
end

fprintf('\ngamma系数:\n');
for k = 0:m
    fprintf('  gamma(%d) = %.10f\n', k, gamma_d(k+1));
end

% 显示phi在数据点上的值
fprintf('\nphi多项式在数据点上的值:\n');
fprintf('%-6s', 'x');
for k = 0:m
    fprintf('  phi_%d', k);
end
fprintf('\n');
for i = 1:n
    fprintf('%.1f    ', xi(i));
    for k = 0:m
        fprintf('  %7.3f', phi(i, k+1));
    end
    fprintf('\n');
end

% 手动转换为标准多项式
pphi = cell(m+1, 1);
pphi{1} = [1];
pphi{2} = [-alpha_d(1), 1];

% phi_2 = (x - alpha_2)*phi_1 - beta_1*phi_0
t1 = conv([0, 1], pphi{2});
t2 = alpha_d(2)*pphi{2};
max_len = max(length(t1), length(t2));
t1 = [t1, zeros(1, max_len-length(t1))];
t2 = [t2, zeros(1, max_len-length(t2))];
t3 = t1 - t2;
t4 = beta_d(1)*pphi{1};
max_len = max(length(t3), length(t4));
t3 = [t3, zeros(1, max_len-length(t3))];
t4 = [t4, zeros(1, max_len-length(t4))];
pphi{3} = t3 - t4;

% phi_3 = (x - alpha_3)*phi_2 - beta_2*phi_1
t1 = conv([0, 1], pphi{3});
t2 = alpha_d(3)*pphi{3};
max_len = max(length(t1), length(t2));
t1 = [t1, zeros(1, max_len-length(t1))];
t2 = [t2, zeros(1, max_len-length(t2))];
t3 = t1 - t2;
t4 = beta_d(2)*pphi{2};
max_len = max(length(t3), length(t4));
t3 = [t3, zeros(1, max_len-length(t3))];
t4 = [t4, zeros(1, max_len-length(t4))];
pphi{4} = t3 - t4;

fprintf('\nphi多项式系数 (升幂排列):\n');
for k = 0:m
    fprintf('  phi_%d: [', k);
    fprintf('%.10f ', pphi{k+1});
    fprintf(']\n');
end

% 组合: p(x) = sum gamma_d(k+1) * phi_k(x)
c3 = zeros(1, m+1);
for k = 0:m
    pc = pphi{k+1};
    pk_pad = zeros(1, m+1);
    pk_pad(1:length(pc)) = pc;
    c3 = c3 + gamma_d(k+1) * pk_pad;
end

fprintf('\n转换为标准多项式:\n');
fprintf('p(x) = %.10f + %.10f*x + %.10f*x^2 + %.10f*x^3\n', c3(1), c3(2), c3(3), c3(4));

y3_all = c3(1) + c3(2)*xi + c3(3)*xi.^2 + c3(4)*xi.^3;
sse3 = sum((fi - y3_all).^2);
fprintf('SSE = %.15f\n', sse3);

fprintf('\n逐点验证:\n');
for i = 1:n
    fprintf('  x=%.1f: f=%.3f, p(x)=%.6f, 残差=%.6f\n', xi(i), fi(i), y3_all(i), fi(i)-y3_all(i));
end

%% ===== 4. 三次Lagrange插值 =====
fprintf('\n===== 4. 三次Lagrange插值 =====\n');
fprintf('选取4个插值节点: x = [-1, -0.5, 0, 0.5]\n');
xi_lag = xi(1:4);
fi_lag = fi(1:4);

d_lag = zeros(1, 4);
for i = 1:4
    d_lag(i) = 1;
    for j = 1:4
        if j ~= i
            d_lag(i) = d_lag(i) * (xi_lag(i) - xi_lag(j));
        end
    end
end

lag_coeffs = zeros(4, 4);
for i = 1:4
    others = xi_lag(setdiff(1:4, i));
    a = others(1); b = others(2); c = others(3);
    lag_coeffs(i, 4) = 1;
    lag_coeffs(i, 3) = -(a+b+c);
    lag_coeffs(i, 2) = (a*b+a*c+b*c);
    lag_coeffs(i, 1) = -(a*b*c);
    lag_coeffs(i,:) = lag_coeffs(i,:) / d_lag(i);
end

c4 = fi_lag * lag_coeffs;
fprintf('p(x) = %.10f + %.10f*x + %.10f*x^2 + %.10f*x^3\n', c4(1), c4(2), c4(3), c4(4));

y_lag_all = c4(1) + c4(2)*xi + c4(3)*xi.^2 + c4(4)*xi.^3;
sse_lag = sum((fi - y_lag_all).^2);
fprintf('SSE = %.15f\n', sse_lag);

fprintf('\n逐点验证:\n');
for i = 1:n
    marker = '';
    if i <= 4, marker = ' (插值点)'; end
    fprintf('  x=%.1f: f=%.3f, p(x)=%.6f, 残差=%.6f%s\n', xi(i), fi(i), y_lag_all(i), fi(i)-y_lag_all(i), marker);
end

%% ===== 汇总 =====
fprintf('\n========================================\n');
fprintf('          最终结果汇总\n');
fprintf('========================================\n');
fprintf('一般多项式拟合:     p(x) = %.6f%+.6fx%+.6fx^2%+.6fx^3, SSE = %.2e\n', c1(1), c1(2), c1(3), c1(4), sse1);
fprintf('正交多项式拟合:     p(x) = %.6f%+.6fx%+.6fx^2%+.6fx^3, SSE = %.2e\n', c2(1), c2(2), c2(3), c2(4), sse2);
fprintf('离散正交多项式拟合: p(x) = %.6f%+.6fx%+.6fx^2%+.6fx^3, SSE = %.2e\n', c3(1), c3(2), c3(3), c3(4), sse3);
fprintf('三次Lagrange插值:   p(x) = %.6f%+.6fx%+.6fx^2%+.6fx^3, SSE = %.2e\n', c4(1), c4(2), c4(3), c4(4), sse_lag);

fprintf('\n三种最小二乘拟合系数差异:\n');
fprintf('  一般 vs Legendre:     [%.2e, %.2e, %.2e, %.2e]\n', c1-c2);
fprintf('  一般 vs 离散正交:     [%.2e, %.2e, %.2e, %.2e]\n', c1-c3);

%% ===== 绘图 =====
x_plot = linspace(-1.2, 2.2, 500);
y1_plot = c1(1) + c1(2)*x_plot + c1(3)*x_plot.^2 + c1(4)*x_plot.^3;
y2_plot = c2(1) + c2(2)*x_plot + c2(3)*x_plot.^2 + c2(4)*x_plot.^3;
y3_plot = c3(1) + c3(2)*x_plot + c3(3)*x_plot.^2 + c3(4)*x_plot.^3;
y4_plot = c4(1) + c4(2)*x_plot + c4(3)*x_plot.^2 + c4(4)*x_plot.^3;

figure('Visible', 'on', 'Position', [100, 100, 900, 600]);
plot(xi, fi, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k'); hold on;
plot(x_plot, y1_plot, 'r-', 'LineWidth', 1.5);
plot(x_plot, y2_plot, 'b--', 'LineWidth', 1.5);
plot(x_plot, y3_plot, 'g-.', 'LineWidth', 1.5);
plot(x_plot, y4_plot, 'm:', 'LineWidth', 2);
xlabel('x'); ylabel('y');
title('三次最小二乘拟合与Lagrange插值比较');
legend('离散数据点', '一般多项式拟合', '正交多项式拟合(Legendre)', '离散正交多项式拟合', '三次Lagrange插值', 'Location', 'best');
grid on;
print(gcf, 'D:\课件\数值计算方法\实验十二\fig1_all_comparison.png', '-dpng', '-r150');

figure('Visible', 'on', 'Position', [100, 100, 1200, 800]);
subplot(2,2,1);
plot(xi, fi, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k'); hold on;
plot(x_plot, y1_plot, 'r-', 'LineWidth', 1.5);
xlabel('x'); ylabel('y');
title(sprintf('一般多项式拟合 (SSE=%.2e)', sse1));
legend('数据点', '拟合曲线'); grid on;

subplot(2,2,2);
plot(xi, fi, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k'); hold on;
plot(x_plot, y2_plot, 'b-', 'LineWidth', 1.5);
xlabel('x'); ylabel('y');
title(sprintf('正交多项式拟合(Legendre) (SSE=%.2e)', sse2));
legend('数据点', '拟合曲线'); grid on;

subplot(2,2,3);
plot(xi, fi, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k'); hold on;
plot(x_plot, y3_plot, 'g-', 'LineWidth', 1.5);
xlabel('x'); ylabel('y');
title(sprintf('离散正交多项式拟合 (SSE=%.2e)', sse3));
legend('数据点', '拟合曲线'); grid on;

subplot(2,2,4);
plot(xi, fi, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k'); hold on;
plot(x_plot, y4_plot, 'm-', 'LineWidth', 1.5);
xlabel('x'); ylabel('y');
title(sprintf('三次Lagrange插值 (SSE=%.2e)', sse_lag));
legend('数据点', '插值曲线'); grid on;
print(gcf, 'D:\课件\数值计算方法\实验十二\fig2_individual.png', '-dpng', '-r150');

fprintf('\n图片已保存。\n');
