function [P, dP] = legendre_poly(n, x)
    if n == 0
        P = 1; dP = 0; return;
    end
    if n == 1
        P = x; dP = 1; return;
    end
    P0 = 1; P1 = x;
    dP0 = 0; dP1 = 1;
    for k = 2:n
        P2 = ((2*k - 1) * x * P1 - (k - 1) * P0) / k;
        dP2 = ((2*k - 1) * (P1 + x * dP1) - (k - 1) * dP0) / k;
        P0 = P1; P1 = P2;
        dP0 = dP1; dP1 = dP2;
    end
    P = P1; dP = dP1;
end
