<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]](https://github.com/rhysdg/ollama-voice-jetson/contributors)
[![Apache][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
  <h3 align="center"> Ollama Voice: Jetson Xavier Edition</h2>
  <p align="center">
     Jetson (Xavier series) compatible LLM based assistant and robot control package<br />
    <a href="https://github.com/rhysdg/ollama-voice-jetson/wiki"<strong>Explore the docs »</strong></a>
    <br />
    <br />
    <img src="ollama-jetson.png" align="middle" width=200>
    <br />
    <br />
    <a href="https://github.com//issues">Report Bug</a>
    .
    <a href="https://github.com//issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
  * [The Story so Far](#the-story-so-far)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Scripts and Tools](#scripts-and-tools)
  * [Supplementary Data](#supplementary-data)
* [Proposed Updates](#proposed-updates)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project

### Built With

* [Ollama](https://ollama.com/)
* [Piper TTS](https://github.com/rhasspy/piper)
* [Open AI Whisper](https://openai.com/index/whisper/)
* [Pytorch](https://pytorch.org/)
* [Onnxruntime](https://onnxruntime.ai/)
* [Jetpack](https://developer.nvidia.com/embedded/jetpack)



### Hardware

* [Jetson Xavier NX Development Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit)
* [Seed studio Respeaker Microphone Array](https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/)
* Generic USB stereo speaker


### The Story So Far

This project came into fruition through an excited bit of research into the increasing ability to deploy LLMs on edge devices. It owes its inspiration and initial structure to a number of initiatives - most notably ollama reference above but also:


- [ollama voice mac](https://github.com/apeatling/ollama-voice-mac)
- [ollama voice](https://github.com/apeatling/ollama-voice-mac)

A number of changes have been made or are in progress that diverge from these original projects:

- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) has been swapped out for Piper TTS - while nsss and Sapi5 have great voice support for mac and Windows respectively, espeak leaves much to be desired for Linux.  Piper tts is not only fast but has outsanding pronounciation and quality in general - you'll find all dependencies and a sample voice is installed by this project

- I'm using [gemma 2b](https://ollama.com/library/gemma) rather than llama here with great results on the board. Both latency and mobile battery power

- Finally you'll notice that support is slowly coming to a halt for Xavier devices with Orin in the picture. This project is both an attenpt to keep the series alive as they're still incredibly powerful - quantised ollama models run with impressive low latency - but also an alternative approach to a dockerised environment for those who are both new to docker and docker as a tool to solve Jetson compatibility issues.

Given the last point the project assumes that you've made it as far as Jetpack 5.1.4 - although Jetpack 6 support would be great once I can get my hands on an Orin device!


<!-- GETTING STARTED -->
## Getting Started:

- We're assuming here that you've have a board ready to go - check out the hardware link above for the Xavier NX I'm using
- If you're not set up yet you'll need to to install jetpack 5.1.4 with an SD card or a NVMe SSD by folling the official guide [here](https://developer.nvidia.com/embedded/learn/get-started-jetson-xavier-nx-devkit)
- If you're headed down the NVMe road you can also use the the following bug fix [branch](https://github.com/rhysdg/bootFromExternalStorage/tree/bug-expand-external) from the fantastic [Jetson Hacks](https://github.com/jetsonhacks) in order to expand the partition size of your root on installation

- All installation scripts are self contained and debugged for this specific setup but note that you'll need to ensure you're in a **Python 3.9** virtual environment rather than the stock Python 3.8 - this is due to dependency conflicts at Piper-TTS. All dependencies at **install.sh** include any relevant 3.9 wheels as a result

- Download the pre-built torch 2.1.0 wheel for Python 3.9 at the following Google Drive [link](https://drive.google.com/file/d/1ufgHQtNfkCFTk_GHhkMe_ji1afGJLMbs/view?usp=sharing) and add to your project root

- Then simply run 
  ```bash
  sh install.sh
  ```

## Customisation:

- You'll notice a number of customisable options at the installation script
    - The whisper model downloaded to the `whisper` subfolder is the stock `base.pt`
    - The onnx voice available via the script is `en_GB-alba-medium.onnx` this is also easily changed by dropping a new voice into `voices`
- **assistant.yaml** also points to a number of project specific parrameters:
    - Notice that my ollama model is **mini-b** named after a robot I'm bulding - check out ollama's [customize prompt](https://github.com/ollama/ollama?tab=readme-ov-file#customize-a-prompt) section for more on this


### Notebooks

1. Coming soon

### Tools and Scripts
1. **coming soon**


### Testing
 - Jetpack 5.1.4 - Xavier NX Development Kit - passing
 - Likely appicable to an AGX Xavier too - I have one available - testing results shortly


### Supplementary Data

**coming soon**

### Latency benchmarks 

**coming soon**

### Similar projects

I went down a pretty lengthy rabbit hole for this one and for those of you who don't wish to stick exclusively to Python there's a numbe of great projects out there - these have not been tested with Jetson boards however:

- [lamma.cpp](https://github.com/ggerganov/llama.cpp)
- [Talk](https://github.com/yacineMTB/talk)


<!-- PROPOSED UPDATES -->
## Latest Updates
- June 3rd 2023 - Swapping out pygame for a terminal based space bar execution with **sshkeyboard**
- Incoming - Whisper tensorrt for better performance

<!-- PROPOSED UPDATES -->
## Future updates
- Wake word based activation
- command execution
- automatic image live camera retrieval and analysis
- optimised RAG
- pip package support

<!-- Contact -->
## Contact
- Project link: https://github.com/rhysdg/ollama-voice-jetson
- Email: [Rhys](rhysdgwilliams@gmail.com)


<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square
[contributors-shield]: https://img.shields.io/badge/contributors-2-orange
[license-shield]: https://img.shields.io/badge/License-GNU%20GPL-blue
[license-url]: LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/rhys-williams-b19472160/
