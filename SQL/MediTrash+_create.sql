-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-02-02 06:11:11.427

-- tables
-- Table: Katalog_odpadu
CREATE TABLE Katalog_odpadu (
    nazev nvarchar(200)  NOT NULL,
    id_odpad nvarchar(6)  NOT NULL,
    kategorie int  NOT NULL,
    CONSTRAINT Katalog_odpadu_pk PRIMARY KEY  (id_odpad)
);

-- Table: Odpad
CREATE TABLE Odpad (
    id int  NOT NULL,
    id_zdravotnicke_zarizeni nvarchar(200)  NOT NULL,
    id_odpad nvarchar(6)  NOT NULL,
    mnozstvi int  NOT NULL,
    datum_uskladneni nvarchar(12)  NOT NULL,
    datum_odvozu nvarchar(12)  NULL,
    id_opravnena_osoba nvarchar(200)  NULL,
    ispop int  NOT NULL,
    CONSTRAINT Odpad_pk PRIMARY KEY  (id,id_zdravotnicke_zarizeni)
);

-- Table: Opravnena_osoba
CREATE TABLE Opravnena_osoba (
    ico nvarchar(200)  NOT NULL,
    nazev nvarchar(20)  NOT NULL,
    CONSTRAINT Opravnena_osoba_pk PRIMARY KEY  (ico)
);

-- Table: Zdravotnicke_zarizeni
CREATE TABLE Zdravotnicke_zarizeni (
    nazev nvarchar(200)  NOT NULL,
    ico nvarchar(200)  NOT NULL,
    heslo nvarchar(200)  NOT NULL,
    mesto nvarchar(200)  NOT NULL,
    telefon nvarchar(200)  NOT NULL,
    email nvarchar(200)  NULL,
    CONSTRAINT ICO UNIQUE (ico),
    CONSTRAINT Zdravotnicke_zarizeni_pk PRIMARY KEY  (ico)
);

-- foreign keys
-- Reference: Odpad_Katalog_odpadu (table: Odpad)
ALTER TABLE Odpad ADD CONSTRAINT Odpad_Katalog_odpadu
    FOREIGN KEY (id_odpad)
    REFERENCES Katalog_odpadu (id_odpad)
	ON DELETE  NO ACTION
	ON UPDATE NO ACTION;


-- Reference: Odpad_Opravnena_osoba (table: Odpad)
ALTER TABLE Odpad ADD CONSTRAINT Odpad_Opravnena_osoba
    FOREIGN KEY (id_opravnena_osoba)
    REFERENCES Opravnena_osoba (ico)
	ON DELETE  NO ACTION
	ON UPDATE NO ACTION;

-- Reference: Odpad_Zdravotnicke_zarizeni (table: Odpad)
ALTER TABLE Odpad ADD CONSTRAINT Odpad_Zdravotnicke_zarizeni
    FOREIGN KEY (id_zdravotnicke_zarizeni)
    REFERENCES Zdravotnicke_zarizeni (ico)
	ON DELETE CASCADE
	ON UPDATE NO ACTION; --Nelze,již by byla jiná organizace

-- End of file.

