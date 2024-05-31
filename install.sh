sudo apt-get install python3-pip
sudo apt-get install libopenblas-base libopenmpi-dev libomp-dev portaudio19-dev espeak ffmpeg libespeak1 python3-pyaudio
wget https://developer.download.nvidia.com/compute/redist/jp/v512/pytorch/torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl

mkdir whisper && cd whisper
wget https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt
cd ..

pip install -r requirements.txt

