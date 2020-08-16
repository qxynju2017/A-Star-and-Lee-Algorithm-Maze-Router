import numpy as np
from pylab import *


# 20×20的栅格地图
# 10表示可通行点
# 0表示障碍物

map = np.full((20, 20), int(10), dtype=np.int8)
# print(map)
# map[3, 3:8] = 0
map[3:10, 7] = 0
# map[10, 3:8] = 0
map[17, 13:17] = 0
map[10:17, 13] = 0
map[10, 13:17] = 0
map[5, 2] = 7
map[15, 15] = 5


class AStar(object):
    def __init__(self):
        self.f = 0
        self.g = 0
        self.last_point = np.array([])
        self.current_point = np.array([])
        self.open = np.array([[], []])
        self.closed = np.array([[], []])
        self.start = np.array([5, 2])
        self.goal = np.array([15, 15])

    def calc_h(self, cur_p):
        h = (cur_p[0] - 15) ** 2 + (cur_p[1] - 15) ** 2
        h = np.sqrt(h)
        return h

    def calc_g(self, chl_p, cu_p):
        g1 = cu_p[0] - chl_p[0]
        g2 = cu_p[1] - chl_p[1]
        g = g1 ** 2 + g2 ** 2
        g = np.sqrt(g)
        return g

    def calc_f(self, chl_p, cu_p):
        f = self.calc_g(chl_p, cu_p) + self.calc_h(cu_p)
        return f

    def min_f(self):
        tem_f = []
        for i in range(self.open.shape[1]):
            # 计算拓展节点的全局f值
            # f_value = self.calc_f(self.current_point, self.open[:, i]) + self.g
            f_value = self.calc_f(self.current_point, self.open[:, i])
            tem_f.append(f_value)
        index = tem_f.index(min(tem_f))  # 返回最小值索引
        location = self.open[:, index]  # 返回最小值坐标
        print(index, location)
        return index, location

    def child_point(self, x):
        for j in range(-1, 2):
            for q in range(-1, 2):
                if j == 0 and q == 0:  # 搜索到父节点去掉
                    continue
                if map[int(x[0] + j), int(x[1] + q)] == 0:  # 搜索到障碍物去掉
                    continue
                if x[0] + j < 0 or x[0] + j > 19 or x[1] + q < 0 or x[1] + q > 19:  # 搜索点出了边界去掉
                    continue
                # 在open表中，则去掉搜索点
                a = self.judge_location(x, j, q, self.open)
                if a == 1:
                    continue
                # 在closed表中,则去掉搜索点
                b = self.judge_location(x, j, q, self.closed)
                if b == 1:
                    continue

                m = np.array([x[0] + j, x[1] + q])
                self.open = np.c_[self.open, m]  # 搜索出的子节点加入open
                # print('打印第一次循环后的open：')
                # print(self.open)

    def judge_location(self, x, j, q, list_co):
        # jud = 0
        for i in range(list_co.shape[1]):
            if x[0] + j == list_co[0, i] and x[1] + q == list_co[1, i]:
                return True
                # jud = jud + 1
            # else:
            #     jud = jud
        # return jud

    def draw_path(self):
        for i in range(self.closed.shape[1]):
            x = self.closed[:, i]
            map[int(x[0]), int(x[1])] = 5

        plt.imshow(map, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        plt.colorbar()
        xlim(-1, 20)  # 设置x轴范围
        ylim(-1, 20)  # 设置y轴范围
        my_x_ticks = np.arange(0, 20, 1)
        my_y_ticks = np.arange(0, 20, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)
        plt.show()

    def main(self):
        self.open = np.c_[self.open, self.start]  # 起点放入open
        self.current_point = self.start  # 起点放入当前点，作为父节点
        # ite = 1
        while True:
            # open为空时无路径
            if self.open.shape[1] == 0:
                print('No Path!!')
                return
            last_point = self.current_point
            index, self.current_point = self.min_f()  # 判断open表中f值
            print(self.current_point)
            # 选取open表中最小f值的节点作为best，放入closed表
            self.closed = np.c_[self.closed, self.current_point]
            if self.current_point[0] == self.goal[0] and self.current_point[1] == self.goal[1]:
                print('Finished!!')
                # print(self.closed)
                return
            self.child_point(self.current_point)  # 生成子节点
            self.open = delete(self.open, index, axis=1)  # 删除open中最优点
            # self.g = self.g + self.calc_g(self.current_point, last_point)
            # print(self.g)

a1 = AStar()
a1.main()
a1.draw_path()
