import os
import json
import pandas as pd

music = pd.read_csv('tcc_ceds_music.csv')
music_dict = dict()
for index, row in music.iterrows():
    name = str(row['artist_name'] + ' ' + row['track_name']).lower()
    music_dict[name] = index


def json_to_csv(folder_path, output_csv):
    data_list = []
    cc = 0
    for filename in os.listdir(folder_path):
        cc += 1
        print(cc)
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as f:
                jsons = json.load(f)
                for tracks in jsons['playlists']:
                    musics = []
                    data = tracks['tracks']
                    if 10 < len(data) < 70:
                        for music in data:
                            try:
                                music_name = music['artist_name'] + ' ' + music['track_name']
                                musics.append(music_dict[music_name.lower()])
                            except KeyError:
                                pass
                        new_jsons = dict({'playlists': musics})
                        if len(musics) > 10 and (len(data) - len(musics)) < 30:
                            data_list.append(new_jsons)

    df = pd.DataFrame(data_list)
    df.to_csv(output_csv, index=False, encoding='utf-8')


folder_path = 'spotify/data'
output_csv = 'playlists.csv'
json_to_csv(folder_path, output_csv)
