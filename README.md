# ✨ Image Generation App

A beautiful, lightning-fast AI image generation desktop application built with Python, featuring a modern bento-grid UI and powered by Stable Diffusion Turbo.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎨 Features

- **Ultra-Fast Generation**: Powered by SD-Turbo model for near-instant image generation
- **Modern UI**: Beautiful dark-themed interface with bento-grid layout
- **GPU Accelerated**: Automatic CUDA support for faster generation
- **Real-time Progress**: Visual feedback with progress bars and status updates
- **Easy to Use**: Simple, intuitive interface suitable for everyone
- **Auto-Save**: All generated images are automatically saved with timestamps
- **Customizable Settings**: Adjustable generation steps and guidance scale

## 🖼️ Preview

The app features:
- Clean, modern dark interface
- Real-time image generation preview
- Adjustable generation parameters
- Automatic image saving with timestamps
- Visual progress indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NVIDIA GPU with CUDA support (recommended) or CPU
- Hugging Face account and API token

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd image-generation-app
```

2. **Install PyTorch with CUDA support** (for GPU acceleration)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

For CPU-only installation:
```bash
pip install torch torchvision torchaudio
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Hugging Face Token**
   - Get your token from [Hugging Face](https://huggingface.co/settings/tokens)
   - Open `authtoken.py` and replace `your_huggingface_token_here` with your actual token:
    ```python

  auth_token = "hf_your_actual_token_here"
   ```

6. **Run the application**
```bash
python app.py
```

## 📋 Requirements

### Core Dependencies
- customtkinter 5.2.2 - Modern UI framework
- Pillow 10.4.0 - Image processing
- diffusers 0.30.3 - Stable Diffusion pipeline
- transformers 4.46.3 - Model support
- PyTorch (with CUDA for GPU support)

See `requirements.txt` for full list of dependencies.

## 🎮 Usage

1. **Launch the app**: Run `python app.py`
2. **Enter a prompt**: Describe the image you want to generate in the text box
3. **Adjust settings** (optional):
   - **Steps**: Number of generation steps (1-4, lower is faster)
   - **Guidance**: How closely to follow the prompt (0.0-2.0)
4. **Click "🚀 Generate Image"**: Watch your creation come to life!
5. **Save your work**: Images are auto-saved, or use the "💾 Save Image" button

### Example Prompts

- "A serene landscape with mountains at sunset"
- "A futuristic city with flying cars"
- "A cute robot playing with puppies"
- "Abstract art with vibrant colors and geometric shapes"
- "A magical forest with glowing mushrooms"

## ⚙️ Configuration

### Model Settings

The app uses **SD-Turbo** by default for fast generation. You can modify the model in `app.py`:

```python
modelid = "stabilityai/sd-turbo"  # Change this to use different models
```

### Performance Optimization

For CUDA-enabled GPUs, the app automatically enables:
- Attention slicing for memory efficiency
- VAE slicing for reduced memory usage
- FP16 precision for faster computation

## 🐛 Troubleshooting

### Common Issues

**"CUDA out of memory"**
- Reduce image resolution
- Close other GPU-intensive applications
- The app will automatically fall back to CPU if needed

**"Model loading failed"**
- Verify your Hugging Face token is correct
- Ensure you have accepted the model license on Hugging Face
- Check your internet connection

**"Import errors"**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify PyTorch installation: `python -c "import torch; print(torch.__version__)"`

**Slow generation**
- Ensure CUDA is properly installed and detected
- Check device status in the app footer
- Consider using fewer generation steps

## 📁 Project Structure

```
image-generation-app/
│
├── app.py              # Main application file
├── authtoken.py        # Hugging Face authentication
├── requirements.txt    # Python dependencies
├── README.md          # This file
│
└── generated_*.png    # Generated images (auto-created)
```

## 🔒 Security Note

**Never commit your `authtoken.py` file with your actual token!** Add it to `.gitignore`:

```bash
echo "authtoken.py" >> .gitignore
```

## 👨‍💻 Author

**Ayushman Banerjee**

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) for the SD-Turbo model
- [Hugging Face](https://huggingface.co/) for the Diffusers library
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI framework

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the [Diffusers documentation](https://huggingface.co/docs/diffusers)

---

**Made with ❤️ and AI**
