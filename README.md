# Harry Potter Invisible Cloak Effect 🧙‍♂️

A Python application that creates the famous Harry Potter invisible cloak effect using OpenCV and computer vision techniques. The application makes a specific color (red or green) disappear by replacing it with a static background captured before the subject enters the frame.

![Invisible Cloak Demo](https://img.shields.io/badge/OpenCV-Magic-blue?style=for-the-badge&logo=opencv)

## ✨ Features

- **Real-time cloak effect**: Makes any of 10 different colored objects disappear in real-time
- **Multi-color support**: Choose from 5 different cloak colors with optimized HSV ranges
- **Robust color detection**: Uses HSV color space with optimized ranges for various lighting conditions
- **Efficient background capture**: Uses deque buffer with median filtering for noise reduction
- **Advanced morphological operations**: Cleans masks using opening and dilation operations
- **Enhanced command-line interface**: Easy configuration with additional width/height options
- **Mirror mode**: Horizontally flipped camera feed for natural interaction
- **Live statistics**: Shows cloak coverage percentage, FPS, and resolution info
- **Interactive controls**: Press 'r' to recapture background, 'q' to quit
- **Visual feedback**: Progress bars and status messages during background capture
- **Color testing tools**: Interactive color detection testing and calibration
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🔧 Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy
- A webcam/camera device

## 📦 Installation

1. **Clone or download this repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install opencv-python numpy
   ```

## 🚀 Usage

### Basic Usage

```bash
# Run with default settings (red cloak, camera 0, 60 background frames)
python invisible_cloak.py

# Specify cloak color
python invisible_cloak.py --color green

# Use different camera
python invisible_cloak.py --camera 1

# Capture more background frames for better quality
python invisible_cloak.py --bg-frames 100
```

### Command-Line Arguments

| Argument | Description | Default | Options |
|----------|-------------|---------|---------|
| `--color` | Cloak color to make invisible | `red` | `red`, `green`, `blue`, `yellow`, `purple`, `orange`, `cyan`, `pink`, `white`, `black` |
| `--camera` | Camera device ID | `0` | Any integer |
| `--bg-frames` | Number of background frames to capture | `60` | Any positive integer |
| `--width` | Camera capture width | `640` | Any positive integer |
| `--height` | Camera capture height | `480` | Any positive integer |

### Example Commands

```bash
# Different cloak colors - Now with 10 options!
python invisible_cloak.py --color red
python invisible_cloak.py --color green  
python invisible_cloak.py --color blue
python invisible_cloak.py --color yellow
python invisible_cloak.py --color purple
python invisible_cloak.py --color orange
python invisible_cloak.py --color cyan
python invisible_cloak.py --color pink
python invisible_cloak.py --color white
python invisible_cloak.py --color black

# With custom settings
python invisible_cloak.py --color orange --camera 1 --bg-frames 80

# High resolution with custom color
python invisible_cloak.py --color cyan --width 1280 --height 720
```

## 🎭 How to Use the Cloak Effect

1. **Run the application**:
   ```bash
   python invisible_cloak.py --color red
   ```

2. **Step out of camera view**: When prompted, move completely out of the camera's field of view

3. **Background capture**: The app will capture 60 frames of the static background (takes ~2-3 seconds)

4. **Enter with cloak**: Put on your red (or green) cloak/cloth and step back into view

6. **Enjoy the magic**: Watch as the cloak becomes invisible!

7. **Interactive controls**: 
   - Press 'q' or ESC to quit
   - Press 'r' to recapture background if needed

8. **Monitor stats**: Check cloak coverage percentage and FPS in real-time

## 🎨 Cloak Requirements

For best results, use a cloak/cloth with these characteristics:

### ✅ Recommended
- **Solid color**: Pure red or green without patterns
- **Matte finish**: Avoid shiny or reflective materials
- **Good coverage**: Large enough to cover the desired area
- **Consistent color**: Evenly colored without variations

### ❌ Avoid
- **Patterned fabrics**: Stripes, polka dots, or mixed colors
- **Shiny materials**: Satin, silk, or metallic fabrics
- **Transparent or semi-transparent**: Must be opaque
- **Colors similar to background**: Ensure good contrast

## 🔧 HSV Color Ranges

The application uses HSV color space for robust color detection:

### Red Color Detection
```python
# Range 1: Lower red hues (0-10)
lower_red1 = [0, 120, 50]
upper_red1 = [10, 255, 255]

# Range 2: Upper red hues (170-179)
lower_red2 = [170, 120, 50]
upper_red2 = [179, 255, 255]
```

### Green Color Detection
```python
# Green range: Most green hues
lower_green = [40, 50, 50]
upper_green = [80, 255, 255]
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. **Poor Color Detection**
- **Problem**: Cloak not being detected properly
- **Solutions**:
  - Ensure good lighting conditions
  - Use a solid-colored, matte cloak
  - Avoid backgrounds with similar colors
  - Try adjusting HSV ranges in the code

#### 2. **Camera Not Found**
- **Problem**: "Could not open camera" error
- **Solutions**:
  - Check if camera is connected and working
  - Try different camera IDs (0, 1, 2, etc.)
  - Close other applications using the camera
  - Restart your computer

#### 3. **Flickering Effect**
- **Problem**: Cloak area flickers between visible and invisible
- **Solutions**:
  - Improve lighting conditions
  - Use more background frames (`--bg-frames 100`)
  - Ensure the cloak is a solid, consistent color
  - Avoid moving during background capture

#### 4. **Performance Issues**
- **Problem**: Low frame rate or lag
- **Solutions**:
  - Close unnecessary applications
  - Use a lower resolution camera setting
  - Reduce the number of background frames
  - Ensure good CPU performance

### HSV Tuning Tips

If color detection is not working well, you may need to adjust the HSV ranges:

1. **Hue (H)**: Controls the color tone (0-179 in OpenCV)
2. **Saturation (S)**: Controls color intensity (0-255, higher = more vivid)
3. **Value (V)**: Controls brightness (0-255, higher = brighter)

**Tuning guidelines**:
- Increase S range if color appears washed out
- Adjust V range based on lighting conditions
- For red, use two ranges due to hue wraparound at 0/180

## 🧪 Technical Details

### Algorithm Overview

1. **Background Capture**: Captures multiple frames and uses median to reduce noise
2. **Color Detection**: Converts frames to HSV and applies color range masking
3. **Mask Cleaning**: Uses morphological operations (opening/closing) to clean the mask
4. **Effect Application**: Replaces masked pixels with corresponding background pixels
5. **Real-time Processing**: Processes frames in real-time at ~30 FPS

### Key Components

- **`InvisibleCloak` class**: Main application logic
- **HSV masking**: Robust color detection in varying lighting
- **Morphological operations**: Noise reduction and hole filling
- **Background subtraction**: Static background replacement
- **Real-time processing**: Live camera feed processing

## 📝 Code Structure

```
invisible_cloak.py
├── parse_args()           # Command-line argument parsing
├── get_hsv_ranges()       # HSV color range definitions
├── capture_background()   # Background capture with deque buffer
├── build_mask()           # Color mask creation and cleaning
└── main()                 # Main application workflow
```

## 🤝 Contributing

Feel free to contribute to this project by:

1. **Reporting bugs**: Open an issue with detailed description
2. **Suggesting features**: Propose new functionality
3. **Adding colors**: Extend color detection to blue, yellow, etc.
4. **Improving performance**: Optimize the algorithms
5. **Better documentation**: Enhance the README or code comments

## 📄 License

This project is open source and available under the MIT License.

## 🎥 Demo Tips

For the best demonstration:

1. **Lighting**: Use even, bright lighting without harsh shadows
2. **Background**: Choose a background that contrasts with your cloak color
3. **Movement**: Move slowly and smoothly for better tracking
4. **Camera position**: Place camera at chest height for optimal view
5. **Cloak size**: Use a large cloak for more dramatic effect

## 🎨 Available Cloak Colors

The application now supports **10 different cloak colors** with optimized HSV ranges:

| Color | HSV Range(s) | Best For | Notes |
|-------|-------------|----------|-------|
| 🔴 **Red** | H: 0-10, 170-179 | Indoor/Outdoor | Uses 2 ranges for hue wraparound |
| 🟢 **Green** | H: 35-85 | Indoor lighting | Most reliable detection |
| 🔵 **Blue** | H: 100-130 | Bright lighting | Good contrast needed |
| 🟡 **Yellow** | H: 20-30 | Indoor lighting | Avoid yellow backgrounds |
| 🟣 **Purple** | H: 140-170 | Various lighting | Less common, good detection |
| 🧡 **Orange** | H: 5-20 | Indoor lighting | Great for autumn themes |
| 🧢 **Cyan** | H: 85-100 | Bright lighting | Cool blue-green effect |
| 🎀 **Pink** | H: 150-170 | Indoor lighting | Fun and vibrant |
| ⚪ **White** | S: 0-30, V: 200-255 | Bright lighting | Requires good contrast |
| ⚫ **Black** | V: 0-50 | Any lighting | Works with shadows |

### 🧪 **Color Testing Tools**

Use the interactive color tester to find the best color for your setup:

```bash
# Interactive color testing and calibration
python color_tester.py
```

This tool helps you:
- 📊 View all HSV color ranges
- 🔍 Test real-time color detection for each color
- 📸 Save detection test images
- 🎯 Find the best color for your lighting conditions

## 🔮 Magic Tips

- **Practice**: Try different movements and poses
- **Dramatic effect**: Move slowly for a more magical appearance
- **Multiple people**: Take turns or use different colored cloaks
- **Recording**: Use screen recording software to capture your magic tricks
- **Lighting effects**: Experiment with colored lighting for enhanced effects

---

**Enjoy your magical invisible cloak experience! 🧙‍♂️✨**

*"It is our choices that show what we truly are, far more than our abilities." - Albus Dumbledore*