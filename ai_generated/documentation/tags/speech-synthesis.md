# Text-to-Speech and Speech Synthesis Functions

Functions for converting text to spoken audio using various backends and voice systems.

## Backend-Specific Functions

### text_to_speech_via_apple
- **Purpose**: Apple macOS text-to-speech backend using system 'say' command
- **Platform**: macOS only
- **Features**: 47 voices, 25+ languages, threading support, rate control
- **Popular voices**: Samantha (US), Alex (US), Daniel (UK), Moira (Irish), Fiona (Scottish)
- **Usage patterns**: Part of RP's multiplexing TTS system
- **Location**: Line 6650 in r.py