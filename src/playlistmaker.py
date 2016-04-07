import httplib
import json
import os.path
import random
import urllib
import urlparse
import re

from setmap import setmap

def makeplaylist(list):
    usuarios = json.loads(list)
    artist_map = setmap()
    playcount_map = setmap()

    savelocally = False

    key = "e3bbd42a3ccda20f3c97de92cb6d6110"
    con = httplib.HTTPConnection("ws.audioscrobbler.com")
    
    for usuario in usuarios:
        print "Requisitando dados de "+usuario
        
        if savelocally and os.path.isfile("local/"+usuario+".json"):
            file = open("local/"+usuario+".json")
            res = json.loads(file.read())
            file.close()
        else:
            #con.request("GET", "/2.0?method=user.getTopTracks&format=json&api_key="+key+"&user="+usuario+"&period=overall&limit=400")
            con.request("GET", "/2.0?method=user.getTopArtists&format=json&api_key="+key+"&user="+usuario+"&period=overall&limit=200")
            res = json.loads(con.getresponse().read())
            #print(res)
            if savelocally:
                if not os.path.exists("local"): os.makedirs("local")
                file = open("local/"+usuario+".json", "w")
                file.write(json.dumps(res))
                file.close()

        try:
            for artist in res["topartists"]["artist"]:
                artist_map.add(artist["name"],usuario)
                playcount_map.add(artist["name"],int(artist["playcount"]))

        except: print "Usuario invalido"+usuario
    con.close()

    if len(artist_map) == 0:
        print "Nenhum artista encontrado"
        return "[]"

    print "Pontuando artistas"

    scorelist = []
    toplist = []
    
    maxa = artist_map.max_count()
    maxt = 1

    for plays in playcount_map:
        maxn = sum(playcount_map.get(plays))
        if maxn > maxt:
            maxt = maxn

    for artist in artist_map:
        pontuacao = 0.90*artist_map.count(artist)/(maxa) + 0.10*sum(playcount_map.get(artist))/maxt
        scorelist.append((artist, pontuacao))
    scorelist.sort(key=lambda tup: -tup[1])

    # Choose top 40 artists
    topart = []
    scorelist = scorelist[:40]
    for artist in scorelist:
        topart.append(artist[0])

    con = httplib.HTTPConnection("ws.audioscrobbler.com")
    songs = []
    print "Requisitando melhores musicas de:"
    for artist in topart:
        print "..."+artist

        if savelocally and os.path.isfile("local/"+artist+".json"):
            file = open("local/"+artist+".json")
            res = json.loads(file.read())
            file.close()
        else:
            artistF = urllib.urlencode({'artist':artist.encode("utf-8")})
            con.request("GET", "/2.0?method=artist.getTopTracks&format=json&api_key="+key+"&"+artistF+"&limit=20")
            res = json.loads(con.getresponse().read())

            if savelocally:
                if not os.path.exists("local"): os.makedirs("local")
                file = open("local/"+artist+".json", "w")
                file.write(json.dumps(res))
                file.close()

        try:
            for song in res["toptracks"]["track"]:
                songs.append((artist,song["name"]))

        except: print "Artista invalido: "+artist
    con.close()

    # Randomly choose 30
    toplist = random.sample(songs,100)
    toplist = random.sample(songs,30)

    #for song in toplist:
    #    print("Artista: "+song[0]+". Musica: "+song[1])
    #print toplist

    # Search top 30 on YouTube
    print "Procurando musicas no youtube!"
    ids = []
    for s in toplist:
        title = unicode(s[1].replace(" ","+")).encode("utf-8")
        artist = unicode(s[0].replace(" ","+")).encode("utf-8")
        #print("Searching for: "+title+"+"+artist)
        query_string = "search_query="+title+"+"+artist

        html_content = urllib.urlopen("http://www.youtube.com/results?" + query_string+"&max-results=1&category=music")
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode('utf-8'))

        try:
            ids.append(search_results[0])
            #print("Found: "+search_results[0])

        except: pass   
    print("Terminou adicionar musicas a lista")
    return json.dumps(ids)

#makeplaylist("[\"zetareticuliana\", \"joaotargino\"]")
#makeplaylist("[\"vctandrade\", \"salesallan\", \"zetareticuliana\",  \"celiorcbf\",\"cfilemon\", \"joaotargino\", \"joaoarthurbm\", \"nazaga\",\"zananeno\", \"lbalby\", \"andryw\", \"aidapontes\"]")que
