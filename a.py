from gtts import gTTS
import os
from playsound import playsound

playsound('welcome.mp3')
os.system("mpg321 welcome.mp3") 
        
cv2.waitKey(0)
os.remove("welcome.mp3")
