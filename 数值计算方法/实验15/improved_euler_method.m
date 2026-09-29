function [T, Y] = improved_euler_method(odefun, tspan, y0, h)
% 改进的Euler方法（预估-校正法，二阶Runge-Kutta）
% 输入: odefun - 右端函数句柄
%        tspan - 时间区间 [t0, tf]
%        y0 - 初值向量
%        h - 固定步长
% 输出: T - 时间向量
%        Y - 数值解矩阵

N = floor((tspan(2) - tspan(1)) / h);
m = length(y0);
T = zeros(N+1, 1);
Y = zeros(N+1, m);

T(1) = tspan(1);
Y(1, :) = y0(:)';

for n = 1:N
    tn = T(n);
    yn = Y(n, :)';

    % 预估步 (Euler)
    K1 = h * odefun(tn, yn);
    y_bar = yn + K1;

    % 校正步 (梯形)
    K2 = h * odefun(tn + h, y_bar);
    Y(n+1, :) = yn + (K1 + K2) / 2;
    T(n+1) = tn + h;
end
end
