import numpy
from pylab import *

w = 20
h = 20
map_grid = np.full((w, h), int(10), dtype=np.int8)
map_grid[3, 3:8] = 0
map_grid[3:10, 7] = 0
map_grid[10, 3:8] = 0
map_grid[17, 13:17] = 0
map_grid[10:17, 13] = 0
map_grid[10, 13:17] = 0
map_grid[5, 2] = 7
map_grid[15, 15] = 5
# print(map_grid)
# w = 6
# h = 6
# map_grid = [[1, 1, 1, 1, 1, 1],
#             [1, 1, 1, 1, 1, 1],
#             [1, 0, 0, 1, 1, 1],
#             [0, 0, 1, 1, 0, 0],
#             [1, 0, 0, 1, 1, 0],
#             [1, 1, 1, 1, 1, 1]]

# class Node(object):
#
#     def __init__(self, x, y, num):
#         self.x_ = x
#         self.y_ = y
#         self.num_ = num


class Lee(object):

    def __init__(self, start, goal):
        self.closed_0 = []
        self.closed_1 = []
        self.open_0 = [start]
        self.open_1 = [goal]
        self.path_0 = []
        self.path_1 = []

    def surround(self, node, open, closed, num):
        l = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in l:
            # closed.append(node)
            if node[0] + i[0] < 0 or node[1] + i[1] < 0 or node[0] + i[0] > w - 1 or node[1] + i[1] > w - 1:
                continue
            # if map_grid[int(node.x_ + i[0]), int(node.y_ + i[1])] == 0:  # 搜索到障碍物去掉
            #     continue
            if map_grid[node[0] + i[0]][node[1] + i[1]] == 0:  # 搜索到障碍物去掉
                continue
            for n in closed:
                if node[0] + i[0] == n[0] and node[1] + i[1] == n[1]:
                    break
            for m in open:
                if node[0] + i[0] == m[0] and node[1] + i[1] == m[1]:
                    break
            # if (node[0] + i[0], node[1] + i[1]) in closed:
            #     continue
            # if (node[0] + i[0], node[1] + i[1]) in open:
            #     continue
            else:
                open.append((node[0] + i[0], node[1] + i[1], num))

    def search(self):
        iter = 0
        while True:
            if iter == 3:
                iter = 0
            iter += 1
            open_0 = self.open_0       # 拷贝记录之前的open表
            self.closed_0 += open_0    # 更新closed表
            self.open_0 = []           # 清空open表
            for n in open_0:
                self.surround(n, self.open_0, self.closed_0, iter)
                for i in self.open_0:       # 两个open表触碰
                    for j in self.open_1:
                        if i[0] == j[0] and i[1] == j[1]:
                            # print(i)
                            return i
            print('0', self.open_0)
            open_1 = self.open_1       # 拷贝记录之前的open表
            self.closed_1 += open_1
            self.open_1 = []
            for n in open_1:
                self.surround(n, self.open_1, self.closed_1, iter)
                for i in self.open_1:  # 两个open表触碰
                    for j in self.open_0:
                        if i[0] == j[0] and i[1] == j[1]:
                            # print(i)
                            return i
            print('1', self.open_1)
            # print(self.closed_1)


    def path(self):
        meet_pin_0 = self.search()
        meet_pin_1 = meet_pin_0
        self.path_1.append(meet_pin_0)
        print(meet_pin_0)
        self.closed_0.reverse()
        self.closed_1.reverse()
        l = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        flag_0 = 1
        for i in self.closed_0:
            if flag_0:
                for d in l:
                    if meet_pin_0[0] + d[0] == i[0] and meet_pin_0[1] + d[1] == i[1]:
                        self.path_0.append(i)
                        meet_pin_0 = i
                        flag_0 = 0
                        print(i)
            else:
                for d in l:
                    if meet_pin_0[0] + d[0] == i[0] and meet_pin_0[1] + d[1] == i[1]:
                        if meet_pin_0[2] == 1 and i[2] == 3:
                            self.path_0.append(i)
                            meet_pin_0 = i
                        elif meet_pin_0[2] - 1 == i[2]:
                            self.path_0.append(i)
                            meet_pin_0 = i
        flag_1 = 1
        for i in self.closed_1:
            if flag_1:
                for d in l:
                    if meet_pin_1[0] + d[0] == i[0] and meet_pin_1[1] + d[1] == i[1]:
                        self.path_1.append(i)
                        meet_pin_1 = i
                        flag_1 = 0
                        print(i)
            else:
                for d in l:
                    if meet_pin_1[0] + d[0] == i[0] and meet_pin_1[1] + d[1] == i[1]:
                        if meet_pin_1[2] == 1 and i[2] == 3:
                            self.path_1.append(i)
                            meet_pin_1 = i
                        elif meet_pin_1[2] - 1 == i[2]:
                            self.path_1.append(i)
                            meet_pin_1 = i
        # print(self.path_0)
        # print(self.path_1)

    def draw_path(self):
        for i in self.closed_0:
            map_grid[int(i[0]), int(i[1])] = 8
        for i in self.closed_1:
            map_grid[int(i[0]), int(i[1])] = 2
        for i in self.path_0:
            map_grid[int(i[0]), int(i[1])] = 4
        for i in self.path_1:
            map_grid[int(i[0]), int(i[1])] = 4
        plt.imshow(map_grid, cmap=plt.cm.hot, interpolation='nearest', vmin=0, vmax=10)
        plt.colorbar()
        xlim(-1, 20)  # 设置x轴范围
        ylim(-1, 20)  # 设置y轴范围
        my_x_ticks = numpy.arange(0, 20, 1)
        my_y_ticks = numpy.arange(0, 20, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.grid(True)
        plt.show()


# start = (0, 0, 0)
# goal = (5, 5, 0)
start = (5, 2, 0)
goal = (15, 15, 0)

lee = Lee(start, goal)
lee.path()
lee.draw_path()



