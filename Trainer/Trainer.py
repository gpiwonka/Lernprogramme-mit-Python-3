import sqlite3
import random
from typing import List, Tuple, Optional

class Trainer:
    """
    Universeller Trainer für Frage-Antwort basierte Lernspiele.
    Kann für Vokabeln, Grammatik, Mathe oder andere Themenbereiche verwendet werden.
    """
    
    def __init__(self, db_name: str, table_name: str):
        """
        Initialisiert den Trainer mit Datenbankname und Tabellenname.
        
        Args:
            db_name: Name der SQLite Datenbankdatei
            table_name: Name der Tabelle für dieses Themengebiet
        """
        self.db_name = db_name
        self.table_name = table_name
        self.verbindung = None
        self._datenbank_initialisieren()
    
    def _datenbank_initialisieren(self):
        """
        Erstellt die Datenbank und Tabelle falls sie nicht existieren.
        Private Methode (durch _ gekennzeichnet).
        """
        try:
            self.verbindung = sqlite3.connect(self.db_name)
            cursor = self.verbindung.cursor()
            
            # Tabelle erstellen falls nicht vorhanden
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frage TEXT NOT NULL,
                    antwort TEXT NOT NULL,
                    schwierigkeitsgrad INTEGER DEFAULT 1,
                    richtig_beantwortet INTEGER DEFAULT 0,
                    falsch_beantwortet INTEGER DEFAULT 0,
                    erstellt_am TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.verbindung.commit()
            print(f"Datenbank '{self.db_name}' und Tabelle '{self.table_name}' bereit.")
            
        except sqlite3.Error as e:
            print(f"Fehler beim Initialisieren der Datenbank: {e}")
    
    def speichern(self, frage: str, antwort: str, schwierigkeitsgrad: int = 1) -> bool:
        """
        Speichert eine neue Frage-Antwort Kombination in der Datenbank.
        
        Args:
            frage: Die Frage die gestellt werden soll
            antwort: Die korrekte Antwort
            schwierigkeitsgrad: Schwierigkeit von 1-5 (Standard: 1)
            
        Returns:
            bool: True wenn erfolgreich gespeichert, False bei Fehler
        """
        try:
            cursor = self.verbindung.cursor()
            cursor.execute(f'''
                INSERT INTO {self.table_name} (frage, antwort, schwierigkeitsgrad)
                VALUES (?, ?, ?)
            ''', (frage, antwort, schwierigkeitsgrad))
            self.verbindung.commit()
            print(f"Erfolgreich gespeichert: '{frage}' -> '{antwort}'")
            return True
            
        except sqlite3.Error as e:
            print(f"Fehler beim Speichern: {e}")
            return False
    
    def bearbeiten(self, id: int, neue_frage: str = None, neue_antwort: str = None, 
                   neuer_schwierigkeitsgrad: int = None) -> bool:
        """
        Bearbeitet eine existierende Frage-Antwort Kombination.
        
        Args:
            id: ID des zu bearbeitenden Eintrags
            neue_frage: Neue Frage (optional)
            neue_antwort: Neue Antwort (optional)
            neuer_schwierigkeitsgrad: Neuer Schwierigkeitsgrad (optional)
            
        Returns:
            bool: True wenn erfolgreich bearbeitet, False bei Fehler
        """
        try:
            cursor = self.verbindung.cursor()
            
            # Zuerst prüfen ob der Eintrag existiert
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,))
            if not cursor.fetchone():
                print(f"Eintrag mit ID {id} nicht gefunden.")
                return False
            
            # Update-Statement dynamisch erstellen
            update_felder = []
            werte = []
            
            if neue_frage is not None:
                update_felder.append("frage = ?")
                werte.append(neue_frage)
            if neue_antwort is not None:
                update_felder.append("antwort = ?")
                werte.append(neue_antwort)
            if neuer_schwierigkeitsgrad is not None:
                update_felder.append("schwierigkeitsgrad = ?")
                werte.append(neuer_schwierigkeitsgrad)
            
            if not update_felder:
                print("Keine Änderungen angegeben.")
                return False
            
            werte.append(id)  # ID für WHERE-Klausel
            
            query = f"UPDATE {self.table_name} SET {', '.join(update_felder)} WHERE id = ?"
            cursor.execute(query, werte)
            self.verbindung.commit()
            
            print(f"Eintrag mit ID {id} erfolgreich bearbeitet.")
            return True
            
        except sqlite3.Error as e:
            print(f"Fehler beim Bearbeiten: {e}")
            return False
    
    def lesen(self, schwierigkeitsgrad: Optional[int] = None, limit: Optional[int] = None) -> List[Tuple]:
        """
        Liest Frage-Antwort Paare aus der Datenbank.
        
        Args:
            schwierigkeitsgrad: Filtert nach bestimmtem Schwierigkeitsgrad (optional)
            limit: Begrenzt die Anzahl der Ergebnisse (optional)
            
        Returns:
            List[Tuple]: Liste von Tupeln (id, frage, antwort, schwierigkeitsgrad, ...)
        """
        try:
            cursor = self.verbindung.cursor()
            
            query = f"SELECT * FROM {self.table_name}"
            params = []
            
            if schwierigkeitsgrad is not None:
                query += " WHERE schwierigkeitsgrad = ?"
                params.append(schwierigkeitsgrad)
            
            if limit is not None:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            ergebnisse = cursor.fetchall()
            
            return ergebnisse
            
        except sqlite3.Error as e:
            print(f"Fehler beim Lesen: {e}")
            return []
    
    def loeschen(self, id: int) -> bool:
        """
        Löscht einen Eintrag aus der Datenbank.
        
        Args:
            id: ID des zu löschenden Eintrags
            
        Returns:
            bool: True wenn erfolgreich gelöscht, False bei Fehler
        """
        try:
            cursor = self.verbindung.cursor()
            cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
            
            if cursor.rowcount == 0:
                print(f"Eintrag mit ID {id} nicht gefunden.")
                return False
            
            self.verbindung.commit()
            print(f"Eintrag mit ID {id} erfolgreich gelöscht.")
            return True
            
        except sqlite3.Error as e:
            print(f"Fehler beim Löschen: {e}")
            return False
    
    def ueben(self, anzahl_fragen: int = 10, schwierigkeitsgrad: Optional[int] = None):
        """
        Startet eine Übungseinheit mit zufälligen Fragen.
        
        Args:
            anzahl_fragen: Anzahl der zu stellenden Fragen
            schwierigkeitsgrad: Filtert nach bestimmtem Schwierigkeitsgrad (optional)
        """
        fragen = self.lesen(schwierigkeitsgrad=schwierigkeitsgrad)
        
        if not fragen:
            print("Keine Fragen in der Datenbank gefunden!")
            return
        
        # Zufällige Auswahl der Fragen
        if len(fragen) < anzahl_fragen:
            print(f"Nur {len(fragen)} Fragen verfügbar. Alle werden verwendet.")
            ausgewaehlte_fragen = fragen
        else:
            ausgewaehlte_fragen = random.sample(fragen, anzahl_fragen)
        
        richtige_antworten = 0
        
        print(f"\n=== Übung gestartet mit {len(ausgewaehlte_fragen)} Fragen ===\n")
        
        for i, (id, frage, korrekte_antwort, schwierigkeit, richtig, falsch, erstellt) in enumerate(ausgewaehlte_fragen, 1):
            print(f"Frage {i}/{len(ausgewaehlte_fragen)}: {frage}")
            benutzer_antwort = input("Deine Antwort: ").strip()
            
            if benutzer_antwort.lower() == korrekte_antwort.lower():
                print("✓ Richtig!\n")
                richtige_antworten += 1
                self._statistik_aktualisieren(id, richtig=True)
            else:
                print(f"✗ Falsch! Die richtige Antwort war: {korrekte_antwort}\n")
                self._statistik_aktualisieren(id, richtig=False)
        
        # Endergebnis anzeigen
        prozent = (richtige_antworten / len(ausgewaehlte_fragen)) * 100
        print(f"=== Übung beendet ===")
        print(f"Richtige Antworten: {richtige_antworten}/{len(ausgewaehlte_fragen)} ({prozent:.1f}%)")
        
        if prozent >= 80:
            print("🎉 Ausgezeichnet!")
        elif prozent >= 60:
            print("👍 Gut gemacht!")
        else:
            print("💪 Weiter üben!")
    
    def _statistik_aktualisieren(self, id: int, richtig: bool):
        """
        Aktualisiert die Statistiken für eine Frage.
        Private Methode zur internen Verwendung.
        
        Args:
            id: ID der Frage
            richtig: True wenn richtig beantwortet, False wenn falsch
        """
        try:
            cursor = self.verbindung.cursor()
            if richtig:
                cursor.execute(f'''
                    UPDATE {self.table_name} 
                    SET richtig_beantwortet = richtig_beantwortet + 1 
                    WHERE id = ?
                ''', (id,))
            else:
                cursor.execute(f'''
                    UPDATE {self.table_name} 
                    SET falsch_beantwortet = falsch_beantwortet + 1 
                    WHERE id = ?
                ''', (id,))
            self.verbindung.commit()
            
        except sqlite3.Error as e:
            print(f"Fehler beim Aktualisieren der Statistik: {e}")
    
    def statistik_anzeigen(self):
        """
        Zeigt Statistiken über die gespeicherten Fragen an.
        """
        try:
            cursor = self.verbindung.cursor()
            cursor.execute(f'''
                SELECT 
                    COUNT(*) as gesamt,
                    AVG(schwierigkeitsgrad) as durchschnittliche_schwierigkeit,
                    SUM(richtig_beantwortet) as gesamt_richtig,
                    SUM(falsch_beantwortet) as gesamt_falsch
                FROM {self.table_name}
            ''')
            
            stats = cursor.fetchone()
            gesamt, avg_schwierigkeit, richtig, falsch = stats
            
            print(f"\n=== Statistiken für {self.table_name} ===")
            print(f"Gesamt Fragen: {gesamt}")
            print(f"Durchschnittliche Schwierigkeit: {avg_schwierigkeit:.1f}")
            print(f"Richtig beantwortet: {richtig}")
            print(f"Falsch beantwortet: {falsch}")
            
            if richtig + falsch > 0:
                erfolgsrate = (richtig / (richtig + falsch)) * 100
                print(f"Erfolgsrate: {erfolgsrate:.1f}%")
            
        except sqlite3.Error as e:
            print(f"Fehler beim Anzeigen der Statistiken: {e}")
    
    def schliessen(self):
        """
        Schließt die Datenbankverbindung.
        """
        if self.verbindung:
            self.verbindung.close()
            print("Datenbankverbindung geschlossen.")


# Beispiel für die Verwendung der Trainer-Klasse
if __name__ == "__main__":
    # Beispiel 1: Vokabeltrainer
    vokabel_trainer = Trainer("lerntrainer.db", "vokabeln")
    
    # Einige Vokabeln hinzufügen
    vokabel_trainer.speichern("Hello", "Hallo", 1)
    vokabel_trainer.speichern("Goodbye", "Auf Wiedersehen", 1)
    vokabel_trainer.speichern("Beautiful", "Schön", 2)
    
    # Beispiel 2: Mathe-Trainer
    mathe_trainer = Trainer("lerntrainer.db", "mathematik")
    
    # Einige Mathe-Aufgaben hinzufügen
    mathe_trainer.speichern("2 + 3 = ?", "5", 1)
    mathe_trainer.speichern("7 * 8 = ?", "56", 2)
    mathe_trainer.speichern("144 / 12 = ?", "12", 2)
    
    # Übung starten
    print("Möchtest du Vokabeln (v) oder Mathe (m) üben?")
    auswahl = input("Deine Wahl: ").lower()
    
    if auswahl == 'v':
        vokabel_trainer.ueben(5)
        vokabel_trainer.statistik_anzeigen()
    elif auswahl == 'm':
        mathe_trainer.ueben(3)
        mathe_trainer.statistik_anzeigen()
    
    # Verbindungen schließen
    vokabel_trainer.schliessen()
    mathe_trainer.schliessen()