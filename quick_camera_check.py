#!/usr/bin/env python3
"""
Quick Camera Check Script

Automatically tests cameras and provides solutions for common issues.
"""

import cv2
import sys
import time


def quick_camera_scan():
    """Quickly scan for available cameras."""
    print("🔍 Scanning for available cameras...")
    available_cameras = []
    
    for i in range(6):  # Test cameras 0-5
        print(f"Testing camera {i}...", end=" ")
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    print(f"✅ WORKING ({w}x{h})")
                    available_cameras.append(i)
                else:
                    print("❌ No frame")
            else:
                print("❌ Cannot open")
            cap.release()
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(0.2)
    
    return available_cameras


def show_camera_solutions():
    """Show common solutions for camera issues."""
    print("\n🔧 CAMERA TROUBLESHOOTING SOLUTIONS:")
    print("\n1. 📱 Check Camera Usage:")
    print("   • Close Skype, Teams, Zoom, or other video apps")
    print("   • Close browser tabs using camera")
    print("   • Check Windows Camera app")
    
    print("\n2. 🔌 Hardware Check:")
    print("   • Unplug and reconnect USB camera")
    print("   • Try different USB port")
    print("   • Check if camera LED is on")
    
    print("\n3. 💻 Windows Settings:")
    print("   • Go to Settings > Privacy > Camera")
    print("   • Enable 'Allow apps to access your camera'")
    print("   • Enable 'Allow desktop apps to access your camera'")
    
    print("\n4. 🐍 Python/OpenCV Fix:")
    print("   • Run: pip install --upgrade opencv-python")
    print("   • Restart command prompt/PowerShell")
    
    print("\n5. 🔄 System Restart:")
    print("   • Sometimes a simple restart fixes camera issues")


def test_opencv_installation():
    """Test if OpenCV is working properly."""
    print("\n🧪 Testing OpenCV installation...")
    try:
        print(f"OpenCV version: {cv2.__version__}")
        
        # Test basic functionality
        test_img = cv2.imread("test.jpg")  # This will fail but shouldn't crash
        print("✅ OpenCV basic functions working")
        
        # Test camera creation (without opening)
        cap = cv2.VideoCapture()
        cap.release()
        print("✅ VideoCapture object creation working")
        
        return True
    except Exception as e:
        print(f"❌ OpenCV issue: {e}")
        return False


def main():
    print("=" * 60)
    print("📷 Quick Camera Diagnostic for Invisible Cloak")
    print("=" * 60)
    
    # Test OpenCV first
    if not test_opencv_installation():
        print("\n❌ OpenCV installation issue detected!")
        print("💡 Try: pip install --upgrade opencv-python")
        return
    
    # Scan for cameras
    cameras = quick_camera_scan()
    
    if cameras:
        print(f"\n🎉 SUCCESS! Found {len(cameras)} working camera(s): {cameras}")
        print(f"\n💡 To use the invisible cloak:")
        for cam_id in cameras:
            print(f"   python invisible_cloak.py --camera {cam_id}")
        
        # Try to run with first available camera
        first_cam = cameras[0]
        print(f"\n🚀 Want to test with camera {first_cam}? (y/n): ", end="")
        choice = input().strip().lower()
        if choice == 'y':
            print(f"Starting invisible cloak with camera {first_cam}...")
            import subprocess
            subprocess.run([sys.executable, "invisible_cloak.py", "--camera", str(first_cam)])
    else:
        print("\n❌ NO WORKING CAMERAS FOUND!")
        show_camera_solutions()
        
        print(f"\n🔄 After fixing the issue, run:")
        print(f"   python quick_camera_check.py")
        print(f"   OR")
        print(f"   python camera_test.py  (for detailed testing)")


if __name__ == "__main__":
    main()