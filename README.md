# 🦮 Multimodal AI Assistant for the Visually Impaired

An AI-powered real-time assistive system designed to help visually impaired individuals better understand their surroundings using Computer Vision, OCR, Scene Understanding, and Speech Interaction.

VisionAssist AI combines object detection, scene captioning, text recognition, and natural voice feedback into a single desktop application that enables hands-free environmental awareness.

---

# ✨ Features

- 🎯 Real-time object detection using YOLO11
- 🖼️ AI-powered scene understanding using Microsoft Florence-2 Large
- 📖 Text recognition using EasyOCR
- 🔊 Natural speech output using Microsoft Edge-TTS
- 🎙️ Hands-free voice interaction
- 🧠 Scene memory to prevent repetitive announcements
- 📍 Relative object localization (Left, Center, Right)
- 📏 Approximate object distance estimation
- ⚡ Priority-based response generation
- 🔄 Continuous real-time assistance
- 🖥️ User Mode and Developer Mode interface

---

# 🏗️ System Architecture

```
                    Camera
                       │
                       ▼
             YOLO11 Object Detection
                       │
        ┌──────────────┴──────────────┐
        │                             │
 Bounding Boxes                Object Positions
        │                             │
        └──────────────┬──────────────┘
                       ▼
          Florence-2 Scene Understanding
                       │
                Scene Description
                       ▼
                 EasyOCR Extraction
                       │
                  Recognized Text
                       ▼
              Response Generator
                       │
               Priority Assignment
                       ▼
                 Speech Queue
                       ▼
           Microsoft Edge-TTS Output
```

---

# 📂 Project Structure

```
multimodal-ai-assistant/

│── app.py
│── README.md
│── requirements.txt
│── .gitignore
│
├── modules/
│   ├── assistant.py
│   ├── camera_manager.py
│   ├── caption.py
│   ├── object_detection.py
│   ├── ocr.py
│   ├── priority.py
│   ├── response_generator.py
│   ├── scene_memory.py
│   ├── speech.py
│   ├── speech_queue.py
│   ├── state_manager.py
│   └── voice_input.py
│
├── assets/
│
└── outputs/
```

---

# 🛠️ Technologies Used

## Programming Language

- Python 3.11

## AI Models

- YOLO11
- Microsoft Florence-2 Large
- EasyOCR

## Libraries

- PyTorch
- Transformers
- Ultralytics
- OpenCV
- EasyOCR
- SpeechRecognition
- Edge-TTS
- Pygame
- PyAudio

---

# 💻 Requirements

- Python 3.11 or newer
- Windows 10/11 or Linux
- Webcam
- Microphone
- Speakers or Headphones
- NVIDIA GPU (Recommended for Florence-2)

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/ManibhushanaKG/multimodal-ai-assistant.git

cd multimodal-ai-assistant
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install PyTorch

### CUDA 12.8

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

### CPU Only

```bash
pip install torch torchvision torchaudio
```

---

## 4. Install Project Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. First Run

The application automatically downloads the required AI models during the first launch.

This includes:

- YOLO11 model weights
- Florence-2 Large model (~1.5 GB)

The initial startup may take several minutes depending on your internet connection.

---

# ▶️ Running the Project

```bash
python app.py
```

---

# 🎙️ Voice Commands

Current supported commands:

- **Start**
- **Stop**

---

# 💡 How It Works

1. Captures live video frames from the webcam.
2. Detects objects using YOLO11.
3. Generates a scene description using Florence-2.
4. Reads visible text using EasyOCR.
5. Combines all outputs into a single prioritized response.
6. Converts the response into natural speech.
7. Uses scene memory to avoid repeated announcements.

---

# 📌 Example Output

```
You appear to be in a bedroom.

Person very close, center.

Bottle on the right.

Text says "HELLO CHATGPT".
```

---

# 📷 Sample Capabilities

- ✅ Detect people
- ✅ Detect vehicles
- ✅ Detect household objects
- ✅ Read printed text
- ✅ Describe indoor and outdoor scenes
- ✅ Announce object positions
- ✅ Continuous spoken assistance

---

# ⚡ Performance

- Real-time object detection
- Scene caption generation
- OCR text extraction
- Continuous speech output
- Intelligent announcement filtering

---

# ⚠️ Known Limitations

- Detection is limited to COCO object classes.
- OCR accuracy depends on image quality.
- Distance estimation is approximate.
- Florence-2 requires significant RAM/VRAM.
- Navigation assistance is limited to scene awareness.

---

# 🔮 Future Improvements

- Indoor navigation
- Obstacle avoidance
- Face recognition
- Currency recognition
- Medication identification
- Open-vocabulary object detection
- Custom-trained detection model
- Smart glasses integration
- Mobile application support

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Manibhushana KG**

Computer Science Engineering Student

Bangalore Institute of Technology

GitHub:
https://github.com/ManibhushanaKG

LinkedIn:
https://www.linkedin.com/in/manibhushanakg

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.