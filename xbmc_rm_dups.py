#!/usr/bin/python
import sqlite3
import sys

if not len(sys.argv) > 1:
	print "Requires sqlite db (~/.xbmc/userdata/Database/MyMusicX.db) as parameter"
else
	con = sqlite3.connect(sys.argv[1])
	con.isolation_level = None

	sql="""
	/*Deletes dupplicate songs in same pathid*/
	delete from song where idSong in(
        select idSong
        from song a
        inner join 
        (
                select idAlbum,idArtist, strTitle, idPath, min(idSong) as min_idSong
                from song 
                group by  idAlbum,idArtist, strTitle, idPath
                having count(*) >1
        ) b on 
		a.idAlbum = b.idAlbum and 
		a.idArtist = b.idArtist and 
		a.strTitle = b.strTitle and 
		a.idPath = b.idPath
        inner join path c on a.idPath = c.idPath
        where idSong <> min_idSong
	);"""
	print "Deleted ", con.execute(sql).rowcount, " buggy dups"
	sql = """
	/*Deletes dupplicate songs across folders*/
	delete from song where idSong in (
        select idSong
        from song a
        inner join 
        (
                select idAlbum, idArtist, strTitle,  min(idSong) as min_idSong
                from song 
                group by  idAlbum,idArtist, strTitle
                having count(*) >1
        ) b on a.idAlbum = b.idAlbum and a.idArtist = b.idArtist and a.strTitle = b.strTitle 
        inner join path c on a.idPath = c.idPath
        where idSong <> min_idSong
	);"""
	print "Deleted ", con.execute(sql).rowcount, " metadata entries from file dups"
