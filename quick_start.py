#!/usr/bin/env python3
"""
Quick start example for the Invisible Cloak application.

This script demonstrates the simplest way to run the invisible cloak effect.
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import cv2
        import numpy as np
        print("✓ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def run_cloak_app(color='red', camera=0):
    """Run the invisible cloak application with specified parameters."""
    if not check_dependencies():
        return False
    
    print(f"\n🧙‍♂️ Starting Harry Potter Invisible Cloak Effect...")
    print(f"   Color: {color}")
    print(f"   Camera: {camera}")
    print(f"   Press 'q' to quit when running")
    
    try:
        # Run the main application
        cmd = [sys.executable, 'invisible_cloak.py', '--color', color, '--camera', str(camera)]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running application: {e}")
        return False
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except FileNotFoundError:
        print("Error: invisible_cloak.py not found. Make sure you're in the correct directory.")
        return False
    
    return True

def main():
    """Main function with interactive menu."""
    print("=" * 60)
    print("🧙‍♂️ Harry Potter Invisible Cloak - Quick Start")
    print("=" * 60)
    
    while True:
        print("\nChoose an option:")
        print("1. Run with RED cloak (default)")
        print("2. Run with GREEN cloak")
        print("3. Run with custom settings")
        print("4. Check dependencies")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            run_cloak_app('red', 0)
        elif choice == '2':
            run_cloak_app('green', 0)
        elif choice == '3':
            color = input("Enter cloak color (red/green): ").strip().lower()
            if color not in ['red', 'green']:
                print("Invalid color! Using red as default.")
                color = 'red'
            
            try:
                camera = int(input("Enter camera ID (0, 1, 2, etc.): ").strip())
            except ValueError:
                print("Invalid camera ID! Using 0 as default.")
                camera = 0
            
            run_cloak_app(color, camera)
        elif choice == '4':
            check_dependencies()
        elif choice == '5':
            print("Goodbye! 🧙‍♂️✨")
            break
        else:
            print("Invalid choice! Please enter 1-5.")

if __name__ == "__main__":
    main()