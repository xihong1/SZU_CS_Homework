% ==================== Chen系统 ====================
function dydt = chen_system(t, y)
    a = 35; b = 3; c = 28;
    dydt = [a*(y(2)-y(1));
            (c-a)*y(1) - y(1)*y(3) + c*y(2);
            y(1)*y(2) - b*y(3)];
end
