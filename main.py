from test import *

# Code principal avec gestion d'erreurs
if __name__ == "__main__":
    try:
        # Optionnel: afficher les périphériques disponibles
        # list_audio_devices()
        
        # Enregistrement audio
        frames = record_audio()
        
        # Sauvegarde
        save_audio(frames)
        
    except Exception as e:
        print(f"Erreur: {e}")
        # Nettoyage en cas d'erreur
        if 'streaming' in locals():
            streaming.stop_stream()
            streaming.close()
        if 'audio' in locals():
            audio.terminate()