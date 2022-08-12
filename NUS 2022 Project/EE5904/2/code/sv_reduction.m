function k = sv_reduction(H, threshold, h_initial)
    singular_value = svd(H);
    summ = 0;
    total_sum = sum(singular_value);

    for i = 1 : h_initial
        if summ >= threshold*total_sum
            k=i;
            break;
        else
            summ = summ + singular_value(i);
        end
    end
end