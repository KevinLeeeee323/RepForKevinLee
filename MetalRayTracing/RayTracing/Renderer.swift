//
//  Renderer.swift
//  RayTraceRender
//
//  Created by 李智成 on 2025/10/5.
//


//This is a single-file starter project scaffold for a Mac app using Swift + Metal that implements a simple GPU path tracer (spheres, lambertian, emissive). The content below contains multiple source files concatenated — copy each section into the corresponding file in an Xcode macOS "App" (Swift) target.

import MetalKit
import simd

struct Uniforms {
    var width: UInt32
    var height: UInt32
    var frameIndex: UInt32
}

class Renderer: NSObject, MTKViewDelegate {
    let device: MTLDevice
    let queue: MTLCommandQueue
    let library: MTLLibrary
    var pipeline: MTLComputePipelineState
    var outTexture: MTLTexture!
    var accumTexture: MTLTexture!
    var uniformsBuffer: MTLBuffer
    var frameIndex: UInt32 = 0
    weak var view: MTKView?

    init(metalView: MTKView) {
        guard let dev = metalView.device else { fatalError() }
        device = dev
        queue = device.makeCommandQueue()!
        library = try! device.makeDefaultLibrary(bundle: .main)
        let kernel = library.makeFunction(name: "pathtrace_kernel")!
        pipeline = try! device.makeComputePipelineState(function: kernel)
        view = metalView

        // initial textures
        let w = Int(metalView.drawableSize.width)
        let h = Int(metalView.drawableSize.height)
//        let desc = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: .rgba16Float, width: max(1,w), height: max(1,h), mipmapped: false)
//        desc.usage = [.shaderRead, .shaderWrite]
//        accumTexture = device.makeTexture(descriptor: desc)
//        outTexture = device.makeTexture(descriptor: desc)

        // accumTexture: high-precision float for accumulation
        let descAccum = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: .rgba16Float,
            width: max(1, w),
            height: max(1, h),
            mipmapped: false)
        descAccum.usage = [.shaderRead, .shaderWrite]
        accumTexture = device.makeTexture(descriptor: descAccum)

        // outTexture: match MTKView drawable pixel format (usually .bgra8Unorm)
        let descOut = MTLTextureDescriptor.texture2DDescriptor(
            pixelFormat: metalView.colorPixelFormat, // <-- match drawable format
            width: max(1, w),
            height: max(1, h),
            mipmapped: false)
        descOut.usage = [.shaderWrite, .shaderRead]
        outTexture = device.makeTexture(descriptor: descOut)
        
        uniformsBuffer = device.makeBuffer(length: MemoryLayout<Uniforms>.stride, options: [])!

        super.init()
    }

    func mtkView(_ view: MTKView, drawableSizeWillChange size: CGSize) {
        // recreate textures
        let w = Int(size.width)
        let h = Int(size.height)
//        let desc = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: .rgba16Float, width: max(1,w), height: max(1,h), mipmapped: false)
//        desc.usage = [.shaderRead, .shaderWrite]
//        accumTexture = device.makeTexture(descriptor: desc)
//        outTexture = device.makeTexture(descriptor: desc)
//        resetAccumulation()
        
        let descAccum = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: .rgba16Float,
                                                                 width: max(1, w),
                                                                 height: max(1, h),
                                                                 mipmapped: false)
        descAccum.usage = [.shaderRead, .shaderWrite]
        accumTexture = device.makeTexture(descriptor: descAccum)

        // outTexture: match view's drawable format
        let descOut = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: view.colorPixelFormat,
           width: max(1, w),
           height: max(1, h),
           mipmapped: false)
        descOut.usage = MTLTextureUsage([.shaderWrite, .shaderRead])
        outTexture = device.makeTexture(descriptor: descOut)

        resetAccumulation()
    }

    func draw(in view: MTKView) {
        guard let drawable = view.currentDrawable else { return }
        if frameIndex < 2000 { frameIndex += 1 } // 最多累积 32 帧

        var u = Uniforms(width: UInt32(outTexture.width), height: UInt32(outTexture.height), frameIndex: frameIndex)
        memcpy(uniformsBuffer.contents(), &u, MemoryLayout<Uniforms>.stride)

        let cmdBuf = queue.makeCommandBuffer()!
        let encoder = cmdBuf.makeComputeCommandEncoder()!
        encoder.setComputePipelineState(pipeline)
        encoder.setTexture(accumTexture, index: 0)
        encoder.setTexture(outTexture, index: 1)
        encoder.setBuffer(uniformsBuffer, offset: 0, index: 0)

        let w = pipeline.threadExecutionWidth
        let h = pipeline.maxTotalThreadsPerThreadgroup / w
        let threadsPerThreadgroup = MTLSize(width: w, height: max(1,h), depth: 1)
        let threadsPerGrid = MTLSize(width: outTexture.width, height: outTexture.height, depth: 1)
        encoder.dispatchThreads(threadsPerGrid, threadsPerThreadgroup: threadsPerThreadgroup)
        encoder.endEncoding()

        // blit to drawable
        let blit = cmdBuf.makeBlitCommandEncoder()!
        blit.copy(from: outTexture, sourceSlice: 0, sourceLevel: 0, sourceOrigin: MTLOrigin(), sourceSize: MTLSize(width: outTexture.width, height: outTexture.height, depth: 1), to: drawable.texture, destinationSlice: 0, destinationLevel: 0, destinationOrigin: MTLOrigin())
        blit.endEncoding()

        cmdBuf.present(drawable)
        cmdBuf.commit()
    }

    func resetAccumulation() {
        frameIndex = 0
        if let t = accumTexture {
            let region = MTLRegionMake2D(0, 0, t.width, t.height)
            var zeros = [Float](repeating: 0, count: t.width * t.height * 4)
            t.replace(region: region, mipmapLevel: 0, withBytes: &zeros, bytesPerRow: t.width * 4 * MemoryLayout<Float>.size)
        }
    }
}


//
//# Notes
//- This is a minimal path-tracer implementation using a compute shader. It focuses on correctness and clarity, not production-level performance.
//- To improve performance: implement stream compaction, blue-noise sampling, hierarchical scene data (SSBO-style buffers for spheres/triangles), or move to raytracing acceleration structures (Metal Ray Tracing on macOS 11+/Apple Silicon).
//- I can: split this into an Xcode project, add model loading, BVH on GPU, materials (dielectric/metal), or convert sphere scene storage to buffers. Tell me which features you want next.
