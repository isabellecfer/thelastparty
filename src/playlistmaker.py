import httplib
import json
import os.path
import random
import urllib

from setmap import setmap

def makeplaylist(list):
    usuarios = json.loads(list)
    song_map = setmap()
    artist_map = setmap()

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
            con.request("GET", "/2.0?method=user.getTopTracks&format=json&api_key="+key+"&user="+usuario+"&period=overall&limit=500")
            res = json.loads(con.getresponse().read())
            if savelocally:
                if not os.path.exists("local"): os.makedirs("local")
                file = open("local/"+usuario+".json", "w")
                file.write(json.dumps(res))
                file.close()

        try:
            for track in res["toptracks"]["track"]:
                artist = track["artist"]["name"]
                artist_map.add(artist, usuario)
                song = (artist, track["name"])
                song_map.add(song, usuario)
        except: print "Usuario invalido"
    con.close()

    if len(song_map) == 0:
        print "Nenhuma musica encontrada"
        return "[]"

    print "Pontuando musicas"

    scorelist = []
    toplist = []
    
    maxa = artist_map.max_count()
    maxt = song_map.max_count()
    
    for song in song_map:
        pontuacao = 0.60*song_map.count(song)/maxt + 0.40*artist_map.count(song[0])/maxa
        scorelist.append((song, pontuacao))
        
    scorelist.sort(key=lambda tup: -tup[1])
    
    for s in scorelist:
        if s[1] >= 0.5:
            toplist.append(s[0])

    if len(toplist) > 40:
        toplist = random.sample(toplist, 40)
    random.shuffle(toplist)
    
    print "Recuperando IDs"
    
    key = "IQRMDIAMCEAQ0APXZ"
    con = httplib.HTTPConnection("developer.echonest.com")
    import urllib
    import urlparse
    import re
    
    ids = []
    for s in toplist:
        title = urllib.quote(s[1].encode('utf-8'))
        artist = urllib.quote(s[0].encode('utf-8'))
        query_string = urllib.urlencode({"search_query" : title+" "+artist})
        html_content = urllib.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode('utf-8'))
        

		# spotify code        
        con.request("GET", "/api/v4/song/search?api_key="+key+"&title="+title+"&artist="+artist+"&results=1&bucket=id:spotify&bucket=tracks")
        res = json.loads(con.getresponse().read())
		
        
        try:
            ids.append(search_results[0])
            #print(search_results[0])

        except: pass   
    print("Terminou adicionar musicas a lista")
    con.close()
    return json.dumps(ids)

#makeplaylist("[\"zetareticuliana\", \"joaotargino\"]")
#makeplaylist("[\"vctandrade\", \"salesallan\", \"zetareticuliana\",  \"celiorcbf\",\"cfilemon\", \"joaotargino\", \"joaoarthurbm\", \"nazaga\",\"zananeno\", \"lbalby\", \"andryw\", \"aidapontes\"]")que
