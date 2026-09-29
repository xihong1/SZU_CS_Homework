% ==================== Chua电路系统 ====================
function dydt = chua_system(t, y)
    alpha = 9; beta = 100/7;
    m0 = -5/7; m1 = -3/14;
    % Chua二极管分段线性特性函数
    fx = m1*y(1) + 0.5*(m0-m1)*(abs(y(1)+1) - abs(y(1)-1));
    dydt = [alpha*(y(2)-y(1)-fx);
            y(1) - y(2) + y(3);
            -beta*y(2)];
end
