import pygame
import os
import time
import threading

class AudioController:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        # Create two channels: one for the AI voice, one for the background buffer
        self.voice_channel = pygame.mixer.Channel(0)
        self.buffer_channel = pygame.mixer.Channel(1)
        
        self.buffer_path = "static/audio/thinking.mp3"

    def play_buffer(self):
        """Plays the 'thinking...' sound on a loop."""
        if hasattr(self, 'socketio') and self.socketio:
            self.socketio.emit('play_buffer')
        if os.path.exists(self.buffer_path):
            # buffer_sound = pygame.mixer.Sound(self.buffer_path)
            # -1 means loop indefinitely
            # self.buffer_channel.play(buffer_sound, loops=-1)
            print("Buffer audio started...")

    def stop_buffer(self):
        """Stops the 'thinking...' sound."""
        if hasattr(self, 'socketio') and self.socketio:
            self.socketio.emit('stop_buffer')
        # self.buffer_channel.stop()

    def play_voice(self, file_path):
        """Plays the generated AI voice file and stops the buffer."""
        if hasattr(self, 'socketio') and self.socketio:
            filename = os.path.basename(file_path)
            self.socketio.emit('play_audio', {'url': f'/static/audio/{filename}'})
            
        if os.path.exists(file_path):
            # Stop the thinking sound right before the AI speaks
            self.stop_buffer()
            
            # voice_sound = pygame.mixer.Sound(file_path)
            # Play without blocking the server
            # self.voice_channel.play(voice_sound)
        else:
            print(f"Error: {file_path} not found.")

    def play_intro(self, language):
        """Plays the welcome message based on language."""
        path = f"static/audio/welcome_{language}.mp3"
        self.play_voice(path)

# Example of how this will be called in the main app:
# audio = AudioController()
# threading.Thread(target=audio.play_buffer).start()
# # ... (Mistral is generating text here) ...
# audio.play_voice("output.mp3")