# Intel Arc GPU Setup Guide for noScribe

This guide will help you set up noScribe to use your Intel Arc GPU for accelerated transcription and speaker diarization.

## System Requirements

- **GPU**: Intel Arc Graphics (Arc 3, Arc 5, Arc 7, or Arc Pro)
- **Operating System**: Windows 11 or Linux (Ubuntu 20.04+)
- **RAM**: 8 GB minimum (16 GB recommended)
- **Python**: 3.8 or newer

## Installation Instructions

### For Windows with Intel Arc GPU

1. **Install Intel Graphics Drivers**
   - Download the latest Intel Arc GPU drivers from: https://www.intel.com/content/www/us/en/download/785597/
   - Install the drivers and restart your computer

2. **Install Python Dependencies**
   ```bash
   # Install PyTorch with Intel XPU support
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/xpu

   # Install Intel Extension for PyTorch
   pip install intel-extension-for-pytorch

   # Install noScribe dependencies
   pip install -r environments/requirements_win_intel_arc.txt
   ```

3. **Verify Installation**
   ```bash
   python test_intel_arc.py
   ```

   This script will check if your Intel Arc GPU is properly detected and configured.

### For Linux with Intel Arc GPU

1. **Install Intel GPU Compute Runtime**

   For Ubuntu/Debian:
   ```bash
   # Add Intel GPU repository
   wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | sudo gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg

   echo "deb [arch=amd64,i386 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy client" | sudo tee /etc/apt/sources.list.d/intel-gpu-jammy.list

   # Update and install drivers
   sudo apt-get update
   sudo apt-get install -y intel-opencl-icd intel-level-zero-gpu level-zero intel-media-va-driver-non-free libmfx1 libmfxgen1 libvpl2
   ```

   For other distributions, see: https://dgpu-docs.intel.com/driver/installation.html

2. **Install Python Dependencies**
   ```bash
   # Install PyTorch with Intel XPU support
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/xpu

   # Install Intel Extension for PyTorch
   pip install intel-extension-for-pytorch

   # Install noScribe dependencies
   pip install -r environments/requirements_linux_intel_arc.txt
   ```

3. **Verify Installation**
   ```bash
   python test_intel_arc.py
   ```

## Configuration

After installation, noScribe will automatically detect your Intel Arc GPU. However, you can manually configure the GPU settings in your `config.yml` file.

### Config File Location

The config file is located at:
- **Windows**: `%APPDATA%\noScribe\config.yml`
- **Linux**: `~/.config/noScribe/config.yml`
- **macOS**: `~/Library/Application Support/noScribe/config.yml`

### Recommended Settings for Intel Arc

Add or modify these settings in your `config.yml`:

```yaml
# Use Intel XPU (Arc GPU) for speaker diarization
pyannote_xpu: xpu

# Whisper will use optimized CPU inference (faster-whisper doesn't support XPU)
whisper_xpu: xpu  # Will automatically fall back to CPU for Whisper

# Optional: Adjust batch sizes based on your VRAM
# For Intel Arc 140V with 18 GB VRAM, you can use larger batch sizes
```

## Performance Notes

### What Gets Accelerated

1. **PyAnnote Speaker Diarization** ✓
   - Runs on Intel XPU (Arc GPU)
   - Significant speedup for speaker identification
   - Optimized with Intel Extension for PyTorch (IPEX)

2. **Whisper Transcription** ⚠
   - Currently runs on CPU with CTranslate2 optimization
   - faster-whisper doesn't support Intel XPU directly
   - Still very fast due to CTranslate2 optimizations

### Expected Performance

With your Intel Arc 140V (18 GB VRAM):
- **Speaker Diarization**: 2-4x faster compared to CPU
- **Transcription**: Similar to optimized CPU (CTranslate2 is already very fast)
- **Overall**: Significant improvement in diarization-heavy workloads

### Memory Usage

Your Intel Arc 140V has 18 GB of VRAM, which is excellent for noScribe:
- PyAnnote models use ~2-4 GB VRAM
- You have plenty of headroom for large audio files
- Can process longer audio segments without splitting

## Troubleshooting

### GPU Not Detected

If `test_intel_arc.py` reports that XPU is not available:

1. **Check drivers**: Make sure Intel Arc drivers are installed
   ```bash
   # Windows: Check Device Manager
   # Linux: Run `clinfo` or `sycl-ls`
   ```

2. **Verify PyTorch XPU support**:
   ```bash
   python -c "import torch; print(f'XPU available: {torch.xpu.is_available() if hasattr(torch, \"xpu\") else False}')"
   ```

3. **Check IPEX installation**:
   ```bash
   python -c "import intel_extension_for_pytorch as ipex; print(f'IPEX version: {ipex.__version__}')"
   ```

### Out of Memory Errors

If you encounter OOM errors:
1. Reduce batch sizes in config.yml
2. Process shorter audio segments
3. Close other GPU-intensive applications

### Slow Performance

If performance is slower than expected:
1. Make sure you're using the correct `pyannote_xpu: xpu` setting
2. Check that no other process is using the GPU
3. Verify Intel Arc drivers are up to date

## Additional Resources

- **Intel Extension for PyTorch**: https://intel.github.io/intel-extension-for-pytorch/
- **Intel Arc Drivers**: https://www.intel.com/content/www/us/en/products/docs/discrete-gpus/arc/downloads.html
- **Intel GPU Documentation**: https://dgpu-docs.intel.com/
- **noScribe Issues**: https://github.com/kaixxx/noScribe/issues

## Support

If you encounter issues:
1. Run `test_intel_arc.py` and share the output
2. Check the log file in your noScribe directory
3. Open an issue on GitHub with your system details

---

**Note**: This Intel Arc support is experimental. Performance and compatibility may vary depending on your system configuration and driver versions.
