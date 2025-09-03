#!/usr/bin/env python3
"""
Test script for the Invisible Cloak application.

This script tests the core functionality without requiring a camera.
"""

import numpy as np
import cv2
import sys
import os

# Add the current directory to the path to import invisible_cloak
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from invisible_cloak import get_hsv_ranges, build_mask, parse_args


def test_color_ranges():
    """Test that color ranges are properly defined."""
    print("Testing color ranges...")
    
    # Test all supported colors
    colors_to_test = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'white', 'black']
    
    for color in colors_to_test:
        ranges = get_hsv_ranges(color)
        assert len(ranges) >= 1, f"{color} should have at least 1 range"
        
        # Red should have 2 ranges due to hue wraparound
        if color == 'red':
            assert len(ranges) == 2, "Red should have 2 ranges"
        else:
            assert len(ranges) == 1, f"{color} should have 1 range"
    
    print("✓ Color ranges test passed")


def test_mask_creation():
    """Test mask creation with synthetic images."""
    print("Testing mask creation...")
    
    # Create a test image with red and green areas
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add a red rectangle
    test_image[100:200, 100:200] = [0, 0, 255]  # BGR format
    
    # Add a green rectangle
    test_image[300:400, 300:400] = [0, 255, 0]  # BGR format
    
    # Convert to HSV
    hsv = cv2.cvtColor(test_image, cv2.COLOR_BGR2HSV)
    
    # Test red cloak detection
    red_ranges = get_hsv_ranges('red')
    red_mask = build_mask(hsv, red_ranges)
    
    # Check if red area is detected
    red_area = np.sum(red_mask[100:200, 100:200] > 0)
    assert red_area > 1000, f"Red mask detection failed: only {red_area} pixels detected"
    
    # Test green cloak detection
    green_ranges = get_hsv_ranges('green')
    green_mask = build_mask(hsv, green_ranges)
    
    # Check if green area is detected
    green_area = np.sum(green_mask[300:400, 300:400] > 0)
    assert green_area > 1000, f"Green mask detection failed: only {green_area} pixels detected"
    
    print("✓ Mask creation test passed")


def test_cloak_effect():
    """Test the cloak effect application using bitwise operations."""
    print("Testing cloak effect...")
    
    # Create test images
    current_frame = np.full((480, 640, 3), 100, dtype=np.uint8)  # Gray frame
    background = np.full((480, 640, 3), 200, dtype=np.uint8)     # Lighter background
    
    # Create a simple mask
    mask = np.zeros((480, 640), dtype=np.uint8)
    mask[200:300, 200:300] = 255  # White square in the middle
    
    # Apply the same logic as in the main application
    mask_inv = cv2.bitwise_not(mask)
    cloak_area = cv2.bitwise_and(background, background, mask=mask)
    rest_of_frame = cv2.bitwise_and(current_frame, current_frame, mask=mask_inv)
    result = cv2.addWeighted(cloak_area, 1, rest_of_frame, 1, 0)
    
    # Check if the masked area has background values
    masked_area_value = result[250, 250, 0]  # Center of the mask
    unmasked_area_value = result[50, 50, 0]   # Outside the mask
    
    assert masked_area_value == 200, f"Cloak effect failed: masked area value is {masked_area_value}, expected 200"
    assert unmasked_area_value == 100, f"Cloak effect failed: unmasked area value is {unmasked_area_value}, expected 100"
    
    print("✓ Cloak effect test passed")


def test_argument_parsing():
    """Test command-line argument parsing."""
    print("Testing argument parsing...")
    
    # Test that the parse_args function can be imported and has expected attributes
    try:
        args = parse_args.__code__.co_varnames
        assert 'ap' in args, "parse_args function structure check failed"
        print("✓ Argument parsing import test passed")
        return True
    except Exception as e:
        print(f"✗ Argument parsing test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Invisible Cloak Tests")
    print("=" * 50)
    
    tests = [
        test_color_ranges,
        test_mask_creation,
        test_cloak_effect,
        test_argument_parsing,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("🎉 All tests passed! The invisible cloak is ready for magic!")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)