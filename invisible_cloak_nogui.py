#!/usr/bin/env python3
"""
Harry Potter Invisible Cloak Effect using OpenCV (No GUI Version)

This version works without OpenCV GUI windows by saving frames to files.
Useful when GUI support is not available.
"""

import cv2
import numpy as np
import argparse
from collections import deque
import os
import time


def parse_args():
    """Parse command-line arguments for the invisible cloak application."""
    ap = argparse.ArgumentParser(description="Harry Potter Invisible Cloak (No GUI)")
    
    ap.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    ap.add_argument("--bg-frames", type=int, default=30, help="Frames to capture background (default: 30)")
    ap.add_argument("--color", type=str, default="red", choices=["red", "green"], help="Cloak color (default: red)")
    ap.add_argument("--output-dir", type=str, default="output", help="Directory to save output frames")
    ap.add_argument("--demo-frames", type=int, default=50, help="Number of demo frames to capture")
    
    return ap.parse_args()


def get_hsv_ranges(color: str):
    """Returns HSV lower/upper bounds for the target cloak color."""
    if color == "red":
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])
        return [(lower1, upper1), (lower2, upper2)]
    else:  # green
        lower = np.array([35, 80, 40])
        upper = np.array([85, 255, 255])
        return [(lower, upper)]


def capture_background_nogui(cap, num_frames=30):
    """Capture background without GUI display."""
    print(f"📷 Capturing {num_frames} background frames...")
    print("🚶 Please step out of camera view for 5 seconds!")
    
    # Wait for user to step away
    for i in range(5, 0, -1):
        print(f"⏰ Starting in {i} seconds...")
        time.sleep(1)
    
    buffer = deque(maxlen=num_frames)
    
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Failed to read from camera")
            
        frame = cv2.flip(frame, 1)  # Mirror
        buffer.append(frame)
        
        if (i + 1) % 10 == 0:
            print(f"📊 Captured {i+1}/{num_frames} frames")
    
    print("🔄 Processing background...")
    median_bg = np.median(np.array(buffer), axis=0).astype(np.uint8)
    
    return median_bg


def build_mask(hsv, ranges):
    """Build a binary mask for the cloak color."""
    mask_total = None
    for (low, high) in ranges:
        mask = cv2.inRange(hsv, low, high)
        mask_total = mask if mask_total is None else (mask_total | mask)

    # Clean mask with morphological operations
    kernel = np.ones((3, 3), np.uint8)
    mask_total = cv2.morphologyEx(mask_total, cv2.MORPH_OPEN, kernel, iterations=2)
    mask_total = cv2.morphologyEx(mask_total, cv2.MORPH_DILATE, kernel, iterations=1)
    
    return mask_total


def main():
    """Main function without GUI."""
    print("=" * 60)
    print("🧙‍♂️ Harry Potter Invisible Cloak (No GUI Mode)")
    print("=" * 60)
    
    args = parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize camera
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"❌ Cannot open camera {args.camera}")
        return
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print(f"📹 Camera {args.camera} initialized")
    print(f"🎨 Cloak color: {args.color.upper()}")
    print(f"📁 Output directory: {args.output_dir}")

    try:
        # Step 1: Capture background
        bg = capture_background_nogui(cap, args.bg_frames)
        
        # Save background
        bg_path = os.path.join(args.output_dir, "background.jpg")
        cv2.imwrite(bg_path, bg)
        print(f"💾 Background saved: {bg_path}")

        # Step 2: Get HSV ranges
        ranges = get_hsv_ranges(args.color)

        print(f"\n🎭 Starting invisible cloak effect...")
        print(f"📸 Capturing {args.demo_frames} demo frames...")
        print("🦸 Put on your cloak and pose!")
        
        time.sleep(3)  # Give user time to get ready

        # Step 3: Capture demo frames with cloak effect
        for frame_num in range(args.demo_frames):
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to capture frame")
                break

            # Mirror frame
            frame = cv2.flip(frame, 1)
            
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Create mask
            mask = build_mask(hsv, ranges)

            # Apply invisible cloak effect
            mask_inv = cv2.bitwise_not(mask)
            cloak_area = cv2.bitwise_and(bg, bg, mask=mask)
            rest_of_frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
            final = cv2.addWeighted(cloak_area, 1, rest_of_frame, 1, 0)

            # Add text overlay
            cv2.putText(final, f"Invisible Cloak - Frame {frame_num+1}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(final, f"Color: {args.color.upper()}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Calculate cloak coverage
            coverage = (np.sum(mask > 0) / mask.size) * 100
            cv2.putText(final, f"Cloak Coverage: {coverage:.1f}%", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Save frames
            original_path = os.path.join(args.output_dir, f"original_{frame_num:03d}.jpg")
            mask_path = os.path.join(args.output_dir, f"mask_{frame_num:03d}.jpg")
            result_path = os.path.join(args.output_dir, f"result_{frame_num:03d}.jpg")
            
            cv2.imwrite(original_path, frame)
            cv2.imwrite(mask_path, mask)
            cv2.imwrite(result_path, final)
            
            if (frame_num + 1) % 10 == 0:
                print(f"📸 Processed {frame_num+1}/{args.demo_frames} frames")

        print(f"\n🎉 Demo complete!")
        print(f"📁 Check {args.output_dir} folder for:")
        print(f"   • background.jpg - Captured background")
        print(f"   • original_*.jpg - Original camera frames")
        print(f"   • mask_*.jpg - Cloak detection masks")
        print(f"   • result_*.jpg - Final invisible cloak effect")
        
        print(f"\n💡 To create a video from frames:")
        print(f"   ffmpeg -r 10 -i {args.output_dir}/result_%03d.jpg -vcodec libx264 invisible_cloak.mp4")

    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        cap.release()
        print("🧹 Camera released")


if __name__ == "__main__":
    main()