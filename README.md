# EmergenSee AI Assistant

## Description

**EmergenSee AI Assistant** is an innovative real-time application designed to bridge the communication gap for the deaf and hard-of-hearing community in public spaces, specifically within a mall environment. The system translates Indonesian Sign Language (SIBI) into text and uses this input to power a location-based virtual assistant.

Users can ask questions like "di mana toilet?" using sign language, and the application will recognize the signs, construct the sentence, and provide a direct, helpful answer with directions relative to the user's current location.

## How It Works

The application operates through a sophisticated pipeline that processes video input and delivers an intelligent response in a matter of seconds.

1.  **Real-time Hand Tracking (MediaPipe)**
    * The application uses the computer's webcam to capture live video.
    * Google's **MediaPipe** library is employed to detect and track the user's hand landmarks (21 key points) with high accuracy and performance. This process is optimized to provide a smooth visual representation of the hand skeleton on the screen.

2.  **Sign Language Recognition (Deep Learning)**
    * The stream of hand landmark data is continuously fed into a trained **TensorFlow/Keras deep learning model**.
    * This model is specifically trained to classify the static and dynamic gestures of SIBI alphabet signs.
    * To prevent lag, the heavy prediction model is run intermittently, while the faster landmark detection runs on every frame, ensuring the UI remains responsive.

3.  **Sentence Construction**
    * The application includes a stability algorithm. A recognized sign must be held for a few consecutive frames before it is officially registered as a letter.
    * Users can string letters together to form words. The **"Save Word"** button confirms the current word and adds it to the sentence. The **"Retake"** button clears the current letters, allowing for easy correction.

4.  **Natural Language Processing (NLP)**
    * Once the user finishes signing and stops the recording, the complete text sentence is sent to a custom-built **NLP Engine**.
    * This engine identifies the user's **intent** (e.g., `find_location`, `greeting`) and extracts key **entities** (e.g., `toilet`, `food court`) from the sentence.

5.  **Response Generation**
    * Using the identified intent and entity, the system queries a structured **JSON knowledge base**.
    * This knowledge base contains detailed information about all locations in the mall, including specific directions from predefined starting points (e.g., "East Entrance Kiosk").
    * The final answer is then displayed on a clean, user-friendly response screen.

## Installation Guide

Follow thes steps to install the application on your computer.

1. **Clone the Repository** 
    * Clone the repository to your local machine using the following command: `git clone https://github.com/emergensee/WADBS-Emergensee.git`
    * Navigate to the project directory: `cd WADBS-Emergensee`

2. **Install the Dependencies**
    * Install the required Python packages using the following command: `pip install -r requirements.txt`
    * This will install the necessary libraries and dependencies required to run the application.

3. **Run the Application**
    * Open the `main.py` file in your preferred code editor.
    * Run the application by executing the `main.py` file.
    * use `python -m main` to run the application directly from the command line.
    * The application will start and display the welcome screen.

## How to Use

Follow these simple steps to interact with the EmergenSee AI Assistant.

1.  **Start Recording**
    * Press the large red circle button on the main screen to activate the camera. The button will change to indicate that it is recording.

2.  **Sign Your Question**
    * Position yourself so your hand is clearly visible in the video frame.
    * Sign the letters of your question one by one. For example, to ask "di mana toilet?", you would sign `D-I-M-A-N-A`, then `T-O-I-L-E-T`.

3.  **Build Your Sentence**
    * **Forming a Word**: As you sign, the recognized letters will appear at the top of the video feed.
    * **Saving a Word**: After you finish spelling a word (e.g., "DIMANA"), press the **"Save Word"** button. This adds the word to your final sentence at the bottom of the screen and clears the letter buffer for the next word.
    * **Correcting a Word**: If you make a mistake, press the **"Retake"** button to clear the current letters and start the word over.

4.  **Get Your Answer**
    * Once you have finished signing your complete question, press the recording button again to stop.
    * The application will process your question and automatically navigate to the response page, where your question and the assistant's answer will be clearly displayed.
    * To ask another question, simply press the **"Ask Another Question"** button to return to the recording screen.