import serial
import numpy as np
import matplotlib.pyplot as plt
import time
import csv
from mpl_toolkits.mplot3d import Axes3D

# Configuration du port série (⚠️ Change si nécessaire)
PORT = "/dev/tty.usbmodem1101"  # Mets ici le bon port trouvé avec `ls /dev/tty.usb*`
BAUD_RATE = 115200

# Connexion au port série
ser = serial.Serial(PORT, BAUD_RATE)

# Création du fichier CSV
csv_filename = "mesures_ultrason.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"])

# Création des graphiques
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)

# Positions des capteurs (en cm)
capteurs_pos = np.array([
    [-20, 0, 0],   # Capteur Avant
    [20, 0, 0],    # Capteur Arrière
    [0, -20, 0],   # Capteur Gauche
    [0, 20, 0],    # Capteur Droite
])

# Stocker les points 3D mesurés
points_mesures = []
historique_mesures = []

def save_csv():
    """Sauvegarde les données historiques dans un fichier CSV"""
    with open("historique_mesures.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"])
        writer.writerows(historique_mesures)

def update_plot():
    ser.flushInput()
    while True:
        try:
            data = ser.readline().decode('utf-8').strip()
            distances = list(map(float, data.split(",")))
            if len(distances) == 4:
                with open(csv_filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(distances)
                
                historique_mesures.append(distances)
                if len(historique_mesures) > 100:
                    historique_mesures.pop(0)
                
                ax.clear()
                ax2.clear()
                ax.set_xlim(-30, 30)
                ax.set_ylim(-30, 30)
                ax.set_zlim(0, 100)
                ax.set_xlabel("X (cm)")
                ax.set_ylabel("Y (cm)")
                ax.set_zlabel("Distance (cm)")
                ax.set_title("Radar 3D - Reconstruction d'un Objet avec des Ondes Ultrasons")
                couleurs_capteurs = ['red', 'blue', 'green', 'orange']
                
                for i in range(4):
                    x, y, z = capteurs_pos[i]
                    z = distances[i]
                    x += np.random.uniform(-2, 2)
                    y += np.random.uniform(-2, 2)
                    points_mesures.append([x, y, z, couleurs_capteurs[i]])
                    ax.scatter(capteurs_pos[i, 0], capteurs_pos[i, 1], capteurs_pos[i, 2], 
                               c=couleurs_capteurs[i], marker='o', s=300, label=f"Capteur {i+1}")
                
                if len(points_mesures) > 500:
                    points_mesures.pop(0)
                
                for point in points_mesures:
                    ax.scatter(point[0], point[1], point[2], c=point[3], marker='.', s=20, alpha=0.8)
                
                historique_array = np.array(historique_mesures)
                if len(historique_array) > 0:
                    ax2.plot(historique_array[:, 0], label='Capteur 1', color='red')
                    ax2.plot(historique_array[:, 1], label='Capteur 2', color='blue')
                    ax2.plot(historique_array[:, 2], label='Capteur 3', color='green')
                    ax2.plot(historique_array[:, 3], label='Capteur 4', color='orange')
                    ax2.set_xlabel("Échantillons")
                    ax2.set_ylabel("Distance (cm)")
                    ax2.set_title("Historique en temps réel")
                    ax2.legend()
                
                plt.draw()
                plt.pause(0.1)
        except Exception as e:
            print(f"Erreur : {e}")
            break
    save_csv()

plt.ion()
update_plot()
