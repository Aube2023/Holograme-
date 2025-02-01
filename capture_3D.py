import pyautogui
import numpy as np
import cv2
import time

def capture_screen():
    """
    Capture l'écran en temps réel et convertit en niveaux de gris.
    """
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)  # Convertit en tableau numpy
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # Convertit en niveaux de gris
    return gray_frame

def apply_3D_effect(image):
    """
    Ajoute un effet de profondeur pour simuler un rendu 3D basique.
    """
    depth = cv2.applyColorMap(image, cv2.COLORMAP_JET)  # Ajoute un effet de relief
    return depth

def main():
    """
    Capture l'écran en temps réel et affiche l'effet 3D.
    """
    print("Démarrage dans 3 secondes...")
    time.sleep(3)  # Donne le temps de minimiser la fenêtre
    
    cv2.namedWindow("Projection 3D", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Projection 3D", 800, 600)

    try:
        while True:
            screen = capture_screen()
            depth_effect = apply_3D_effect(screen)

            # Affiche la fenêtre
            cv2.imshow("Projection 3D", depth_effect)

            # Sortie si 'q' est pressé
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Arrêt de la capture.")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
