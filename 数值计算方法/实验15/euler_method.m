function [T, Y] = euler_method(odefun, tspan, y0, h)
% 显式Euler法求解常微分方程组
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
    Y(n+1, :) = Y(n, :) + h * odefun(T(n), Y(n, :)')';
    T(n+1) = T(n) + h;
end
end
