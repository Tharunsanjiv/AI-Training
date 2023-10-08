import streamlit as st
import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

st.title("Speech Recognition and Text Extraction")

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

if uploaded_file:
    # Check if the file format is supported
    if uploaded_file.type == "audio/wav" or uploaded_file.type == "audio/mp3":
        # Convert the uploaded file to WAV format
        st.info("Converting the audio file to WAV format...")
        audio = AudioSegment.from_file(uploaded_file)
        temp_wav_path = "temp.wav"
        audio.export(temp_wav_path, format="wav")

        # Play the converted audio (optional)
        play(audio)

        # Perform speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_wav_path) as source:
            st.info("Processing audio...")
            audio_data = recognizer.record(source)  # Record the audio file

        # Recognize the audio using Google Web Speech API
        st.info("Transcribing audio to text...")
        try:
            text = recognizer.recognize_google(audio_data)
            st.success("Transcription completed successfully.")

            # Extract text after "medications"
            separator_sentence = "medications"
            extracted_text = ""

            sentences = text.split(separator_sentence)
            if len(sentences) > 1:
                extracted_text = separator_sentence + sentences[1]

            # Display the extracted text
            st.subheader("Prescription:")
            st.write(extracted_text.strip())

        except sr.UnknownValueError:
            st.error("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Web Speech API: {e}")
    else:
        st.error("Unsupported file format. Please upload an MP3 or WAV file.")
