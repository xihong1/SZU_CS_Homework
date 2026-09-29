function dydt = vdp_ode(t, y, mu)
% Van der Pol振子的一阶微分方程组
% y = [x; dx/dt]
% 方程: d²x/dt² - μ(1-x²)dx/dt + x = 0
dydt = zeros(2, 1);
dydt(1) = y(2);                              % dx/dt = y(2)
dydt(2) = mu * (1 - y(1)^2) * y(2) - y(1);   % d²x/dt²
end
