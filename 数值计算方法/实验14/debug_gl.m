clear; clc;

f = @(x) cos(x);
a = 0; b = pi/2;
exact_val = 1;

fprintf('Testing Gauss-Legendre nodes and weights:\n');
for n = 1:5
    [nodes, weights] = gauss_legendre_nodes(n);
    fprintf('n=%d: nodes = [', n);
    fprintf('%.8f ', nodes);
    fprintf('], weights = [');
    fprintf('%.8f ', weights);
    fprintf('], sum_weights = %.8f\n', sum(weights));
end

fprintf('\nTesting integration:\n');
for n = 1:10
    [nodes, weights] = gauss_legendre_nodes(n);
    x_gl = (b - a) / 2 * nodes + (a + b) / 2;
    w_gl = (b - a) / 2 * weights;
    I_n = sum(w_gl .* f(x_gl));
    fprintf('n=%d: I=%.15f, error=%.2e\n', n, I_n, abs(I_n - exact_val));
end

% Also test with MATLAB's built-in
I_exact = integral(f, a, b);
fprintf('\nMATLAB integral: %.15f\n', I_exact);
