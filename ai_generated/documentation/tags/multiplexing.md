# Multiplexing Pattern Functions

Functions that implement RP's "no useless args" multiplexing pattern, where base functions dispatch to _via_ variants with backend-specific parameters.

## Via Variants

### text_to_speech_via_apple
- **Base function**: text_to_speech
- **Backend**: Apple macOS 'say' command
- **Specific parameters**: voice selection from Apple's 47 voices, rate_in_words_per_minute
- **Platform restriction**: macOS only
- **Location**: Line 6650 in r.py

## Supporting Utilities

### fog
- **Purpose**: Creates deferred function calls for threading and delayed execution
- **Used by**: text_to_speech_via_apple (for threading), many other RP functions
- **Pattern**: Encapsulates function + arguments into parameterless callable
- **Location**: Line 276 in r.py