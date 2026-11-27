# Google Text to Speech API
from gtts import gTTS

# Library to play an mp3 using python
from playsound3 import playsound

# The text that you want to convert to audio
text = "test"

# Language in which you want to convert
language = 'fr'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=text, lang=language, slow=False)

# Saving the converted audio in a mp3 file
myobj.save("tts_output/test.mp3")

# Playing the converted file
playsound('tts_output/test.mp3', True)