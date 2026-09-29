function [I, iter, history] = varstep_trapezoid(f, a, b, epsilon, max_iter)
    h = b - a;
    T_prev = h / 2 * (f(a) + f(b));
    history = T_prev;
    
    for k = 1:max_iter
        h = h / 2;
        s = 0;
        x = a + h;
        while x < b
            s = s + f(x);
            x = x + 2 * h;
        end
        T_curr = T_prev / 2 + h * s;
        history(end+1) = T_curr;
        
        if abs(T_curr - T_prev) < epsilon
            iter = k;
            I = T_curr;
            return;
        end
        T_prev = T_curr;
    end
    iter = max_iter;
    I = T_prev;
end
