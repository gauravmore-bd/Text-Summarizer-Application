# 🧠 Text Summarizer App

A desktop-based Text Summarization application built using **Python**, **Tkinter**, and **Hugging Face Transformers**. It allows users to summarize long pieces of text or uploaded `.txt` files using state-of-the-art NLP models.

---

## 🚀 Features

- 📄 Upload `.txt` files or input raw text
- 📝 Summarize large paragraphs using NLP
- 🎛️ Adjustable summary length (min/max length sliders)
- ⚡ Real-time feedback with progress indication
- 🎨 Modern, responsive GUI (Tkinter-based)

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** – GUI framework
- **Transformers** – Hugging Face models for summarization
- **Torch** – Backend for transformer models

---

## 📦 Installation

### 🔧 Clone the Repository
```bash
git clone https://github.com/gauravmore-bd/text-summarizer-app.git
cd text-summarizer-app

## 🚚 Deployment (Desktop Executable)

To deploy the app as a standalone `.exe` (Windows):

### 1. Install PyInstaller
```bash
pip install pyinstaller


```
## 🖥️ How to Run

Run the application using Python:

```bash
python summarizer.py

---
```
### 2. **Folder Structure**

```markdown

text-summarizer-app/
│
├── summarizer.py # Main Python GUI app
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── .gitignore # Git ignore rules
└── assets/ # (Optional) images/icons/screenshots
```
## 🚚 Deployment (Desktop Executable)

### 1. Install PyInstaller
```bash
pip install pyinstaller

```
### Create Executable
```bash
pyinstaller --onefile summarizer.py
```

---

### 5. **Features**

```markdown
## 🚀 Features

- Upload `.txt` files or input raw text  
- Summarize large paragraphs using NLP  
- Adjustable summary length with sliders  
- Real-time progress feedback  
- User-friendly Tkinter GUI  
