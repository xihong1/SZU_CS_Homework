% ==================== 改进Euler方法（预估-校正法，二阶精度）====================
function [t, y] = improved_euler_method(f, t_span, y0, h)
    t0 = t_span(1); tf = t_span(2);
    N = floor((tf - t0) / h);
    t = linspace(t0, tf, N+1)';
    y = zeros(N+1, length(y0));
    y(1, :) = y0(:)';
    for i = 1:N
        y_pred = y(i, :) + h * f(t(i), y(i, :)')';
        y(i+1, :) = y(i, :) + h/2 * (f(t(i), y(i, :)') + f(t(i+1), y_pred'))';
    end
end
