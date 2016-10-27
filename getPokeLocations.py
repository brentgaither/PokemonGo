#!/usr/bin/env python
import json
import csv


def get_pokemon_names():
    pokemon = []
    f = open('pokemonlist.csv', 'rb')
    reader = csv.reader(f)
    for row in reader:
        pokemon.append(row[1])
    return pokemon


def read_tweets():
    pokemon_names = get_pokemon_names()
    server_down = 0
    total = 0
    with open('pokemon.json', 'r') as f:
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for line in f:
            tweet = json.loads(line)
            try:
                if tweet['coordinates']:
                    for pokemon in pokemon_names:
                        if pokemon in tweet['text'].upper():
                            print tweet['text']
                            geo_json_feature = {
                                "type": "Feature",
                                "geometry": tweet['coordinates'],
                                "properties": {
                                    "text": tweet['text'],
                                    "created_at": tweet['created_at'],
                                    "pokemon": pokemon_names.index(pokemon),
                                    "popupContent":tweet['text'] + "<br/> At: " + tweet['created_at']
                                }
                            }
                            geo_data['features'].append(geo_json_feature)
                elif 'SERVER' in tweet['text'].upper():
                    server_down += 1
                total += 1
            except KeyError:
                continue
            except UnicodeDecodeError:
                continue
    if (server_down/ total) > .5:
        print "The servers are probably down"
    return geo_data

if __name__ == "__main__":
    geo_data = read_tweets()
    print geo_data
    with open('geo_data.json', 'w') as fout:
        fout.write(json.dumps(geo_data, indent=4))
