# ✨ Docify

**Transform your code into beautiful documentation, instantly.**

An AI-powered tool that automatically generates comprehensive documentation from your code and provides an interactive chat interface to answer questions about your codebase.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## ✨ Features

- 📄 **Instant Documentation** - Generate professional Word documents with one click
- 💬 **AI Code Assistant** - Chat with AI to understand any codebase
- 🌍 **13+ Languages** - Python, JavaScript, Java, C++, Go, Rust, and more
- 🎨 **Beautiful Interface** - Modern UI with smooth animations
- 🔒 **Secure** - Token-based API authentication
- ⚡ **Fast** - GPU-accelerated responses with Mistral AI

---

## 🎯 Why Docify?

Ever opened old code and thought *"What does this even do?"* 

Docify solves that problem. Upload your code, and get:
- Professional documentation in seconds
- Instant answers to your questions
- Clear explanations of complex logic

Perfect for developers, teams, and anyone who needs to understand code quickly.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **AI Model** | Mistral-Nemo-Instruct (7B) |
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **Documents** | python-docx |
| **Hosting** | Kaggle + ngrok |

---

## 📋 Supported Languages
```
Python • JavaScript • TypeScript • Java • C++ • C • C# 
Go • Rust • PHP • Ruby • Swift • Kotlin
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Kaggle account with GPU quota
- ngrok account ([free tier works](https://ngrok.com))

### Step 1: Setup Backend

1. **Go to Kaggle**
   - Upload `backend/docify_api.ipynb`
   - Enable GPU accelerator (Settings → Accelerator → GPU T4 x2)
   - Enable internet access

2. **Configure ngrok**
   - Get your auth token from [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
   - Paste it in the notebook (cell 7)
   - Change the API key if desired (default: `secret123`)

3. **Run the notebook**
   - Click "Run All"
   - Wait for model to load (~3 minutes)
   - Copy the ngrok URL from output

### Step 2: Setup Frontend
```bash
# Clone repository
git clone https://github.com/yourusername/docify.git
cd docify/frontend

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Step 3: Connect & Use

1. Open the Streamlit app (opens automatically in browser)
2. Enter your ngrok URL in the sidebar
3. Enter your API key
4. Click "Test Connection"
5. Upload a code file and start using Docify!

---

## 📖 Usage

### Generate Documentation

1. **Upload** your code file (any supported language)
2. Navigate to **"Generate Documentation"** tab
3. Click **"Generate Documentation"**
4. Download your formatted Word document

### Chat with Your Code

1. **Upload** your code file
2. Go to **"Chat with AI"** tab
3. Ask questions like:
   - "What does the main function do?"
   - "Are there any bugs in this code?"
   - "How can I optimize this?"
4. Get instant AI-powered answers


---

## 🎥 Demo Video

[Watch the demo on LinkedIn →](#)

---

## ⚙️ Configuration

### API Settings

Configure in the Streamlit sidebar:
- **Ngrok URL**: Your public API endpoint
- **API Key**: Authentication token (set in Kaggle notebook)

### Model Parameters

Adjust in `backend/docify_api.ipynb`:
```python
max_new_tokens = 1500  # Length of documentation
temperature = 0.3      # Creativity (0.0-1.0)
top_p = 0.92          # Sampling threshold
```

---

## 🏗️ Architecture
```
┌─────────────────┐
│  Streamlit UI   │ (Frontend)
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│   FastAPI       │ (Backend)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Mistral AI     │ (7B Model)
│  + GPU Accel    │
└─────────────────┘
         │
         ↓
┌─────────────────┐
│  python-docx    │ (Document Gen)
└─────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Hesham Abdelnaser**

- LinkedIn: [Your LinkedIn Profile](#)
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) - For the incredible language model
- [Streamlit](https://streamlit.io/) - For the amazing web framework
- [Kaggle](https://www.kaggle.com/) - For free GPU access
- [ngrok](https://ngrok.com/) - For secure tunneling

---

## ⚠️ Important Notes

- Kaggle sessions expire after 12 hours of inactivity
- Keep your API keys and ngrok URLs secure
- Large files (>5000 lines) are automatically truncated
- First response may take 30-60 seconds while model loads

---

## 🐛 Known Issues

- Very long code files may hit token limits
- Kaggle GPU quota limits apply
- ngrok free tier has connection limits

See [Issues](https://github.com/yourusername/docify/issues) for full list.

---

## 🗺️ Roadmap

- [ ] Support for more languages
- [ ] PDF export option
- [ ] Code diff documentation
- [ ] VS Code extension
- [ ] Self-hosted option
- [ ] Multi-file project support

---

## ⭐ Show Your Support

If Docify helped you, please give it a star! It helps others discover the project.

---

<div align="center">

**Made with ❤️ by Hesham Abdelnaser**

[⬆ Back to Top](#-docify)

</div>
```

---