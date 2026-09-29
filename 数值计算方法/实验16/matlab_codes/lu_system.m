% ==================== Lü系统 ====================
function dydt = lu_system(t, y)
    a = 36; b = 3; c = 20;
    dydt = [a*(y(2)-y(1));
            -y(1)*y(3) + c*y(2);
            y(1)*y(2) - b*y(3)];
end
