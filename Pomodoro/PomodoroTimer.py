import time
import threading
import os
import sys
from datetime import datetime
from typing import Optional

class PomodoroTimer:
    """
    Ein vollständiger Pomodoro-Timer mit allen klassischen Features.
    25 Min Arbeit -> 5 Min Pause -> Nach 4 Zyklen: 30 Min lange Pause
    """
    
    def __init__(self):
        # Zeiten in Sekunden (für Tests kannst du die Werte reduzieren)
        self.arbeitszeit = 25 * 60  # 25 Minuten
        self.kurze_pause = 5 * 60   # 5 Minuten  
        self.lange_pause = 30 * 60  # 30 Minuten
        
        # Status-Variablen
        self.aktuelle_session = 0
        self.completed_pomodoros = 0
        self.timer_laeuft = False
        self.pause_timer = False
        self.timer_thread = None
        
        # Für Statistiken
        self.session_start = None
        self.tagesstatistik = []
    
    def clear_screen(self):
        """Bildschirm leeren für bessere Übersicht"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def zeige_banner(self):
        """Zeigt einen schönen Banner"""
        print("🍅" * 50)
        print("           P O M O D O R O   T I M E R")
        print("🍅" * 50)
        print()
    
    def formatiere_zeit(self, sekunden: int) -> str:
        """Formatiert Sekunden zu MM:SS Format"""
        minuten = sekunden // 60
        sek = sekunden % 60
        return f"{minuten:02d}:{sek:02d}"
    
    def spiele_ton(self, typ: str = "normal"):
        """
        Spielt einen Benachrichtigungston (plattformabhängig)
        Typ: 'normal', 'pause', 'fertig'
        """
        try:
            if os.name == 'nt':  # Windows
                import winsound
                if typ == "pause":
                    winsound.Beep(800, 500)  # Höherer Ton für Pause
                elif typ == "fertig":
                    # Drei Töne für "Session komplett"
                    for _ in range(3):
                        winsound.Beep(1000, 300)
                        time.sleep(0.1)
                else:
                    winsound.Beep(600, 800)  # Normaler Ton
            else:  # Linux/Mac
                # Einfacher Systemton
                os.system('echo -e "\a"')
        except:
            # Fallback: Text-basierte "Töne"
            if typ == "pause":
                print("🔔 BEEP BEEP! Zeit für eine Pause!")
            elif typ == "fertig":
                print("🎉 DING DING DING! Session komplett!")
            else:
                print("⏰ DING! Zeit um!")
    
    def countdown(self, dauer: int, beschreibung: str, typ: str = "arbeit"):
        """
        Haupt-Countdown Funktion
        
        Args:
            dauer: Dauer in Sekunden
            beschreibung: Was gerade läuft (z.B. "Arbeitszeit")
            typ: "arbeit", "kurze_pause", "lange_pause"
        """
        self.timer_laeuft = True
        verbleibend = dauer
        
        # Icon basierend auf Typ
        if typ == "arbeit":
            icon = "💼"
        elif typ == "kurze_pause":
            icon = "☕"
        else:
            icon = "🏖️"
        
        while verbleibend > 0 and self.timer_laeuft:
            if not self.pause_timer:
                self.clear_screen()
                self.zeige_banner()
                
                print(f"{icon} {beschreibung}")
                print(f"Pomodoro #{self.aktuelle_session + 1}")
                print(f"Heute abgeschlossen: {self.completed_pomodoros}")
                print()
                
                # Große Zeitanzeige
                zeit_str = self.formatiere_zeit(verbleibend)
                print("┌" + "─" * 20 + "┐")
                print(f"│    {zeit_str}    │")
                print("└" + "─" * 20 + "┘")
                print()
                
                # Fortschrittsbalken
                fortschritt = (dauer - verbleibend) / dauer
                balken_laenge = 30
                gefuellt = int(fortschritt * balken_laenge)
                balken = "█" * gefuellt + "░" * (balken_laenge - gefuellt)
                prozent = int(fortschritt * 100)
                print(f"[{balken}] {prozent}%")
                print()
                
                # Steuerung
                print("Steuerung: [SPACE] Pause/Weiter | [S] Stopp | [R] Reset")
                print("           [Q] Beenden | [ENTER] für Menü")
                
                verbleibend -= 1
            
            time.sleep(1)
        
        if self.timer_laeuft:  # Nur wenn nicht manuell gestoppt
            # Session beenden
            if typ == "arbeit":
                self.completed_pomodoros += 1
                self.tagesstatistik.append({
                    'zeit': datetime.now().strftime("%H:%M"),
                    'typ': 'Pomodoro',
                    'dauer': self.arbeitszeit // 60
                })
                self.spiele_ton("normal")
            elif typ == "kurze_pause":
                self.spiele_ton("pause")
            else:
                self.spiele_ton("fertig")
    
    def tastatur_listener(self):
        """
        Lauscht auf Tastatureingaben während der Timer läuft
        Läuft in separatem Thread
        """
        while self.timer_laeuft:
            try:
                if os.name == 'nt':
                    import msvcrt
                    if msvcrt.kbhit():
                        taste = msvcrt.getch().decode('utf-8').lower()
                        self.handle_input(taste)
                else:
                    # Linux/Mac - einfachere Variante
                    pass
            except:
                pass
            time.sleep(0.1)
    
    def handle_input(self, taste: str):
        """Behandelt Tastatureingaben"""
        if taste == ' ':  # Leertaste für Pause/Weiter
            self.pause_timer = not self.pause_timer
            if self.pause_timer:
                print("\n⏸️  Timer pausiert - Drücke SPACE zum Fortsetzen")
            else:
                print("\n▶️  Timer läuft weiter...")
        elif taste == 's':  # S für Stopp
            self.timer_laeuft = False
            print("\n🛑 Timer gestoppt!")
        elif taste == 'r':  # R für Reset
            self.reset_session()
        elif taste == 'q':  # Q für Beenden
            self.timer_laeuft = False
            print("\n👋 Pomodoro Timer beendet!")
            sys.exit()
    
    def starte_arbeitszeit(self):
        """Startet eine 25-minütige Arbeitsphase"""
        if self.session_start is None:
            self.session_start = datetime.now()
        
        print(f"🍅 Starte Pomodoro #{self.aktuelle_session + 1}")
        print("Konzentriere dich auf EINE Aufgabe!")
        input("\nDrücke ENTER wenn du bereit bist...")
        
        # Keyboard listener in separatem Thread starten
        listener_thread = threading.Thread(target=self.tastatur_listener, daemon=True)
        listener_thread.start()
        
        self.countdown(self.arbeitszeit, "🍅 ARBEITSZEIT - Stay focused!", "arbeit")
        
        if self.timer_laeuft:
            self.aktuelle_session += 1
            
            # Entscheiden was als nächstes kommt
            if self.aktuelle_session % 4 == 0:
                self.starte_lange_pause()
            else:
                self.starte_kurze_pause()
    
    def starte_kurze_pause(self):
        """Startet eine 5-minütige Pause"""
        print("\n☕ Zeit für eine kurze Pause!")
        print("Steh auf, bewege dich, trink was!")
        input("Drücke ENTER um die Pause zu starten...")
        
        self.countdown(self.kurze_pause, "☕ KURZE PAUSE - Entspann dich!", "kurze_pause")
        
        if self.timer_laeuft:
            print("\n⚡ Pause vorbei! Bereit für den nächsten Pomodoro?")
            input("Drücke ENTER um weiterzumachen...")
            self.starte_arbeitszeit()
    
    def starte_lange_pause(self):
        """Startet eine 30-minütige lange Pause"""
        print("\n🏖️  Fantastisch! Du hast 4 Pomodoros geschafft!")
        print("Zeit für eine längere Pause - du hast sie dir verdient!")
        input("Drücke ENTER um die lange Pause zu starten...")
        
        self.countdown(self.lange_pause, "🏖️ LANGE PAUSE - Richtig entspannen!", "lange_pause")
        
        if self.timer_laeuft:
            print("\n🔥 Wow! Du bist wirklich produktiv heute!")
            print("Möchtest du eine neue Session starten?")
            antwort = input("(j/n): ").lower()
            
            if antwort == 'j':
                self.aktuelle_session = 0  # Reset für neue 4er-Runde
                self.starte_arbeitszeit()
            else:
                self.zeige_tagesstatistik()
    
    def reset_session(self):
        """Setzt die aktuelle Session zurück"""
        self.timer_laeuft = False
        self.aktuelle_session = 0
        self.pause_timer = False
        print("\n🔄 Session zurückgesetzt!")
    
    def zeige_tagesstatistik(self):
        """Zeigt die Statistiken des Tages"""
        self.clear_screen()
        print("📊 DEINE HEUTIGE BILANZ")
        print("=" * 40)
        
        if self.session_start:
            dauer = datetime.now() - self.session_start
            print(f"Session-Dauer: {str(dauer).split('.')[0]}")
        
        print(f"Abgeschlossene Pomodoros: {self.completed_pomodoros}")
        print(f"Gesamte Arbeitszeit: {self.completed_pomodoros * 25} Minuten")
        
        if self.completed_pomodoros > 0:
            print(f"Durchschnitt pro Stunde: {self.completed_pomodoros * 25 / max(1, (datetime.now() - self.session_start).seconds / 3600):.1f} Min")
        
        print("\n📈 Verlauf:")
        for eintrag in self.tagesstatistik:
            print(f"  {eintrag['zeit']} - {eintrag['typ']} ({eintrag['dauer']} Min)")
        
        if self.completed_pomodoros >= 8:
            print("\n🏆 CHAMPION! 8+ Pomodoros sind Weltklasse!")
        elif self.completed_pomodoros >= 4:
            print("\n🌟 SUPER! Sehr produktiver Tag!")
        elif self.completed_pomodoros >= 1:
            print("\n👍 GUT! Ein guter Anfang!")
        
        print("\n" + "=" * 40)
    
    def zeige_menu(self):
        """Hauptmenü des Pomodoro Timers"""
        while True:
            self.clear_screen()
            self.zeige_banner()
            
            print("Was möchtest du tun?")
            print()
            print("1. 🍅 Pomodoro starten")
            print("2. ⚙️  Einstellungen")
            print("3. 📊 Heute's Statistik")
            print("4. ❓ Hilfe")
            print("5. 👋 Beenden")
            print()
            
            auswahl = input("Deine Wahl (1-5): ").strip()
            
            if auswahl == '1':
                self.starte_arbeitszeit()
            elif auswahl == '2':
                self.einstellungen_menu()
            elif auswahl == '3':
                self.zeige_tagesstatistik()
                input("\nDrücke ENTER um zurück zum Menü zu gehen...")
            elif auswahl == '4':
                self.zeige_hilfe()
            elif auswahl == '5':
                self.zeige_tagesstatistik()
                print("\n👋 Bis bald! Bleib produktiv!")
                break
            else:
                print("🤔 Ungültige Auswahl. Bitte wähle 1-5.")
                time.sleep(1)
    
    def einstellungen_menu(self):
        """Einstellungen für den Timer"""
        while True:
            self.clear_screen()
            print("⚙️  EINSTELLUNGEN")
            print("=" * 30)
            print(f"1. Arbeitszeit: {self.arbeitszeit // 60} Minuten")
            print(f"2. Kurze Pause: {self.kurze_pause // 60} Minuten")
            print(f"3. Lange Pause: {self.lange_pause // 60} Minuten")
            print("4. Zurück zum Hauptmenü")
            print()
            
            auswahl = input("Was möchtest du ändern? (1-4): ").strip()
            
            if auswahl == '1':
                neue_zeit = self.eingabe_zeit("Arbeitszeit")
                if neue_zeit:
                    self.arbeitszeit = neue_zeit * 60
            elif auswahl == '2':
                neue_zeit = self.eingabe_zeit("Kurze Pause")
                if neue_zeit:
                    self.kurze_pause = neue_zeit * 60
            elif auswahl == '3':
                neue_zeit = self.eingabe_zeit("Lange Pause")
                if neue_zeit:
                    self.lange_pause = neue_zeit * 60
            elif auswahl == '4':
                break
    
    def eingabe_zeit(self, typ: str) -> Optional[int]:
        """Hilfsfunktion für Zeiteingabe"""
        try:
            zeit = int(input(f"Neue {typ} in Minuten (1-120): "))
            if 1 <= zeit <= 120:
                print(f"✅ {typ} auf {zeit} Minuten geändert!")
                time.sleep(1)
                return zeit
            else:
                print("❌ Bitte eine Zahl zwischen 1 und 120 eingeben.")
                time.sleep(1)
        except ValueError:
            print("❌ Bitte eine gültige Zahl eingeben.")
            time.sleep(1)
        return None
    
    def zeige_hilfe(self):
        """Zeigt Hilfe und Tipps"""
        self.clear_screen()
        print("❓ HILFE & TIPPS")
        print("=" * 40)
        print()
        print("🍅 WAS IST POMODORO?")
        print("25 Min fokussiert arbeiten → 5 Min Pause")
        print("Nach 4 Pomodoros → 30 Min lange Pause")
        print()
        print("💡 TIPPS FÜR MAXIMALE PRODUKTIVITÄT:")
        print("• Wähle VOR dem Start eine konkrete Aufgabe")
        print("• Schalte Handy stumm & schließe andere Apps")  
        print("• Bei Unterbrechungen: notiere sie kurz und mach weiter")
        print("• In Pausen: aufstehen, sich bewegen, nicht am Bildschirm bleiben")
        print("• Sei nicht zu hart zu dir - Übung macht den Meister!")
        print()
        print("⌨️  STEUERUNG WÄHREND DES TIMERS:")
        print("SPACE - Timer pausieren/fortsetzen")
        print("S - Timer stoppen")
        print("R - Session zurücksetzen")
        print("Q - Programm beenden")
        print()
        input("Drücke ENTER um zurück zum Menü zu gehen...")


# Hauptprogramm
if __name__ == "__main__":
    try:
        timer = PomodoroTimer()
        timer.zeige_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Pomodoro Timer beendet!")
    except Exception as e:
        print(f"\n❌ Ein Fehler ist aufgetreten: {e}")
        print("Bitte starte das Programm neu.")