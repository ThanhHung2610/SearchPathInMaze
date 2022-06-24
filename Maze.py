import os
import matplotlib.pyplot as plt

#quy ước mỗi bước đi không có điểm thưởng có giá trị là 1
CostI = 1

#hàm trả về giá trị điểm thưởng
def bonusPoint(bonus, cur):
    for _, point in enumerate(bonus):
      if (cur[0] == point[0] and cur[1] == point[1]):
          return point[2]
    return 0

def visualize_maze(matrix, bonus, start, end, route=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v')
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^')    
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)
    cost = -1
    if route:
        for ri in route:
            cost += CostI + bonusPoint(bonus, ri)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    print('Cost: ', cost)
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix

#hàm Depth First Search 
def DFS(start,end,matrix,route):
    #cập nhật điểm vào route
    route.append(start)
    if (start == end):
        return True
    #ma trận hướng đi (theo thứ tự lên, trái, xuống, phải)
    row = [-1,0,1,0]
    col = [0,-1,0,1]
    #duyệt các điểm tiếp theo theo thứ tự trên
    for i in range(4):
        next_row = start[0]+row[i]
        next_col = start[1]+col[i]
        next = (next_row,next_col)
        
        #nếu điểm tiếp theo nằm trong route thì bỏ qua điểm này
        if (next_row,next_col) in route: 
            continue
        #nếu điểm tiếp theo là đi được thì cập nhật
        if matrix[next_row][next_col] != 'x':
            if DFS(next,end,matrix,route):
                return True
            #nếu là đường cụt thì đi lui
            route.pop()
    return False

def BFS(start,end,matrix):
    # thứ tự duyệt lên, phải, xuống, trái)
    row = [-1,0,1,0]
    col = [0,1,0,-1]
    #route để lưu đường đi đến đích
    route =  []
    #hàng đợi các điểm biên
    queue = []
    #cùng index trong 2 mảng prev và ele thì prev[i] là điểm phía trước ele[i] trên đường đi
    #ele là mảng chứa các điểm được duyệt
    ele = []
    prev = [] 

    queue.append(start)
    
    while (len(queue) > 0):
        #cur là điểm đang xét
        cur = queue.pop(0)
        if (cur == end):
            route.append(cur)
            temp = cur
            #đệ qui tìm đường đi
            while(1):
                #lấy index để truy cập phần tử trước đó
                ind = ele.index(temp)
                temp = prev[ind]
                #cập nhật đường đi lui
                route.append(temp)
                if (temp == start):
                    break
            #lúc hồi quy tìm đường đi thì lúc này route lưu từ đích đến điểm bắt đầu nên cần đảo chiều list route lại
            route.reverse()
            return route

        
        #duyệt các điểm tiếp theo theo thứ tự trên
        for i in range(4):
            next_row = cur[0]+row[i]
            next_col = cur[1]+col[i]
            next = (next_row,next_col)
            #nếu điểm tiếp theo chưa duyệt thì thêm vào queue, và cập nhật điểm trước của nó (để hồi quy)
            if next not in queue and next not in route and matrix[next_row][next_col] != 'x': 
                ele.append(next)
                prev.append(cur)
                queue.append(next)

import math
#hàm heuristic1 là khoảng cách euclid từ điểm được xét đến điểm đích
def heuristic1(cur,end):
    return math.sqrt((cur[0]-end[0])**2 + (cur[1]-end[1])**2)

#thuật toán tham lam
def GBFS(start,end,matrix):
    
    #route để lưu đường đi đến đích
    route =  []
    #mảng chứa heutistic của các điểm tiếp theo, nếu là tường hoặc đã duyệt thì H[i] = 1000 
    # 1000 là giá trị mặc định (không ảnh hưởng tới việc tìm heuristic nhỏ nhất)
    H = [1000,1000,1000,1000]
    #cùng index trong 2 mảng prev và ele thì prev[i] là điểm phía trước ele[i] trên đường đi
    #ele là mảng chứa các điểm được duyệt
    prev = [] 
    ele = []
    #cùng index trong 2 mảng OpenH và queue thì OpenH[i] là giá trị heuristic của queue[i]
    #hàng đợi ưu tiên các điểm biên
    Priority_queue = [start]
    #mảng chứa giá trị heuristic các điểm nằm trong Priority_queue với index tương ứng
    OpenH = [0] 
    #ma trận hướng đi (theo thứ tự lên,trái,xuống,phải)
    row = [-1,0,1,0]
    col = [0,-1,0,1]
    while (len(Priority_queue) > 0):
        #pop điểm có heuritic thấp nhất
        #tìm heuristic thấp nhất trong queue
        IndexMin = 0
        for i in range(len(OpenH)):
            if OpenH[IndexMin] > OpenH[i]:
                IndexMin = i
        #pop điểm có heuristic thấp nhất trong queue
        cur = Priority_queue.pop(IndexMin)
        OpenH.pop(IndexMin)

        #nếu đến đích thì kết thúc
        if (cur == end):
            route.append(cur)
            temp = cur
            #đệ qui tìm đường đi
            while(1):
                #lấy index để truy cập phần tử trước đó
                ind = ele.index(temp)
                temp = prev[ind]
                #cập nhật đường đi lui
                route.append(temp)
                if temp == start:
                    break
            #lúc hồi quy tìm đường đi thì lúc này route lưu từ đích đến điểm bắt đầu nên cần đảo chiều list route lại
            route.reverse()
            return route
        #duyệt từng điểm tiếp theo
        for i in range(4):
            next_row = cur[0]+row[i]
            next_col = cur[1]+col[i]
            next = (next_row,next_col)

            #nếu là tường thì cập nhật lại H[i] = 1000 (1000 là giá trị mặc định để không ảnh hưởng tới việc so sánh tìm điểm có heuristic nhỏ nhất)
            if matrix[next_row][next_col] == 'x': 
                H[i] = 1000
                continue
    
            #nếu điểm tiếp theo chưa được duyệt thì đưa vào danh sách open
            if next not in Priority_queue and next not in ele and matrix[next_row][next_col] != 'x':
                #thực hiện hàm heuristic
                H[i] = heuristic1(next,end)
                #cập nhập heuristic của điểm được thêm vào danh sách open và điểm trước đó của điểm này (để hồi quy)
                Priority_queue.append(next)
                OpenH.append(H)
                ele.append(next)
                prev.append(cur)

def Astar(start,end,matrix, bonus_points):
    #route để lưu đường đi đến đích
    route =  []
    #hàm đánh giá f
    f = [1000,1000,1000,1000]
    #cùng index trong 2 mảng prev và ele thì prev[i] là điểm phía trước ele[i] trên đường đi
    #ele là mảng chứa các điểm được duyệt
    prev = [] 
    ele = []
    #cùng index trong 2 mảng OpenH và queue thì OpenH[i] là giá trị heuristic của queue[i]
    #hàng đợi ưu tiên các điểm biên
    Priority_queue = [start]
    #mảng chứa giá trị heuristic các điểm nằm trong Priority_queue với index tương ứng
    Openf = [0]
    #mảng chứa chi phí của các điểm nằm trong Priority_queue với index tương ứng
    Cost = [0]
    #lưu điểm thưởng trên đường đi
    
    prevBonusPoint = [] #mảng lưu các điểm trước điểm thưởng trong BPinPath
    BPinPath = []       #mảng lưu các điểm thưởng mà tác nhân gặp trên đường tìm đường đi
    #ma trận hướng đi (theo thứ tự lên,trái,xuống,phải)
    row = [-1,0,1,0]
    col = [0,-1,0,1]
    while (len(Priority_queue) > 0):
        #pop điểm có heuritic thấp nhất
        #tìm index của điểm có giá trị f(n) thấp nhất trong queue
        IndexMin = 0
        for i in range(len(Openf)):
            if Openf[IndexMin] > Openf[i]:
                IndexMin = i
        
        #pop điểm đã tìm được ra khỏi queue
        cur = Priority_queue.pop(IndexMin)
        Openf.pop(IndexMin)
        #lấy chi phí của điểm trên để cập nhật giá trị f(n) cho cái điểm tiếp theo
        CostOfCur = Cost.pop(IndexMin)

        #nếu đến đích thì kết thúc
        if (cur == end):
            route.append(cur)
            temp = cur
            #đệ qui tìm đường đi
            while(1):
                #lấy index để truy cập phần tử trước đó
                ind = ele.index(temp)
                # check nếu đường đi không đi qua điểm thưởng, nhưng điểm thưởng nằm bên cạnh đường đi với giá trị điểm thưởng nhỏ hơn -1 
                # thì đi qua ô điểm thưởng và đi về lại để lấy điểm thưởng

                #nếu temp là điểm phía trước điểm thưởng
                if temp in prevBonusPoint:
                    #nếu điểm tiếp theo của temp trên đường đi không phải là điểm thưởng 
                    # -> điểm thưởng này k nằm trên đường đi và nằm bên đường đi
                    if route[len(route) - 1] not in BPinPath:
                        #lấy index điểm thưởng trên trong mảng các điểm thưởng mà tác nhân gặp trên đường tìm đường đi
                        ind1 = prevBonusPoint.index(temp)
                        #nếu giá trị điểm thưởng nhỏ hơn -1, vì nếu là -1 hoặc lớn hơn
                        # thì chi phí đi lấy lớn hơn giá trị điểm thưởng -> bị lỗ
                        if bonusPoint(bonus_points,BPinPath[ind1])< -1:
                            route.append(BPinPath[ind1])
                            route.append(temp)
                #lấy giá trị trước temp
                temp = prev[ind]
                #cập nhật đường đi lui
                route.append(temp)
                if temp == start:
                    break
            #lúc hồi quy tìm đường đi thì lúc này route lưu từ đích đến điểm bắt đầu nên cần đảo chiều list route lại
            route.reverse()
            return route

        #duyệt các điểm tiếp theo
        for i in range(4):
            next_row = cur[0]+row[i]
            next_col = cur[1]+col[i]
            next = (next_row,next_col)

            #nếu là tường thì cập nhật lại H[i] = 1000 (1000 là giá trị mặc định để không ảnh hưởng tới việc so sánh tìm điểm có heuristic nhỏ nhất)
            if matrix[next_row][next_col] == 'x': 
                f[i] = 1000
                continue

            #nếu điểm tiếp theo chưa được duyệt thì đưa vào danh sách open
            if next not in Priority_queue and next not in ele and matrix[next_row][next_col] != 'x':
                
                if matrix[next_row][next_col] == ' ':
                    costOfNext = CostI + CostOfCur
                else:
                    #nếu là điểm thưởng thì cập nhật điểm này vào mảng các điểm thưởng mà tác nhân gặp trên đường tìm đường đi
                    # và cập nhật điểm trước của điểm thưởng này
                    costOfNext = CostI + CostOfCur + bonusPoint(bonus_points, next)
                    BPinPath.append(next)
                    prevBonusPoint.append(cur)
                
                #cập nhập giá trị f(n) của điểm được thêm vào danh sách open, điểm trước đó của điểm này (để hồi quy)
                # và chi phí của điểm này
                f[i] = heuristic1(next,end) + costOfNext
                Priority_queue.append(next)
                Openf.append(f)
                ele.append(next)
                prev.append(cur)
                Cost.append(costOfNext)

cost = [-1]
#file_name phải có dạng 'maze_mapi.txt' (với i thuộc N+)
def runFuncSearch(file_name: str = 'maze.txt'):
    
    stt = file_name[8]
    route = []
    bonus_points, matrix = read_file(file_name)
    map_name = "Map " + str(stt) + ":"
    print(map_name)
    print(f'The height of the matrix: {len(matrix)}')
    print(f'The width of the matrix: {len(matrix[0])}')

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]=='S':
                start=(i,j)

            elif matrix[i][j]==' ':
                if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                    end=(i,j)
                
            else:
                pass
    print("DFS")
    route.clear()
    DFS(start, end, matrix, route)
    visualize_maze(matrix,bonus_points,start,end, route)

    print("BFS")
    route.clear()
    route = BFS(start,end,matrix)
    visualize_maze(matrix,bonus_points,start,end, route)

    print("GBFS")
    route.clear()
    route = GBFS(start, end, matrix)
    visualize_maze(matrix,bonus_points,start,end, route)

    print("A*")
    route.clear()
    route = Astar(start, end, matrix, bonus_points)
    visualize_maze(matrix,bonus_points,start,end, route)

print("Ban do khong co diem thuong:")
runFuncSearch('maze_map1.txt')
runFuncSearch('maze_map2.txt')
runFuncSearch('maze_map3.txt')
runFuncSearch('maze_map4.txt')
runFuncSearch('maze_map5.txt')
print("Ban do co diem thuong:")
runFuncSearch('maze_map6.txt')
runFuncSearch('maze_map7.txt')
runFuncSearch('maze_map8.txt')

#bonus_points, matrix = read_file('maze_map3.txt')

#print(f'The height of the matrix: {len(matrix)}')
#print(f'The width of the matrix: {len(matrix[0])}')

#for i in range(len(matrix)):
#    for j in range(len(matrix[0])):
#        if matrix[i][j]=='S':
#            start=(i,j)

#        elif matrix[i][j]==' ':
#            if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
#                end=(i,j)
                
#        else:
#            pass

#print("Map 3:")
#print("DFS")
#route.clear()
#DFS(start, end, matrix, route)
#visualize_maze(matrix,bonus_points,start,end, route)

#print("BFS")
#route.clear()
#route = BFS(start,end,matrix)
#visualize_maze(matrix,bonus_points,start,end, route)

#print("GBFS")
#route.clear()
#route = GBFS(start, end, matrix, 1)
#visualize_maze(matrix,bonus_points,start,end, route)

#print("A*")
#route.clear()
#route = Astar(start, end, matrix, 1)
#visualize_maze(matrix,bonus_points,start,end, route)