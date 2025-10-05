import numpy as np
from PIL import Image
from multiprocessing import Pool,cpu_count

'''
    原始代码. 通过 numpy 和其他库实现光线追踪.
    作者:wdz
    就是代码跑起来太慢
'''
# 三维向量和点就直接用numpy表示了，偷个懒
# 定义光线类
class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = direction # 时刻牢记这是一个三维向量

    def get_point(self, t):
        return self.origin + t * self.direction

# 定义材质类(也是个没啥用的基类)
class Material:
    def __init__(self,color,albedo,emit,refractive_index=1.0) -> None:
        '''
        颜色,漫反射系数,光照,折射率
        '''
        self.color=color
        self.albedo=np.array(albedo)
        self.refractivity_index=refractive_index
        self.emit=np.array(emit)
    
    def scatter(self, ray, hit_record):
        print("你似乎调用了一个抽象类中的方法，这不合理")
        scatter_direction=hit_record.normal+random_sphere_vec()
        scattered_ray=Ray(hit_record.point,scatter_direction)
        attenuation=self.albedo
        return scattered_ray,attenuation
    # 反射方法,在金属类、透明物体类或者完全镜面反射物体中都会用到
    def reflect(self,v:np.ndarray,n:np.ndarray):
        '''
        v: 入射光线
        n: 表面法线
        注意返回的是反射光的方向
        '''
        return v - 2*np.dot(v,n)*n
    # 发光方法
    def emitted(self):
        print("你必须在子类中覆写这个方法")
        return self.emit

# 交点记录
class HitRecord:
    def __init__(self, point:np.ndarray, normal:np.ndarray, material:Material|None, t, is_front:bool) -> None:
        self.point=point
        self.normal=normal
        self.material=material
        self.t=t
        self.front_face=is_front

# 漫反射
class Lambertian(Material):

    def __init__(self, albedo,color) -> None:
        '''
        albedo: 反射率(反射多少光线),但它是一个颜色向量
        '''
        self.color=np.array(color)
        self.albedo=np.array(albedo)
    
    def scatter(self, ray, hit_record:HitRecord):
        scatter_direction=hit_record.normal+random_sphere_vec()
        scattered_ray=Ray(hit_record.point,scatter_direction)
        attenuation=self.albedo*self.color
        return scattered_ray,attenuation
        
# 金属材质
class Metal(Material):
    def __init__(self, albedo , fuzz) -> None:
        self.albedo=np.array(albedo)
        self.fuzz=fuzz

    def scatter(self, ray:Ray, hit_record:HitRecord):
        scattered_direction=self.reflect(ray.direction,hit_record.normal)
        scattered_ray=Ray(hit_record.point,scattered_direction+self.fuzz*random_sphere_vec())
        attenuation = self.albedo
        return scattered_ray,attenuation
        
# 介质类(这名字真不准确)
class Dielectric(Material):
    def __init__(self,refractive_index=1.0) -> None:
        # 此为折射率，名字真么长，很烦人呢
        self.refractivity_index=refractive_index

    def refract(self, uv:np.ndarray, n: np.ndarray, eta: float):
        '''
        uv: 入射光线方向
        n: 法线方向
        eta: 相对折射率
        此函数用来计算折射光，不包含对是否合理的判断
        '''
        n=n/np.linalg.norm(n)
        cos_theta=np.dot(-uv,n)
        r_out_parallel = eta*(uv+cos_theta*n)
        r_out_perp=-np.sqrt(1.0-(np.linalg.norm(r_out_parallel)**2))*n
        return r_out_parallel+r_out_perp
    
    def scatter(self,ray:Ray,hit_record:HitRecord):
        # 透明物体，当做不吸收光
        attenuation=np.array([1.0,1.0,1.0])
        # 相对折射率，默认是空气比介质，所以分子是1.0
        relative_ratio = (1.0/self.refractivity_index) if hit_record.front_face else self.refractivity_index

        unit_direction = ray.direction/np.linalg.norm(ray.direction)
        cos_theta=min(np.dot(-unit_direction,hit_record.normal),1.0)
        sin_theta=np.sqrt(1.0-cos_theta**2)
        # 发生反射的概率(当既可以反射，也可以折射时)
        reflect_prob=self.reflectance(cos_theta,relative_ratio)
        
        # 全反射或者以一定概率发生反射
        if relative_ratio*sin_theta>1.0 or reflect_prob>np.random.rand():
            direction=self.reflect(unit_direction,hit_record.normal)
        else:
            direction=self.refract(unit_direction,hit_record.normal,relative_ratio)
            # print("折射方向为：",direction)
        scattered_ray=Ray(hit_record.point,direction)
        return scattered_ray, attenuation
    
    # 根据入射角计算反射率(反射比例),近似公式
    def reflectance(self,cosine,ref_idx:float):
        '''
        ref_idx: 相对折射率=入/折
        '''
        r=(1-ref_idx)/(1+ref_idx)
        r=r**2
        return r+(1-r)*((1-cosine)**5)

# 发光材质类(终于到光源了)
class DiffuseLight(Material):
    def __init__(self, emit) -> None:
        self.emit=np.array(emit)
    
    def scatter(self,ray:Ray,hit_record:HitRecord):
        return None,None
    
    # 只考虑纯白色的光源而不考虑纹理坐标的差异，但接口还是保留
    def emitted(self):
        return self.emit

# 包围盒
class AABB:
    def __init__(self,minimum:list|np.ndarray,maximum:list|np.ndarray) -> None:
        self.min=np.array(minimum)
        self.max=np.array(maximum)
    
    def hit(self,ray:Ray,tmin,tmax):
        # 使用np.divide来处理除数为0的情况
        # numpy的广播特性真的好方便
        # 写起来很简洁，但是看起来很抽象,写完就后悔了┭┮﹏┭┮
        divisor=np.divide(1.0,ray.direction,
                          out=np.full_like(ray.direction,np.inf),
                          where=ray.direction!=0)
        t0 = (self.min-ray.origin)*divisor
        t1 = (self.max-ray.origin)*divisor

        tmin=np.maximum(np.minimum(t0,t1),tmin)
        tmax=np.minimum(np.maximum(t0,t1),tmax)
        return np.all(tmax>=tmin)
    
# 定义物体抽象类
class Hittable:
    def __init__(self, material: Material):
        self.material=material
    
    def hit(self,ray:Ray,t_min,t_max)->HitRecord|None:
        return None
    
    def bounding_box(self,t0,t1):
        return AABB([0.01,0.01,0.01],[1000,1000,1000])

# 物体列表类
class HittableList(Hittable):
    def __init__(self,objects:list|None=None) -> None:
        self.objects:list[Hittable]=objects or []
        self.root:BVHNode|None = None
    
    def add(self,object):
        self.objects.append(object)
    
    def hit(self, ray: Ray, t_min, t_max):
        closest_so_far = t_max
        hit_anything = None

        for obj in self.objects:
            hit_record=obj.hit(ray,t_min,closest_so_far)
            if hit_record:
                closest_so_far = hit_record.t
                hit_anything = hit_record
        
        return hit_anything
    
    def bounding_box(self, t0, t1):
        # 检查列表是否为空
        if not self.objects:
            return None
        # 初始化为None
        box=None
        # 构造合并包围盒
        for obj in self.objects:
            temp=obj.bounding_box(t0,t1)
            if temp is None:
                return None
            box=surrounding_box(box,temp) if box else temp
        return box
    
    def build_bvh(self,t0,t1):
        # 首先沿着x轴方向排序
        comparator=lambda obj: obj.bounding_box(t0,t1).min[0]
        self.objects.sort(key= comparator)
        self.root = BVHNode(self,0,len(self.objects),t0,t1)

# BVH结点类
class BVHNode(Hittable):
    def __init__(self, hittable_list:HittableList,start,end,t0,t1):
        objects:list[Hittable]=hittable_list.objects[start:end]
        length=end-start
        box= surrounding_box(objects[0].bounding_box(t0, t1),
                             objects[-1].bounding_box(t0, t1))
        box_dims = box.max-box.min
        axis = box_dims.argmax()
        # print(axis)
        comparator=lambda obj: obj.bounding_box(t0,t1).min[axis]
        objects.sort(key= comparator)
        if length == 1:
            self.left = self.right = objects[0]
        elif length == 2:
            self.left = objects[0]
            self.right = objects[1]
        else:
            mid = length // 2
            self.left = BVHNode(hittable_list,start,start+mid, t0, t1)
            self.right = BVHNode(hittable_list,start+mid,end, t0, t1)

        box_left = self.left.bounding_box(t0, t1)
        box_right = self.right.bounding_box(t0, t1)
        self.box = surrounding_box(box_left, box_right)
    
    def bounding_box(self, t0, t1):
        return self.box
    
    # 检测光线与包围盒是否相交
    def hit(self,ray:Ray,t_min,t_max):
        if not self.box.hit(ray,t_min,t_max):
            return None
        hit_left = self.left.hit(ray, t_min, t_max)
        # 最终返回最接近摄像机的命中点
        # 下面这个判断的含义是右子节点与光线相交，且右结点到达时间比左节点短，或者左节点和光线无交
        if hit_left:
            t_max=hit_left.t
        hit_right = self.right.hit(ray, t_min, t_max)

        return hit_right if hit_right else hit_left

# 定义球体类
class Sphere(Hittable):
    def __init__(self, center:list, radius: float, material: Material|None):
        '''
        center: 球心
        radius: 半径
        material: 材料(目前还没有)
        '''
        self.center = np.array(center)
        self.radius = radius
        self.material=material

        self.r2=self.radius**2

    def get_normal(self,coord:np.ndarray,direction:np.ndarray):
        is_outter=True
        out_normal=(coord-self.center)/self.radius
        if np.dot(out_normal,-direction) < 0:
            is_outter=False
            out_normal=-out_normal
        return out_normal,is_outter
    
    def hit(self, ray: Ray, t_min, t_max) ->HitRecord|None:
        '''
        ray: 判断的光线
        record: 记录击中点信息的对象
        '''
        oc = ray.origin - self.center
        a = np.dot(ray.direction, ray.direction)
        b = 2.0 * np.dot(oc, ray.direction)
        c = np.dot(oc, oc) - self.r2
        delta = b * b - 4 * a * c
        if delta < 0:
            return None
        else:
            t = (-b - np.sqrt(delta)) / (2.0 * a)
            if not (t_min < t < t_max):
                t = (-b + np.sqrt(delta)) / (2.0 * a)
            if not (t_min < t < t_max):
                return None
            point=ray.get_point(t)
            normal,is_outter=self.get_normal(point,ray.direction)
            return HitRecord(point,normal,self.material,t,is_outter)
    
    # t0和t1是预留给运动物体使用的，但我暂时用不上
    def bounding_box(self, t0, t1):
        return AABB(self.center - np.abs(self.radius),
                    self.center + np.abs(self.radius))

# 定义三角形类
class Triangle(Hittable):
    def __init__(self, v0, v1, v2, material):
        self.v0 = np.array(v0)
        self.v1 = np.array(v1)
        self.v2 = np.array(v2)
        self.material = material
        self.e1 = self.v1 - self.v0
        self.e2 = self.v2 - self.v0
        self.normal=self.get_normal()

    def get_normal(self):
        normal = np.cross(self.e1, self.e2)
        normal /= np.linalg.norm(normal)
        return normal

    def hit(self, ray, t_min, t_max):
        # Möller–Trumbore 算法
        self.e1 = self.v1 - self.v0
        self.e2 = self.v2 - self.v0
        p = np.cross(ray.direction, self.e2)
        det = np.dot(self.e1, p)
        if abs(det) < 1e-8:
            return None
        inv_det = 1.0 / det
        tvec = ray.origin - self.v0
        u = np.dot(tvec, p) * inv_det
        if u < 0 or u > 1:
            return None
        q = np.cross(tvec, self.e1)
        v = np.dot(ray.direction, q) * inv_det
        if v < 0 or u + v > 1:
            return None
        t = np.dot(self.e2, q) * inv_det
        if t < t_min or t > t_max:
            return None
        point = ray.get_point(t)
        normal = self.normal
        is_front = np.dot(ray.direction, normal) < 0
        if not is_front:
            normal = -normal
        return HitRecord(point, normal, self.material, t, is_front)

    def bounding_box(self, t0, t1):
        min_coords = np.min([self.v0, self.v1, self.v2], axis=0)
        max_coords = np.max([self.v0, self.v1, self.v2], axis=0)
        return AABB(min_coords, max_coords)

# 我们还需要一个三角形网格类来组织所有的三角形图元
class TriangleMesh(HittableList):
    def __init__(self, vertices, indices, material, t0=None, t1=None):
        self.vertices = np.array(vertices)
        self.indices = np.array(indices)
        self.material = material
        self.objects = [] #这里的objects里面存储的就是三角形
        self.root=None
        # self.node=None
        for i in range(0, len(self.indices), 3):
            v0 = self.vertices[self.indices[i]]
            v1 = self.vertices[self.indices[i + 1]]
            v2 = self.vertices[self.indices[i + 2]]
            self.objects.append(Triangle(v0, v1, v2, self.material))
        # 构建 BVH 树
        # self.build_bvh(t0, t1)

    def build_bvh(self, t0, t1):
        # 滤清思路，首先排序，然后构建树
        comparator=lambda obj: obj.bounding_box(t0,t1).min[0]
        self.objects.sort(key= comparator)
        self.node = BVHNode(self, 0, len(self.objects),t0, t1)

    def bounding_box(self, t0, t1):
        min_coords = np.min(self.vertices, axis=0)
        max_coords = np.max(self.vertices, axis=0)
        return AABB(min_coords, max_coords)

# 矩形平面
class Rectangle(Hittable):
    def __init__(self, center, width, height, axis, material):
        """
        center: 矩形中心的坐标，为 numpy 数组
        width: 矩形的宽度
        height: 矩形的高度
        axis: 矩形所在平面的法向量，只能是 [1, 0, 0]、[0, 1, 0] 或 [0, 0, 1] 表示 x、y 或 z 轴法向
        material: 矩形的材质
        """
        self.center = np.array(center)
        self.width = width
        self.height = height
        self.axis = np.array(axis)
        self.material = material
        # 计算矩形的四个顶点坐标
        if np.array_equal(axis, [1, 0, 0]):  # 平面平行于 yz 平面
            self.v0 = np.array([center[0] , center[1] - height / 2, center[2]- width / 2])
            self.v1 = np.array([center[0] , center[1] + height / 2, center[2]- width / 2])
            self.v2 = np.array([center[0] , center[1] + height / 2, center[2]+ width / 2])
            self.v3 = np.array([center[0] , center[1] - height / 2, center[2]+ width / 2])
        elif np.array_equal(axis, [0, 1, 0]):  # 平面平行于 xz 平面
            self.v0 = np.array([center[0] - width / 2, center[1], center[2] - height / 2])
            self.v1 = np.array([center[0] + width / 2, center[1], center[2] - height / 2])
            self.v2 = np.array([center[0] + width / 2, center[1], center[2] + height / 2])
            self.v3 = np.array([center[0] - width / 2, center[1], center[2] + height / 2])
        elif np.array_equal(axis, [0, 0, 1]):  # 平面平行于 xy 平面
            self.v0 = np.array([center[0] - width / 2, center[1] - height / 2, center[2]])
            self.v1 = np.array([center[0] + width / 2, center[1] - height / 2, center[2]])
            self.v2 = np.array([center[0] + width / 2, center[1] + height / 2, center[2]])
            self.v3 = np.array([center[0] - width / 2, center[1] + height / 2, center[2]])
        else:
            raise ValueError("Invalid axis. Must be [1, 0, 0], [0, 1, 0] or [0, 0, 1].")
        self.normal = self.get_normal()

    def get_normal(self):
        """
        获取矩形的法线方向，根据初始化时的轴信息
        """
        return self.axis

    def hit(self, ray, t_min, t_max):
        """
        计算光线与矩形的交点，使用光线与平面相交公式和矩形边界检查
        """
        # 计算光线与平面的交点
        denominator = np.dot(ray.direction, self.normal)
        if np.abs(denominator) < 1e-8:  # 光线与平面平行
            return None
        t = np.dot(self.center - ray.origin, self.normal) / denominator
        if t < t_min or t > t_max:
            return None
        # 计算交点在平面上的位置
        point = ray.get_point(t)
        # 检查交点是否在矩形内
        if np.array_equal(self.axis, [1, 0, 0]):  # 平面平行于 yz 平面
            u = point[1]
            v = point[2]
            if u < self.v0[1] or u > self.v2[1] or v < self.v0[2] or v > self.v2[2]:
                return None
        elif np.array_equal(self.axis, [0, 1, 0]):  # 平面平行于 xz 平面
            u = point[0]
            v = point[2]
            if u < self.v0[0] or u > self.v2[0] or v < self.v0[2] or v > self.v2[2]:
                return None
        elif np.array_equal(self.axis, [0, 0, 1]):  # 平面平行于 xy 平面
            u = point[0]
            v = point[1]
            if u < self.v0[0] or u > self.v2[0] or v < self.v0[1] or v > self.v2[1]:
                return None
        # 交点在矩形内，返回交点信息
        normal = self.normal
        is_front = np.dot(ray.direction, normal) < 0
        if not is_front:
            normal = -normal
        return HitRecord(point, normal, self.material, t, is_front)
    
    def bounding_box(self, t0, t1):
        """
        获取矩形的包围盒
        """
        if np.array_equal(self.axis, [1, 0, 0]):  # 平面平行于 yz 平面
            min_coords = np.array([self.center[0] - 1e-4, self.v0[1], self.v0[2]])
            max_coords = np.array([self.center[0] + 1e-4, self.v2[1], self.v2[2]])
        elif np.array_equal(self.axis, [0, 1, 0]):  # 平面平行于 xz 平面
            min_coords = np.array([self.v0[0], self.center[1] - 1e-4, self.v0[2]])
            max_coords = np.array([self.v2[0], self.center[1] + 1e-4, self.v2[2]])
        elif np.array_equal(self.axis, [0, 0, 1]):  # 平面平行于 xy 平面
            min_coords = np.array([self.v0[0], self.v0[1], self.center[2] - 1e-4])
            max_coords = np.array([self.v2[0], self.v2[1], self.center[2] + 1e-4])
        return AABB(min_coords, max_coords)

# 立方体
import numpy as np


class Cuboid(Hittable):
    def __init__(self, center, x_length, y_length, z_length, material, rotation_axis='y', rotation_angle=0):
        """
        center: 长方体的中心，是一个 numpy 数组
        x_length: 长方体在 x 轴方向的边长
        y_length: 长方体在 y 轴方向的边长
        z_length: 长方体在 z 轴方向的边长
        material: 长方体的材质
        rotation_axis: 旋转轴，默认为 'y'
        rotation_angle: 旋转角度，默认为 0 度
        """
        self.center = np.array(center)
        self.x_length = x_length
        self.y_length = y_length
        self.z_length = z_length
        self.material = material
        self.rotation_axis = rotation_axis
        self.rotation_angle = np.radians(rotation_angle)  # 将角度转换为弧度
        self.faces = []
        # 创建六个面，考虑不同的边长
        # +x 面
        self.faces.append(Rectangle(center + np.array([x_length / 2, 0, 0]), z_length, y_length, [1, 0, 0], material))
        # -x 面
        self.faces.append(Rectangle(center - np.array([x_length / 2, 0, 0]), z_length, y_length, [1, 0, 0], material))
        # +y 面
        self.faces.append(Rectangle(center + np.array([0, y_length / 2, 0]), x_length, z_length, [0, 1, 0], material))
        # -y 面
        self.faces.append(Rectangle(center - np.array([0, y_length / 2, 0]), x_length, z_length, [0, 1, 0], material))
        # +z 面
        self.faces.append(Rectangle(center + np.array([0, 0, z_length / 2]), x_length, y_length, [0, 0, 1], material))
        # -z 面
        self.faces.append(Rectangle(center - np.array([0, 0, z_length / 2]), x_length, y_length, [0, 0, 1], material))
        # 计算旋转矩阵
        self.rotation_matrix = self.get_rotation_matrix()

    def get_rotation_matrix(self):
        """
        生成旋转矩阵
        """
        cos_theta = np.cos(self.rotation_angle)
        sin_theta = np.sin(self.rotation_angle)
        if self.rotation_axis == 'x':
            return np.array([[1, 0, 0],
                           [0, cos_theta, -sin_theta],
                           [0, sin_theta, cos_theta]])
        elif self.rotation_axis == 'y':
            return np.array([[cos_theta, 0, sin_theta],
                           [0, 1, 0],
                           [-sin_theta, 0, cos_theta]])
        elif self.rotation_axis ==  'z':
            return np.array([[cos_theta, -sin_theta, 0],
                           [sin_theta, cos_theta, 0],
                           [0, 0, 1]])
        else:
            raise ValueError("Invalid rotation axis. Use 'x', 'y', or 'z'.")

    def hit(self, ray, t_min, t_max):
        """
        检查光线是否与长方体的六个面相交，找到最近的交点
        """
        # 对光线进行逆旋转
        inv_rotation_matrix = self.rotation_matrix.T  # 旋转矩阵的逆矩阵等于其转置
        origin = np.dot(ray.origin - self.center, inv_rotation_matrix) + self.center
        direction = np.dot(ray.direction, inv_rotation_matrix)
        rotated_ray = Ray(origin, direction)
        closest_so_far = t_max
        hit_anything = None
        for face in self.faces:
            hit_record = face.hit(rotated_ray, t_min, closest_so_far)
            if hit_record:
                # 旋转交点信息回来
                point = np.dot(hit_record.point - self.center, self.rotation_matrix) + self.center
                normal = np.dot(hit_record.normal, self.rotation_matrix)
                hit_record.point = point
                hit_record.normal = normal
                closest_so_far = hit_record.t
                hit_anything = hit_record
        return hit_anything

    def bounding_box(self, t0, t1):
        """
        获取长方体的包围盒
        """
        half_x = self.x_length / 2
        half_y = self.y_length / 2
        half_z = self.z_length / 2
        vertices = []
        vertices.append(self.center + np.array([-half_x, -half_y, -half_z]))
        vertices.append(self.center + np.array([half_x, -half_y, -half_z]))
        vertices.append(self.center + np.array([half_x, half_y, -half_z]))
        vertices.append(self.center + np.array([-half_x, half_y, -half_z]))
        vertices.append(self.center + np.array([-half_x, -half_y, half_z]))
        vertices.append(self.center + np.array([half_x, -half_y, half_z]))
        vertices.append(self.center + np.array([half_x, half_y, half_z]))
        vertices.append(self.center + np.array([-half_x, half_y, half_z]))
        # 旋转顶点
        rotated_vertices = [np.dot(vertex - self.center, self.rotation_matrix) + self.center for vertex in vertices]
        min_coords = np.min(rotated_vertices, axis=0)
        max_coords = np.max(rotated_vertices, axis=0)
        return AABB(min_coords, max_coords)

# 定义摄像机类
class Camera:
    def __init__(self, lookfrom, lookat, up, fov, aspect):
        '''
        up: 摄像机的上方向
        fov: 垂直视场角(角度制)
        aspect: 宽高比
        '''
        lookfrom=np.array(lookfrom)
        lookat=np.array(lookat)
        up=np.array(up)
        self.origin = lookfrom
        # w,u,v分别是z方向，x方向，y方向(但摄像机看向的方向是-z轴)
        self.w = (lookfrom - lookat) / np.linalg.norm(lookfrom - lookat)
        self.u = np.cross(up, self.w) / np.linalg.norm(np.cross(up, self.w))
        self.v = np.cross(self.w, self.u)
        # 屏幕的高度和宽度
        theta = fov * np.pi / 180
        self.height = 2 * np.tan(theta / 2)
        self.width = aspect * self.height
        # 影像平面的水平和竖直方向(这是两个向量)
        self.horizontal = self.u * self.width
        self.vertical = self.v * self.height
    # 生成光线,u,v是屏幕上的坐标，范围是[0,1]
    def get_ray(self, u, v):
        direction = -self.w + (u-0.5)*self.horizontal + (v-0.5)*self.vertical
        return Ray(self.origin, direction)

max_depth=100

# 合并包围盒的辅助函数
def surrounding_box(box0:AABB,box1:AABB):
    small=np.minimum(box0.min,box1.min)
    large=np.maximum(box0.max,box1.max)
    return AABB(small,large)

# 随机单位向量
def random_sphere_vec():
    phi = 2*np.pi*np.random.rand()
    cos_theta = 2*np.random.rand()-1
    sin_theta = np.sqrt(1-cos_theta**2)
    # 转换到笛卡尔坐标
    x = sin_theta * np.cos(phi)
    y = sin_theta * np.sin(phi)
    z = cos_theta
    return np.array([x, y, z])

# 递归实现改成循环实现，提高效率
def get_color(ray: Ray, world: HittableList, max_depth: int):

    ray_color = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    attenuation = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    background=np.array([0.1,0.1,0.1])
    for i in range(max_depth):
        if world.root:
            hit_record = world.root.hit(ray, 0.001, 1000)
        else:
            hit_record = None
        # 击中物体就继续追踪反射光线，未击中物体就返回背景颜色
        if hit_record and hit_record.material:
            scattered, atn = hit_record.material.scatter(ray, hit_record)
            # 因为只有光源不反射光
            if scattered==None:
                emitted=hit_record.material.emitted()
                return attenuation*emitted
            attenuation *= atn
            ray = scattered
        else:
            return ray_color + attenuation * background   
    return ray_color

# 确定像素点颜色
def write_color(x,y,size:tuple,world:HittableList,source:Camera,sample_times):
    '''
    size: 第一项是宽，第二项是高
    '''
    color=np.array([0,0,0],dtype=np.float64)
    if sample_times==1:
        u = x/size[0]
        v = y/size[1]
        color+=get_color(source.get_ray(u,v),world,max_depth)
        return np.array(255.9*np.clip(color,0,1),dtype=np.uint8)
    for i in range(sample_times):
        u = (x+np.random.rand())/size[0]
        v = (y+np.random.rand())/size[1]
        color+=get_color(source.get_ray(u,v),world,max_depth)
    color/=sample_times
    # gamma校正,似乎不需要
    color=np.sqrt(color)
    return np.array(255.9*np.clip(color,0,1),dtype=np.uint8)

# 多进程优化
def process_row(y,width,height,world,camera,samples_per_pixel):
    '''
    作用是处理一行像素并返回该行的颜色数据
    '''
    row_data = np.zeros((width, 3), dtype=np.uint8)
    for x in range(width):
        color = write_color(x, y, (width, height), world, camera, samples_per_pixel)
        row_data[x, :] = color
    return y, row_data

# 渲染函数
def render_scene(world,camera,width,height,samples_per_pixel):
    img_data = np.zeros((height, width, 3), dtype=np.uint8)

    with Pool(cpu_count()) as pool:
        for y, row_data in pool.starmap(process_row, [(y, width, height,world, camera, samples_per_pixel) for y in range(height)]):
            img_data[height-1-y, :, :] = row_data
    return img_data

# 读取模型文件
def read_obj_file(file_path, material):
    vertices = []
    indices = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if not parts:  # 处理空行
                continue
            if parts[0] == '#':  # 处理注释行
                continue
            if parts[0] == 'v':  # 顶点信息
                vertex = [float(coord) for coord in parts[1:4]]  # 只取前三个坐标
                vertices.append(vertex)
            elif parts[0] == 'f':  # 面信息
                face = []
                for part in parts[1:]:
                    vertex_index = int(part.split('/')[0]) - 1  # 只取顶点索引
                    face.append(vertex_index)
                # 将面拆分为三角形
                for i in range(1, len(face) - 1):
                    indices.extend([face[0], face[i], face[i + 1]])
    return TriangleMesh(vertices, indices, material)

# 创建康奈尔盒子，首先构建网格数据
# 生成一个平面正方形
def generate_rectangle(width, height, rotation_axis, rotation_angle, translation_vector):
    # 生成位于 xy 平面上的矩形的四个顶点
    half_width = width / 2
    half_height = height / 2
    v0 = np.array([-half_width, -half_height, 0, 1])  # 齐次坐标，w = 1
    v1 = np.array([half_width, -half_height, 0, 1])
    v2 = np.array([half_width, half_height, 0, 1])
    v3 = np.array([-half_width, half_height, 0, 1])
    vertices = np.array([v0, v1, v2, v3])
    indices = np.array([0, 1, 2, 0, 2, 3])
    # 生成旋转矩阵
    cos_theta = np.cos(np.radians(rotation_angle))
    sin_theta = np.sin(np.radians(rotation_angle))
    if rotation_axis == 'x':
        rotation_matrix = np.array([[1, 0, 0, 0],
                                [0, cos_theta, -sin_theta, 0],
                                [0, sin_theta, cos_theta, 0],
                                [0, 0, 0, 1]])
    elif rotation_axis == 'y':
        rotation_matrix = np.array([[cos_theta, 0, sin_theta, 0],
                                [0, 1, 0, 0],
                                [-sin_theta, 0, cos_theta, 0],
                                [0, 0, 0, 1]])
    elif rotation_axis == 'z':
        rotation_matrix = np.array([[cos_theta, -sin_theta, 0, 0],
                                [sin_theta, cos_theta, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
    else:
        raise ValueError("Invalid rotation axis. Use 'x', 'y', or 'z'.")
    # 旋转顶点
    rotated_vertices =np.dot(vertices,rotation_matrix.T)
    # 生成平移矩阵
    tx, ty, tz = translation_vector
    translation_matrix = np.array([
                               [1, 0, 0, tx],
                               [0, 1, 0, ty],
                               [0, 0, 1, tz],
                               [0, 0, 0, 1]
                               ])
    # 平移顶点
    translated_vertices = np.dot(rotated_vertices,translation_matrix.T)
    # 转换回 3D 坐标
    translated_vertices = translated_vertices[:, :3]
    # 生成三角形索引
    
    return translated_vertices, indices

def create_cornell_box(world: HittableList, a):
    """
    a: 底面正方形的边长
    """
    # 定义墙壁和地板的材质
    red_material = Lambertian(albedo=[0.65, 0.05, 0.05], color=[0.65, 0.05, 0.05])
    green_material = Lambertian(albedo=[0.12, 0.45, 0.15], color=[0.12, 0.45, 0.15])
    white_material = Lambertian(albedo=[0.73, 0.73, 0.73], color=[0.73, 0.73, 0.73])
    light_material = DiffuseLight(emit=[10,10,10])

    # 生成地板
    floor = Rectangle(center=[0, 0, 0], width=a, height=a, axis=[0, 1, 0], material=white_material)
    world.add(floor)

    # 生成天花板
    ceiling = Rectangle(center=[0, 1.4*a, 0], width=a, height=a, axis=[0, 1, 0], material=white_material)
    world.add(ceiling)

    # 生成左侧墙壁
    left_wall = Rectangle(center=[-a / 2, 0.7 * a, 0], width=a, height=1.4 * a, axis=[1, 0, 0], material=red_material)
    world.add(left_wall)

    # 生成右侧墙壁
    right_wall = Rectangle(center=[a / 2, 0.7 * a, 0], width=a, height=1.4 * a, axis=[1, 0, 0], material=green_material)
    world.add(right_wall)

    # 生成后墙
    back_wall = Rectangle(center=[0, 0.7 * a, -a / 2], width=a, height=1.4 * a, axis=[0, 0, 1], material=white_material)
    world.add(back_wall)

    # 生成光源
    light = Rectangle(center=[0, 1.4*a-0.01, 0], width=2.0, height=2.0, axis=[0, 1, 0], material=light_material)
    world.add(light)

    # 生成2个立方体
    cuboid_material = Lambertian(albedo=[1.0,1.0,1.0], color=[0.9, 0.9, 0.9])
    
    cuboid = Cuboid([-1.2, 2, -1], 1.6, 4 ,1.6,cuboid_material, rotation_axis='y', rotation_angle=30)  # 沿 y 轴旋转 45 度
    world.add(cuboid)

    cubo = Cuboid([1, 0.75, 1], 1.5, 1.5 ,1.5,cuboid_material, rotation_axis='y', rotation_angle=-30)  # 沿 y 轴旋转 45 度
    world.add(cubo)
    return world

# 以下为主程序
def main():
    world=HittableList()
    world.add(Sphere([1,2.2,1],0.7,Lambertian(albedo=[1,1,1],color=[0.0,0.8,0.8])))
    create_cornell_box(world,6)
    print("场景构建完毕")
    world.build_bvh(0.001,1000)
    print("包围盒构建完毕")
    camera=Camera([0,4,8],[0,4,-10],[0,1,0],70,2/3)
    width,height=(200,300)
    samples_per_pixel=50
    img_data=render_scene(world,camera,width,height,samples_per_pixel)
    image = Image.fromarray(img_data)
    image.save('高清版.png')

if __name__=="__main__":
    main()