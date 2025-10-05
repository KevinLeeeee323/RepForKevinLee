//
//  ViewController.swift
//  RayTraceRender
//
//  Created by 李智成 on 2025/10/5.
//


import Cocoa
import MetalKit

class ViewController: NSViewController {
    var metalView: MTKView! = nil
    var renderer: Renderer! = nil

    override func loadView() {
        self.view = NSView()
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        guard let device = MTLCreateSystemDefaultDevice() else {
            fatalError("Metal is not supported on this device")
        }

        metalView = MTKView(frame: self.view.bounds, device: device)
        metalView.autoresizingMask = [.width, .height]
        metalView.colorPixelFormat = .bgra8Unorm
        metalView.framebufferOnly = false
        metalView.enableSetNeedsDisplay = true
        metalView.isPaused = false
        metalView.preferredFramesPerSecond = 60

        self.view.addSubview(metalView)

        renderer = Renderer(metalView: metalView)
        metalView.delegate = renderer

        // keyboard reset
        let opts: NSTrackingArea.Options = [.activeAlways, .inVisibleRect, .mouseEnteredAndExited]
        metalView.addTrackingArea(NSTrackingArea(rect: metalView.bounds, options: opts, owner: self, userInfo: nil))
    }

    override func keyDown(with event: NSEvent) {
        if event.keyCode == 49 { // space
            renderer.resetAccumulation()
        }
    }
}

