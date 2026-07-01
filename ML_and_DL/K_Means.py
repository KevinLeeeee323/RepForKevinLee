import sys
import math
parts=sys.stdin.readline().split()
K=int(parts[0])
N=int(parts[1])
speed=float(parts[2])
K=min(K, N)

points=[]
for i in range(N):
    x, y=map(float, sys.stdin.readline().split())
    points.append((x, y))


def get_dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


points.sort(key=lambda x:get_dist(x[0], x[1], 0, 0), reverse=False)

centers=[]
for i in range(K):
    centers.append(points[i])

MAX_ITERS = 50
TOL=1e-4

for _ in range(MAX_ITERS):
    total_move_dist=0.0
    clusters=[[] for _ in range(K)]

    for i in range(N):
        # 确定当前样本距离最近的类, 并且添加进去
        min_dist=float('inf')
        min_dist_center_id=-1
        for center_id in range(K):
            dist=get_dist(points[i][0], points[i][1], centers[center_id][0], centers[center_id][1])
            if dist<min_dist:
                min_dist=dist
                min_dist_center_id=center_id
        
        clusters[min_dist_center_id].append(points[i])
    
    # 更新每个聚类--重新计算类中心
    new_centers=[]
    for i in range(K):
        if not clusters[i]:
            # 没有新的点加入中心, 因此不发生偏移
            new_centers.append(centers[i])
        else:
            avg_x=sum(pt[0] for pt in clusters[i])/len(clusters[i])
            avg_y=sum(pt[1] for pt in clusters[i])/len(clusters[i])
            new_centers.append((avg_x, avg_y))
            total_move_dist+=get_dist(centers[i][0], centers[i][1], avg_x, avg_y)

    centers=new_centers # 更新中心

    if total_move_dist<TOL:
        break


