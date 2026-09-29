function [T, Y] = rk4_method(odefun, tspan, y0, h)
% 经典四阶Runge-Kutta方法求解常微分方程组
% 输入: odefun - 右端函数句柄
%        tspan - 时间区间 [t0, tf]
%        y0 - 初值向量
%        h - 固定步长
% 输出: T - 时间向量
%        Y - 数值解矩阵 (每行对应一个时间步)

N = floor((tspan(2) - tspan(1)) / h);
m = length(y0);
T = zeros(N+1, 1);
Y = zeros(N+1, m);

T(1) = tspan(1);
Y(1, :) = y0(:)';

for n = 1:N
    tn = T(n);
    yn = Y(n, :)';

    K1 = h * odefun(tn, yn);
    K2 = h * odefun(tn + h/2, yn + K1/2);
    K3 = h * odefun(tn + h/2, yn + K2/2);
    K4 = h * odefun(tn + h, yn + K3);

    Y(n+1, :) = yn + (K1 + 2*K2 + 2*K3 + K4) / 6;
    T(n+1) = tn + h;
end
end
