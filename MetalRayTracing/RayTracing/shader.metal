//
//  shader.metal
//  RayTraceRender
//
//  Created by 李智成 on 2025/10/5.
//

#include <metal_stdlib>
using namespace metal;

float radians(float deg) { return deg * 0.017453292519943295; } // π/180

struct Uniforms {
    uint width;
    uint height;
    uint frameIndex;
};

// simple rng: xorshift
uint wang_hash(uint seed) {
    seed = (seed ^ 61u) ^ (seed >> 16);
    seed *= 9u;
    seed = seed ^ (seed >> 4);
    seed *= 0x27d4eb2du;
    seed = seed ^ (seed >> 15);
    return seed;
}

float randf(thread uint &state) {
    state = wang_hash(state);
    return (float)(state & 0x00FFFFFFu) / (float)0x01000000u;
}

struct Sphere { float3 center; float radius; float3 color; float emission; int material; };

// very small scene encoded in shader for simplicity
constant Sphere sceneSpheres[] = {
    { float3(0.0, -100.5, -1.0), 100.0, float3(0.8,0.8,0.8), 0.0, 0 },
    { float3(0.0, 0.0, -1.0), 0.5, float3(0.1,0.2,0.5), 0.0, 0 },
    { float3(1.0, 0.0, -1.0), 0.5, float3(0.8,0.6,0.2), 0.0, 0 },
    { float3(-1.0, 0.0, -1.0), 0.5, float3(0.8,0.8,0.8), 0.0, 0 }
};


bool hit_sphere(const constant Sphere &s, float3 ro, float3 rd, thread float &t) {
    float3 oc = ro - s.center;
    float a = dot(rd, rd);
    float b = dot(oc, rd);
    float c = dot(oc, oc) - s.radius*s.radius;
    float discriminant = b*b - a*c;
    if (discriminant > 0) {
        float temp = (-b - sqrt(discriminant)) / a;
        if (temp > 0.001) { t = temp; return true; }
        temp = (-b + sqrt(discriminant)) / a;
        if (temp > 0.001) { t = temp; return true; }
    }
    return false;
}


struct Box {
    float3 minCorner;
    float3 maxCorner;
    float3 color;
    float emission;
    int material;
};

constant Box sceneBoxes[] = {
    { float3(-2.0, -0.5, -3.0), float3(2.0, 0.0, 1.0), float3(0.8, 0.8, 0.8), 0.0, 0 }
};

bool hit_box(const constant Box &b, float3 ro, float3 rd, thread float &t) {
    float3 invD = 1.0 / rd;
    float3 t0s = (b.minCorner - ro) * invD;
    float3 t1s = (b.maxCorner - ro) * invD;
    float3 tsmaller = min(t0s, t1s);
    float3 tbigger  = max(t0s, t1s);
    float tmin = max(max(tsmaller.x, tsmaller.y), tsmaller.z);
    float tmax = min(min(tbigger.x, tbigger.y), tbigger.z);
    if (tmax >= max(tmin, 0.001)) {
        t = tmin > 0.001 ? tmin : tmax;
        return true;
    }
    return false;
}


kernel void pathtrace_kernel(texture2d<float, access::read_write> accum [[texture(0)]], texture2d<float, access::write> outTex [[texture(1)]], constant Uniforms &u [[buffer(0)]], uint2 gid [[thread_position_in_grid]])
{
    uint y = u.height - 1 - gid.y;
    uint2 pix = uint2(gid.x, y);
    
    if (gid.x >= u.width || gid.y >= u.height) return;
    uint seed = gid.x * 1973u + gid.y * 9277u + u.frameIndex * 26699u + 1u;
    float3 ro = float3(0.0,0.0,3.0);
    float3 lookat = float3(0.0,0.0,-1.0);
    float3 up = float3(0.0,1.0,0.0);
    float fov = 45.0;
    float aspect = float(u.width)/float(u.height);

    float3 forward = normalize(lookat - ro);
    float3 right = normalize(cross(forward, up));
    float3 realup = cross(right, forward);

    float u1 = ( (float(gid.x) + randf(seed)) / float(u.width) )*2.0 - 1.0;
    float v1 = ( (float(gid.y) + randf(seed)) / float(u.height) )*2.0 - 1.0;
    u1 *= aspect * tan(radians(fov*0.5));
    v1 *= tan(radians(fov*0.5));

    float3 rd = normalize(u1*right + v1*realup + forward);

    float3 radiance = float3(0.0);
    float3 throughput = float3(1.0);

    for (int bounce=0;bounce<20;bounce++) {
        float nearest = 1e20;
        int hitIndex = -1;
        float t = 0.0;
        // check spheres
        for (uint i=0;i<sizeof(sceneSpheres)/sizeof(Sphere);++i) {
            if (hit_sphere(sceneSpheres[i], ro, rd, t)) {
                if (t < nearest) { nearest = t; hitIndex = int(i); }
            }
        }
        
        if (hitIndex == -1) {
            // sky
            float tsky = 0.5*(rd.y+1.0);
            float3 col = mix(float3(1.0,1.0,1.0), float3(0.5,0.7,1.0), tsky);
            radiance += throughput * col;
            break;
        }
        Sphere s = sceneSpheres[hitIndex];
        float3 hitPos = ro + nearest*rd;
        float3 normal = normalize(hitPos - s.center);

        // simple lambertian bounce
        float3 target = hitPos + normal + float3(randf(seed), randf(seed), randf(seed));
        rd = normalize(target - hitPos);
        ro = hitPos + 0.001*normal; // offset

        throughput *= s.color;
        // if sphere has emission
        if (s.emission > 0.0) {
            radiance += throughput * s.emission;
            break;
        }
    }

    // read previous accumulation
    float4 prev = accum.read(pix);
    float3 prevCol = prev.xyz;
    float3 col = prevCol * float(u.frameIndex-1) + radiance;
    float inv = 1.0/float(u.frameIndex);
    float3 avg = col * inv;

    // write to accum (HDR, keep high precision)
    accum.write(float4(avg, 1.0), pix);

    // clamp for LDR output and write to outTex (matches bgra8Unorm)
    float3 clamped = clamp(avg, 0.0, 1.0);
    outTex.write(float4(clamped, 1.0), pix);
}


