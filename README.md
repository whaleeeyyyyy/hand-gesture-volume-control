# 🖐️ Hand Gesture Volume Control

Control your Windows volume with hand gestures! Pinch your thumb and index finger to change the volume.

![Demo](screenshots/demo.gif)

## ✨ Features

- 🖐️ Real-time hand tracking
- 🔊 System volume control
- 📹 Live camera feed
- 🎨 Beautiful GUI
- ⚡ Fast and responsive
- 🔒 Uses virtual environment (clean installation)

## 🚀 Quick Start (3 Easy Steps)

### Prerequisites

- Windows 10/11
- Python 3.8 or higher ([Download here](https://www.python.org/downloads/))
  - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation!
- Webcam
- ~300MB free disk space

### Step 1: Download Project

```bash
# Option 1: Download ZIP
# Click "Code" → "Download ZIP" → Extract to folder

# Option 2: Use Git
git clone https://github.com/yourusername/hand-gesture-volume-control.git
cd hand-gesture-volume-control
```

### Step 2: Run Setup (One-Time Only)

```bash
# Double-click: setup.bat
# This will:
#   ✓ Create virtual environment
#   ✓ Install all dependencies
#   ✓ Take 2-3 minutes
```

### Step 3: Launch App

```bash
# Double-click: run.bat
# App will start automatically!
```

## 🎮 How to Use

1. **Show your hand** to the camera (palm facing forward)
2. **Pinch fingers together** (thumb + index) = Lower volume
3. **Spread fingers apart** = Higher volume
4. **Press X** on window to close

## 📂 Project Structure

hand-gesture-volume-control/
├── gesture_volume_app.py # Main application
├── requirements.txt # Python dependencies
├── setup.bat # One-time setup script
├── run.bat # Launch application
├── clean.bat # Remove virtual environment (optional)
├── venv/ # Virtual environment (auto-created)
└── README.md # This file

## 🔧 Manual Installation (Advanced)

If you prefer command line:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python gesture_volume_app.py
```

## 🐛 Troubleshooting

### "Python is not recognized"

- **Solution**: Reinstall Python and check "Add Python to PATH"
- Or add Python manually to system PATH

### "venv creation failed"

```bash
# Try installing virtualenv explicitly
pip install virtualenv
python -m venv venv
```

### "Camera not working"

- Allow camera permissions in Windows Settings
- Close other apps using camera (Zoom, Teams, Skype)
- Try different USB port (if external webcam)

### "Volume not changing"

- Run as Administrator (right-click run.bat → Run as administrator)
- Check Windows volume is not muted
- Reinstall pycaw: `pip install pycaw --upgrade`

### "Missing module" error

```bash
# Activate venv and reinstall
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

### Start fresh

```bash
# Double-click: clean.bat (removes venv)
# Then run: setup.bat (reinstalls everything)
```

## 🎨 Customization

Edit `gesture_volume_app.py`:

```python
# Window size (line ~20)
self.root.geometry("1000x700")  # Width x Height

# Detection sensitivity (line ~28)
min_detection_confidence=0.7    # 0.5 = easier, 0.9 = stricter

# Gesture range (line ~199)
volume = np.interp(distance, [30, 200], [0, 100])
# [30, 200] = min/max finger distance in pixels
```

## 🧹 Uninstallation

```bash
# Option 1: Delete entire folder
# (Virtual environment is self-contained)

# Option 2: Clean venv only
# Double-click: clean.bat
```

## 📸 Screenshots

### Main Interface

![Main](screenshots/main.png)

### Hand Detection

![Detection](screenshots/detection.png)

## 💡 Why Virtual Environment?

- ✅ **Isolated**: Doesn't affect your system Python
- ✅ **Clean**: Easy to remove (just delete venv folder)
- ✅ **Reproducible**: Same setup for everyone
- ✅ **Safe**: No conflicts with other projects
- ✅ **Professional**: Industry best practice

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🌟 Show Your Support

If this helped you, please ⭐ star this repository!

## 📬 Contact

Questions or issues? Open an issue on GitHub!

---

Made with ❤️ using Python, OpenCV, MediaPipe, and Tkinter

**Virtual Environment Size**: ~250MB (self-contained, safe to delete)
