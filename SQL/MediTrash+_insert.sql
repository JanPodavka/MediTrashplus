
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

--Zdravotnicke zarizeni
INSERT INTO Zdravotnicke_zarizeni VALUES ('Ortopedie Kamenick� �enov','42546887','heslo123','Kamenick� �enov','739788455','ortopedieSenov@gmail.com')
INSERT INTO Zdravotnicke_zarizeni VALUES ('Neurologie Liberec','12689647','neurologie','Liberec','608269451','neurolib@nemoclib.cz')
INSERT INTO Zdravotnicke_zarizeni VALUES ('U�n� Kamenick� �enov','42546811','heslo123','Kamenick� �enov','729788454','usniSenov@gmail.com')
INSERT INTO Zdravotnicke_zarizeni VALUES ('Urologie Liberec','12619647','heslo15','Liberec','718269451','urolib@nemoclib.cz')
INSERT INTO Zdravotnicke_zarizeni VALUES ('D�tsk� ordinace Praha','22546887','heslo123','�Praha','739788455','detskaPraha@tul.cz')
INSERT INTO Zdravotnicke_zarizeni VALUES ('JIP Jihlava','12689247','heslo','Jihlava','739269451','jipjih@nemocjih.cz')
INSERT INTO Zdravotnicke_zarizeni VALUES ('Zubn� ordinace D���n','42526884','heslo123','D���n','739488455','zubydecin@gmail.com')



--Opravnena osoba
INSERT INTO Opravnena_osoba VALUES ('12689648','Honza Odvozce')
INSERT INTO Opravnena_osoba VALUES ('12689644','Petr Novotn�')
INSERT INTO Opravnena_osoba VALUES ('12689647','Meditrash collectors')
INSERT INTO Opravnena_osoba VALUES ('12689492','Fast trash')
INSERT INTO Opravnena_osoba VALUES ('12689645','Sber odpadu Pavel')
INSERT INTO Opravnena_osoba VALUES ('12689646','Trashers')
INSERT INTO Opravnena_osoba VALUES ('12689161','Odpad sro')
INSERT INTO Opravnena_osoba VALUES ('12689122','Trashgiver')
INSERT INTO Opravnena_osoba VALUES ('12689649','Lenka Odpad')
INSERT INTO Opravnena_osoba VALUES ('12689610','MediOdpad')




select * from Opravnena_osoba
select * from Katalog_odpadu
select * from Zdravotnicke_zarizeni
select * from Odpad

