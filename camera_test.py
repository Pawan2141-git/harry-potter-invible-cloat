#!/usr/bin/env python3
"""
Camera Test and Troubleshooting Script

This script helps diagnose and fix camera issues for the Invisible Cloak application.
"""

import cv2
import numpy as np
import sys
import time


def test_camera_availability():
    """Test which camera indices are available on the system."""
    print("🔍 Testing camera availability...")
    available_cameras = []
    
    # Test camera indices 0 through 5
    for i in range(6):
        print(f"Testing camera index {i}...", end=" ")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                print(f"✅ WORKING - Resolution: {width}x{height}")
                available_cameras.append(i)
            else:
                print("❌ Failed to read frame")
        else:
            print("❌ Cannot open")
        
        cap.release()
        time.sleep(0.5)  # Small delay between tests
    
    return available_cameras


def test_camera_detailed(camera_id):
    """Test a specific camera with detailed information."""
    print(f"\n🔬 Detailed test for camera {camera_id}:")
    
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"❌ Cannot open camera {camera_id}")
        return False
    
    # Get camera properties
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"📊 Camera Properties:")
    print(f"   Resolution: {int(width)}x{int(height)}")
    print(f"   FPS: {fps}")
    
    # Try to read a few frames
    print(f"📹 Testing frame capture...")
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"   Frame {i+1}: ✅ Success")
        else:
            print(f"   Frame {i+1}: ❌ Failed")
            cap.release()
            return False
        time.sleep(0.1)
    
    cap.release()
    print(f"✅ Camera {camera_id} is working properly!")
    return True


def show_camera_live(camera_id):
    """Show live camera feed to verify it's working."""
    print(f"\n📺 Opening live view for camera {camera_id}")
    print("Press 'q' to close the camera view")
    
    cap = cv2.VideoCapture(camera_id)
    
    if not cap.isOpened():
        print(f"❌ Cannot open camera {camera_id}")
        return False
    
    # Set reasonable resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    cv2.namedWindow(f"Camera {camera_id} Test", cv2.WINDOW_AUTOSIZE)
    
    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break
        
        frame_count += 1
        
        # Add some info on the frame
        cv2.putText(frame, f"Camera {camera_id} - Frame {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Calculate and display FPS
        elapsed = time.time() - start_time
        if elapsed > 0:
            fps = frame_count / elapsed
            cv2.putText(frame, f"FPS: {fps:.1f}", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow(f"Camera {camera_id} Test", frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Camera {camera_id} test completed")
    return True


def fix_common_issues():
    """Provide solutions for common camera issues."""
    print("\n🔧 Common Camera Issues and Solutions:")
    print("\n1. 📷 Camera Permission Issues:")
    print("   - Check if other applications are using the camera")
    print("   - Close Skype, Teams, OBS, or other camera apps")
    print("   - Restart your computer if needed")
    
    print("\n2. 🔌 Hardware Issues:")
    print("   - Check if camera is properly connected")
    print("   - Try different USB ports")
    print("   - Test with different camera indices (0, 1, 2, etc.)")
    
    print("\n3. 💻 Software Issues:")
    print("   - Update camera drivers")
    print("   - Check Windows Camera privacy settings")
    print("   - Ensure OpenCV is properly installed")
    
    print("\n4. 🐍 Python/OpenCV Issues:")
    print("   - Try: pip install --upgrade opencv-python")
    print("   - Try: pip uninstall opencv-python && pip install opencv-python")


def interactive_camera_setup():
    """Interactive setup to find and configure the best camera."""
    print("=" * 60)
    print("📷 Interactive Camera Setup for Invisible Cloak")
    print("=" * 60)
    
    # Step 1: Find available cameras
    available_cameras = test_camera_availability()
    
    if not available_cameras:
        print("\n❌ No working cameras found!")
        fix_common_issues()
        return None
    
    print(f"\n✅ Found {len(available_cameras)} working camera(s): {available_cameras}")
    
    # Step 2: Test each camera in detail
    working_cameras = []
    for cam_id in available_cameras:
        if test_camera_detailed(cam_id):
            working_cameras.append(cam_id)
    
    if not working_cameras:
        print("\n❌ No cameras passed detailed testing!")
        return None
    
    # Step 3: Let user choose and test live
    if len(working_cameras) == 1:
        chosen_camera = working_cameras[0]
        print(f"\n🎯 Using camera {chosen_camera} (only working camera)")
    else:
        print(f"\n🎯 Multiple working cameras found: {working_cameras}")
        while True:
            try:
                chosen_camera = int(input(f"Choose camera ID {working_cameras}: "))
                if chosen_camera in working_cameras:
                    break
                else:
                    print("❌ Invalid choice. Please select from available cameras.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    # Step 4: Show live preview
    print(f"\n🎬 Testing live preview for camera {chosen_camera}...")
    if show_camera_live(chosen_camera):
        print(f"\n🎉 Camera {chosen_camera} is ready for the Invisible Cloak!")
        print(f"\n💡 To use this camera, run:")
        print(f"   python invisible_cloak.py --camera {chosen_camera}")
        return chosen_camera
    else:
        print(f"\n❌ Camera {chosen_camera} failed live test")
        return None


def main():
    """Main function for camera troubleshooting."""
    print("🧙‍♂️ Harry Potter Invisible Cloak - Camera Troubleshooter")
    
    while True:
        print("\n" + "=" * 50)
        print("Choose an option:")
        print("1. 🔍 Quick camera scan")
        print("2. 🔬 Test specific camera")
        print("3. 📺 Live camera preview")
        print("4. 🎯 Interactive camera setup")
        print("5. 🔧 Common issues help")
        print("6. 🚀 Run Invisible Cloak")
        print("7. ❌ Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            available = test_camera_availability()
            if available:
                print(f"\n✅ Working cameras: {available}")
            else:
                print("\n❌ No working cameras found")
                
        elif choice == '2':
            try:
                cam_id = int(input("Enter camera ID to test: "))
                test_camera_detailed(cam_id)
            except ValueError:
                print("❌ Please enter a valid camera ID number")
                
        elif choice == '3':
            try:
                cam_id = int(input("Enter camera ID for live preview: "))
                show_camera_live(cam_id)
            except ValueError:
                print("❌ Please enter a valid camera ID number")
                
        elif choice == '4':
            camera_id = interactive_camera_setup()
            if camera_id is not None:
                print(f"\n🎉 Setup complete! Use camera {camera_id}")
                
        elif choice == '5':
            fix_common_issues()
            
        elif choice == '6':
            available = test_camera_availability()
            if available:
                cam_id = available[0]
                print(f"\n🚀 Starting Invisible Cloak with camera {cam_id}...")
                import subprocess
                subprocess.run([sys.executable, "invisible_cloak.py", "--camera", str(cam_id)])
            else:
                print("\n❌ No working cameras found. Please fix camera issues first.")
                
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()