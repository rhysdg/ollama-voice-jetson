#!/bin/bash

sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install -y g++-11

sudo apt-get install python3-pip
sudo apt-get install libopenblas-base libopenmpi-dev libomp-dev portaudio19-dev espeak ffmpeg libespeak1 python3-pyaudio

###grabbing all relevant wheels
wget https://download.pytorch.org/whl/cpu/torch-2.1.0-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl#sha256=de7d63c6ecece118684415a3dbd4805af4a4c1ee1490cccf7405d8c240a481b4
wget https://nvidia.box.com/shared/static/6orewbbm76n871pmchr7u3nfeecl5r20.whl -O onnxruntime_gpu-1.17.0-cp39-cp39-linux_aarch64.whl

#Grabbing Open AI Whisper base model 
mkdir whisper && cd whisper
wget https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt

cd ..

#Feel free to change to whatever vocie you need!
mkdir voices && cd voices
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx?download=true
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alba/medium/en_GB-alba-medium.onnx.json?download=true.json

cd ..

pip install -r requirements.txt

echo "done!"