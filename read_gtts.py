from gtts import gTTS

import os

mytext = "Thank you for reading my blog"

language = "en"

myobj = gTTS(text=mytext, lang=language, slow=False)

myobj.save("Thank you.mp3")

os.system("mpg321 Thank you.mp3")