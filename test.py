


import pyaudio # biblio audio permet de capturer le son en temps reel
import webrtcvad # voice activity detection => distingue la voix du silence/bruit (IA)
import wave #  sauvegarde l'audio au format wav




# les configuration 

FORMAT = pyaudio.paInt16 # format de donnée audio

CHANNELS = 1 # nbre de canaux (un seul canal)

RATE = 16000 # frequence d'echantillonage

CHUNK = 480 # taille de chaque paquet audio ( chunk = paquet audio)



# Initialise des objets audio


audio = pyaudio.PyAudio()

# confirguration du streaming


streaming = audio.open (format =FORMAT,
                        channels =CHANNELS,
                        rate = RATE,
                        input = True, # mode écoute (pas lecture)
                        frames_per_buffer = CHUNK) # taille des paquets






# Initialise la voice activity detection (analyseur de la parole)



vad = webrtcvad.Vad()
vad.set_mode(1) # mode  équilibré (ni trop sensible, ni trop strict)



#prend un "morceau" d'audio (frame)
#le fait analyser par l'algorithme VAD
# retourne True si c'est de la parole, False sinon

def is_speech(frame, sample_rate):
    return vad.is_speech(frame, sample_rate)


# fonction principale qui enregitre la parole

def record_audio():

    frames = []  # liste pour stocker l'audio 

    recording = False  # etat : enregistre ou pas

    silence_compteur  = 0 #   compteur de silence

    silence_threshold = 150      #  le temps de silence avant l' arrêt  du pgm

    print (" je parle, ecoutez svp....")
    
    try : 

        while True :  # Ecoute en continue, boucle infinie qui lit constamment le micro
            
            
            frame = streaming.read(CHUNK) # Lit 1024 échantillons, frame correspond  0.064 secondes d'audio ( (chunk = 1024)/(rate = 16000 ))

            if is_speech(frame, RATE): # test de parole

                if not recording:
                    print("Enregistrement commencé.")
                    recording = True
                frames.append(frame)  # stocke l'audio
                silence_compteur = 0   # remet le compteur à zéro

            
            else:  # Pas de parole = silence
                if recording:
                    frames.append(frame)      # Continue à enregistrer
                    silence_compteur += 1      # Compte les frames silencieux
            
                    if silence_compteur >= silence_threshold: # 150 × 0.064s ≈ silence de 10 secondes
                        print("Silence détecté, arrêt de l'enregistrement.")
                        
                        break                 # Arrête l'enregistrement
        
    except KeyboardInterrupt:
        print("\nArrêt manuel de l'enregistrement.")

    finally:
        streaming.stop_stream()
        streaming.close()
        audio.terminate()
    
    return frames



def save_audio(frames, filename="output.wav"):
    """Sauvegarde les frames audio dans un fichier WAV"""
    if not frames:
        print("Aucun audio à sauvegarder.")
        return
    
    fic_wav = wave.open(filename, 'wb')
    fic_wav .setnchannels(CHANNELS)
    fic_wav .setsampwidth(audio.get_sample_size(FORMAT))
    fic_wav .setframerate(RATE)
    fic_wav .writeframes(b''.join(frames))
    fic_wav.close()
    print(f"Audio sauvegardé comme {filename}")


def list_audio_devices():
    """Affiche la liste des périphériques audio disponibles"""
    p = pyaudio.PyAudio()
    print("\n=== Périphériques audio disponibles ===")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"ID {i}: {info['name']} "
              f"(Entrées: {info['maxInputChannels']}, "
              f"Sorties: {info['maxOutputChannels']}, "
              f"Fréquence max: {int(info['defaultSampleRate'])} Hz)")
    p.terminate()
    print("======================================\n")

    





