function [nodes, weights] = gauss_legendre_nodes(n)
    nodes = zeros(n, 1);
    weights = zeros(n, 1);
    
    m = ceil((n + 1) / 2);
    
    for i = 1:m
        % Better initial guess
        x = cos(pi * (4*i - 1) / (4*n + 2));
        
        for iter = 1:100
            [P, dP] = legendre_poly(n, x);
            if abs(dP) < 1e-30
                break;
            end
            dx = -P / dP;
            x = x + dx;
            if abs(dx) < 1e-14
                break;
            end
        end
        
        nodes(i) = x;
        weights(i) = 2 / ((1 - x^2) * dP^2);
    end
    
    % Mirror for symmetry
    for i = 1:m
        nodes(n + 1 - i) = -nodes(i);
        weights(n + 1 - i) = weights(i);
    end
    
    if mod(n, 2) == 1
        nodes(m) = 0;
        [P, dP] = legendre_poly(n, 0);
        weights(m) = 2 / (1 * dP^2);
    end
end
