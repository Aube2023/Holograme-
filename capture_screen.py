import pyautogui
import time
import os

# Définir le chemin du fichier image sur le Bureau
desktop_path = os.path.expanduser("~/Desktop/screen_capture.png")

def capture_screen():
    while True:
        screenshot = pyautogui.screenshot()
        screenshot.save(desktop_path)  # Sauvegarde sur le Bureau
        print(f"Image capturée et enregistrée : {desktop_path}")
        time.sleep(0.1)  # Capture toutes les 100 ms

if __name__ == "__main__":
    capture_screen()
