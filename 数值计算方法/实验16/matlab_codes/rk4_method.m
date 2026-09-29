% ==================== 四阶Runge-Kutta方法（四阶精度）====================
function [t, y] = rk4_method(f, t_span, y0, h)
    t0 = t_span(1); tf = t_span(2);
    N = floor((tf - t0) / h);
    t = linspace(t0, tf, N+1)';
    y = zeros(N+1, length(y0));
    y(1, :) = y0(:)';
    for i = 1:N
        ti = t(i); yi = y(i, :)';
        k1 = f(ti, yi);
        k2 = f(ti + h/2, yi + h/2 * k1);
        k3 = f(ti + h/2, yi + h/2 * k2);
        k4 = f(ti + h, yi + h * k3);
        y(i+1, :) = yi' + h/6 * (k1 + 2*k2 + 2*k3 + k4)';
    end
end
