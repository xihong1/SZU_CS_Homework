clear; clc; close all;

f = @(x) cos(x);
a = 0; b = pi/2;
exact_val = 1;

f_verify = @(x) x.^2;
a_v = 0; b_v = 1;
exact_verify = 1/3;

epsilon = 0.5e-6;

fprintf('========================================\n');
fprintf('  Experiment 14\n');
fprintf('========================================\n');

%% 1. Variable-step Trapezoidal
fprintf('---------- 1. Variable-step Trapezoidal ----------\n');
[I_trap, iter_trap, trap_history] = varstep_trapezoid(f, a, b, epsilon, 20);
fprintf('Iterations: %d\n', iter_trap);
fprintf('Approx: %.15f\n', I_trap);
fprintf('Error: %.2e\n', abs(I_trap - exact_val));

[I_trap_v, ~, ~] = varstep_trapezoid(f_verify, a_v, b_v, epsilon, 20);
fprintf('Verify: %.15f, Error: %.2e\n\n', I_trap_v, abs(I_trap_v - exact_verify));

%% 2. Adaptive Simpson
fprintf('---------- 2. Adaptive Simpson ----------\n');
[I_simp, depth_simp, simp_history] = adaptive_simpson_main(f, a, b, epsilon, 50);
fprintf('Max depth: %d\n', depth_simp);
fprintf('Approx: %.15f\n', I_simp);
fprintf('Error: %.2e\n', abs(I_simp - exact_val));

[I_simp_v, ~, ~] = adaptive_simpson_main(f_verify, a_v, b_v, epsilon, 50);
fprintf('Verify: %.15f, Error: %.2e\n\n', I_simp_v, abs(I_simp_v - exact_verify));

%% 3. Romberg
fprintf('---------- 3. Romberg ----------\n');
[I_rom, iter_rom, R] = romberg_quad(f, a, b, epsilon, 15);
fprintf('Iterations: %d\n', iter_rom);
fprintf('Approx: %.15f\n', I_rom);
fprintf('Error: %.2e\n', abs(I_rom - exact_val));

fprintf('Romberg T-table:\n');
fprintf('%-16s', 'T(k,0)');
for j = 1:min(iter_rom, 7)
    fprintf('%-16s', sprintf('T(k,%d)', j));
end
fprintf('\n');
for k = 0:min(iter_rom, 10)
    fprintf('%-16.12f', R(k+1, 1));
    for j = 1:min(iter_rom, 7)
        if j <= k
            fprintf('%-16.12f', R(k+1, j+1));
        else
            fprintf('%-16s', '---');
        end
    end
    fprintf('\n');
end
fprintf('\n');

[I_rom_v, ~, ~] = romberg_quad(f_verify, a_v, b_v, epsilon, 15);
fprintf('Verify: %.15f, Error: %.2e\n\n', I_rom_v, abs(I_rom_v - exact_verify));

%% 4. Gauss-Legendre
fprintf('---------- 4. Gauss-Legendre ----------\n');
[I_gl, n_gl] = gauss_legendre_auto(f, a, b, epsilon);
fprintf('Nodes needed: %d\n', n_gl);
fprintf('Approx: %.15f\n', I_gl);
fprintf('Error: %.2e\n', abs(I_gl - exact_val));

fprintf('GL different node counts:\n');
fprintf('%-8s %-20s %-15s\n', 'n', 'Approx', 'Error');
fprintf('%s\n', repmat('-', 1, 45));
gl_errors_all = zeros(1, 10);
for n = 1:10
    [nodes, weights] = gauss_legendre_nodes(n);
    x_gl = (b - a) / 2 * nodes + (a + b) / 2;
    w_gl = (b - a) / 2 * weights;
    I_n = sum(w_gl .* f(x_gl));
    gl_errors_all(n) = abs(I_n - exact_val);
    fprintf('%-8d %-20.15f %-15.2e\n', n, I_n, abs(I_n - exact_val));
end

[I_gl_v, ~] = gauss_legendre_auto(f_verify, a_v, b_v, epsilon);
fprintf('Verify: %.15f, Error: %.2e\n\n', I_gl_v, abs(I_gl_v - exact_verify));

%% Summary
fprintf('\n========================================\n');
fprintf('  Summary (epsilon = %.1e, exact = 1)\n', epsilon);
fprintf('========================================\n');
fprintf('%-24s %-18s %-15s %-10s\n', 'Method', 'Approx', 'Error', 'Iters');
fprintf('%s\n', repmat('-', 1, 70));
fprintf('%-24s %-18.12f %-15.2e %-10d\n', 'Trapezoid', I_trap, abs(I_trap-exact_val), iter_trap);
fprintf('%-24s %-18.12f %-15.2e %-10d\n', 'Adaptive Simpson', I_simp, abs(I_simp-exact_val), depth_simp);
fprintf('%-24s %-18.12f %-15.2e %-10d\n', 'Romberg', I_rom, abs(I_rom-exact_val), iter_rom);
fprintf('%-24s %-18.12f %-15.2e %-10d\n', sprintf('Gauss-Legendre(n=%d)', n_gl), I_gl, abs(I_gl-exact_val), n_gl);

%% Plotting
trap_errors = abs(trap_history - exact_val);
rom_errors = [];
for k = 1:min(iter_rom+1, size(R,1))
    rom_errors(k) = abs(R(k, 1) - exact_val);
end
simp_errors_list = abs(simp_history - exact_val);

figure('Position', [50, 50, 1200, 800]);

subplot(2, 3, 1);
semilogy(0:length(trap_errors)-1, trap_errors, 'bo-', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('Iteration k'); ylabel('Absolute Error');
title('(a) Variable-step Trapezoid');
grid on;

subplot(2, 3, 2);
semilogy(0:length(simp_errors_list)-1, simp_errors_list, 'rs-', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('Recursion Depth'); ylabel('Absolute Error');
title('(b) Adaptive Simpson');
grid on;

subplot(2, 3, 3);
semilogy(0:length(rom_errors)-1, rom_errors, 'g^-', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('Iteration k'); ylabel('Absolute Error');
title('(c) Romberg');
grid on;

subplot(2, 3, 4);
semilogy(1:10, gl_errors_all, 'md-', 'LineWidth', 1.5, 'MarkerSize', 6);
xlabel('Node Count n'); ylabel('Absolute Error');
title('(d) Gauss-Legendre');
grid on;

subplot(2, 3, 5);
semilogy(0:length(trap_errors)-1, trap_errors, 'bo-', 'LineWidth', 1.5, 'MarkerSize', 5); hold on;
semilogy(0:length(simp_errors_list)-1, simp_errors_list, 'rs-', 'LineWidth', 1.5, 'MarkerSize', 5);
semilogy(0:length(rom_errors)-1, rom_errors, 'g^-', 'LineWidth', 1.5, 'MarkerSize', 5);
semilogy(1:10, gl_errors_all, 'md-', 'LineWidth', 1.5, 'MarkerSize', 5);
yline(epsilon, 'k--', 'LineWidth', 1.5);
xlabel('Step'); ylabel('Absolute Error');
title('(e) All Methods Comparison');
legend('Trapezoid', 'Simpson', 'Romberg', 'Gauss-L', '\epsilon', 'Location', 'southwest');
grid on;

subplot(2, 3, 6);
verify_vals = [I_trap_v, I_simp_v, I_rom_v, I_gl_v];
bar_colors = [0.2 0.4 0.8; 0.8 0.2 0.2; 0.2 0.7 0.3; 0.6 0.2 0.8];
bh = bar(verify_vals);
bh.FaceColor = 'flat';
for k = 1:4, bh.CData(k,:) = bar_colors(k,:); end
hold on;
yline(exact_verify, 'k--', 'LineWidth', 1.5);
set(gca, 'XTickLabel', {'Trap', 'Simp', 'Romberg', 'Gauss-L'});
ylabel('Value');
title('(f) Verify x^2');
grid on;

sgtitle('Fig1: Convergence Curves', 'FontSize', 14, 'FontWeight', 'bold');
saveas(gcf, 'fig1_convergence.png');

figure('Position', [100, 100, 800, 500]);
x_plot = linspace(a, b, 500);
y_plot = f(x_plot);
plot(x_plot, y_plot, 'b-', 'LineWidth', 2); hold on;
x_patch = [x_plot, fliplr(x_plot)];
y_patch = [y_plot, zeros(size(y_plot))];
patch(x_patch, y_patch, 'b', 'FaceAlpha', 0.15, 'EdgeColor', 'none');
xlabel('x'); ylabel('f(x) = cos(x)');
title('Fig2: Integrand cos(x) on [0, \pi/2]');
legend('cos(x)', 'Region', 'Location', 'northeast');
text(0.3, 0.3, 'I = 1', 'FontSize', 12, 'BackgroundColor', 'w');
grid on;
saveas(gcf, 'fig2_integrand.png');

fprintf('\nSaved: fig1_convergence.png, fig2_integrand.png\n');
