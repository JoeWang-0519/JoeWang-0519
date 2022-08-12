# Total cost per week
def TCPW(q, p, c, h, week):
    # initialization
    x_inv = q;  # inventory level
    x_dis = 0;  # remaining failure days
    T = 0;  # total cost
    PURCHASEPERMITTED = True;

    # update process
    for iter in range(week):
        if x_dis > 0:
            x_dis -= 1;
            PURCHASEPERMITTED = False;
        else:
            PURCHASEPERMITTED = True;

        if x_inv > 0:
            x_inv -= 1;
        else:
            T += p;

        if PURCHASEPERMITTED == True:
            u = random.uniform(0, 1);
            if u < 0.95:
                if x_inv <= q - 2:
                    x_inv += 2;
                    T += 2 * c;
                elif x_inv == q - 1:
                    x_inv += 1;
                    T += c;
            else:
                x_dis = 19;
        T += h * x_inv
    return T/week;