function [I, max_depth_reached, history] = adaptive_simpson_main(f, a, b, epsilon, max_depth)
    history = [];
    max_depth_reached = 0;
    
    % Stack-based iterative implementation
    % Stack entries: [a, b, S_whole, eps, depth]
    stack = [a, b, 0, epsilon, 0];
    stack(1,3) = simpson_single(f, a, b);
    results = [];
    
    while ~isempty(stack)
        a_in = stack(end, 1);
        b_in = stack(end, 2);
        S_whole = stack(end, 3);
        eps = stack(end, 4);
        depth = stack(end, 5);
        stack(end, :) = [];
        
        h = (b_in - a_in) / 2;
        m = (a_in + b_in) / 2;
        S_left = simpson_single(f, a_in, m);
        S_right = simpson_single(f, m, b_in);
        S = S_left + S_right;
        
        if depth > max_depth_reached
            max_depth_reached = depth;
        end
        
        if depth >= max_depth || abs(S - S_whole) < 15 * eps
            result = S + (S - S_whole) / 15;
            results(end+1) = result; %#ok<AGROW>
        else
            stack(end+1, :) = [m, b_in, S_right, eps/2, depth+1]; %#ok<AGROW>
            stack(end+1, :) = [a_in, m, S_left, eps/2, depth+1]; %#ok<AGROW>
        end
    end
    
    I = sum(results);
    history = results;
end

function S = simpson_single(f, a, b)
    h = (b - a) / 2;
    m = (a + b) / 2;
    S = h / 3 * (f(a) + 4 * f(m) + f(b));
end
