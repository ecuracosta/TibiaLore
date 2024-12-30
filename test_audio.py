from TTS.api import TTS
import os
import random
from pydub import AudioSegment

def convert_audio(text, output_path):
    # Load an end-to-end TTS model
    model_name = "tts_models/en/vctk/vits"  # Replace with your chosen model
    tts = TTS(model_name=model_name)
    
    # List available speakers
    speakers = tts.speakers
    print(f"Available speakers: {speakers}")
    
    # Generate and save audio
    tts.tts_to_file(text=text, file_path=output_path, speaker="p229")    # p229
    print(f"Audio saved to {output_path}")
    narration = AudioSegment.from_file(output_path)
    
    # Function to slow down audio by changing its frame rate
    def slow_down(audio, playback_speed):
        slowed = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * playback_speed)
        }).set_frame_rate(audio.frame_rate)
        return slowed
    
    # Slow down the narration
    narration = slow_down(narration, playback_speed=0.9)  # Adjust playback_speed as needed
    
    # Define the folder path
    folder_path = "./TibiaSoundtrack"  # Adjust the folder path if needed
    files_with_city = os.listdir(folder_path)
    random_file = random.choice(files_with_city)
    background_music = AudioSegment.from_file(folder_path+"/"+random_file)
    
    # Ensure the background music is at least as long as the narration
    if len(background_music) < len(narration) + 3000:  # Add 3 seconds for the narration delay
        # Loop the music if it's shorter than the narration
        loops_needed = (len(narration) + 3000) // len(background_music) + 1
        background_music = background_music * loops_needed
    
    # Trim the background music to match the narration length
    background_music = background_music[:len(narration) + 6000]
    
    # Lower the volume of the background music
    background_music = background_music - 25  # Adjust volume as needed
    
    # Add 3 seconds of silence at the start of the narration
    silence = AudioSegment.silent(duration=3000)
    narration_with_delay = silence + narration + silence
    
    # Overlay the narration onto the background music
    combined_audio = background_music.overlay(narration_with_delay)
    
    # Export the processed audio
    combined_audio.export(output_path, format="wav")
