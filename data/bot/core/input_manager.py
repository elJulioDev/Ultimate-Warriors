import json
import keyboard
from config import Config


class InputManager:
    __slots__ = ('keys', 'pause_key')
    
    def __init__(self):
        self.keys = {}
        self.pause_key = "enter"
        self._load_controls()

    def _load_controls(self):
        if not Config.CONTROLS_FILE.exists():
            print(f"No se encontro {Config.CONTROLS_FILE}")
            return

        try:
            with open(Config.CONTROLS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            controls = data.get("Controls", {}).get(Config.JUGADOR_CONTROLADO, {})
            others = data.get("Controls", {}).get("Others", {})
            
            self.keys = {
                "jump": controls.get("Movement", {}).get("Jump", "").lower(),
                "left": controls.get("Movement", {}).get("Left", "").lower(),
                "right": controls.get("Movement", {}).get("Right", "").lower(),
                "cover": controls.get("Movement", {}).get("Cover up", "").lower(),
                "punch": controls.get("Combat", {}).get("Punch", "").lower(),
                "kick": controls.get("Combat", {}).get("Kick", "").lower(),
                "charge": controls.get("Energy", {}).get("Charge", "").lower(),
                "shot": controls.get("Energy", {}).get("Ki shot", "").lower(),
                "tackle": controls.get("Energy", {}).get("Tackle", "").lower(),
                "emote": controls.get("Emote", "").lower()
            }
            
            self.pause_key = others.get("Pause", "enter").lower()
            
        except Exception as e:
            print(f"Error cargando controles: {e}")

    def get_pause_key(self):
        return self.pause_key

    def press(self, action):
        key = self.keys.get(action)
        if key:
            try:
                keyboard.press(key)
            except:
                pass

    def release(self, action):
        key = self.keys.get(action)
        if key:
            try:
                keyboard.release(key)
            except:
                pass

    def press_and_release(self, action):
        key = self.keys.get(action)
        if key:
            try:
                keyboard.press_and_release(key)
            except:
                pass
                
    def release_all_keys(self):
        for key in self.keys.values():
            if key:
                try:
                    keyboard.release(key)
                except:
                    pass