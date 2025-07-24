import speech_recognition as sr
from gtts import gTTS
import io
import os
import tempfile
from pydub import AudioSegment
from typing import Dict, Optional
import logging
from langdetect import detect

class VoiceService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        
        # Language codes for gTTS
        self.language_codes = {
            'english': 'en',
            'hindi': 'hi',
            'tamil': 'ta',
            'telugu': 'te',
            'bengali': 'bn'
        }
    
    def speech_to_text(self, audio_data: bytes, language: str = 'en-IN') -> Dict:
        """Convert speech to text"""
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Load audio file
            with sr.AudioFile(temp_audio_path) as source:
                audio = self.recognizer.record(source)
            
            # Recognize speech
            try:
                text = self.recognizer.recognize_google(audio, language=language)
                detected_lang = self.detect_language(text)
                
                result = {
                    'success': True,
                    'text': text,
                    'language': detected_lang,
                    'confidence': 0.95  # Google Speech API doesn't provide confidence
                }
                
            except sr.UnknownValueError:
                result = {
                    'success': False,
                    'error': 'Could not understand audio',
                    'text': '',
                    'language': 'unknown',
                    'confidence': 0.0
                }
            except sr.RequestError as e:
                result = {
                    'success': False,
                    'error': f'Speech recognition service error: {e}',
                    'text': '',
                    'language': 'unknown',
                    'confidence': 0.0
                }
            
            # Clean up temp file
            os.unlink(temp_audio_path)
            
            self.logger.info(f"Speech to text result: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in speech to text: {e}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'language': 'unknown',
                'confidence': 0.0
            }
    
    def text_to_speech(self, text: str, language: str = 'english') -> Dict:
        """Convert text to speech"""
        try:
            # Get language code
            lang_code = self.language_codes.get(language, 'en')
            
            # Create gTTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            result = {
                'success': True,
                'audio_data': audio_buffer.getvalue(),
                'language': language,
                'text': text,
                'format': 'mp3'
            }
            
            self.logger.info(f"Text to speech successful for language: {language}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in text to speech: {e}")
            return {
                'success': False,
                'error': str(e),
                'audio_data': None,
                'language': language,
                'text': text,
                'format': None
            }
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            detected = detect(text)
            language_map = {
                'hi': 'hindi',
                'ta': 'tamil',
                'te': 'telugu',
                'bn': 'bengali',
                'en': 'english'
            }
            return language_map.get(detected, 'english')
        except:
            return 'english'
    
    def process_audio_input(self, audio_data: bytes) -> Dict:
        """Process audio input and return text with language detection"""
        # Convert speech to text
        stt_result = self.speech_to_text(audio_data)
        
        if stt_result['success']:
            return {
                'success': True,
                'text': stt_result['text'],
                'language': stt_result['language'],
                'audio_processed': True
            }
        else:
            return {
                'success': False,
                'error': stt_result['error'],
                'text': '',
                'language': 'unknown',
                'audio_processed': False
            }
    
    def generate_audio_response(self, text: str, language: str = 'english') -> bytes:
        """Generate audio response from text"""
        tts_result = self.text_to_speech(text, language)
        
        if tts_result['success']:
            return tts_result['audio_data']
        else:
            # Return empty bytes if TTS fails
            return b''