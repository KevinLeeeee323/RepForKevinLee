import taichi as ti
import numpy as np
import sys
import io
import time

'''
    wdz 重构的代码.
    通过使用 taichi 架构, 提升了速度.
    渲染一张图, 平均用时 1min.
    需要调整的参数一般为:(都在1628 行)
    width, height :分辨率, 画幅大小
    samples_per_pixel = 1600  # 采样点数.采样点数增加到 1600或者更大, 会无法生成完整图片
    max_depth = 15 # 最大递归深度

    相比于 rebuild.py, 这一版加上了 BVH , 但是有点问题
'''
# 设置标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ti.init(arch=ti.metal)

# ==================== 常量定义 ====================
MAT_LAMBERTIAN = 0
MAT_METAL = 1
MAT_DIELECTRIC = 2
MAT_LIGHT = 3

# ==================== 材质系统 ====================
@ti.data_oriented
class MaterialSystem:
    def __init__(self, max_materials=256):
        self.max_materials = max_materials
        # 定义材质数据结构
        self.Material = ti.types.struct(
            mat_type=ti.i32,           # 材质类型
            albedo=ti.types.vector(3, ti.f32),  # 基础颜色/反射率
            fuzz=ti.f32,               # 金属模糊度
            refractive_idx=ti.f32,     # 折射率
            emit=ti.types.vector(3, ti.f32),    # 发光颜色
            roughness=ti.f32,          # 粗糙度（为未来扩展）
            metallic=ti.f32            # 金属度（为未来扩展）
        )
        self.materials = self.Material.field(shape=(max_materials,))
        self.material_count = ti.field(ti.i32, shape=())
        self.next_id = ti.field(ti.i32, shape=())  # 改为Taichi字段
        self.next_id[None] = 0  # 初始化值
        
        # 初始化默认材质
        self.init_default_materials()
    
    """初始化默认材质的内核"""
    @ti.kernel
    def init_default_materials(self):
        # 漫反射材质
        self.materials[0].mat_type = MAT_LAMBERTIAN
        self.materials[0].albedo = ti.Vector([0.8, 0.2, 0.2])
        self.materials[0].fuzz = 0.0
        self.materials[0].refractive_idx = 1.0
        self.materials[0].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[0].roughness = 1.0
        self.materials[0].metallic = 0.0
        
        self.materials[1].mat_type = MAT_LAMBERTIAN
        self.materials[1].albedo = ti.Vector([0.2, 0.8, 0.2])
        self.materials[1].fuzz = 0.0
        self.materials[1].refractive_idx = 1.0
        self.materials[1].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[1].roughness = 1.0
        self.materials[1].metallic = 0.0
        
        self.materials[2].mat_type = MAT_LAMBERTIAN
        self.materials[2].albedo = ti.Vector([0.2, 0.2, 0.8])
        self.materials[2].fuzz = 0.0
        self.materials[2].refractive_idx = 1.0
        self.materials[2].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[2].roughness = 1.0
        self.materials[2].metallic = 0.0
        
        self.materials[3].mat_type = MAT_LAMBERTIAN
        self.materials[3].albedo = ti.Vector([0.73, 0.73, 0.73])
        self.materials[3].fuzz = 0.0
        self.materials[3].refractive_idx = 1.0
        self.materials[3].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[3].roughness = 1.0
        self.materials[3].metallic = 0.0
        
        self.materials[4].mat_type = MAT_LAMBERTIAN
        self.materials[4].albedo = ti.Vector([0.5, 0.5, 0.5])
        self.materials[4].fuzz = 0.0
        self.materials[4].refractive_idx = 1.0
        self.materials[4].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[4].roughness = 1.0
        self.materials[4].metallic = 0.0
        
        # 金属材质
        self.materials[5].mat_type = MAT_METAL
        self.materials[5].albedo = ti.Vector([1.0, 0.8, 0.2])
        self.materials[5].fuzz = 0.1
        self.materials[5].refractive_idx = 1.0
        self.materials[5].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[5].roughness = 0.1
        self.materials[5].metallic = 1.0
        
        self.materials[6].mat_type = MAT_METAL
        self.materials[6].albedo = ti.Vector([0.8, 0.8, 0.8])
        self.materials[6].fuzz = 0.05
        self.materials[6].refractive_idx = 1.0
        self.materials[6].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[6].roughness = 0.1
        self.materials[6].metallic = 1.0
        
        self.materials[7].mat_type = MAT_METAL
        self.materials[7].albedo = ti.Vector([0.8, 0.5, 0.2])
        self.materials[7].fuzz = 0.1
        self.materials[7].refractive_idx = 1.0
        self.materials[7].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[7].roughness = 0.1
        self.materials[7].metallic = 1.0
        
        # 介质材质
        self.materials[8].mat_type = MAT_DIELECTRIC
        self.materials[8].albedo = ti.Vector([1.0, 1.0, 1.0])
        self.materials[8].fuzz = 0.0
        self.materials[8].refractive_idx = 1.5
        self.materials[8].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[8].roughness = 0.0
        self.materials[8].metallic = 0.0
        
        self.materials[9].mat_type = MAT_DIELECTRIC
        self.materials[9].albedo = ti.Vector([1.0, 1.0, 1.0])
        self.materials[9].fuzz = 0.0
        self.materials[9].refractive_idx = 2.4
        self.materials[9].emit = ti.Vector([0.0, 0.0, 0.0])
        self.materials[9].roughness = 0.0
        self.materials[9].metallic = 0.0
        
        # 光源
        self.materials[10].mat_type = MAT_LIGHT
        self.materials[10].albedo = ti.Vector([0.0, 0.0, 0.0])
        self.materials[10].fuzz = 0.0
        self.materials[10].refractive_idx = 1.0
        self.materials[10].emit = ti.Vector([8.0, 8.0, 8.0])
        self.materials[10].roughness = 0.0
        self.materials[10].metallic = 0.0
        
        self.materials[11].mat_type = MAT_LIGHT
        self.materials[11].albedo = ti.Vector([0.0, 0.0, 0.0])
        self.materials[11].fuzz = 0.0
        self.materials[11].refractive_idx = 1.0
        self.materials[11].emit = ti.Vector([6.0, 5.4, 4.2])  # 暖色光
        self.materials[11].roughness = 0.0
        self.materials[11].metallic = 0.0
        self.next_id[None] = 12
        print("texture innitializing succeed!")

    @ti.kernel
    def set_material_params(self, id: ti.i32, m_type: ti.i32, 
                            albedo_r: ti.f32, albedo_g: ti.f32, albedo_b: ti.f32,
                            f: ti.f32, ri: ti.f32,
                            emit_r: ti.f32, emit_g: ti.f32, emit_b: ti.f32,
                            rough: ti.f32, metal: ti.f32):
        self.materials[id].mat_type = m_type
        self.materials[id].albedo = ti.Vector([albedo_r, albedo_g, albedo_b])
        self.materials[id].fuzz = f
        self.materials[id].refractive_idx = ri
        self.materials[id].emit = ti.Vector([emit_r, emit_g, emit_b])
        self.materials[id].roughness = rough
        self.materials[id].metallic = metal

    def add_custom_material(self, mat_type, albedo=None, fuzz=0.0, refractive_idx=1.0, emit=None, roughness=0.5, metallic=0.0):
        """添加自定义材质"""
        if self.next_id[None] >= self.max_materials:
            raise ValueError("超出最大材质数量限制")
        mat_id = self.next_id[None]
        # 设置默认值
        if albedo is None:
            albedo = [1.0, 1.0, 1.0]
        if emit is None:
            emit = [0.0, 0.0, 0.0]
        # 使用内核参数设置材质
        self.set_material_params(mat_id, mat_type, 
                           albedo[0], albedo[1], albedo[2],
                           fuzz, refractive_idx,
                           emit[0], emit[1], emit[2],
                           roughness, metallic)
        self.next_id[None] += 1
        return mat_id

# ==================== 材质散射系统 ====================
@ti.data_oriented
class MaterialScatterSystem:
    def __init__(self, material_system):
        self.materials = material_system.materials
    
    @ti.func
    def scatter(self, ray_dir, normal, hit_point, mat_id, rng_state, front_face):
        """
        统一的材质散射函数
        """
        scattered_dir = ti.Vector([0.0, 0.0, 0.0])
        attenuation = ti.Vector([1.0, 1.0, 1.0])
        emitted = ti.Vector([0.0, 0.0, 0.0])
        should_scatter = False
        
        mat = self.materials[mat_id]
        
        if mat.mat_type == MAT_LAMBERTIAN:
            scattered_dir, attenuation, should_scatter = self._scatter_lambertian(
                normal, mat, rng_state
            )
        elif mat.mat_type == MAT_METAL:
            scattered_dir, attenuation, should_scatter = self._scatter_metal(
                ray_dir, normal, mat, rng_state
            )
        elif mat.mat_type == MAT_DIELECTRIC:
            scattered_dir, attenuation, should_scatter = self._scatter_dielectric(
                ray_dir, normal, mat, rng_state, front_face
            )
        elif mat.mat_type == MAT_LIGHT:
            emitted = mat.emit
            # 光源不散射光线
        
        return scattered_dir, attenuation, emitted, should_scatter
    
    @ti.func
    def _scatter_lambertian(self, normal, mat, rng_state):
        """漫反射材质散射"""
        scatter_dir = normal + self._random_in_unit_sphere(rng_state)
        
        # if scatter_dir.norm_sqr() < 1e-8:
        #     scatter_dir = normal
        
        scattered_dir = scatter_dir.normalized()
        attenuation = mat.albedo
        should_scatter = True
        
        return scattered_dir, attenuation, should_scatter
    
    @ti.func
    def _scatter_metal(self, ray_dir, normal, mat, rng_state):
        """金属材质散射"""
        unit_direction = ray_dir.normalized()
        reflected = self._reflect(unit_direction, normal)
        
        scattered_dir = reflected + mat.fuzz * self._random_in_unit_sphere(rng_state)
        attenuation = mat.albedo
        
        should_scatter = scattered_dir.dot(normal) > 0
        
        return scattered_dir, attenuation, should_scatter
    
    @ti.func
    def _scatter_dielectric(self, ray_dir, normal, mat, rng_state, front_face):
        """介质材质散射"""
        attenuation = ti.Vector([1.0, 1.0, 1.0])

        unit_direction = ray_dir.normalized()
        
        refraction_ratio = 1.0 / mat.refractive_idx if front_face else mat.refractive_idx
        
        cos_theta = min(-unit_direction.dot(normal), 1.0)
        sin_theta = ti.sqrt(1.0 - cos_theta * cos_theta)
        # 初始化scattered_dir，确保所有路径都有定义
        scattered_dir = ti.Vector([0.0, 0.0, 0.0])
        cannot_refract = refraction_ratio * sin_theta > 1.0
        # print("no_refract:",cannot_refract)
        reflect_prob = self._reflectance(cos_theta, refraction_ratio)
        
        if cannot_refract or reflect_prob > ti.random():
            scattered_dir = self._reflect(unit_direction, normal)
        else:
            scattered_dir = self._refract(unit_direction, normal, refraction_ratio)
        
        should_scatter = True
        
        return scattered_dir, attenuation, should_scatter
    
    @ti.func
    def _random_in_unit_sphere(self, rng_state):
        """生成单位球内的随机向量"""
        p = ti.Vector([0.0, 0.0, 0.0])
        while True:
            p = 2.0 * ti.Vector([ti.random(), ti.random(), ti.random()]) - 1.0
            if p.norm_sqr() <= 1.0:
                break
        return p
    
    @ti.func
    def _reflect(self, v, n):
        """计算反射方向"""
        # print("v:",v)
        # print("n:",n)
        return v - 2.0 * v.dot(n) * n
    
    @ti.func
    def _refract(self, uv, n, etai_over_etat):
        """计算折射方向"""
        cos_theta = min(-uv.dot(n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta * n)
        r_out_parallel = -ti.sqrt(abs(1.0 - r_out_perp.norm_sqr())) * n
        return r_out_perp + r_out_parallel
    
    @ti.func
    def _reflectance(self, cosine, ref_idx):
        """计算反射率（Schlick近似）"""
        r0 = (1.0 - ref_idx) / (1.0 + ref_idx)
        r0 = r0 * r0
        return r0 + (1.0 - r0) * ti.pow((1.0 - cosine), 5.0)

# ==================== 场景材质管理器 ====================
@ti.data_oriented
class SceneMaterialManager:
    def __init__(self):
        self.material_system = MaterialSystem()
        self.scatter_system = MaterialScatterSystem(self.material_system)
        
        # 预定义材质ID映射
        self.material_ids = {
            "red": 0, "green": 1, "blue": 2,
            "white": 3, "gray": 4,
            "gold": 5, "silver": 6, "copper": 7,
            "glass": 8, "diamond": 9,
            "bright_light": 10, "warm_light": 11
        }
    
    def get_material_id(self, name):
        """通过名称获取材质ID"""
        return self.material_ids.get(name, 3)  # 默认为白色
    
    def add_custom_lambertian(self, albedo):
        """添加自定义漫反射材质"""
        return self.material_system.add_custom_material(MAT_LAMBERTIAN, albedo=albedo)
    
    def add_custom_metal(self, albedo, fuzz=0.0):
        """添加自定义金属材质"""
        return self.material_system.add_custom_material(MAT_METAL, albedo=albedo, fuzz=fuzz)
    
    def add_custom_dielectric(self, refractive_idx=1.5):
        """添加自定义介质材质"""
        return self.material_system.add_custom_material(MAT_DIELECTRIC, refractive_idx=refractive_idx)
    
    def add_custom_light(self, emit_color, intensity=1.0):
        """添加自定义发光材质"""
        emit = [emit_color[0] * intensity, emit_color[1] * intensity, emit_color[2] * intensity]
        return self.material_system.add_custom_material(MAT_LIGHT, emit=emit)
    
    @ti.func
    def scatter_ray(self, ray_dir, normal, hit_point, mat_id, rng_state, front_face):
        """散射光线接口"""
        return self.scatter_system.scatter(ray_dir, normal, hit_point, mat_id, rng_state, front_face)

# ==================== 几何形状管理 ====================
@ti.data_oriented
class SphereSystem:
    def __init__(self, max_spheres=1024):
        self.max_spheres = max_spheres
        self.Sphere = ti.types.struct(
            center=ti.types.vector(3, ti.f32),
            radius=ti.f32,
            material_id=ti.i32,
            radius_sqr=ti.f32,  # 新增该字段
        )
        # 创建球体数组 - 这才是实例
        self.spheres = self.Sphere.field(shape=(max_spheres,))
        self.object_count = ti.field(ti.i32, shape=())
        self.object_count[None] = 0
        # 为加速结构预留的字段
        self.enable_acceleration = ti.field(ti.i32, shape=())  # 是否启用加速
        self.acceleration_structure = None  # 将来存放BVH等加速结构
    
    @ti.kernel
    def set_sphere_params(self, id: ti.i32, center_x: ti.f32, center_y: ti.f32, center_z: ti.f32, rad: ti.f32, mat_id: ti.i32):
        self.spheres[id].center = ti.Vector([center_x, center_y, center_z])
        self.spheres[id].radius = rad
        self.spheres[id].radius_sqr = rad * rad
        self.spheres[id].material_id = mat_id

    def add_sphere(self, center, radius, material_id):
        # 添加球体的逻辑
        if self.object_count[None] >= self.max_spheres:
            raise ValueError(f"超出最大球体数量限制: {self.max_spheres}")
        sphere_id = self.object_count[None]
        # 使用内核函数设置球体参数
        self.set_sphere_params(sphere_id, center[0], center[1], center[2], radius, material_id)
        self.object_count[None] += 1
        pass
    
    # 光线求交测试
    @ti.func
    def intersect(self, ray_origin, ray_dir, t_min, t_max, candidate_ids=None):
        """球体求交测试 - 必须用@ti.func装饰
        
        参数:
            ray_origin: 光线起点
            ray_dir: 光线方向
            t_min, t_max: 有效的t值范围
            candidate_id: 可选,要测试的球体id列表
        
        返回:
            hit_t: 命中点的t值，如果没有命中则返回t_max
            hit_normal: 命中点法线
            hit_point: 命中点坐标
            hit_material_id: 命中的材质ID
            hit_sphere_id: 命中的球体ID
        """
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        hit_sphere_id = -1
        front_face = True
        # 决定要测试哪些球体
        if candidate_ids is None:
            # 没有候选列表，测试所有球体（当前行为）
            for i in range(self.object_count[None]):
                t, normal, point, mat_id, sphere_id, is_front_face= self.hit_single(
                    ray_origin, ray_dir, t_min, closest_t, i
                )
                if t < closest_t:
                    closest_t = t
                    hit_normal = normal
                    hit_point = point
                    hit_material_id = mat_id
                    hit_sphere_id = sphere_id
                    front_face = is_front_face
        else:
            # 只测试候选列表中的球体
            for i in range(candidate_ids.shape[0]):
                sphere_idx = candidate_ids[i]
                t, normal, point, mat_id, sphere_id, is_front_face = self.hit_single(
                    ray_origin, ray_dir, t_min, closest_t, sphere_idx
                )
                if t < closest_t:
                    closest_t = t
                    hit_normal = normal
                    hit_point = point
                    hit_material_id = mat_id
                    hit_sphere_id = sphere_id
                    front_face = is_front_face
        
        return closest_t, hit_normal, hit_point, hit_material_id, hit_sphere_id, front_face
    # 对单个物体求交
    @ti.func
    def hit_single(self, ray_origin, ray_dir, t_min, t_max, sphere_id):
        """单个球体的求交测试,返回4元组"""
        sphere = self.spheres[sphere_id]
        oc = ray_origin - sphere.center
        
        a = ray_dir.dot(ray_dir)
        b = 2.0 * oc.dot(ray_dir)
        c = oc.dot(oc) - sphere.radius_sqr
        
        discriminant = b * b - 4 * a * c
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        front_face = True
        
        if discriminant >= 0:
            sqrt_d = ti.sqrt(discriminant)
            root1 = (-b - sqrt_d) / (2.0 * a)
            root2 = (-b + sqrt_d) / (2.0 * a)
            t = root1
            if not (t_min < root1 < t_max):
                t = root2
            if t_min < t < closest_t:
                closest_t = t
                hit_point = ray_origin + t * ray_dir
                hit_normal = self._get_normal(hit_point, sphere.center, ray_dir)
                hit_material_id = sphere.material_id
                front_face = (ray_dir.dot(hit_point-sphere.center) < 0)
        
        return closest_t, hit_normal, hit_point, hit_material_id, front_face

    @ti.func
    def _get_normal(self, hit_point, center, ray_dir):
        """
        计算法线 - 必须用@ti.func装饰，因为会被@ti.func函数调用
        
        注意：这里我们处理法线方向，确保指向光线来源的反方向
        """
        # 计算外向法线
        outward_normal = (hit_point - center).normalized()
        # 检查光线是从外部还是内部击中
        front_face = ray_dir.dot(outward_normal) < 0
        # 如果是从内部击中，翻转法线
        if not front_face:
            outward_normal=-outward_normal
        return outward_normal

    @ti.func
    def get_sphere(self, sphere_id):
        """获取球体数据 - 必须用@ti.func装饰"""
        return self.spheres[sphere_id]
    
    def get_object_count(self):
        """获取球体数量 - 在Python作用域调用，不需要装饰器"""
        return self.object_count[None]
    
    @ti.func
    def get_bounding_box(self, sphere_id):
        """获取球体的包围盒 - 为BVH准备"""
        sphere = self.spheres[sphere_id]
        radius = sphere.radius
        center = sphere.center
        
        min_point = center - radius
        max_point = center + radius
        # print(f"Bbox of Sphere {sphere_id}:",min_point, "->",max_point)
        return min_point, max_point

@ti.data_oriented
class TriangleSystem:
    def __init__(self, max_triangles=65536):
        self.max_triangles = max_triangles
        self.Triangle = ti.types.struct(
            v0=ti.types.vector(3, ti.f32),
            v1=ti.types.vector(3, ti.f32),
            v2=ti.types.vector(3, ti.f32),
            normal=ti.types.vector(3, ti.f32),  # 预计算法线
            e1=ti.types.vector(3, ti.f32),
            e2=ti.types.vector(3, ti.f32),
            material_id=ti.i32
        )
        self.triangles = self.Triangle.field(shape=(max_triangles,))
        self.object_count = ti.field(ti.i32, shape=())
    
    @ti.kernel
    def set_triangle_params(self,id: ti.i32, 
                        v0x: ti.f32, v0y: ti.f32, v0z: ti.f32,
                        v1x: ti.f32, v1y: ti.f32, v1z: ti.f32,
                        v2x: ti.f32, v2y: ti.f32, v2z: ti.f32,
                        normal_x: ti.f32, normal_y: ti.f32, normal_z: ti.f32,
                        mat_id: ti.i32):
        self.triangles[id].v0 = ti.Vector([v0x, v0y, v0z])
        self.triangles[id].v1 = ti.Vector([v1x, v1y, v1z])
        self.triangles[id].v2 = ti.Vector([v2x, v2y, v2z])
        self.triangles[id].normal = ti.Vector([normal_x, normal_y, normal_z])
        self.triangles[id].material_id = mat_id
        # 预计算边向量，用于求交测试
        self.triangles[id].e1 = self.triangles[id].v1 - self.triangles[id].v0
        self.triangles[id].e2 = self.triangles[id].v2 - self.triangles[id].v0

    def add_triangle(self, v0, v1, v2, material_id):
        """添加三角形到系统"""
        if self.object_count[None] >= self.max_triangles:
            raise ValueError(f"超出最大三角形数量限制: {self.max_triangles}")
        
        triangle_id = self.object_count[None]
        
        # 在Python作用域中计算法线（使用numpy）
        v0_np = np.array(v0)
        v1_np = np.array(v1)
        v2_np = np.array(v2)
        
        # 计算法线
        e1_np = v1_np - v0_np
        e2_np = v2_np - v0_np
        normal_np = np.cross(e1_np, e2_np)
        normal_np = normal_np / np.linalg.norm(normal_np)
        
        # 使用内核设置三角形参数，包括预计算的法线
        self.set_triangle_params(triangle_id, 
                        v0[0], v0[1], v0[2],
                        v1[0], v1[1], v1[2],
                        v2[0], v2[1], v2[2],
                        normal_np[0], normal_np[1], normal_np[2],
                        material_id)
        
        self.object_count[None] += 1
        return triangle_id

    @ti.func
    def intersect(self, ray_origin, ray_dir, t_min, t_max, candidate_ids=None):
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        hit_triangle_id = -1
        front_face = True
        # 决定要测试哪些球体
        if candidate_ids is None:
            # 没有候选列表，测试所有球体（当前行为）
            for i in range(self.object_count[None]):
                t, normal, point, mat_id, triangle_id, is_front_face = self.hit_single(
                    ray_origin, ray_dir, t_min, closest_t, i
                )
                if t < closest_t:
                    closest_t = t
                    hit_normal = normal
                    hit_point = point
                    hit_material_id = mat_id
                    hit_triangle_id = triangle_id
                    front_face = is_front_face
        else:
            # 只测试候选列表中的球体
            for i in range(candidate_ids.shape[0]):
                triangle_idx = candidate_ids[i]
                t, normal, point, mat_id, triangle_id, is_front_face = self.hit_single(
                    ray_origin, ray_dir, t_min, closest_t, triangle_idx
                )
                if t < closest_t:
                    closest_t = t
                    hit_normal = normal
                    hit_point = point
                    hit_material_id = mat_id
                    hit_triangle_id = triangle_id
                    front_face = is_front_face
        
        return closest_t, hit_normal, hit_point, hit_material_id, hit_triangle_id, front_face
    
    @ti.func
    def hit_single(self, ray_origin, ray_dir, t_min, t_max, triangle_id):
        """
        单个三角形求交测试 - Möller–Trumbore算法
        返回: (t, normal, hit_point, material_id, hit_triangle_id, front_face)
        """
        triangle = self.triangles[triangle_id]
        
        # Möller–Trumbore算法
        e1 = triangle.e1
        e2 = triangle.e2
        h = ray_dir.cross(e2)
        a = e1.dot(h)
        
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        front_face = True
        # 检查射线是否与三角形平面平行
        if abs(a) > 1e-8:
            f = 1.0 / a
            s = ray_origin - triangle.v0
            u = f * s.dot(h)
            if 0.0 <= u <= 1.0:
                q = s.cross(e1)
                v = f * ray_dir.dot(q)
                if v >= 0.0 and u + v <= 1.0:
                    t = f * e2.dot(q)
                    # 检查t是否在有效范围内
                    if t_min < t < t_max and t < closest_t:
                        closest_t = t
                        hit_point = ray_origin + t * ray_dir
                        hit_material_id = triangle.material_id
                        # 计算法线方向（考虑光线是从正面还是背面击中）
                        hit_normal = triangle.normal
                        is_front_face = (ray_dir.dot(hit_normal) < 0)
                        front_face = is_front_face
                        if not is_front_face:
                            hit_normal = -hit_normal
        
        return closest_t, hit_normal, hit_point, hit_material_id, front_face

    @ti.func
    def _get_normal(self, triangle_id):
        """
        在Taichi作用域中计算三角形法线
        注意：这主要用于动态更新法线，通常我们使用预计算的法线
        """
        triangle = self.triangles[triangle_id]
        e1 = triangle.v1 - triangle.v0
        e2 = triangle.v2 - triangle.v0
        normal = e1.cross(e2)
        return normal.normalized()

    @ti.func
    def get_bounding_box(self, triangle_id):
        """获取三角形的包围盒 - 为BVH准备"""
        triangle = self.triangles[triangle_id]
        v0 = triangle.v0
        v1 = triangle.v1
        v2 = triangle.v2
        # 计算三个顶点在每个轴上的最小值和最大值
        min_point = ti.Vector([
            min(v0[0], v1[0], v2[0]), min(v0[1], v1[1], v2[1]), min(v0[2], v1[2], v2[2])
        ])
        max_point = ti.Vector([
            max(v0[0], v1[0], v2[0]), max(v0[1], v1[1], v2[1]), max(v0[2], v1[2], v2[2])
        ])
        # print(f"Bbox of Triangle {triangle_id}:",min_point, "->",max_point)
        return min_point, max_point

@ti.data_oriented
class RectangleSystem:
    """改进的矩形构建器 - 支持任意旋转和高效向量化操作"""
    def __init__(self, triangle_system):
        self.triangle_system = triangle_system
    def add_rectangle(self, center, width, height, rotation_angles=[0.0,0.0,0.0], material_id=0):
        """
        添加矩形
        
        参数:
            center: 矩形中心点 [x, y, z]
            width: 宽度
            height: 高度
            rotation_angles: 绕x,y,z轴的旋转角度 [rx, ry, rz]，单位度
            material_id: 材质ID
        """
        # 创建旋转矩阵
        rotation_matrix = self._create_rotation_matrix(*rotation_angles)
        
        # 在局部坐标系中定义矩形的四个顶点
        half_width = width * 0.5
        half_height = height * 0.5
        
        # 使用numpy数组进行向量化计算
        local_vertices = np.array([
            [-half_width, -half_height, 0.0],  # 左下
            [ half_width, -half_height, 0.0],  # 右下
            [ half_width,  half_height, 0.0],  # 右上
            [-half_width,  half_height, 0.0]   # 左上
        ])
        
        # 向量化旋转和平移
        rotated_vertices = np.dot(local_vertices, rotation_matrix.T)
        world_vertices = rotated_vertices + np.array(center)
        
        # 创建两个三角形
        tri1_id = self.triangle_system.add_triangle(
            world_vertices[0], 
            world_vertices[1], 
            world_vertices[2], 
            material_id
        )
        tri2_id = self.triangle_system.add_triangle(
            world_vertices[0], 
            world_vertices[2], 
            world_vertices[3], 
            material_id
        )
        
        return [tri1_id, tri2_id]
    # 创建旋转矩阵
    def _create_rotation_matrix(self, rx_deg, ry_deg, rz_deg):
        """创建绕x,y,z轴旋转的复合旋转矩阵"""
        rx = np.radians(rx_deg)
        ry = np.radians(ry_deg)
        rz = np.radians(rz_deg)
        # 绕x轴旋转矩阵
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])
        # 绕y轴旋转矩阵
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])
        # 绕z轴旋转矩阵
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])
        # 复合旋转矩阵：先绕z轴，再绕y轴，最后绕x轴
        return np.dot(Rx, np.dot(Ry, Rz))

@ti.data_oriented
class CubeSystem:
    """改进的立方体构建器 - 支持长方体和任意旋转"""
    
    def __init__(self, triangle_system):
        self.triangle_system = triangle_system
    
    def add_cuboid(self, center, dimensions, rotation_angles=None, material_id=0):
        """
        添加长方体
        
        参数:
            center: 中心点 [x, y, z]
            dimensions: 长宽高 [length, width, height]
            rotation_angles: 绕x,y,z轴的旋转角度 [rx, ry, rz]，单位度
            material_id: 材质ID
        """
        if rotation_angles is None:
            rotation_angles = [0.0, 0.0, 0.0]
        
        # 创建旋转矩阵
        rotation_matrix = self._create_rotation_matrix(*rotation_angles)
        
        # 提取长宽高
        length, width, height = dimensions
        half_length = length * 0.5
        half_width = width * 0.5
        half_height = height * 0.5
        
        # 在局部坐标系中定义长方体的8个顶点
        local_vertices = np.array([
            # 底面四个顶点
            [-half_length, -half_width, -half_height],  # 0: 左前下
            [ half_length, -half_width, -half_height],  # 1: 右前下
            [ half_length,  half_width, -half_height],  # 2: 右后下
            [-half_length,  half_width, -half_height],  # 3: 左后下
            
            # 顶面四个顶点
            [-half_length, -half_width,  half_height],  # 4: 左前上
            [ half_length, -half_width,  half_height],  # 5: 右前上
            [ half_length,  half_width,  half_height],  # 6: 右后上
            [-half_length,  half_width,  half_height]   # 7: 左后上
        ])
        
        # 向量化旋转和平移
        rotated_vertices = np.dot(local_vertices, rotation_matrix.T)
        world_vertices = rotated_vertices + np.array(center)
        
        # 定义6个面的三角形（每个面2个三角形）
        faces = [
            [0, 1, 2, 0, 2, 3],  
            [4, 5, 6, 4, 6, 7],  
            [0, 4, 5, 0, 5, 1], 
            [2, 3, 7, 2, 7, 6],  
            [0, 3, 7, 0, 7, 4],  
            [1, 2, 6, 1, 6, 5]  
        ]
        
        triangle_ids = []
        for face in faces:
            tri1_id = self.triangle_system.add_triangle(
                world_vertices[face[0]],
                world_vertices[face[1]], 
                world_vertices[face[2]],
                material_id
            )
            tri2_id = self.triangle_system.add_triangle(
                world_vertices[face[3]],
                world_vertices[face[4]],
                world_vertices[face[5]],
                material_id
            )
            triangle_ids.extend([tri1_id, tri2_id])
        
        return triangle_ids
    
    def add_cube(self, center, size, rotation_angles=None, material_id=0):
        """
        添加正方体（长方体的特例）
        
        参数:
            center: 中心点 [x, y, z]
            size: 边长
            rotation_angles: 绕x,y,z轴的旋转角度 [rx, ry, rz]，单位度
            material_id: 材质ID
        """
        return self.add_cuboid(center, [size, size, size], rotation_angles, material_id)
    
    def _create_rotation_matrix(self, rx_deg, ry_deg, rz_deg):
        """创建绕x,y,z轴旋转的复合旋转矩阵（与矩形构建器相同）"""
        rx = np.radians(rx_deg)
        ry = np.radians(ry_deg)
        rz = np.radians(rz_deg)
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])
        return np.dot(Rx, np.dot(Ry, Rz))

# 构建三角网格数据结构
class MeshBuilder:
    """高级网格构建器 - 支持顶点索引，避免重复顶点"""
    
    def __init__(self, triangle_system: TriangleSystem):
        self.triangle_system = triangle_system
        self.vertex_cache = {}  # 顶点哈希缓存
        self.next_vertex_id = 0
    
    def add_mesh(self, vertices, indices, material_id=0):
        """
        添加三角网格
        
        参数:
            vertices: 顶点列表 [[x1,y1,z1], [x2,y2,z2], ...]
            indices: 三角形索引列表 [[v0,v1,v2], [v3,v4,v5], ...]
            material_id: 材质ID
        """
        vertices_np = np.array(vertices)
        indices_np = np.array(indices)
        
        triangle_ids = []
        
        # 批量处理所有三角形
        for tri_indices in indices_np:
            v0 = vertices_np[tri_indices[0]].tolist()
            v1 = vertices_np[tri_indices[1]].tolist()
            v2 = vertices_np[tri_indices[2]].tolist()
            
            tri_id = self.triangle_system.add_triangle(v0, v1, v2, material_id)
            triangle_ids.append(tri_id)
        
        return triangle_ids
    
    def add_mesh_with_normals(self, vertices, normals, indices, material_id=0):
        """
        添加带法线的三角网格（如果三角形系统支持预计算法线）
        
        参数:
            vertices: 顶点列表
            normals: 法线列表
            indices: 三角形索引列表
            material_id: 材质ID
        """
        # 这里可以扩展以支持顶点法线
        # 目前先调用基本方法
        return self.add_mesh(vertices, indices, material_id)
    
    def load_obj_file(self, obj_path, material_id=0, scale=1.0, translation=None):
        """
        从OBJ文件加载网格
        
        参数:
            obj_path: OBJ文件路径
            material_id: 材质ID
            scale: 缩放因子
            translation: 平移向量 [x, y, z]
        """
        vertices = []
        indices = []
        
        with open(obj_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                
                if parts[0] == 'v':  # 顶点
                    vertex = [float(parts[1]) * scale, 
                            float(parts[2]) * scale, 
                            float(parts[3]) * scale]
                    if translation:
                        vertex[0] += translation[0]
                        vertex[1] += translation[1]
                        vertex[2] += translation[2]
                    vertices.append(vertex)
                
                elif parts[0] == 'f':  # 面
                    # 处理面索引（支持不同格式：v, v/vt, v/vt/vn）
                    face_vertices = []
                    for part in parts[1:]:
                        vertex_index = int(part.split('/')[0]) - 1  # OBJ索引从1开始
                        face_vertices.append(vertex_index)
                    
                    # 将多边形分解为三角形
                    for i in range(1, len(face_vertices) - 1):
                        indices.append([face_vertices[0], face_vertices[i], face_vertices[i + 1]])
        
        return self.add_mesh(vertices, indices, material_id)

# 定义图元类型常量
PRIMITIVE_SPHERE = 0
PRIMITIVE_TRIANGLE = 1

@ti.data_oriented
class PrimitiveSystem:
    """统一管理所有图元的系统"""
    
    def __init__(self, max_primitives=100000):
        self.max_primitives = max_primitives
        # 图元数据：类型、在对应系统中的索引、包围盒
        self.primitive_types = ti.field(ti.i32, shape=(max_primitives,))
        self.primitive_indices = ti.field(ti.i32, shape=(max_primitives,))
        self.bbox_mins = ti.Vector.field(3, ti.f32, shape=(max_primitives,))
        self.bbox_maxs = ti.Vector.field(3, ti.f32, shape=(max_primitives,))
        
        self.primitive_count = ti.field(ti.i32, shape=())
        self.primitive_count[None] = 0
        
        # 引用各个几何系统
        self.sphere_system = None
        self.triangle_system = None
    
    def set_geometry_systems(self, sphere_system: SphereSystem, triangle_system: TriangleSystem):
        """设置几何系统引用"""
        self.sphere_system = sphere_system
        self.triangle_system = triangle_system
    
    def add_sphere(self, sphere_id):
        """添加球体图元（Python层面的接口）"""
        idx = self.primitive_count[None]
        if idx >= self.max_primitives:
            raise ValueError("超出最大图元数量限制")
        # 调用Taichi内核，在Taichi作用域中获取包围盒并设置图元
        self._add_sphere_kernel(idx, sphere_id)
        self.primitive_count[None] += 1

    @ti.kernel
    def _add_sphere_kernel(self, prim_idx: ti.i32, sphere_id: ti.i32):
        """Taichi内核：实际执行包围盒获取和图元设置（Taichi作用域）"""
        # 现在可以安全调用@ti.func装饰的get_bounding_box
        min_point, max_point = self.sphere_system.get_bounding_box(sphere_id)
        
        self.primitive_types[prim_idx] = PRIMITIVE_SPHERE
        self.primitive_indices[prim_idx] = sphere_id
        self.bbox_mins[prim_idx] = min_point
        self.bbox_maxs[prim_idx] = max_point
    
    def add_triangle(self, triangle_id):
        """添加三角形图元"""
        idx = self.primitive_count[None]
        if idx >= self.max_primitives:
            raise ValueError("超出最大图元数量限制")
        # 获取三角形的包围盒
        self._add_triangle_kernel(idx, triangle_id)
        self.primitive_count[None] += 1
    
    @ti.kernel
    def _add_triangle_kernel(self, idx: ti.i32, triangle_id: ti.i32):
        min_point, max_point = self.triangle_system.get_bounding_box(triangle_id)
        self.primitive_types[idx] = PRIMITIVE_TRIANGLE
        self.primitive_indices[idx] = triangle_id
        self.bbox_mins[idx] = min_point
        self.bbox_maxs[idx] = max_point

    @ti.func
    def intersect_primitive(self, ray_origin, ray_dir, t_min, t_max, primitive_id):
        """单个图元的求交测试"""
        prim_type = self.primitive_types[primitive_id]
        prim_index = self.primitive_indices[primitive_id]
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        front_face = True
        if prim_type == PRIMITIVE_SPHERE:
            closest_t, hit_normal, hit_point, hit_material_id, front_face = self.sphere_system.hit_single(ray_origin, ray_dir, t_min, t_max, prim_index)
        else:  # PRIMITIVE_TRIANGLE
            closest_t, hit_normal, hit_point, hit_material_id, front_face = self.triangle_system.hit_single(ray_origin, ray_dir, t_min, t_max, prim_index)
        return closest_t, hit_normal, hit_point, hit_material_id, front_face
    
    # 在PrimitiveSystem中添加
    @ti.func
    def intersect_all(self, ray_origin, ray_dir, t_min, t_max):
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        front_face = True
        for i in range(self.primitive_count[None]):
            t, normal, point, mat_id, is_front_face = self.intersect_primitive(ray_origin, ray_dir, t_min, closest_t, i)
            if t < closest_t:
                closest_t = t
                hit_normal = normal
                hit_point = point
                hit_material_id = mat_id
                front_face = is_front_face
        return closest_t, hit_normal, hit_point, hit_material_id, front_face

    @ti.func
    def get_primitive_bbox(self, primitive_id):
        """获取图元的包围盒"""
        return self.bbox_mins[primitive_id], self.bbox_maxs[primitive_id]

@ti.data_oriented
class BVHSystem:
    """BVH加速结构"""
    def __init__(self, max_nodes=200000):
        self.max_nodes = max_nodes
        # BVH节点数据结构
        self.BVHNode = ti.types.struct(
            bbox_min=ti.types.vector(3, ti.f32),
            bbox_max=ti.types.vector(3, ti.f32),
            left_child=ti.i32,      # 左子节点索引
            right_child=ti.i32,     # 右子节点索引
            primitive_count=ti.i32, # 叶子节点中的图元数量
            primitive_offset=ti.i32 # 叶子节点中第一个图元的索引
        )
        self.nodes = self.BVHNode.field(shape=(max_nodes,))
        self.node_count = ti.field(ti.i32, shape=())
        # 图元索引列表（用于叶子节点）
        self.primitive_indices = ti.field(ti.i32, shape=(max_nodes * 2,))  # 粗略估计
        self.primitive_indices_count = ti.field(ti.i32, shape=())
        
        self.node_count[None] = 0
        self.primitive_indices_count[None] = 0
    
    def build_bvh(self, primitive_system):
        """构建BVH（在CPU上执行）"""
        # 收集所有图元的包围盒
        primitives = []
        for i in range(primitive_system.primitive_count[None]):
            bbox_min = primitive_system.bbox_mins[i].to_numpy()
            bbox_max = primitive_system.bbox_maxs[i].to_numpy()
            # 计算图元中心，用于排序
            center = (bbox_min + bbox_max) / 2
            primitives.append({
                'bbox_min': bbox_min,
                'bbox_max': bbox_max,
                'center': center,
                'index': i
            })
        # 递归构建BVH（使用空间轴划分）
        root_index = self._build_bvh_recursive(primitives, 0, len(primitives))
        
        return root_index
    
    @ti.kernel
    def create_internal_node(self, idx: ti.i32, min_x: ti.f32, min_y: ti.f32, min_z: ti.f32,
                            max_x: ti.f32, max_y: ti.f32, max_z: ti.f32,
                            left: ti.i32, right: ti.i32):
        self.nodes[idx].bbox_min = ti.Vector([min_x, min_y, min_z])
        self.nodes[idx].bbox_max = ti.Vector([max_x, max_y, max_z])
        self.nodes[idx].left_child = left
        self.nodes[idx].right_child = right
        self.nodes[idx].primitive_count = 0
        self.nodes[idx].primitive_offset = -1

    @ti.kernel
    def create_leaf_node(self, idx: ti.i32, min_x: ti.f32, min_y: ti.f32, min_z: ti.f32,
                         max_x: ti.f32, max_y: ti.f32, max_z: ti.f32,
                         prim_start: ti.i32, prim_count: ti.i32):
        self.nodes[idx].bbox_min = ti.Vector([min_x, min_y, min_z])
        self.nodes[idx].bbox_max = ti.Vector([max_x, max_y, max_z])
        self.nodes[idx].left_child = -1
        self.nodes[idx].right_child = -1
        self.nodes[idx].primitive_count = prim_count
        self.nodes[idx].primitive_offset = prim_start

    def _build_bvh_recursive(self, primitives, start, end, depth=0):
        """递归构建BVH（核心改进：按空间最长轴拆分）"""
        if start >= end:
            return -1
        
        node_index = self.node_count[None]
        self.node_count[None] += 1
        if self.node_count[None] >= self.max_nodes:
            raise ValueError("BVH节点数量超出最大值限制")
        
        # 1. 计算当前节点的总包围盒（合并所有图元的包围盒）
        bbox_min = np.array([float('inf'), float('inf'), float('inf')])
        bbox_max = np.array([float('-inf'), float('-inf'), float('-inf')])
        
        for i in range(start, end):
            prim = primitives[i]
            bbox_min = np.minimum(bbox_min, prim['bbox_min'])
            bbox_max = np.maximum(bbox_max, prim['bbox_max'])
        
        # 2. 终止条件：图元数量少或深度过大时创建叶子节点
        if (end - start) <= 4 or depth >= 20:
            # 存储图元索引（Python层面操作）
            prim_offset = self.primitive_indices_count[None]
            for i in range(start, end):
                self.primitive_indices[self.primitive_indices_count[None]] = primitives[i]['index']
                self.primitive_indices_count[None] += 1
            # 调用Taichi内核创建叶子节点（从Python到Taichi的交互）
            self.create_leaf_node(
                node_index,
                bbox_min[0], bbox_min[1], bbox_min[2],
                bbox_max[0], bbox_max[1], bbox_max[2],
                prim_offset, end - start
            )
            
            return node_index
        
        # 3. 核心改进：按空间最长轴拆分
        # 3.1 计算包围盒在三个轴上的长度
        extent = bbox_max - bbox_min
        longest_axis = 0  # 0=x, 1=y, 2=z
        if extent[1] > extent[longest_axis]:
            longest_axis = 1
        if extent[2] > extent[longest_axis]:
            longest_axis = 2
        
        # 3.2 按最长轴的中心坐标排序图元（Python层面排序）
        # 注意：Taichi kernel中不适合做复杂排序，因此在Python层面完成
        primitives_sorted = primitives[start:end]
        # 按图元中心在最长轴上的坐标排序
        primitives_sorted.sort(key=lambda p: p['center'][longest_axis])
        # 将排序结果写回原列表
        primitives[start:end] = primitives_sorted
        
        # 3.3 按排序后的中点拆分
        mid = start + (end - start) // 2  # 中点位置
        
        # 4. 递归构建左右子树
        left_child = self._build_bvh_recursive(primitives, start, mid, depth + 1)
        right_child = self._build_bvh_recursive(primitives, mid, end, depth + 1)
        
        # 5. 创建内部节点（通过Taichi内核）
        self.create_internal_node(
            node_index,
            bbox_min[0], bbox_min[1], bbox_min[2],
            bbox_max[0], bbox_max[1], bbox_max[2],
            left_child, right_child
        )
        
        return node_index
    
    @ti.func
    def intersect_bvh(self, ray_origin, ray_dir, t_min, t_max, primitive_system, node_index):
        """BVH遍历求交"""
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        front_face = True
        # 使用堆栈进行迭代遍历（避免递归）,注意每个线程自己的堆栈必须独立！！！！
        stack = ti.Vector([-1] * 64, dt=ti.i32)
        stack[0] = node_index
        stack_size = 1
        while stack_size > 0:
            stack_size -= 1
            current_node_idx = stack[stack_size]
            node = self.nodes[current_node_idx]
            # 检查光线与节点包围盒是否相交
            if self.ray_aabb_intersect(ray_origin, ray_dir, node.bbox_min, node.bbox_max, t_min, closest_t):
                if node.primitive_count > 0:
                    # 叶子节点：与所有图元求交
                    for i in range(node.primitive_offset, node.primitive_offset + node.primitive_count):
                        prim_id = self.primitive_indices[i]
                        t, normal, point, mat_id, is_front_face = primitive_system.intersect_primitive(
                            ray_origin, ray_dir, t_min, closest_t, prim_id
                        )
                        if t < closest_t:
                            closest_t = t
                            hit_normal = normal
                            hit_point = point
                            hit_material_id = mat_id
                            front_face = is_front_face
                else:
                    # 内部节点：将子节点加入堆栈
                    if node.right_child != -1:
                        stack[stack_size] = node.right_child
                        stack_size += 1
                    if node.left_child != -1:
                        stack[stack_size] = node.left_child
                        stack_size += 1
        
        return closest_t, hit_normal, hit_point, hit_material_id, front_face
    
    @ti.func
    def ray_aabb_intersect(self, ray_origin, ray_dir, bbox_min, bbox_max, t_min, t_max):
        """光线与AABB包围盒求交测试"""
        # 使用slab方法
        inv_dir = 1.0 / ray_dir
        t0 = (bbox_min - ray_origin) * inv_dir
        t1 = (bbox_max - ray_origin) * inv_dir
        
        t_small = ti.min(t0, t1)
        t_large = ti.max(t0, t1)
        
        t_near = ti.max(t_small[0], t_small[1], t_small[2], t_min)
        t_far = ti.min(t_large[0], t_large[1], t_large[2], t_max)
        
        return t_near <= t_far

@ti.data_oriented
class SceneManager:
    """更新后的场景管理器"""
    
    def __init__(self):
        # 核心几何系统
        self.sphere_system = SphereSystem()
        self.triangle_system = TriangleSystem()
        # 几何构建器
        self.rectangle_builder = RectangleSystem(self.triangle_system)
        self.cube_builder = CubeSystem(self.triangle_system)
        self.mesh_builder = MeshBuilder(self.triangle_system)
        
        # 统一图元系统（用于BVH）
        self.primitive_system = PrimitiveSystem()
        self.primitive_system.set_geometry_systems(
            self.sphere_system, self.triangle_system
        )
        
        # BVH系统
        self.bvh_system = BVHSystem()
        self.bvh_root = -1
    
    def add_sphere(self,center, radius, material_id):
        return self.sphere_system.add_sphere(center, radius, material_id)

    def add_rectangle(self, center, width, height, rotation_angles=None, material_id=0):
        """添加矩形"""
        return self.rectangle_builder.add_rectangle(center, width, height, rotation_angles, material_id)
    
    def add_cube(self, center, size, rotation_angles=None, material_id=0):
        """添加正方体"""
        return self.cube_builder.add_cube(center, size, rotation_angles, material_id)
    
    def add_cuboid(self, center, dimensions, rotation_angles=None, material_id=0):
        """添加长方体"""
        return self.cube_builder.add_cuboid(center, dimensions, rotation_angles, material_id)
    
    def add_mesh(self, vertices, indices, material_id=0):
        """添加三角网格"""
        return self.mesh_builder.add_mesh(vertices, indices, material_id)
    
    def load_obj_model(self, obj_path, material_id=0, scale=1.0, translation=None):
        """从OBJ文件加载模型"""
        return self.mesh_builder.load_obj_file(obj_path, material_id, scale, translation)
    
    def build_bvh(self):
        """构建场景的BVH"""
        # 注册所有图元到统一系统
        for i in range(self.sphere_system.object_count[None]):
            self.primitive_system.add_sphere(i)
        
        for i in range(self.triangle_system.object_count[None]):
            self.primitive_system.add_triangle(i)
        
        # 构建BVH
        # self.bvh_root = self.bvh_system.build_bvh(self.primitive_system)
    
    @ti.func
    def intersect_scene(self, ray_origin, ray_dir, t_min, t_max):
        """场景级求交"""
        closest_t = t_max
        hit_normal = ti.Vector([0.0, 0.0, 0.0])
        hit_point = ti.Vector([0.0, 0.0, 0.0])
        hit_material_id = -1
        front_face = True
        if self.bvh_root != -1:
            closest_t, hit_normal, hit_point, hit_material_id, front_face = self.bvh_system.intersect_bvh(
                ray_origin, ray_dir, t_min, t_max, 
                self.primitive_system, self.bvh_root
            )
        else:
            closest_t, hit_normal, hit_point, hit_material_id, front_face = self.primitive_system.intersect_all(
                ray_origin, ray_dir, t_min, t_max
            )
        return closest_t, hit_normal, hit_point, hit_material_id, front_face

@ti.data_oriented
class Camera:
    """支持任意位置和方向的摄像机类"""  
    def __init__(self, lookfrom, lookat, up, fov, aspect_ratio):
        """
        参数:
            lookfrom: 摄像机位置 [x, y, z]
            lookat: 观察目标点 [x, y, z] 
            up: 摄像机上方向 [x, y, z]
            fov: 垂直视场角(角度)
            aspect_ratio: 宽高比 (width / height)
        """
        self.lookfrom = ti.Vector(lookfrom)
        self.lookat = ti.Vector(lookat)
        self.up = ti.Vector(up)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        # 在Taichi字段中存储摄像机参数
        self.origin = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.lower_left_corner = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.horizontal = ti.Vector.field(3, dtype=ti.f32, shape=())
        self.vertical = ti.Vector.field(3, dtype=ti.f32, shape=())
        
        # 初始化摄像机坐标系
        self._setup_camera()
    
    def _setup_camera(self):
        """设置摄像机坐标系 - 在Python作用域执行"""
        lookfrom_np = np.array(self.lookfrom)
        lookat_np = np.array(self.lookat)
        up_np = np.array(self.up)
        
        # 计算摄像机坐标系
        w = (lookfrom_np - lookat_np) / np.linalg.norm(lookfrom_np - lookat_np)
        u = np.cross(up_np, w) / np.linalg.norm(np.cross(up_np, w))
        v = np.cross(w, u)
        
        # 计算视口尺寸
        theta = np.radians(self.fov)
        half_height = np.tan(theta / 2)
        half_width = self.aspect_ratio * half_height
        
        # 计算视口角点
        self.origin[None] = self.lookfrom
        self.horizontal[None] = ti.Vector([2 * half_width * u[0], 2 * half_width * u[1], 2 * half_width * u[2]])
        self.vertical[None] = ti.Vector([2 * half_height * v[0], 2 * half_height * v[1], 2 * half_height * v[2]])
        self.lower_left_corner[None] = (
            self.origin[None] - 
            self.horizontal[None] * 0.5 - 
            self.vertical[None] * 0.5 - 
            ti.Vector([w[0], w[1], w[2]])
        )
    @ti.func
    def get_ray(self, u, v):
        """生成光线 - 在Taichi作用域中执行"""
        direction = (
            self.lower_left_corner[None] + 
            u * self.horizontal[None] + 
            v * self.vertical[None] - 
            self.origin[None]
        )
        return self.origin[None], direction.normalized()


@ti.data_oriented
class PathTracer:
    """路径追踪渲染器"""
    def __init__(self, width, height, max_depth=50, samples_per_pixel=100):
        self.width = width
        self.height = height
        self.max_depth = max_depth
        self.samples_per_pixel = samples_per_pixel
        # 渲染结果存储
        self.frame_buffer = ti.Vector.field(3, dtype=ti.f32, shape=(width, height))
        self.sample_count = ti.field(ti.i32, shape=())
    
    @ti.func
    def ray_color(self, ray_origin, ray_dir, scene_manager, material_manager, depth):
        """计算光线颜色 - 核心路径追踪算法"""
        color = ti.Vector([0.0, 0.0, 0.0])
        attenuation = ti.Vector([1.0, 1.0, 1.0])
        
        current_ray_origin = ray_origin
        current_ray_dir = ray_dir
        for bounce in range(depth):
            # 光线与场景求交
            t, normal, hit_point, mat_id, front_face = scene_manager.intersect_scene(
                current_ray_origin, current_ray_dir, 0.01, 1000.0
            )
            if 0.001 < t < 1000:
                # 命中物体，处理材质散射
                # print("hit")
                scattered_dir, scatter_attenuation, emitted, should_scatter = material_manager.scatter_ray(
                    current_ray_dir, normal, hit_point, mat_id, 
                    0,
                    front_face
                )
                # 累加发光材质的贡献
                color += attenuation * emitted
                if should_scatter:
                    # 更新光线继续追踪
                    attenuation *= scatter_attenuation
                    current_ray_origin = hit_point
                    current_ray_dir = scattered_dir
                else:
                    # 光线被吸收（如光源）
                    break
            else:
                # 未命中，使用背景色
                background_color = ti.Vector([0.01, 0.01, 0.01])
                color += attenuation * background_color
                break
        return color
    
    @ti.kernel
    def render_frame(self, camera_origin: ti.template(), camera_lower_left: ti.template(), 
                    camera_horizontal: ti.template(), camera_vertical: ti.template(),
                    scene_manager: ti.template(), material_manager: ti.template()):
        """渲染一帧 - Taichi内核"""
        for i, j in self.frame_buffer:
            pixel_color = ti.Vector([0.0, 0.0, 0.0])
            # 多重采样抗锯齿
            for sample in range(self.samples_per_pixel):
                u = (i + ti.random()) / self.width
                v = (j + ti.random()) / self.height
                
                # 生成光线
                ray_origin, ray_dir = (
                    camera_origin[None], camera_lower_left[None] + u * camera_horizontal[None] + v * camera_vertical[None] - camera_origin[None]
                )
                ray_dir = ray_dir.normalized()
                # 路径追踪
                pixel_color += self.ray_color(
                    ray_origin, ray_dir, scene_manager, material_manager, self.max_depth
                )
            
            # 平均颜色并gamma校正
            scale = 1.0 / self.samples_per_pixel
            r = ti.sqrt(pixel_color[0] * scale)
            g = ti.sqrt(pixel_color[1] * scale) 
            b = ti.sqrt(pixel_color[2] * scale)
            
            self.frame_buffer[i, j] = ti.Vector([r, g, b])
        
        self.sample_count[None] += 1
    
    def render(self, camera, scene_manager, material_manager, save_path=None):
        """执行渲染"""
        print(f"开始渲染: {self.width}x{self.height}, {self.samples_per_pixel}采样/像素")
        # 渲染帧
        self.render_frame(
            camera.origin, camera.lower_left_corner, 
            camera.horizontal, camera.vertical,
            scene_manager, material_manager
        )
        # 保存结果
        if save_path:
            self.save_image(save_path)
        return self.get_image()
    
    def get_image(self):
        """获取渲染图像"""
        return self.frame_buffer.to_numpy().transpose(1, 0, 2)
    
    def save_image(self, filename):
        """保存图像到文件"""
        import matplotlib.pyplot as plt
        
        img = self.get_image()
        img = np.flipud(img)
        img = np.clip(img, 0.0, 1.0)
        plt.imsave(filename, img)
        print(f"图像已保存: {filename}")

# ==================== 使用示例 ====================
def create_cornell_box():
    """创建经典的Cornell Box场景"""
    print("正在构建Cornell Box场景...")
    # 创建场景和材质管理器
    scene_manager = SceneManager()
    material_manager = SceneMaterialManager()
    # ==================== 创建材质 ====================
    # 墙壁材质
    red_wall_id = material_manager.add_custom_lambertian([0.9, 0.05, 0.05])      # 左墙红色
    green_wall_id = material_manager.add_custom_lambertian([0.12, 0.45, 0.15])    # 右墙绿色
    white_wall_id = material_manager.get_material_id("white")                     # 其他墙白色
    # 物体材质
    white_diffuse_id = material_manager.get_material_id("white")                  # 白色漫反射
    # 光源材质
    light_intensity = 8.0
    light_mat_id = material_manager.add_custom_light([1.0, 1.0, 1.0], light_intensity)
    # ==================== 构建房间 ====================
    room_size = 10.0
    half_size = room_size / 2
    # 地板 (y = -5)
    scene_manager.add_rectangle(
        center=[0, -half_size, 0],
        width=room_size,
        height=room_size,
        rotation_angles=[90, 0, 0],  # 水平放置
        material_id=white_wall_id
    )
    # 天花板 (y = 5) 
    scene_manager.add_rectangle(
        center=[0, half_size, 0],
        width=room_size,
        height=room_size,
        rotation_angles=[90, 0, 0],  # 翻转使其朝下
        material_id=white_wall_id
    )
    # 后墙 (z = -5)
    scene_manager.add_rectangle(
        center=[0, 0, -half_size],
        width=room_size,
        height=room_size,
        rotation_angles=[0, 0, 0],  # 垂直放置，朝向房间内部
        material_id=white_wall_id
    )
    # 左墙 (x = -5) - 红色
    scene_manager.add_rectangle(
        center=[-half_size, 0, 0],
        width=room_size,
        height=room_size,
        rotation_angles=[0, -90, 0],  # 垂直放置，朝向房间内部
        material_id=red_wall_id
    )
    # 右墙 (x = 5) - 绿色  
    scene_manager.add_rectangle(
        center=[half_size, 0, 0],
        width=room_size,
        height=room_size,
        rotation_angles=[0, -90, 0],  # 垂直放置，朝向房间内部
        material_id=green_wall_id
    )
    # ==================== 添加光源 ====================
    # 天花板上的发光矩形
    light_size = 4.0
    scene_manager.add_rectangle(
        center=[0, half_size - 0.01, 0], width=light_size, height=light_size, rotation_angles=[90, 0, 0], material_id=light_mat_id
    )
    
    scene_manager.add_sphere([2,-4,3],1,5)
    # ==================== 添加几何物体 ====================
    
    # 正方体 (绕y轴顺时针旋转30度)
    cube_size = 3
    scene_manager.add_cube(
        center=[-1.8, -half_size + cube_size/2, 1], size=cube_size, rotation_angles=[0, -10, 0], material_id=0
    )
    
    # # 长方体 (绕y轴逆时针旋转20度)尺寸: 长(x)1.5, 高(y)2.5, 宽(z)1.5
    cuboid_dims = [3, 5, 3]
    scene_manager.add_cuboid(
        center=[1.6, -half_size + cuboid_dims[1]/2, -0.5],  # 放在地板上
        dimensions=cuboid_dims,
        rotation_angles=[0, 20, 0],  # 绕y轴逆时针旋转20度
        material_id=white_diffuse_id
    )
    

    
    # ==================== 构建加速结构 ====================
    print("正在构建BVH加速结构...")
    scene_manager.build_bvh()
    # 输出场景统计信息
    print(f"\nCornell Box构建完成:")
    print(f"- 球体数量: {scene_manager.sphere_system.object_count[None]}")
    print(f"- 三角形数量: {scene_manager.triangle_system.object_count[None]}")
    print(f"- 图元总数: {scene_manager.primitive_system.primitive_count[None]}")
    print(f"- BVH节点数量: {scene_manager.bvh_system.node_count[None]}")
    return scene_manager, material_manager

def render_cornell_box():
    """渲染Cornell Box场景"""
    # 创建场景
    scene_manager, material_manager = create_cornell_box()
    
    # 设置摄像机参数
    lookfrom = [0, 0, 15]          # 摄像机位置
    lookat = [0, 0, -5]            # 看向房间中心
    up = [0, 1, 0]                 # 上方向
    fov = 60                       # 视场角
    aspect_ratio = 1.0             # 1:1 宽高比
    
    # 创建摄像机
    camera = Camera(lookfrom, lookat, up, fov, aspect_ratio)
    
    # 创建渲染器 (降低分辨率用于测试)
    width, height = 800, 800
    samples_per_pixel = 1600  # 测试时使用较少采样
    max_depth = 20
    
    renderer = PathTracer(width, height, max_depth, samples_per_pixel)
    
    # 执行渲染
    print("开始路径追踪渲染...")
    image = renderer.render(camera, scene_manager, material_manager, "cornell_box.png")
    
    print("渲染完成!")
    return image


# 在main函数中调用
if __name__ == "__main__":

    start=time.time()

    # 测试渲染
    cornell_image = render_cornell_box()
    
    end=time.time()
    print('running time', end-start, 's')
    # 可以添加实时预览或渐进式渲染功能
    # progressive_render()  # 可选：渐进式渲染