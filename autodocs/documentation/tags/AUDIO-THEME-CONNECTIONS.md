# AUDIO-THEME-CONNECTIONS.md

Comprehensive mapping of all audio/sound related functions and their interconnections in the RP module.

## Overview

RP provides a comprehensive audio ecosystem with 50+ audio-related functions spanning:
- Text-to-speech synthesis (TTS)
- Sound file loading/saving/playing
- Audio recording and microphone input
- Tone generation and musical synthesis
- MIDI input/output control
- Audio processing and analysis
- Video-audio integration
- Audio format conversion

## Core Audio Processing Pipeline

### 1. AUDIO FILE I/O SYSTEM

**File Loading Functions:**
- `load_sound_file(file_path, samplerate=None)` [r.py:7937] - Main audio file loader, returns numpy array [-1,1]
  - Multiplexes to: `load_wav_file()`, `load_mp3_file()`
  - Supports: WAV, MP3 formats
  - Handles samplerate conversion automatically

- `load_wav_file(path)` [r.py:7912] - WAV file specific loader using scipy
- `load_mp3_file(path)` [r.py:7888] - MP3 file loader using pydub/ffmpeg

**File Saving Functions:**
- `save_wav(samples, path, samplerate=None)` [r.py:8003] - Save numpy array as WAV file
- `convert_audio_file(input_file, output_file, *, skip_existing=False)` [r.py:8166] - Audio format conversion via FFmpeg
  - Supports: WAV, MP3, OGG, MP4
  - Auto-creates unique filenames

**File Detection:**
- `is_sound_file(file_path)` [r.py:20534] - Detects audio files by MIME type

### 2. SOUND PLAYBACK SYSTEM

**Main Playback Functions:**
- `play_sound_from_samples(samples, samplerate=None, blocking=False, loop=False, **kwargs)` [r.py:8011]
  - Core playback engine using sounddevice/IPython.Audio
  - Handles stereo via numpy matrix
  - Jupyter notebook compatible
  
- `play_sound_file(path)` [r.py:8036] - Cross-platform audio file player
  - Linux: Uses `load_sound_file()` + `play_sound_from_samples()`  
  - macOS: Uses `play_sound_file_via_afplay()`
  - Windows: Uses playsound library
  - Fallback: `play_sound_file_via_pygame()`

**Platform-Specific Playback:**
- `play_sound_file_via_afplay(absolute_file_path_and_name, volume=None, rate=None, rate_quality=None, parallel=True, debug=True)` [r.py:8058]
  - High-quality macOS playback via afplay command
  - Supports volume, rate, quality controls
  - Parallel execution by default

- `play_sound_file_via_pygame(file_name, return_simple_stopping_function=True)` [r.py:8080]
  - pygame.mixer fallback option

- `stop_sound()` [r.py:8097] - Universal sound stopping function

### 3. TEXT-TO-SPEECH SYNTHESIS SYSTEM

**Multiplexing Base Function:**
- `text_to_speech(text, voice=None, run_as_thread=True)` [r.py:7794]
  - Automatically chooses best TTS backend for platform
  - Supports both Apple and Google TTS voices
  - Thread-based execution by default

**Apple TTS Backend:**
- `text_to_speech_via_apple(text, voice="Samantha", run_as_thread=True, rate_in_words_per_minute=None, filter_characters=True)` [r.py:7393]
  - Uses macOS 'say' command via shell_command
  - 47 voices supporting 25+ languages
  - Rate control (90-720 WPM effective range)
  - Character filtering for shell safety
  - Threading via fog() function

**Google TTS Backend:**  
- `text_to_speech_via_google(text, voice='en', *, play_sound=True, run_as_thread=True)` [r.py:7566]
  - Google Translate TTS API
  - 50+ language/voice codes
  - Automatic text chunking for long content
  - Result caching via `_text_to_speech_via_google_sound_cache`
  - Internet connection required

**Voice Management:**
- `text_to_speech_voices_for_apple` [r.py:7391] - 47 Apple voice names
- `text_to_speech_voices_for_google` [r.py:7559] - 50+ Google language codes  
- `text_to_speech_voices_all` [r.py:7783] - Combined voice list
- `text_to_speech_voices_favorites` [r.py:7784] - Curated favorite voices
- `text_to_speech_voices_comparison(text="Hello world", time_per_voice=2, voices=None)` [r.py:7785] - Voice testing utility

### 4. AUDIO RECORDING SYSTEM

**Microphone Input:**
- `record_mono_audio(time_in_seconds, samplerate=default_samplerate, stream=None, chunk_size=default_audio_stream_chunk_size)` [r.py:13399]
  - Records mono audio from default microphone
  - Uses pyaudio with pyaudio.paInt16 format
  - Maintains persistent `default_audio_mono_input_stream` for low latency
  - Returns numpy array in [-1,1] range
  - ~10⁻⁵ second startup delay

**Stream Management:**
- `default_audio_mono_input_stream` [r.py:13398] - Persistent audio input stream
- `default_audio_stream_chunk_size=1024` [r.py:13397] - Buffer size for recording

### 5. TONE GENERATION & MUSICAL SYNTHESIS

**Tone Samplers:**
- `sine_tone_sampler(ƒ=None, T=None, samplerate=None)` [r.py:15641] - Pure sine waves
- `triangle_tone_sampler(ƒ=None, T=None, samplerate=None)` [r.py:15648] - Triangle waves  
- `sawtooth_tone_sampler(ƒ=None, T=None, samplerate=None)` [r.py:15651] - Sawtooth waves
- `square_tone_sampler(ƒ=None, T=None, samplerate=None)` [r.py:15658] - Square waves

**Musical Functions:**
- `play_tone(hz=None, seconds=None, samplerate=None, tone_sampler=None, blocking=False)` [r.py:15664]
  - Plays single tone using specified sampler
  - Default: 440Hz (A4) sine wave for 1 second

- `play_semitone(ↈ_semitones_from_A4_aka_440hz=0, seconds=None, samplerate=None, tone_sampler=None, blocking=False)` [r.py:15667]
  - Plays tone by semitone offset from A4
  - Uses `semitone_to_hz(ↈ)` for frequency conversion

- `play_chord(*semitones, t=1, block=True, sampler=triangle_tone_sampler)` [r.py:15672]
  - Plays multiple notes simultaneously
  - Sums individual tone samplers

- `semitone_to_hz(ↈ)` [r.py:15670] - Converts semitone offset to frequency

**Musical Constants:**
- `default_tone_frequency=440` [r.py:15661] - A4 reference
- `default_tone_sampler=sine_tone_sampler` [r.py:15662]
- `default_tone_seconds=1` [r.py:15663]

### 6. MIDI INPUT/OUTPUT SYSTEM

**MIDI Output Functions:**
- `MIDI_output(message: list)` [r.py:13421] - Raw MIDI message sender
  - Uses python-rtmidi library
  - Supports standard MIDI commands (NOTE_ON, NOTE_OFF, etc.)

**MIDI Control Functions:**
- `MIDI_control(controller_number, value)` [r.py:13473] - Single-byte controller
- `MIDI_control_precisely(coarse_controller_number, fine_controller_number, value)` [r.py:13475] - Two-byte precision
- `MIDI_jiggle_control(controller_number)` [r.py:13480] - Quick 0→1→0 control

**MIDI Note Functions:**
- `MIDI_note_on(note, velocity=1)` [r.py:13484] - Note on with velocity
- `MIDI_note_off(note, velocity=0)` [r.py:13486] - Note off
- `MIDI_pitch_bend(Δsemitones)` [r.py:13490] - Pitch bend control (-2 to +6 semitones)

**MIDI Constants:**
- `MIDI_pitch_bend_min=-2` [r.py:13488] - FL Studio compatible range
- `MIDI_pitch_bend_max=6` [r.py:13489]

### 7. AUDIO PROCESSING & ANALYSIS

**Signal Processing:**
- `audio_stretch(mono_audio, new_number_of_samples)` [r.py:16367] - Time-stretch audio using linear interpolation
- `adjust_samplerate(samples, original_samplerate, target_samplerate)` - Samplerate conversion (referenced in load_sound_file)

**Core Constants:**
- `default_samplerate=44100` [r.py:8010] - Standard audio samplerate for all functions

### 8. VIDEO-AUDIO INTEGRATION

**Video Functions:**
- `add_audio_to_video_file(video_path, audio_path, output_path=None)` [r.py:38077]
  - Adds audio track to video using FFmpeg
  - Preserves video quality by avoiding recompression

### 9. MUSIC ACQUISITION (GRAVEYARD)

**YouTube/Stream Ripping (Moved to Graveyard):**
- `rip_music(URL, output_filename=default_rip_music_output_filename, desired_output_extension='wav', quiet=False)` [graveyard.py:154]
  - Downloads audio from YouTube/SoundCloud/400+ sites
  - Uses youtube_dl + FFmpeg for format conversion
  - Supports WAV, MP3, OGG output formats

- `rip_info(URL)` [graveyard.py:188] - Extracts metadata from streaming URLs

## Audio Processing Workflows

### Workflow 1: Record → Process → Play
```python
# Record 5 seconds of audio
samples = record_mono_audio(5)

# Process (e.g., stretch to double length)
stretched = audio_stretch(samples, len(samples) * 2)

# Play back processed audio
play_sound_from_samples(stretched)
```

### Workflow 2: TTS → Save → Convert
```python
# Generate speech and get samples
text_to_speech_via_google("Hello world", play_sound=False)

# Save as WAV
save_wav(samples, "speech.wav")

# Convert to MP3
convert_audio_file("speech.wav", "speech.mp3")
```

### Workflow 3: Load → Analyze → Modify → Play
```python  
# Load audio file
samples, samplerate = load_sound_file("music.mp3", samplerate=True)

# Stretch audio (slow down)
modified = audio_stretch(samples, int(len(samples) * 1.5))

# Play modified version
play_sound_from_samples(modified, samplerate)
```

### Workflow 4: Musical Composition
```python
# Generate individual tones
tone1 = sine_tone_sampler(440, 2)    # A4 for 2 seconds  
tone2 = sine_tone_sampler(554.37, 2) # C#5 for 2 seconds

# Play as chord
play_chord(0, 4, t=2)  # A4 + C#5 chord
```

### Workflow 5: MIDI Control Integration
```python
# Send MIDI control data
MIDI_note_on(60, 0.8)     # Middle C at 80% velocity
sleep(1)
MIDI_pitch_bend(2)        # Bend up 2 semitones
sleep(1)
MIDI_note_off(60)         # Release note
```

## Cross-Domain Connections

### Audio ↔ Threading Integration
- All TTS functions support `run_as_thread=True` parameter
- Uses `run_as_new_thread()` and `fog()` for deferred execution
- `play_sound_file_via_afplay()` uses parallel execution by default

### Audio ↔ Platform Detection
- `text_to_speech()` automatically chooses Apple vs Google backend based on platform
- `play_sound_file()` uses platform-specific players (afplay/playsound/pygame)
- Cross-platform compatibility via multiplexing pattern

### Audio ↔ Shell Integration  
- Apple TTS uses `shell_command()` to invoke macOS 'say' command
- Character filtering prevents shell injection attacks
- FFmpeg integration for format conversion

### Audio ↔ File System
- Audio file detection via MIME type analysis
- Automatic file extension handling
- Path validation and unique filename generation

### Audio ↔ Jupyter Integration
- `play_sound_from_samples()` automatically detects Jupyter environment
- Uses `IPython.display.Audio` for notebook playback
- Image display functions also detect notebook context

## Performance Characteristics

### Memory Efficiency
- Audio samples stored as numpy arrays for efficient processing
- TTS results cached to avoid repeated API calls
- Persistent audio streams to reduce initialization overhead

### Latency Optimization
- Recording functions maintain open streams for ~10⁻⁵ second response
- Threading prevents blocking on audio playback
- Platform-native audio APIs for minimal overhead

### Error Handling
- Graceful fallbacks between audio backends
- Comprehensive format support validation
- Shell injection protection for TTS

## Dependencies by Function Category

### Core Audio I/O
- **scipy**: WAV file handling
- **pydub**: MP3 file processing  
- **sounddevice**: Cross-platform audio playback
- **pyaudio**: Microphone recording

### Text-to-Speech
- **gtts**: Google TTS API
- **gtts_token**: Google TTS authentication
- **shell commands**: Apple TTS (macOS 'say')

### MIDI
- **python-rtmidi**: MIDI input/output

### Format Conversion
- **FFmpeg**: Audio/video format conversion
- **subprocess**: External command execution

### Fallback Options
- **pygame**: Alternative audio playback
- **playsound**: Windows audio playback
- **IPython.display**: Jupyter notebook audio

## Function Relationships Map

```
TEXT-TO-SPEECH MULTIPLEXING:
text_to_speech() 
├── text_to_speech_via_apple() → shell_command("say") 
└── text_to_speech_via_google() → Google TTS API → play_sound_from_samples()

AUDIO PLAYBACK MULTIPLEXING:  
play_sound_file()
├── Linux: load_sound_file() → play_sound_from_samples()
├── macOS: play_sound_file_via_afplay() → shell_command("afplay")
├── Windows: playsound()
└── Fallback: play_sound_file_via_pygame()

AUDIO FILE I/O MULTIPLEXING:
load_sound_file() 
├── WAV: load_wav_file() → scipy.io.wavfile
└── MP3: load_mp3_file() → pydub → FFmpeg

TONE GENERATION CHAIN:
play_tone() → tone_sampler() → play_sound_from_samples() → sounddevice
play_semitone() → semitone_to_hz() → play_tone()
play_chord() → [multiple tone_sampler() calls] → sum → play_sound_from_samples()

AUDIO RECORDING CHAIN:
record_mono_audio() → pyaudio.stream.read() → numpy conversion → [-1,1] range

MIDI OUTPUT CHAIN:
MIDI_note_on/off() → MIDI_output() → python-rtmidi → Hardware MIDI
MIDI_control() → MIDI_output() → python-rtmidi  
MIDI_pitch_bend() → MIDI_output() → python-rtmidi
```

## Integration Points with Other RP Systems

### Image/Video System
- `add_audio_to_video_file()` integrates with video processing pipeline
- Jupyter notebook compatibility shared between audio and image display

### File System
- `is_sound_file()` integrates with file type detection system
- Path handling follows RP conventions for cross-platform compatibility

### Shell Integration
- TTS and audio playback use shell commands on appropriate platforms
- Consistent error handling with other shell-based RP functions

### Threading System  
- Audio functions extensively use RP's threading utilities
- Non-blocking execution patterns consistent across RP

### Progress Tracking
- Audio conversion functions could integrate with RP's progress bar system
- Long-running TTS operations benefit from threading

This audio ecosystem demonstrates RP's core design principles: multiplexing for cross-platform compatibility, comprehensive error handling, performance optimization, and seamless integration across functional domains.