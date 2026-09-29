% ==================== Lorenz系统 ====================
function dydt = lorenz_system(t, y)
    sigma = 10; rho = 28; beta = 8/3;
    dydt = [sigma*(y(2)-y(1));
            rho*y(1) - y(1)*y(3) - y(2);
            y(1)*y(2) - beta*y(3)];
end
