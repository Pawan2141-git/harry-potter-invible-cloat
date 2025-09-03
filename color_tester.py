#!/usr/bin/env python3
"""
Color Demonstration Script for Invisible Cloak

This script helps you understand and test different cloak colors.
"""

import cv2
import numpy as np
from invisible_cloak import get_hsv_ranges


def create_color_chart():
    """Create a visual chart showing all available colors and their HSV ranges."""
    print("🎨 Available Cloak Colors and HSV Ranges:")
    print("=" * 60)
    
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'white', 'black']
    
    for color in colors:
        ranges = get_hsv_ranges(color)
        print(f"\n🔴 {color.upper()}:")
        
        for i, (lower, upper) in enumerate(ranges):
            print(f"   Range {i+1}: H({lower[0]}-{upper[0]}) S({lower[1]}-{upper[1]}) V({lower[2]}-{upper[2]})")
        
        # Create a small sample image of the color
        sample = np.full((100, 200, 3), 128, dtype=np.uint8)
        
        # Convert sample color to show approximate appearance
        if color == 'red':
            sample[:, :] = [0, 0, 255]  # BGR
        elif color == 'green':
            sample[:, :] = [0, 255, 0]
        elif color == 'blue':
            sample[:, :] = [255, 0, 0]
        elif color == 'yellow':
            sample[:, :] = [0, 255, 255]
        elif color == 'purple':
            sample[:, :] = [255, 0, 255]
        elif color == 'orange':
            sample[:, :] = [0, 165, 255]
        elif color == 'cyan':
            sample[:, :] = [255, 255, 0]
        elif color == 'pink':
            sample[:, :] = [203, 192, 255]
        elif color == 'white':
            sample[:, :] = [255, 255, 255]
        elif color == 'black':
            sample[:, :] = [0, 0, 0]
        
        cv2.imwrite(f"color_sample_{color}.jpg", sample)
        print(f"   📄 Sample saved as: color_sample_{color}.jpg")


def test_color_detection(color, camera_id=0):
    """Test color detection in real-time for a specific color."""
    print(f"\n🧪 Testing {color.upper()} detection...")
    print("Press 'q' to quit, 's' to save current frame")
    
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"❌ Cannot open camera {camera_id}")
        return
    
    ranges = get_hsv_ranges(color)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for the color
        mask = None
        for (lower, upper) in ranges:
            color_mask = cv2.inRange(hsv, lower, upper)
            mask = color_mask if mask is None else (mask | color_mask)
        
        # Clean mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)
        
        # Show results side by side
        result = np.hstack([frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)])
        
        # Add labels
        cv2.putText(result, f"Original - {color.upper()} Detection", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(result, "Original Feed", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(result, f"{color.upper()} Mask", 
                   (frame.shape[1] + 10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show coverage percentage
        coverage = (np.sum(mask > 0) / mask.size) * 100
        cv2.putText(result, f"Coverage: {coverage:.1f}%", 
                   (10, result.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow(f"{color.upper()} Color Detection Test", result)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            cv2.imwrite(f"{color}_detection_test.jpg", result)
            print(f"📸 Saved: {color}_detection_test.jpg")
    
    cap.release()
    cv2.destroyAllWindows()


def interactive_color_test():
    """Interactive menu for testing colors."""
    print("🎨 Interactive Color Testing for Invisible Cloak")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. 📊 Show all color ranges")
        print("2. 🔴 Test RED detection")
        print("3. 🟢 Test GREEN detection") 
        print("4. 🔵 Test BLUE detection")
        print("5. 🟡 Test YELLOW detection")
        print("6. 🟣 Test PURPLE detection")
        print("7. 🧡 Test ORANGE detection")
        print("8. 🧢 Test CYAN detection")
        print("9. 🎀 Test PINK detection")
        print("10. ⚪ Test WHITE detection")
        print("11. ⚫ Test BLACK detection")
        print("12. 🎮 Run invisible cloak with selected color")
        print("13. ❌ Exit")
        
        choice = input("\nEnter your choice (1-13): ").strip()
        
        if choice == '1':
            create_color_chart()
            
        elif choice in ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
            color_map = {'2': 'red', '3': 'green', '4': 'blue', '5': 'yellow', '6': 'purple', 
                        '7': 'orange', '8': 'cyan', '9': 'pink', '10': 'white', '11': 'black'}
            color = color_map[choice]
            
            try:
                camera = int(input(f"Enter camera ID (default 0): ") or "0")
                test_color_detection(color, camera)
            except ValueError:
                print("❌ Invalid camera ID, using 0")
                test_color_detection(color, 0)
                
        elif choice == '12':
            print("\nAvailable colors: red, green, blue, yellow, purple, orange, cyan, pink, white, black")
            color = input("Enter color: ").strip().lower()
            
            if color in ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'white', 'black']:
                try:
                    camera = int(input(f"Enter camera ID (default 0): ") or "0")
                    print(f"\n🚀 Starting invisible cloak with {color} color...")
                    
                    import subprocess
                    import sys
                    subprocess.run([sys.executable, "invisible_cloak.py", 
                                  "--color", color, "--camera", str(camera)])
                except ValueError:
                    print("❌ Invalid camera ID")
                except Exception as e:
                    print(f"❌ Error running invisible cloak: {e}")
            else:
                print("❌ Invalid color!")
                
        elif choice == '13':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-13.")


if __name__ == "__main__":
    interactive_color_test()