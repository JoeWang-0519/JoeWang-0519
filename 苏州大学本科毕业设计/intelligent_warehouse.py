import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy
from IPython import display

xm = 25
ym = 20
m = np.zeros((ym, xm), int)

#note shelf as 1 
for i in [3, 7, 11, 15]:
    for j in [4, 11, 18]:
        m[i:i + 2, j:j + 5] = 1
        
#note cargoin as 2, cargoout as 3
for i in [7, 14, 21]:
    m[0, i] = 2
    m[19, i] = 3

#note charging area as 4
m[3:18, 0:1] = 4

#note inshelf as 5
for i in [3, 7, 11, 15]:
    for j in [9, 16, 23]:
        m[i, j] = 5


def drawmap(m, carall):
    plt.figure(figsize=(12.5, 10))
    for i in range(-1,m.shape[0]):
        y = [i + 0.5]*5
        x = np.linspace(-0.5, m.shape[1] - 0.5, 5)
        plt.plot(x, y, 'lightsteelblue')
    for i in range(-1,m.shape[1]):
        x = [i + 0.5]*5
        y = np.linspace(-0.5, m.shape[0] - 0.5, 5)
        plt.plot(x, y, 'lightsteelblue')
    for i in range(m.shape[1]):
        for j in range(m.shape[0]):
            xt = np.linspace(i-0.5,i+0.5, 5)
            color = 'white'
            if m[j,i] == 1:
                color = 'k'
            elif m[j,i] == 2:
                color = 'darkorange'
            elif m[j,i] == 3:
                color = 'b'
            elif m[j,i] == 4:
                color = 'violet'
            elif m[j,i] == 5:
                color = 'yellow'
            plt.fill_between(xt, j-0.5, j+0.5, facecolor=color)     
    plt.xlim(-0.5, m.shape[1] - 0.5)
    plt.ylim(-0.5, m.shape[0] - 0.5)
    
    car_color = 'lawngreen'
    for car in carall:
        if car[2] < 30:
            car_color = 'r'
        elif car[8] == 1:
            car_color = 'k'
        plt.plot(car[0], car[1], 'o', markersize = 10, color = car_color)
    plt.axis('off')
    plt.savefig('Map')
        

        
def getmission(file):
    f = open(file)
    mission = f.read()
    mission = [int(i) for i in mission.split()]
    mission = [[mission[i], mission[i+1]] for i in range(0, len(mission), 2)]
    return mission


def purchase(s, mission):
    i = int(input("请输入进货拣货台编号（1-3）："))
    mission.insert(0, [i, s])
    return


def add_mission(shelf, mission):
    a = int(input("请输入添加的任务类型（0：入库，1：出库）"))
    if a not in [0,1]:
        return False
    if a == 0:
        b = int(input("请输入拣货台编号（1-3）："))
        c = int(input("请输入货架编号（1-12）："))
        mission.append([b, c])
        print("添加完成")
        shelf[c-1] += 1
    else:
        b = int(input("请输入拣货台编号（4-6）："))
        c = int(input("请输入货架编号（1-12）："))
        if shelf[c-1] != 0:
            mission.append([b, c])
            print("添加完成")
            shelf[c-1] -= 1
        else:
            print("库存不足")
            judge = int(input("是否需要进货（不需要：0，需要：1）："))
            if judge == 0:
                print("添加失败")
            else:
                mission.append([b, c])
                purchase(c, mission)
                print("添加完成")
            
    
    
def del_mission(mission):
    x = int(input("请输入要删除任务的拣货台编号："))
    y = int(input("请输入要删除任务的货架编号："))
    if [x, y] in mission:
        mission.remove([x, y])
        print("删除成功")
    else:
        print("任务不存在")
    

def appoint(mission, carall):
    car_id = -1
    min_dis = 99999
    start = [0, 0]
    end = [0, 0]
    if mission[0] <= 3:
        start[0] = 7*mission[0]
        start[1] = 0
        if mission[1] <= 3:
            end[0] = 7 * mission[1] + 2
            end[1] = 3
        elif mission[1] <= 6:
            end[0] = 7 * (mission[1] - 3) + 2
            end[1] = 7
        elif mission[1] <= 9:
            end[0] = 7 * (mission[1] - 6) + 2
            end[1] = 11
        elif mission[1] <= 12:
            end[0] = 7 * (mission[1] - 9) + 2
            end[1] = 15
    else:
        end[0] = 7*(mission[0] - 3)
        end[1] = 19
        if mission[1] <= 3:
            start[0] = 7 * mission[1] + 2
            start[1] = 3
        elif mission[1] <= 6:
            start[0] = 7 * (mission[1] - 3) + 2
            start[1] = 7
        elif mission[1] <= 9:
            start[0] = 7 * (mission[1] - 6) + 2
            start[1] = 11
        elif mission[1] <= 12:
            start[0] = 7 * (mission[1] - 9) + 2
            start[1] = 15
    for i in range(len(carall)):
        if carall[i][3] == 0 and carall[i][2] >= 30 and carall[i][10] == 0:
            
            dis = (carall[i][0]-start[0])**2 + (carall[i][1]-start[1])**2
            if dis < min_dis:
                min_dis = dis
                car_id = i
    if car_id != -1:
        carall[car_id][4], carall[car_id][5] = start[0], start[1]
        carall[car_id][6], carall[car_id][7] = end[0], end[1]
    return car_id


def charge(car, path, busy, carall):
    # 需要改
    car[10] = 1
    
    for i in range(14):
        if car[1] >= 17:
            if 17 - i not in busy:
                car[4], car[5] = 0, 17 - i
                car[6], car[7] = 0, 17 - i
                break
        elif car[1] <= 3:
            if 3 + i not in busy:
                car[4], car[5] = 0, 3 + i
                car[6], car[7] = 0, 3 + i
                break
        elif car[1] > 3 and car[1] < 17:
            if car[1] + i not in busy and car[1] + i <= 17:
                car[4], car[5] = 0, car[1] + i
                car[6], car[7] = 0, car[1] + i
                break
            elif car[1] - i not in busy and car[1] - i >= 3:
                car[4], car[5] = 0, car[1] - i
                car[6], car[7] = 0, car[1] - i
                break
    busy.append(car[5])
    findpath_ultimate(carall, car[11], path)
    

class ACO(object):
    def __init__(self, start, end, num_x, num_y, obstacle):
        self.ant = 50     # 蚁群规模
        self.alpha = 1  # 信息素因子
        self.beta = 3.    # 启发函数因子
        self.rho = 0.3    # 信息素挥发因子
        self.kesi = 0.2   # 启发函数初始强化因子
        
        
        self.Q = 5        # 信息素强度
        self.num_x = num_x    # 二维仓库横格点个数
        self.num_y = num_y    # 二维仓库竖格点个数
        self.obstacle = obstacle    # 障碍物tuple表
        
        
        
        # 在每次循环之后需要更新
        self.Table = np.zeros([self.ant, num_x * num_y, 2])   # 记录一次循环中蚂蚁的所有路径
        self.State = np.zeros([self.ant, 1])    # 记录一次循环中蚂蚁是否陷入死锁
        self.paths = None    # 记录一次循环中所有蚂蚁的路径长度
        self.Tau = np.ones([num_x, num_y])    # 信息素矩阵
        
        
        self.start = start    # 任务的开始位置  (list)
        self.end = end    # 任务的结束为止（目的地）
        
        
        # 可视化
        self.iter_x = []    # 记录循环次数（x axis）
        self.iter_y = []    # 记录每次循环中的最短路径 (y axis)
        
        self.iter_max = 100    # 总循环次数(所有蚂蚁走一次成为一个循环)
        
    
    # 生成下一步位置候选
    def init_Tau(self):
        a = self.start[0]
        b = self.start[1]
        x = self.end[0]
        y = self.end[1]
        k = a * (y-b) / (x-a) - b
        slash1 = (y - b) / ((x-a)*k)
        slash2 = - 1 / k
        # equation is: slash1 * i + slash2 * j = 1
        
    def next_candidate(self, current, tabu):
        set_tabu = set(tabu)
        all_candidate = []
        
        #设置单行道
        """
        #4方向
        direction = [[0,1],[0,-1],[1,0],[-1,0]]
        """
        #8方向
        direction = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                direction.append([i, j])
        direction.remove([0,0])
        
        if current[0] == 0:
            direction.remove([0, 1])
            direction.remove([0, -1])
        
        if current[0] in [1, 3, 10, 17, 24]:
            if [0,1] in direction:
                direction.remove([0, 1])
            if [1,1] in direction:
                direction.remove([1, 1])
            if [-1,1] in direction:
                direction.remove([-1, 1])
        if current[0] in [2, 9, 16, 23]:
            if [0,-1] in direction:
                direction.remove([0, -1])
            if [1,-1] in direction:
                direction.remove([1, -1])
            if [-1,-1] in direction:
                direction.remove([-1, -1])
        if current[1] in [6, 10, 14] and 3 <= current[0] <= 23:
            if [-1,0] in direction:
                direction.remove([-1, 0])
            if [-1,1] in direction:
                direction.remove([-1, 1])
            if [-1,-1] in direction:
                direction.remove([-1, -1])
        if current[1] in [0, 2, 18]:
            if [-1,0] in direction:
                direction.remove([-1, 0])
            if [-1,1] in direction:
                direction.remove([-1, 1])
            if [-1,-1] in direction:
                direction.remove([-1, -1])
        if current[1] in [5, 9, 13, 17] and 3 <= current[0] <= 23:
            if [1,0] in direction:
                direction.remove([1, 0])
            if [1,1] in direction:
                direction.remove([1, 1])
            if [1,-1] in direction:
                direction.remove([1, -1])
        if current[1] in [1, 19]:
            if [1,0] in direction:
                direction.remove([1, 0])
            if [1,1] in direction:
                direction.remove([1, 1])
            if [1,-1] in direction:
                direction.remove([1, -1])
       
        
                
                
        for pertube in direction:
            pertube_x, pertube_y = pertube[0], pertube[1]
            current_x, current_y = current[0], current[1]
            if 0 <= current_x + pertube_x <= self.num_x - 1 and 0 <= current_y + pertube_y <= self.num_y - 1:
                all_candidate.append((current_x + pertube_x, current_y + pertube_y))
        set_all_candidate = set(all_candidate)
        
        return list(set_all_candidate - set_tabu)
        
    
    # 轮盘赌选择
    def rand_choose(self, p, candidate):
        # 返回值: tuple
        x = np.random.rand()
        for i in range(len(p)):
            x -= p[i]
            if x <= 0:
                break
        return candidate[i]
    
    # 生成蚁群
    def get_ants(self, start, end, obstacle, cnt):
        self.Table[:, 0, :2] = start
  
        for i in range(self.ant):
            # 初始化禁忌表
            tabu = copy.deepcopy(obstacle)
            current = start
            j = 1
            while current != end:
                P = []
                next_cand = self.next_candidate(current, tabu)    # a list whose element is tuple [(1,1),(1,2)]
                
                if len(next_cand) == 0:
                    self.State[i, 0] = 1    # 表示该蚂蚁陷入死锁
                    break
                else:
                    # 通过信息素计算转移概率
                    for cand in next_cand:
                        '''
                        # 启发式函数eta (加快速度)， 可改
                        if cand[0] != current[0] and cand[1] != current[1]:
                            Eta = 1 / math.sqrt(2)
                        else:
                            Eta = 1
                        
                        '''
                        
                        distance = math.sqrt((cand[0] - end[0])**2 + (cand[1] - end[1])**2)

                        if distance == 0:
                            Eta = 1000
                        else:    
                            Eta = 1 / distance * (1 - self.kesi) / self.kesi * (self.iter_max - cnt) / self.iter_max
                        
                        P.append(self.Tau[cand] ** self.alpha * Eta ** self.beta)

                    P_sum = sum(P)
                    P = [x / P_sum for x in P]
                    # 轮盘赌选择一个位置
                    next_loc = list(self.rand_choose(P, next_cand))
                    self.Table[i, j, :] = next_loc 
                    
                    # 更新tabu表
                    tabu.append(tuple(current))
                    current = next_loc
                    j += 1                
            self.Table[i, j, :] = [math.inf, math.inf]    # 停止记号
    # 计算一条路径的长度
    def compute_pathlen(self, path):
        # path例子: [[0,0],[0,1],[1,2],...] k*2 numpy
        result = 0
        [path_len, tmp] = path.shape
        for i in range(path_len - 1):
            head = path[i]
            tail = path[i + 1]
            if tail[0] == math.inf:
                break
            else:
                result += np.linalg.norm(head - tail)
        return result
 
    # 计算一次循环中所有蚂蚁路径的长度
    def compute_paths(self, paths):
        # paths例子: self.Table a*b*2 numpy
        result = []
        for idx in range(self.ant):
            if self.State[idx, 0] == 1:
                # 死锁蚂蚁
                result.append(math.inf)
            else:
                # 到达终点蚂蚁
                path_len = self.compute_pathlen(paths[idx])
                result.append(path_len)
        return np.array(result)

    # 更新信息素
    def update_Tau(self):
        delta_tau = np.zeros([self.num_x, self.num_y])
        paths = self.compute_paths(self.Table)    # numpy
        
        # 采用只对部分好的路径更新信息素的策略
        paths_noinf = paths[paths != math.inf]
        paths_median = np.median(paths_noinf)
        for i in range(self.ant):
            if paths[i] < paths_median:
                # 判断是否陷入死锁并且路径是否太差，若是，不参与信息素更新
                # 第i只蚂蚁的完整路径route
                route = self.Table[i]
                [route_len, tmp] = route.shape
                for j in range(route_len):
                    loc = route[j]
                    if loc[0] == math.inf:
                        # 检查路径是否到达终点
                        break
                    else:
                        x = int(loc[0])
                        y = int(loc[1])
                        delta_tau[x,y] = delta_tau[x,y] + self.Q / paths[i]

        self.Tau = (1 - self.rho) * self.Tau + delta_tau

        
    # 更新系统中记录路径Table以及记录状态State
    def update_Record(self):
        self.Table = np.zeros([self.ant, self.num_x * self.num_y, 2])   # 记录一次循环中蚂蚁的所有路径
        self.State = np.zeros([self.ant, 1])    # 记录一次循环中蚂蚁是否陷入死锁
        self.paths = None    # 记录一次循环中所有蚂蚁的路径长度
    
    
    
    def aco(self):
        best_lenth = math.inf           # math.inf返回浮点正无穷大
        best_path = None
        for cnt in range(self.iter_max):
            # 生成新的蚁群
            self.get_ants(self.start, self.end, self.obstacle, cnt)  # out >> self.Table
            self.paths = self.compute_paths(self.Table)
            
            # 取该蚁群的最优解
            tmp_lenth = self.paths.min()
            tmp_idx = self.paths.argmin()
            tmp_path = self.Table[tmp_idx]
            
            # 可视化初始的路径
            #if cnt == 0:
            #    init_show = self.location[tmp_path]
            #    init_show = np.vstack([init_show, init_show[0]])
            
            # 更新最优解
            if tmp_lenth < best_lenth:
                best_lenth = tmp_lenth
                best_path = tmp_path
            
            #更新信息素
            self.update_Tau()
            
            #更新记录信息
            if cnt < self.iter_max - 1:
                self.update_Record()
 
            # 保存结果
            self.iter_x.append(cnt)
            self.iter_y.append(best_lenth)
            # print(cnt, best_lenth)
        return best_lenth, best_path
    
    def run(self):
        best_length, best_path = self.aco()
        return best_path, best_length

    

def create_obstacle(map):
    Obstacle = []
    # Generate the Obstacle Table
    for i in range(xm):
        for j in range(ym):
            if map[j,i] == 1:
                Obstacle.append((i,j))
    return Obstacle


def findpath(car):
    curr = car[0:2]
    start = car[4:6]
    end = car[6:8]
    obstacle = create_obstacle(m)
    aco = ACO(curr, start, xm, ym, obstacle)
    path_cs, Best_length = aco.run()
    for i in range(len(path_cs)):
        if path_cs[i, 0] == math.inf:
            e = i
            break
    path_cs = path_cs[:e].tolist()
    
    aco = ACO(start, end, xm, ym, obstacle)
    path_se, Best_length = aco.run()
    for i in range(len(path_se)):
        if path_se[i, 0] == math.inf:
            e = i
            break
    path_se = path_se[:e].tolist()
    return path_cs + path_se

def findpath_nopush(car, add_obstacle):
    # add_obstacle is the intersaction with the current route -> [(1,2),(3,4)] 
    curr = car[0:2]
    start = car[4:6]
    end = car[6:8]
    
    obstacle = create_obstacle(m)
    obstacle_new = obstacle + add_obstacle
    
    aco = ACO(curr, start, xm, ym, obstacle_new)
    path_cs, Best_length = aco.run()
    for i in range(len(path_cs)):
        if path_cs[i, 0] == math.inf:
            e = i
            break
    path_cs = path_cs[:e].tolist()
    
    aco = ACO(start, end, xm, ym, obstacle_new)
    path_se, Best_length = aco.run()
    for i in range(len(path_se)):
        if path_se[i, 0] == math.inf:
            e = i
            break
    path_se = path_se[:e].tolist()
    return path_cs + path_se
"""
def findpath_ultimate(carall, i, path):
    # first try
    candidate_path = findpath(carall[i])
    # 储存除此之外的已有path
    path_else = []
    
    tmp = [[] for i in range(len(carall))]
    for j in range(i):
        tmp[j] = [[carall[j][0], carall[j][1]]] + path[j]
    for j in range(i, len(carall)):
        tmp[j] = copy.deepcopy(path[j])
        
    for idx in range(len(carall)):
        if idx != i:
            path_else.append(tmp[idx])
            
            
    max_len_else = max([len(i) for i in path_else])
            
    if max_len_else == 0:
        path[i] = candidate_path
        print('no')
        print(path)
    else:
        count = 0
        add_obstacle = []
        while count <= 10: 
            print(count)
            cur_add_obstacle = []
            len_cur = len(candidate_path)
            judge_idx = min([max_len_else, len_cur])
            # 碰撞是否为终点
            flag = 0
            
            # 记录所有碰撞点
            for judge in range(judge_idx):
                # time judge的所有已经预约的点
                block = [a[judge] for a in path_else if len(a) >= judge + 1]
                if candidate_path[judge] in block:
                    # 包括终点
                    if candidate_path[judge] in [[7, 0], [14, 0], [21, 0], [7, 19], [14, 19], [21, 19], [9, 3], [9, 7], [9,11], [9, 15], [16, 3], [16, 7], [16,11], [16, 15], [23, 3], [23, 7], [23,11], [23, 15]]:
                        # 平移
                        candidate_path = [candidate_path[0]] + candidate_path
                        
                        #add_obstacle.append(tuple(candidate_path[judge]))
                        cur_add_obstacle.append(tuple(candidate_path[judge]))
                        flag = 1
                        print('hit at the end, so we wait')
                        print(candidate_path)
                    # 不包括终点
                    else:
                        add_obstacle.append(tuple(candidate_path[judge]))
                        cur_add_obstacle.append(tuple(candidate_path[judge]))
            
            
            if len(cur_add_obstacle) == 0:
                path[i] = candidate_path
                break
                
            elif flag == 0:
                candidate_path = findpath_nopush(carall[i], add_obstacle)
                
            count += 1
            
        if count == 10:
            path[i] = candidate_path
"""
def findpath_ultimate(carall, i, path):
    # first try
    # list
    candidate_path = findpath(carall[i])
    
    start_state = (carall[i][4], carall[i][5])
    end_state = (carall[i][6], carall[i][7])
    
    # 储存除此之外的已有path
    path_else = []
    
    tmp = [[] for i in range(len(carall))]
    for j in range(i):
        if path[j] != []:
            tmp[j] = [[carall[j][0], carall[j][1]]] + path[j] + [path[j][-1]] + [path[j][-1]]
    for j in range(i, len(carall)):
        tmp[j] = copy.deepcopy(path[j])
        if path[j] != []:
            tmp[j] = tmp[j] + [path[j][-1]] + [path[j][-1]]
        
    for idx in range(len(carall)):
        if idx != i:
            path_else.append(tmp[idx])
            
    max_len_else = max([len(i) for i in path_else])
            
    if max_len_else == 0:
        path[i] = candidate_path
        print('Other cars are all idle')
        # print(path)
    else:
        count = 1
        add_obstacle = []
        while count <= 30: 
            print("Try", count)
            cur_add_obstacle = []
            len_cur = len(candidate_path)
            judge_idx = min([max_len_else, len_cur])
            # 碰撞是否为终点
            flag = 0
            
            # 记录所有碰撞点 
            # cur_add -> 当前循环中candidate_path的碰撞点
            # add -> 所有碰撞点
            for judge in range(judge_idx):
                # (time) judge的所有已经预约的点
                block = [a[judge] for a in path_else if len(a) >= judge + 1]
                if candidate_path[judge] in block:
                    cur_add_obstacle.append(tuple(candidate_path[judge]))
                    add_obstacle.append(tuple(candidate_path[judge]))
                    # 判断要wait的标志
                    if (candidate_path[judge] in [list(start_state), list(end_state)]) and (candidate_path[judge] in [[7, 0], [14, 0], [21, 0], [7, 19], [14, 19], [21, 19], [9, 3], [9, 7], [9,11], [9, 15], [16, 3], [16, 7], [16,11], [16, 15], [23, 3], [23, 7], [23,11], [23, 15]]):
                        flag = 1
            
            # 无碰撞
            if len(cur_add_obstacle) == 0:
                path[i] = candidate_path
                print("No crash!")
                break
            cur = (carall[i][0], carall[i][1])
            
            while start_state in add_obstacle:
                add_obstacle.remove(start_state)
            while end_state in add_obstacle:
                add_obstacle.remove(end_state)
            
            #while cur in add_obstacle:
             #   add_obstacle.remove(cur)
            # flag=1表示生成的路径在终点处会出现碰撞
            if flag == 1:
                # 保证add_obstacle里没有终点，不会死循环
                while start_state in add_obstacle:
                    add_obstacle.remove(start_state)
                while end_state in add_obstacle:
                    add_obstacle.remove(end_state)
                    
                candidate_path = [candidate_path[0]] + candidate_path
                print("The end node is blocked!! Wait!!")
            else:
                candidate_path = findpath_nopush(carall[i], add_obstacle)
                print("The intermdeidate node is blocked!! Try another one!!")
            
            count += 1
            print(add_obstacle)
            print(carall[i])
            print(cur_add_obstacle)
        if count == 30:
            path[i] = candidate_path            
            
            

def animation(m, record, ar, cr, t):
    #plt.figure(figsize=(12.5, 10))
    for i in range(m.shape[0]):
        y = [i + 0.5]*5
        x = np.linspace(-0.5, m.shape[1] - 0.5, 5)
        plt.plot(x, y, 'lightsteelblue')
    for i in range(m.shape[1]):
        x = [i + 0.5]*5
        y = np.linspace(-0.5, m.shape[0] - 0.5, 5)
        plt.plot(x, y, 'lightsteelblue')
    for i in range(m.shape[1]):
        for j in range(m.shape[0]):
            xt = np.linspace(i-0.5,i+0.5, 5)
            color = 'white'
            if m[j,i] == 1:
                color = 'k'
            elif m[j,i] == 2:
                color = 'darkorange'
            elif m[j,i] == 3:
                color = 'b'
            elif m[j,i] == 4:
                color = 'violet'
            elif m[j,i] == 5:
                color = 'yellow'
            plt.fill_between(xt, j-0.5, j+0.5, facecolor=color)     
    plt.xlim(-0.5, m.shape[1] - 0.5 + 7)
    plt.ylim(-0.5, m.shape[0] - 0.5)
    
    
    for i in range(len(record)):
        car_color = 'lawngreen'
        if record[i][t][3] == 1:
            car_color = 'k'
        elif record[i][t][2] < 30 and record[i][t][4] != 0:
            car_color = 'r'
        elif record[i][t][2] >= 30 and record[i][t][2] < 100 and record[i][t][4] == 2:
            car_color = 'gold'
        plt.plot(record[i][t][0], record[i][t][1], 'o', markersize = 10, color = car_color)
    plt.text(25, 19, "Mission Appointment:"+str(ar[t]))
    plt.text(25, 18, "Mission Complete:"+str(cr[t]))
    
    plt.text(25, 17, "Car"+str(1)+":("+str(int(record[0][t][0]))+","+str(int(record[0][t][1]))+");battery:"+str(record[0][t][2]))
    plt.text(25, 16, "Car"+str(2)+":("+str(int(record[1][t][0]))+","+str(int(record[1][t][1]))+");battery:"+str(record[1][t][2]))
    plt.text(25, 15, "Car"+str(3)+":("+str(int(record[2][t][0]))+","+str(int(record[2][t][1]))+");battery:"+str(record[2][t][2]))
    plt.text(25, 14, "Car"+str(4)+":("+str(int(record[3][t][0]))+","+str(int(record[3][t][1]))+");battery:"+str(record[3][t][2]))
    plt.text(25, 13, "Car"+str(5)+":("+str(int(record[4][t][0]))+","+str(int(record[4][t][1]))+");battery:"+str(record[4][t][2]))
    plt.text(25, 12, "Car"+str(6)+":("+str(int(record[5][t][0]))+","+str(int(record[5][t][1]))+");battery:"+str(record[5][t][2]))
    plt.text(25, 11, "Car"+str(7)+":("+str(int(record[6][t][0]))+","+str(int(record[6][t][1]))+");battery:"+str(record[6][t][2]))
    plt.text(25, 10, "Car"+str(8)+":("+str(int(record[7][t][0]))+","+str(int(record[7][t][1]))+");battery:"+str(record[7][t][2]))
    #text = "car "str(1) +":"+ +str(record[0][t][0])+","+str(record[0][t][1])+";battery：" +str(record[0][t][2]) 
    #plt.text(25, 17 - i,"car "str(1) +":"+ +str(record[0][t][0])+","+str(record[0][t][1])+";battery：" +str(record[0][t][2]))
    """
    for k in range(8):
        text = "car "str(k+1) +":"+ +str(record[k][t][0])+","+str(record[k][t][1])+";battery：" +str(record[k][t][2]) 
        plt.text(25, 17 - i,text)
     """
    display.clear_output(wait=True)
    plt.pause(0.1)
    
    
def writerecord(record, file = "record.txt"):
    f = open(file,"w")
    
    for r in record:
        for i in r:
            i = str(i).strip('[').strip(']').replace(',','').replace('\'','')+'\n'
            f.write(i)

def writear_cr(r, file):
    f = open(file,"w")
    for i in r:
        i = str(i) + '\n'
        f.write(i)

def getrecord(file = "record.txt"):
    f = open(file)
    record = [float(i) for i in f.read().split()]
    record = [[record[i], record[i+1], record[i+2], record[i+3], record[i+4]] for i in range(0,len(record) - 4,5)]
    t = int(len(record)/8)
    ans = [[],[],[],[],[],[],[],[]]
    for i in range(8):
        ans[i] = [record[j] for j in range(i*t,(i+1)*t)]
    return ans


def getr(file):
    f = open(file)
    record = [int(i) for i in f.read().split()]
    return record