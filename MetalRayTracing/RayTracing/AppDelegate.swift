//
//  AppDelegate.swift
//  RayTraceRender
//
//  Created by 李智成 on 2025/10/5.
//

import Cocoa
import MetalKit

@main
class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var viewController: ViewController!

    func applicationDidFinishLaunching(_ aNotification: Notification) {
        let contentRect = NSRect(x: 0, y: 0, width: 800, height: 600)
        window = NSWindow(contentRect: contentRect, styleMask: [.titled, .closable, .resizable], backing: .buffered, defer: false)
        window.title = "Metal Path Tracer"

        viewController = ViewController()
        window.contentView = viewController.view
        window.makeKeyAndOrderFront(nil)
    }
}


