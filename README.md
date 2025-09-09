
---

# EchoCore - Voice Reminder Assistant (Development Branch)

## 🎯 Overview
EchoCore is an offline voice-controlled reminder assistant built with Python and Kivy. This development branch contains the latest features and experimental implementations.

## 🚀 Current Features
- **Offline Voice Recognition** using Vosk models
- **Cross-platform** compatibility (macOS, Windows, Linux)
- **Native GUI** with Kivy framework
- **Reminder management** through voice commands
- **No internet dependency** for speech recognition

## 🛠️ Development Setup

### Prerequisites
```bash
Python 3.11+
pip
```

### Installation
1. **Clone the repository**
```bash
git clone -b development https://github.com/G-OrdiaD/EchoCore.git
cd EchoCore
```

2. **Create virtual environment**
```bash
python -m venv myenv_311
source myenv_311/bin/activate  # On macOS/Linux
# or
myenv_311\Scripts\activate    # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Vosk Model**
```bash
# Download small English model from:
# https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
# Unzip into project root directory
```

### Running the Application
```bash
python main.py
```

## 🗣️ Voice Commands
- "Remind me to [task] at [time]"
- "Set a reminder for [task]"
- "What are my reminders?"
- "Clear all reminders"

## 📁 Project Structure
```
EchoCore/
├── main.py              # Main application entry point
├── vosk-model-small-en-us-0.15/  # Speech recognition model
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Technical Stack
- **Frontend**: Kivy 2.3.1
- **Speech Recognition**: Vosk (offline)
- **Audio Processing**: PyAudio
- **Python**: 3.11.13

## 🐛 Known Issues
- Microphone permissions may require manual setup on macOS
- Vosk model needs to be downloaded separately
- UI layout optimization in progress

## 📋 Development Goals
- [ ] Implement reminder persistence
- [ ] Add notification system
- [ ] Improve voice command accuracy
- [ ] Enhance UI/UX design
- [ ] Add multi-language support

## 🤝 Contributing
1. Fork the development branch
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting
**Microphone Access Issues:**
- On macOS: System Settings → Privacy & Security → Microphone → Enable terminal access
- Test microphone with: `python -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_default_input_device_info())"`

**Vosk Model Issues:**
- Ensure model is downloaded and placed in project root
- Verify model path in code matches actual directory name

---

**Note**: This is the development branch - features may be unstable. For production use, check the main branch.