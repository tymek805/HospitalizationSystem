import sqlite3
from enum import Enum

class UserType(Enum):
    HEAD_OF_DEPARTMENT = "HEAD_OF_DEPARTMENT"
    DEAN = "DEAN"
    ZJK_MEMBER = "Członek Zespołu Jakości Kształcenia"
    INSPECTION_TEAM_MEMBER = "INSPECTION_TEAM_MEMBER"
    INSPECTED = "Hospitowany"

class DatabaseManager:
    DATABASE_NAME = "pwr.db"
    logged_user = None

    def __init__(self):
        self.initialize_database()

    def initialize_database(self):
        connection = sqlite3.connect(self.DATABASE_NAME)
        cursor = connection.cursor()

        cursor.executescript('''
        -- Tabla: Ramowy harmonogram hospitacji
        CREATE TABLE IF NOT EXISTS Ramowy_harmonogram_hospitacji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zatwierdzony BOOLEAN
        );

        -- Tabla: Katedra
        CREATE TABLE IF NOT EXISTS Katedra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numer INTEGER NOT NULL,
            nazwa VARCHAR(255) NOT NULL
        );

        -- Tabla: Pracownik uczelni
        CREATE TABLE IF NOT EXISTS Pracownik_uczelni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            katedra_id INTEGER,
            termin_ostatniej_hospitacji DATE,
            czas_od_ostatniej_hospitacji INTEGER,
            stanowisko VARCHAR(255),
            imie VARCHAR(255),
            nazwisko VARCHAR(255),
            pesel VARCHAR(255),
            adres_email VARCHAR(255),
            telefon VARCHAR(255),
            plec VARCHAR(1),
            adres_zamieszkania VARCHAR(255),
            FOREIGN KEY (katedra_id) REFERENCES Katedra(id)
        );

        -- Tabla: Hospitacja
        CREATE TABLE IF NOT EXISTS Hospitacja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zespol_hospitujacy_id INTEGER,
            pracownik_uczelni_id INTEGER,
            ramowy_harmonogram_hospitacji_id INTEGER,
            termin_hospitacji DATE,
            FOREIGN KEY (zespol_hospitujacy_id) REFERENCES Zespol_hospitujacy(id),
            FOREIGN KEY (pracownik_uczelni_id) REFERENCES Pracownik_uczelni(id),
            FOREIGN KEY (ramowy_harmonogram_hospitacji_id) REFERENCES Ramowy_harmonogram_hospitacji(id)
        );

        -- Tabla: Zespol hospitujacy
        CREATE TABLE IF NOT EXISTS Zespol_hospitujacy (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );

        -- Tabla: Pracownik uczelni Zespol hospitujacy
        CREATE TABLE IF NOT EXISTS Pracownik_uczelni_Zespol_hospitujacy (
            pracownik_uczelni_id INTEGER,
            zespol_hospitujacy_id INTEGER,
            PRIMARY KEY (pracownik_uczelni_id, zespol_hospitujacy_id),
            FOREIGN KEY (pracownik_uczelni_id) REFERENCES Pracownik_uczelni(id),
            FOREIGN KEY (zespol_hospitujacy_id) REFERENCES Zespol_hospitujacy(id)
        );

        -- Tabla: Protokół hospitacji
        CREATE TABLE IF NOT EXISTS Protokol_hospitacji (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            HospitacjaID INTEGER,
            Zespol_hospitujacyID INTEGER,
            Ocena_koncowa FLOAT,
            Data_utworzenia DATE,
            Sciezka_do_pliku VARCHAR(255),
            Raport_z_hospitacjiID INTEGER,
            FOREIGN KEY (HospitacjaID) REFERENCES Hospitacja(ID),
            FOREIGN KEY (Zespol_hospitujacyID) REFERENCES Zespol_hospitujacy(ID),
            FOREIGN KEY (Raport_z_hospitacjiID) REFERENCES Raport_z_hospitacji(ID)
        );

        -- Tabla: Raport z hospitacji
        CREATE TABLE IF NOT EXISTS Raport_z_hospitacji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semestr_id INTEGER,
            sciezka_do_pliku VARCHAR(255),
            FOREIGN KEY (semestr_id) REFERENCES Semestr(id)
        );

        -- Tabla: Semestr
        CREATE TABLE IF NOT EXISTS Semestr (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Rok INTEGER NOT NULL,
            Ktora_polowa BOOLEAN,
            Nazwa_semestru VARCHAR(255)
        );

        -- Tabla: Zajęcia
        CREATE TABLE IF NOT EXISTS Zajecia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pracownik_uczelni_id INTEGER,
            dzien_tygodnia INTEGER,
            czas_rozpoczecia TIME,
            FOREIGN KEY (pracownik_uczelni_id) REFERENCES Pracownik_uczelni(id)
        );

        -- Tabla: Wykaz osób proponowanych do hospitacji
        CREATE TABLE IF NOT EXISTS Wykaz_osob_proponowanych_do_hospitacji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_utworzenia DATE
        );

        -- Tabla: Wykaz osób proponowanych do hospitacji Pracownik uczelni
        CREATE TABLE IF NOT EXISTS Wykaz_osob_proponowanych_Pracownik_uczelni (
            Wykaz_osob_proponowanych_do_hospitacjiID INTEGER,
            Pracownik_uczelniID INTEGER,
            PRIMARY KEY (Wykaz_osob_proponowanych_do_hospitacjiID, Pracownik_uczelniID),
            FOREIGN KEY (Wykaz_osob_proponowanych_do_hospitacjiID) REFERENCES Wykaz_osob_proponowanych_do_hospitacji(ID),
            FOREIGN KEY (Pracownik_uczelniID) REFERENCES Pracownik_uczelni(ID)
        );

        -- Tabela: Użytkownicy
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pracownik_uczelni_id INTEGER NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            FOREIGN KEY (pracownik_uczelni_id) REFERENCES Pracownik_uczelni(id)
        );
        ''')

        connection.commit()
        connection.close()
        self.populate_database()

    def populate_database(self):
        connection = sqlite3.connect(self.DATABASE_NAME)
        cursor = connection.cursor()

        # Katedra
        cursor.execute("INSERT OR IGNORE INTO Katedra (numer, nazwa) VALUES (?, ?)", (45, 'Katedra Informatyki Stosowanej'))

        cursor.execute("SELECT id FROM Katedra")
        katedra_id = cursor.fetchone()[0]

        # Pracownicy
        employees = [
            (katedra_id, "2024-01-15", 365, UserType.INSPECTED.name, "Jan", "Kowalski", "12345678901", "jan.kowalski@example.com",
             "27092606378", "M", "Żeromskiego 1"),
            (katedra_id, "2023-11-20", 400, UserType.INSPECTION_TEAM_MEMBER.name, "Anna", "Nowak", "98765432109", "anna.nowak@example.com",
             "55041509281", "K", "1 Maja 10"),
            (katedra_id, "2024-05-10", 150, UserType.ZJK_MEMBER.name, "Piotr", "Zieliński", "63041773698",
             "piotr.zielinski@example.com", "555666777", "M", "Czwartaków 3"),
            (katedra_id, "2024-02-05", 300, UserType.DEAN.name, "Maria", "Wiśniewska", "86100808117",
             "maria.wisniewska@example.com", "444555666", "K", "Morcinka 4"),
            (katedra_id, "2022-09-15", 700, UserType.HEAD_OF_DEPARTMENT.name, "Tomasz", "Lewandowski", "77788899900",
             "tomasz.lewandowski@example.com", "222333444", "M", "Kasprzaka Marcina 5"),
        ]

        cursor.executemany("""
                INSERT OR IGNORE INTO Pracownik_uczelni (katedra_id, termin_ostatniej_hospitacji, czas_od_ostatniej_hospitacji, 
                stanowisko, imie, nazwisko, pesel, adres_email, telefon, plec, adres_zamieszkania) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, employees)

        cursor.execute("SELECT ID FROM Pracownik_uczelni")
        employees_id = cursor.fetchall()

        users = [(employees_id[i][0], f"user{i + 1}", f"password{i + 1}") for i in range(len(UserType))]

        cursor.executemany("""
            INSERT OR IGNORE INTO Users (pracownik_uczelni_id, username, password) 
            VALUES (?, ?, ?)
        """, users)

        connection.commit()
        connection.close()

    def login(self, username, password):
        connection = sqlite3.connect(self.DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT pracownik_uczelni_id FROM Users WHERE username=? AND password=?", (username, password))
        self.logged_user = cursor.fetchone()

        connection.close()

        return self.get_user_role() if self.logged_user is not None else None

    def get_user_role(self):
        connection = sqlite3.connect(self.DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT stanowisko FROM Pracownik_uczelni WHERE id=?", self.logged_user)
        role = cursor.fetchone()[0]

        connection.close()

        return role

    def get_user_fullname(self):
        connection = sqlite3.connect(self.DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT imie, nazwisko FROM Pracownik_uczelni WHERE id=?", self.logged_user)
        fullname = cursor.fetchone()

        connection.close()

        return ' '.join(fullname)
