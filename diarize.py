# noScribe - AI-powered Audio Transcription
# Copyright (C) 2023 Kai Dröge
# ported to MAC by Philipp Schneider (gernophil)

# Diarization with PyAnnote (https://github.com/pyannote/pyannote-audio)
# usage: python diarize.py <device['cpu', 'mps', 'cuda', 'xpu']> <audio file> <output yaml-file>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import platform
import yaml
from pyannote.audio import Pipeline
import torch
from typing import Any, Mapping, Optional, Text
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

# Try to import Intel Extension for PyTorch for Intel Arc GPU support
try:
    import intel_extension_for_pytorch as ipex
    IPEX_AVAILABLE = True
except ImportError:
    IPEX_AVAILABLE = False

app_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(app_dir)

device = sys.argv[1]
audio_file = sys.argv[2]
segments_yaml = sys.argv[3]
if sys.argv[4].isdigit():
    my_num_speakers = int(sys.argv[4])
else:
    my_num_speakers = None

class SimpleProgressHook:
    #Hook to show progress of each internal step
    def __init__(self, parent, transient: bool = False):
        super().__init__()
        self.parent = parent
        self.transient = transient

    def __enter__(self):
        self.progress = 0
        return self

    def __exit__(self, *args):
        pass

    def __call__(
        self,
        step_name: Text,
        step_artifact: Any,
        file: Optional[Mapping] = None,
        total: Optional[int] = None,
        completed: Optional[int] = None,
    ):                       
        if completed is None:
            completed = total = 1

        if not hasattr(self, 'step_name') or step_name != self.step_name:
            self.step_name = step_name
        
        progress_percent = int(completed/total*100)
        if progress_percent > 100:
            progress_percent = 100
        print(f'progress {step_name} {progress_percent}', flush=True)
        
# Start Diarization:

try:
    if platform.system() == 'Windows':
        # Check if Intel XPU is requested and available
        if device == 'xpu':
            if not IPEX_AVAILABLE:
                print("log: Intel Extension for PyTorch not found. Install it for Intel Arc GPU support.")
                print("log: Falling back to CPU.")
                device = 'cpu'
            elif not (hasattr(torch, 'xpu') and torch.xpu.is_available()):
                print("log: Intel XPU requested but not available on this system.")
                print("log: Falling back to CPU.")
                device = 'cpu'
            else:
                print(f"log: Using Intel XPU (Intel Arc GPU) for diarization")
                # Optimize models for Intel XPU
                try:
                    torch.xpu.empty_cache()
                except:
                    pass

        pipeline = Pipeline.from_pretrained(os.path.join(app_dir, 'pyannote', 'pyannote_config.yaml'))
        pipeline.to(torch.device(device))

        # Apply IPEX optimizations if using XPU
        if device == 'xpu' and IPEX_AVAILABLE:
            try:
                # Optimize the pipeline models for Intel XPU
                pipeline = ipex.optimize(pipeline)
                print(f"log: PyAnnote pipeline optimized with Intel Extension for PyTorch")
            except Exception as e:
                print(f"log: Could not apply IPEX optimizations: {e}")

    elif platform.system() in ("Darwin", "Linux"): # = MAC or Linux
        if device == 'mps' and not torch.backends.mps.is_available():  # should only happen on x86_64, but checked on all archs to be sure
            device = 'cpu'
            print("log: 'pyannote_xpu: mps' was selected, but mps is not available on this system!")
            print("log: This happens, because availability cannot be checked earlier.")
            print("log: 'pyannote_xpu: cpu' was set.") # The string needs to be the same as in noScribe.py `if line.strip() == "log: 'pyannote_xpu: cpu' was set.":`.

        # Check if Intel XPU is requested on Linux
        if device == 'xpu':
            if not IPEX_AVAILABLE:
                print("log: Intel Extension for PyTorch not found. Install it for Intel Arc GPU support.")
                print("log: Falling back to CPU.")
                device = 'cpu'
            elif not (hasattr(torch, 'xpu') and torch.xpu.is_available()):
                print("log: Intel XPU requested but not available on this system.")
                print("log: Falling back to CPU.")
                device = 'cpu'
            else:
                print(f"log: Using Intel XPU (Intel Arc GPU) for diarization")
                try:
                    torch.xpu.empty_cache()
                except:
                    pass

        with open(os.path.join(app_dir, 'pyannote', 'pyannote_config.yaml'), 'r') as yaml_file:
            pyannote_config = yaml.safe_load(yaml_file)

        pyannote_config['pipeline']['params']['embedding'] = os.path.join(app_dir, *pyannote_config['pipeline']['params']['embedding'].split("/"))
        pyannote_config['pipeline']['params']['segmentation'] = os.path.join(app_dir, *pyannote_config['pipeline']['params']['segmentation'].split("/"))

        tmpdir = TemporaryDirectory('noScribe_diarize')
        with open(os.path.join(tmpdir.name, 'pyannote_config_macOS.yaml'), 'w') as yaml_file:
            yaml.safe_dump(pyannote_config, yaml_file)

        pipeline = Pipeline.from_pretrained(os.path.join(tmpdir.name, 'pyannote_config_macOS.yaml'))
        pipeline.to(torch.device(device))

        # Apply IPEX optimizations if using XPU on Linux
        if device == 'xpu' and IPEX_AVAILABLE:
            try:
                pipeline = ipex.optimize(pipeline)
                print(f"log: PyAnnote pipeline optimized with Intel Extension for PyTorch")
            except Exception as e:
                print(f"log: Could not apply IPEX optimizations: {e}")

    else:
        raise Exception('Platform not supported yet.')

    with SimpleProgressHook(parent=None) as hook:
        if my_num_speakers is not None:
            diarization = pipeline(audio_file, hook=hook, num_speakers=my_num_speakers) # apply the pipeline to the audio file
        else:
            diarization = pipeline(audio_file, hook=hook)

    seg_list = []

    for segment, _, label in diarization.itertracks(yield_label=True):
        seg_list.append({'start': int(segment.start * 1000), 
                         'end': int((segment.start + segment.duration) * 1000),
                         'label': label})
            
    with open(segments_yaml, 'w') as filestream:
        yaml.safe_dump(seg_list, filestream)

except Exception as e:
    print('error ', e, file=sys.stderr)
    sys.exit(1) # return error code