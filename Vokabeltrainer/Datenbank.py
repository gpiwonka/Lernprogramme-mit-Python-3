import sqlite3

class VokabeltrainerDB:
    def __init__(self, db_name="vokabeltrainer.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Tabelle für Vokabeln erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vokabeln (
                Id INTEGER PRIMARY KEY,           
                begriff TEXT,
                bedeutung TEXT
            )
        ''')

        # Tabelle für Fortschritt erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fortschritt (
                Id INTEGER PRIMARY KEY,           
                begriff TEXT,
                richtig INTEGER DEFAULT 0,
                FOREIGN KEY (Id) REFERENCES vokabeln(Id)
            )
        ''')

        self.conn.commit()

    def vokabel_hinzufuegen(self, begriff, bedeutung):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vokabeln (begriff, bedeutung)
            VALUES (?, ?)
        ''', (begriff, bedeutung))

        cursor.execute('''
            INSERT OR IGNORE INTO fortschritt (begriff) VALUES (?)
        ''', (begriff,))

        self.conn.commit()

    def get_fortschritt(self, begriff):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT richtig FROM fortschritt WHERE begriff = ?
        ''', (begriff,))

        result = cursor.fetchone()
        return result[0] if result else 0

    def update_fortschritt(self, begriff, richtig):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE fortschritt SET richtig = ? WHERE begriff = ?
        ''', (richtig, begriff))

        self.conn.commit()

# Beispielanwendung mit Datenbank-Layer
if __name__ == "__main__":
    trainer_db = VokabeltrainerDB()

    # Vokabeln hinzufügen
    trainer_db.vokabel_hinzufuegen("Haus", "House")
    trainer_db.vokabel_hinzufuegen("Auto", "Car")
    trainer_db.vokabel_hinzufuegen("Apfel", "Apple")

    # Vokabeln üben
    for _ in range(3):  # Übe 3 Mal
        begriff = random.choice(list(trainer_db.vokabeln.keys()))
        richtig = input(f"Bedeutung von {begriff}: ").strip().lower() == trainer_db.vokabeln[begriff].lower()
        fortschritt = trainer_db.get_fortschritt(begriff)

        if richtig:
            fortschritt += 1
        else:
            fortschritt = 0

        trainer_db.update_fortschritt(begriff, fortschritt)

    # Fortschritt anzeigen
    for begriff in trainer_db.vokabeln:
        fortschritt = trainer_db.get_fortschritt(begriff)
        print(f"{begriff}: {fortschritt} Mal richtig")

    trainer_db.conn.close()
