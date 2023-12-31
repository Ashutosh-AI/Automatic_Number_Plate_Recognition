# Automatic_Number_Plate_Recognition

![Interface](https://github.com/Ashutosh-AI/Automatic_Number_Plate_Recognition/assets/53949585/034927a8-a893-404e-aa5f-1ddaff74507b)

**Automatic Number Plate Recognition (ANPR)** is the process of reading the characters on the plate with various optical character recognition (OCR) methods by separating the plate region on the vehicle image obtained from automatic plate recognition.

## Table of Content

- [Automatic Number Plate Recognition](#automatic-number-plate-recognition)

  * [What will you learn this project ](#what-will-you-learn-this-project)
  * [Dataset](#dataset)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Project architecture](#project-architecture)

## What will you learn from this project 

* Custom Object Detection using SSD
* Scene Text Detection
* Scene Text Recognition
* Optic Character Recognition
* PyTesseract
* Applying project in Real Time
* Develop a front UI using pyqt5

## Dataset
The dataset I use for license plate detection:  

https://www.kaggle.com/datasets/andrewmvd/car-plate-detection

## Installation

Clone repo and install requirements.txt in a Python>=3.7.0 environment.

## Usage

After installing the req libraries, you can run the project by main.py.

    python mainApp.py

![runing_ss](https://github.com/Ashutosh-AI/Automatic_Number_Plate_Recognition/assets/53949585/d252cff7-97b6-4cbb-9705-f7afc37c7645)

## Project architecture

The pipeline in the project is as follows:  

The first step to detect Number plates using SSD Networks
- After detecting the plate, apply the ocr, Apply the extracted plate to PyTesseract
- Get plate text
- Write Database and CSV format
- Upload to Qt Designer based UI
