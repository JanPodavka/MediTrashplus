
--Katalog_odpad
INSERT INTO Katalog_odpadu VALUES ('Ostré pøedmìty','180101',0)
INSERT INTO Katalog_odpadu VALUES ('Èásti tìl,orgánù a krevních tekutin','180102',0)
INSERT INTO Katalog_odpadu VALUES ('Infekèní pøedmìty','180103',1)
INSERT INTO Katalog_odpadu VALUES ('Neinfekèní pøedmìty','180104',0)
INSERT INTO Katalog_odpadu VALUES ('Chemikálie','180106',1)
INSERT INTO Katalog_odpadu VALUES ('Bezpeèné chemikálie','180107',0)
INSERT INTO Katalog_odpadu VALUES ('Nepoužitá cytostatika','180108',1)
INSERT INTO Katalog_odpadu VALUES ('Jiná nepoužitelná léèiva','180109',1)
INSERT INTO Katalog_odpadu VALUES ('Odpadní amalgám','180110',1)
INSERT INTO Katalog_odpadu VALUES ('Ostré pøedmìty','180101',0)

--Zdravotnicke zarizeni
INSERT INTO Zdravotnicke_zarizeni VALUES ('Ortopedie Kamenický Šenov','42546887','heslo123','Kamenický Šenov','739788455','ortopedieSenov@gmail.com')
INSERT INTO Zdravotnicke_zarizeni VALUES ('Neurologie Liberec','12689647','neurologie','Liberec','608269451','neurolib@nemoclib.cz')

--Opravnena osoba
INSERT INTO Opravnena_osoba VALUES ('12689648','Honza Odvozce')

select * from Opravnena_osoba
select * from Katalog_odpadu
select * from Zdravotnicke_zarizeni