function [I, iter, R] = romberg_quad(f, a, b, epsilon, max_iter)
    R = zeros(max_iter + 1, max_iter + 1);
    h = b - a;
    R(1, 1) = h / 2 * (f(a) + f(b));
    
    for k = 1:max_iter
        h = h / 2;
        s = 0;
        x = a + h;
        while x < b
            s = s + f(x);
            x = x + 2 * h;
        end
        R(k+1, 1) = R(k, 1) / 2 + h * s;
        
        for j = 1:k
            R(k+1, j+1) = R(k+1, j) + (R(k+1, j) - R(k, j)) / (4^j - 1);
        end
        
        if abs(R(k+1, k+1) - R(k, k)) < epsilon
            iter = k;
            I = R(k+1, k+1);
            R = R(1:k+1, 1:k+1);
            return;
        end
    end
    iter = max_iter;
    I = R(max_iter + 1, max_iter + 1);
end
