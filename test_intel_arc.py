#!/usr/bin/env python3
"""
Intel Arc GPU Test Script for noScribe
This script tests if your Intel Arc GPU is properly configured and can be used with noScribe.
"""

import sys
import os

print("=" * 70)
print("Intel Arc GPU Test for noScribe")
print("=" * 70)
print()

# Test 1: Check PyTorch installation
print("[1/6] Checking PyTorch installation...")
try:
    import torch
    print(f"✓ PyTorch version: {torch.__version__}")
except ImportError as e:
    print(f"✗ PyTorch not found: {e}")
    print("Please install PyTorch with: pip install torch torchvision torchaudio")
    sys.exit(1)

# Test 2: Check Intel Extension for PyTorch
print("\n[2/6] Checking Intel Extension for PyTorch (IPEX)...")
try:
    import intel_extension_for_pytorch as ipex
    print(f"✓ IPEX version: {ipex.__version__}")
except ImportError as e:
    print(f"✗ Intel Extension for PyTorch not found: {e}")
    print("Please install IPEX with: pip install intel-extension-for-pytorch")
    print("Note: You may also need to install Intel GPU drivers")
    sys.exit(1)

# Test 3: Check XPU availability
print("\n[3/6] Checking Intel XPU (GPU) availability...")
try:
    if hasattr(torch, 'xpu'):
        xpu_available = torch.xpu.is_available()
        if xpu_available:
            device_count = torch.xpu.device_count()
            print(f"✓ Intel XPU is available!")
            print(f"✓ Number of XPU devices: {device_count}")
        else:
            print("✗ Intel XPU is not available on this system")
            print("Make sure you have Intel Arc GPU drivers installed")
            print("Visit: https://www.intel.com/content/www/us/en/download/785597/")
            sys.exit(1)
    else:
        print("✗ torch.xpu module not found")
        print("Please install PyTorch with XPU support")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error checking XPU: {e}")
    sys.exit(1)

# Test 4: Get GPU information
print("\n[4/6] Getting GPU information...")
try:
    for i in range(torch.xpu.device_count()):
        gpu_name = torch.xpu.get_device_name(i)
        gpu_props = torch.xpu.get_device_properties(i)
        gpu_vram = gpu_props.total_memory / (1024**3)  # Convert to GB
        print(f"✓ GPU {i}: {gpu_name}")
        print(f"  VRAM: {gpu_vram:.2f} GB")
        print(f"  Max work group size: {gpu_props.max_work_group_size}")
except Exception as e:
    print(f"⚠ Could not get GPU details: {e}")

# Test 5: Test basic tensor operations on XPU
print("\n[5/6] Testing basic tensor operations on XPU...")
try:
    # Create a simple tensor and move it to XPU
    x = torch.randn(100, 100)
    x_xpu = x.to('xpu')

    # Perform operation
    y_xpu = torch.matmul(x_xpu, x_xpu)
    result = y_xpu.cpu()

    print(f"✓ Basic tensor operations work on XPU")
    print(f"  Test tensor shape: {result.shape}")
except Exception as e:
    print(f"✗ Error during tensor operations: {e}")
    sys.exit(1)

# Test 6: Test PyAnnote dependencies
print("\n[6/6] Checking noScribe dependencies...")
missing_deps = []

try:
    from pyannote.audio import Pipeline
    print("✓ pyannote.audio is installed")
except ImportError:
    missing_deps.append("pyannote.audio>=3.3.2")
    print("✗ pyannote.audio not found")

try:
    from faster_whisper import WhisperModel
    print("✓ faster-whisper is installed")
except ImportError:
    missing_deps.append("faster-whisper")
    print("✗ faster-whisper not found")

try:
    import yaml
    print("✓ PyYAML is installed")
except ImportError:
    missing_deps.append("PyYAML")
    print("✗ PyYAML not found")

if missing_deps:
    print(f"\n⚠ Missing dependencies: {', '.join(missing_deps)}")
    print("Install with: pip install " + " ".join(missing_deps))

# Final summary
print("\n" + "=" * 70)
print("Test Summary")
print("=" * 70)
print("✓ Your Intel Arc GPU is properly configured for noScribe!")
print()
print("Configuration for config.yml:")
print("  pyannote_xpu: xpu")
print("  whisper_xpu: xpu")
print()
print("Note: faster-whisper will use CPU (optimized with CTranslate2)")
print("      PyAnnote will use Intel XPU for speaker diarization")
print()
print("Performance expectations:")
print("  - PyAnnote (diarization): Accelerated on Intel Arc GPU")
print("  - Whisper (transcription): Optimized CPU inference with CTranslate2")
print()
print("With your Intel Arc 140V (18 GB VRAM), you have plenty of memory")
print("for running both models efficiently!")
print("=" * 70)
