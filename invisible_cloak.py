#!/usr/bin/env python3
"""
Harry Potter Invisible Cloak Effect using OpenCV

Makes a red/green cloak "invisible" by replacing it with the captured background.
Usage:
  python invisible_cloak.py --color red
  python invisible_cloak.py --color green --camera 0 --bg-frames 80

Author: AI Assistant
Requirements: opencv-python, numpy
"""

import cv2
import numpy as np
import argparse
from collections import deque


def parse_args():
    """Parse command-line arguments for the invisible cloak application."""
    ap = argparse.ArgumentParser(
        description="Harry Potter Invisible Cloak (OpenCV)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python invisible_cloak.py --color red --camera 0 --bg-frames 60
  python invisible_cloak.py --color green --camera 1
  python invisible_cloak.py  # Use defaults (red cloak, camera 0, 60 bg frames)

HSV Tuning Tips:
- If detection is poor, adjust lighting conditions
- For red detection issues, ensure good contrast with background
- Green typically works better in indoor lighting
- Avoid shiny or reflective cloak materials
        """
    )
    
    ap.add_argument("--camera", type=int, default=0, 
                    help="Camera index (default: 0)")
    ap.add_argument("--bg-frames", type=int, default=60, 
                    help="Frames to capture background (default: 60)")
    ap.add_argument("--color", type=str, default="red", 
                    choices=["red", "green", "blue", "yellow", "purple", "orange", "cyan", "pink", "white", "black"], 
                    help="Cloak color to make invisible (default: red)")
    ap.add_argument("--width", type=int, default=640, 
                    help="Camera capture width (default: 640)")
    ap.add_argument("--height", type=int, default=480, 
                    help="Camera capture height (default: 480)")
    return ap.parse_args()


def get_hsv_ranges(color: str):
    """
    Returns HSV lower/upper bounds for the target cloak color.
    Values are a good starting point; adjust for your lighting & cloth.
    
    Args:
        color (str): Target color ('red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'white', 'black')
        
    Returns:
        list: List of (lower, upper) HSV range tuples
        
    HSV Tuning Tips:
    - Hue (H): Color tone (0-179 in OpenCV)
    - Saturation (S): Color intensity (0-255, higher = more vivid)  
    - Value (V): Brightness (0-255, higher = brighter)
    
    For better detection:
    - Increase S range if color appears washed out
    - Adjust V range based on lighting conditions
    - Red uses TWO ranges due to hue wraparound at 0/180
    """
    if color == "red":
        # Red wraps around HSV hue, so we use TWO ranges and OR the masks.
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        return [(lower1, upper1), (lower2, upper2)]
    
    elif color == "green":
        lower = np.array([35, 80, 40])
        upper = np.array([85, 255, 255])
        return [(lower, upper)]
    
    elif color == "blue":
        # Blue color range
        lower = np.array([100, 80, 50])
        upper = np.array([130, 255, 255])
        return [(lower, upper)]
    
    elif color == "yellow":
        # Yellow color range
        lower = np.array([20, 80, 50])
        upper = np.array([30, 255, 255])
        return [(lower, upper)]
    
    elif color == "purple":
        # Purple/Magenta color range
        lower = np.array([140, 80, 50])
        upper = np.array([170, 255, 255])
        return [(lower, upper)]
    
    elif color == "orange":
        # Orange color range (between red and yellow)
        lower = np.array([5, 100, 100])
        upper = np.array([20, 255, 255])
        return [(lower, upper)]
    
    elif color == "cyan":
        # Cyan/Light Blue color range
        lower = np.array([85, 50, 50])
        upper = np.array([100, 255, 255])
        return [(lower, upper)]
    
    elif color == "pink":
        # Pink/Magenta color range (similar to purple but lighter)
        lower = np.array([150, 50, 100])
        upper = np.array([170, 255, 255])
        return [(lower, upper)]
    
    elif color == "white":
        # White color range (low saturation, high value)
        lower = np.array([0, 0, 200])
        upper = np.array([179, 30, 255])
        return [(lower, upper)]
    
    elif color == "black":
        # Black color range (low value)
        lower = np.array([0, 0, 0])
        upper = np.array([179, 255, 50])
        return [(lower, upper)]
    
    else:
        # Default to red if unknown color
        print(f"⚠️ Warning: Unknown color '{color}', defaulting to red")
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        return [(lower1, upper1), (lower2, upper2)]


def capture_background(cap, num_frames=60):
    """
    Capture a stable background while the scene is empty.
    Uses median over a small buffer to reduce flicker/noise.
    
    Args:
        cap: OpenCV VideoCapture object
        num_frames (int): Number of frames to capture for background
        
    Returns:
        numpy.ndarray: Median background frame
        
    The deque-based approach provides better memory efficiency
    and the median calculation reduces noise and movement artifacts.
    """
    print(f"\n🎬 Capturing background...")
    print("📍 Please step out of the camera view!")
    print(f"⏱️ Capturing {num_frames} frames...")
    
    buffer = deque(maxlen=num_frames)
    
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Failed to read from camera while capturing background.")
            
        # Mirror the frame for natural webcam interaction
        frame = cv2.flip(frame, 1)
        buffer.append(frame)
        
        # Show progress with visual feedback
        progress_frame = frame.copy()
        cv2.putText(progress_frame, f"Capturing background {i+1}/{num_frames}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(progress_frame, "Stay out of camera view!", 
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Progress bar
        bar_width = 400
        bar_height = 20
        progress = int((i + 1) / num_frames * bar_width)
        cv2.rectangle(progress_frame, (20, 100), (20 + bar_width, 100 + bar_height), (255, 255, 255), 2)
        cv2.rectangle(progress_frame, (20, 100), (20 + progress, 100 + bar_height), (0, 255, 0), -1)
        
        cv2.imshow("Invisible Cloak", progress_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print("🔄 Processing background...")
    median_bg = np.median(np.array(buffer), axis=0).astype(np.uint8)
    print("✅ Background captured successfully!")
    return median_bg


def build_mask(hsv, ranges):
    """
    Build a binary mask for the cloak color using one or more HSV ranges.
    Then denoise with morphology.
    
    Args:
        hsv (numpy.ndarray): HSV image
        ranges (list): List of (lower, upper) HSV range tuples
        
    Returns:
        numpy.ndarray: Clean binary mask
        
    Morphological Operations:
    - MORPH_OPEN: Removes small noise (erosion followed by dilation)
    - MORPH_DILATE: Connects small gaps and expands the mask
    """
    mask_total = None
    
    # Combine all HSV ranges for the target color
    for (low, high) in ranges:
        mask = cv2.inRange(hsv, low, high)
        mask_total = mask if mask_total is None else (mask_total | mask)

    # Morphological operations to clean mask
    kernel = np.ones((3, 3), np.uint8)
    
    # Remove noise with opening operation
    mask_total = cv2.morphologyEx(mask_total, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Connect gaps with dilation  
    mask_total = cv2.morphologyEx(mask_total, cv2.MORPH_DILATE, kernel, iterations=1)
    
    return mask_total


def main():
    """
    Main function to run the Invisible Cloak application.
    
    Workflow:
    1. Parse command-line arguments
    2. Initialize camera with specified settings
    3. Capture background frames using median filtering
    4. Real-time processing loop:
       - Capture frame and convert to HSV
       - Create mask for cloak color
       - Apply invisible cloak effect
       - Display result with UI elements
    5. Clean up resources
    """
    print("=" * 60)
    print("🧙‍♂️ Harry Potter Invisible Cloak Effect")
    print("=" * 60)
    
    args = parse_args()

    # Initialize camera with specified settings
    cap = cv2.VideoCapture(args.camera)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {args.camera}. Try a different --camera index.")

    print(f"📹 Camera {args.camera} initialized: {args.width}x{args.height}")
    print(f"🎨 Cloak color: {args.color.upper()}")
    print(f"📊 Background frames: {args.bg_frames}")

    cv2.namedWindow("Invisible Cloak", cv2.WINDOW_AUTOSIZE)

    try:
        # Step 1: Capture background with empty scene
        bg = capture_background(cap, num_frames=args.bg_frames)

        # HSV ranges for selected color
        ranges = get_hsv_ranges(args.color)

        print(f"\n🎭 Ready! Wear the {args.color} cloak and step into the frame.")
        print("⌨️ Press 'q' to quit, 'r' to recapture background")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                break

            # Mirror the frame for a natural webcam feel
            frame = cv2.flip(frame, 1)

            # Convert to HSV for robust color segmentation
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Step 2: Create color mask for the cloak
            mask = build_mask(hsv, ranges)

            # Step 3: Invert mask to keep non-cloak regions
            mask_inv = cv2.bitwise_not(mask)

            # Step 4: Extract background where cloak is present
            cloak_area = cv2.bitwise_and(bg, bg, mask=mask)

            # Step 5: Extract current frame where cloak is NOT present
            rest_of_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)

            # Step 6: Combine both parts
            final = cv2.addWeighted(cloak_area, 1, rest_of_frame, 1, 0)

            # Add UI elements for better user experience
            cv2.putText(final, f"Harry Potter Invisible Cloak", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(final, f"Cloak: {args.color.upper()} | Press 'q' to quit, 'r' to reset",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show cloak coverage percentage
            mask_coverage = (np.sum(mask > 0) / mask.size) * 100
            cv2.putText(final, f"Cloak Coverage: {mask_coverage:.1f}%", 
                        (10, final.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(final, f"FPS: ~30 | Resolution: {args.width}x{args.height}", 
                        (10, final.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            cv2.imshow("Invisible Cloak", final)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
            elif key == ord('r'):  # Recapture background
                print("\n🔄 Recapturing background...")
                bg = capture_background(cap, num_frames=args.bg_frames)

    except KeyboardInterrupt:
        print("\n⏹️ Application interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Cleanup resources
        cap.release()
        cv2.destroyAllWindows()
        print("🧹 Resources cleaned up successfully")
        print("✨ Thanks for using the Invisible Cloak! Magic session ended.")


if __name__ == "__main__":
    main()