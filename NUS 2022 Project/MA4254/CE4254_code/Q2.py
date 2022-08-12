import numpy as np
import random
import math
import matplotlib.pyplot as plt
import copy
# Aim: construct the stimulate annealing algorithm for TSP

#(a) Distance function
def TotalDist(tourlist, distance):
    '''
    :param tourlist: n-dimensional list(permutation of [1,2,...,n])
    :param distance: n*n list
    :return: totaldist
    '''
    totaldist = 0
    for start, end in zip(tourlist[:-1], tourlist[1:]):
        totaldist += distance[start-1][end-1]

    totaldist += distance[tourlist[-1]-1][tourlist[0]-1]
    return totaldist

#(b) Candidate-created function
def Create_candidatetour1(currenttour):
    '''
    :param currenttour:
    :return: candidate tour
    '''
    # choose the position of the elements which need to change
    i,j = random.sample(currenttour, 2)
    temp=currenttour[i-1:j]
    currenttour[i-1:j] = temp[::-1]
    return currenttour

def Create_candidatetour2(currenttour):
    '''
    :param currenttour:
    :return: candidate tour
    '''
    # choose the position of the elements which need to change
    i,j = random.sample(currenttour, 2)
    currenttour[i-1], currenttour[j-1] = currenttour[j-1], currenttour[i-1]
    return currenttour

def Create_candidatetour3(currenttour):
    '''
    :param currenttour:
    :return: candidate tour
    '''
    # choose the position of the elements which need to change
    i,j = random.sample(currenttour, 2)
    currenttour.insert(i-1, currenttour[j-1])
    if i > j:
        del currenttour[j-1]
    else:
        del currenttour[j]
    return currenttour

def Create_candidatetour4(currenttour):
    u = np.random.rand()
    if 0 <= u < 1 / 3:
        return Create_candidatetour1(currenttour)
    elif 1 / 3 <= u < 2 / 3:
        return Create_candidatetour2(currenttour)
    else:
        return Create_candidatetour3(currenttour)



def SA(N, distance, eta, N_iteration, T, Improvement = True, Method=1, Augument=False):
    '''
    :param N: number of city
    :param distance: N*N matrix of distance between two cities
    :param eta: speed of temperature decresing
    :param N_iteration: the maximum iteration
    :param T: temperature parameter
    :return: the solution of TSP(tourlist)
    '''
    #initialization(By randomly choosing a sequence)
    tourlist = random.sample(list(range(1,N+1)),N)
    opt_tourlist = tourlist[:]
    opt_len = TotalDist(opt_tourlist,distance)

    # record all the candidate distance
    all_opt = []
    all_len = []

    for k in range(N_iteration):
        len = TotalDist(tourlist, distance)
        temple_path= copy.deepcopy(tourlist)
        #choose candidate
        if Method == 1:
            tourlist_candidate = Create_candidatetour1(tourlist)
        elif Method == 2:
            tourlist_candidate = Create_candidatetour2(tourlist)
        elif Method == 3:
            tourlist_candidate = Create_candidatetour3(tourlist)
        else:
            tourlist_candidate = Create_candidatetour4(tourlist)

        len_candidate = TotalDist(tourlist_candidate, distance)

        # if decrease, update; if not decrease, update with probability p
        if not Augument:
            if len_candidate < len:
                tourlist = tourlist_candidate[:]
            elif math.exp(-(len_candidate - len) / T) >= np.random.rand():
                tourlist = tourlist_candidate[:]
            else:
                tourlist = temple_path
        else:
            if k<=10000:
                if len_candidate < len:
                    tourlist = tourlist_candidate[:]
                elif math.exp(-(len_candidate - len) / T) >= np.random.rand():
                    tourlist = tourlist_candidate[:]
                else:
                    tourlist = temple_path
            else:
                if len_candidate < len:
                    tourlist = tourlist_candidate[:]
                else:
                    tourlist=temple_path

        # additional part
        if Improvement == True:
            if TotalDist(tourlist, distance) < opt_len:
                opt_tourlist = tourlist[:]
                opt_len = TotalDist(tourlist, distance)

        T = T * eta

        all_opt.append(opt_len)
        all_len.append(TotalDist(tourlist, distance))

    if Improvement == True:
        print(opt_len)
        print(opt_tourlist)
        return opt_tourlist, all_opt, all_len, opt_len
    else:
        print(len)
        print(tourlist)
        return tourlist, all_opt, all_len,len

def SA_modify(N, distance, eta, N_iteration, T, tourlist):
    # initialization(By randomly choosing a sequence)
    #tourlist = random.sample(list(range(1, N + 1)), N)
    all_opt=[]
    temp_path=[]
    temp_len = 0
    for out_iter in range(N_iteration):

        for in_iter in range(N):
            temple_path=copy.deepcopy(tourlist)
            len = TotalDist(tourlist, distance)

            tourlist_candidate = Create_candidatetour4(tourlist)
            len_candidate = TotalDist(tourlist_candidate, distance)

            if len_candidate < len:
                tourlist = tourlist_candidate[:]
                #print('good')
            elif math.exp(-(len_candidate - len) / T) >= np.random.rand():
                tourlist = tourlist_candidate[:]
                #print('yes')
            else:
                tourlist = temple_path
                #print('no')


            if in_iter == N-1:
                temp_len = TotalDist(tourlist,distance)
                temp_path = tourlist

        all_opt.append(temp_len)
        print(out_iter)
        T=T*eta
    print(temp_len)
    print(temp_path)
    return temp_path, all_opt

def initial_temp(N, distance, eta):
    dist_list=[]
    temp=list(range(1,N+1))
    for _ in range(30):
        temp = random.sample(temp,N)
        dist = TotalDist(temp, distance)
        dist_list.append(dist)

    t0=-(max(dist_list)-min(dist_list))/math.log(eta)
    return t0
def plot_scatter(x_city, y_city):
    plt.scatter(x_city, y_city)
    return 0

def plot_route(N,x_city, y_city, sol, color='b'):
    x_modify = np.zeros(N + 1)
    y_modify = np.zeros(N + 1)
    for i in range(N):
        x_modify[i] = x_city[sol[i] - 1]
        y_modify[i] = y_city[sol[i] - 1]

    x_modify[N] = x_modify[0]
    y_modify[N] = y_modify[0]
    plt.plot(x_modify, y_modify,color=color)
    return 0

def plot_iter(iter, all_dist):
    plt.plot(range(iter), all_dist)
    return 0








