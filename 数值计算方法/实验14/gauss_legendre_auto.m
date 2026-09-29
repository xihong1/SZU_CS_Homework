function [I, n_final] = gauss_legendre_auto(f, a, b, epsilon)
    I_prev = 0;
    for n = 1:20
        [nodes, weights] = gauss_legendre_nodes(n);
        x_gl = (b - a) / 2 * nodes + (a + b) / 2;
        w_gl = (b - a) / 2 * weights;
        I = sum(w_gl .* f(x_gl));
        if n > 1 && abs(I - I_prev) < epsilon
            n_final = n;
            return;
        end
        I_prev = I;
    end
    n_final = 20;
end
