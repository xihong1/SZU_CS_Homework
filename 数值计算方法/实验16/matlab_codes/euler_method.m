% ==================== Euler方法（一阶精度）====================
function [t, y] = euler_method(f, t_span, y0, h)
    t0 = t_span(1); tf = t_span(2);
    N = floor((tf - t0) / h);
    t = linspace(t0, tf, N+1)';
    y = zeros(N+1, length(y0));
    y(1, :) = y0(:)';
    for i = 1:N
        y(i+1, :) = y(i, :) + h * f(t(i), y(i, :)')';
    end
end
