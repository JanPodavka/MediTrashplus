
--Katalog_odpad
INSERT INTO Katalog_odpadu VALUES ('Ostr� p�edm�ty','180101',0)
INSERT INTO Katalog_odpadu VALUES ('��sti t�l,org�n� a krevn�ch tekutin','180102',0)
INSERT INTO Katalog_odpadu VALUES ('Infek�n� p�edm�ty','180103',1)
INSERT INTO Katalog_odpadu VALUES ('Neinfek�n� p�edm�ty','180104',0)
INSERT INTO Katalog_odpadu VALUES ('Chemik�lie','180106',1)
INSERT INTO Katalog_odpadu VALUES ('Bezpe�n� chemik�lie','180107',0)
INSERT INTO Katalog_odpadu VALUES ('Nepou�it� cytostatika','180108',1)
INSERT INTO Katalog_odpadu VALUES ('Jin� nepou�iteln� l��iva','180109',1)
INSERT INTO Katalog_odpadu VALUES ('Odpadn� amalg�m','180110',1)
INSERT INTO Katalog_odpadu VALUES ('Ostr� p�edm�ty','180101',0)

--Zdravotnicke zarizeni
INSERT INTO Zdravotnicke_zarizeni VALUES ('Ortopedie Kamenick� �enov','42546887','heslo123','Kamenick� �enov','739788455','ortopedieSenov@gmail.com')
INSERT INTO Zdravotnicke_zarizeni VALUES ('Neurologie Liberec','12689647','neurologie','Liberec','608269451','neurolib@nemoclib.cz')

--Opravnena osoba
INSERT INTO Opravnena_osoba VALUES ('12689648','Honza Odvozce')

select * from Opravnena_osoba
select * from Katalog_odpadu
select * from Zdravotnicke_zarizeni