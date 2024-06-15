import ast

import numpy as np
import pandas as pd
from fuzzywuzzy import process
import random

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


def _flatten(lst):
    return [x for xs in lst for x in xs]


class PredictionModel:
    def __init__(self, transformed_data, initial_data, playlists_data):
        self.transformed_data = transformed_data

        initial_data['full_title'] = initial_data['artist_name'] + ' - ' + initial_data['track_name']
        self.initial_data = initial_data
        self.playlists_data = playlists_data

        self.genres = initial_data['genre'].unique()

    def get_prediction(self, list_ID, genres, gen_size=60, recommend_size=20):

        def get_nearest_music_by_knn(data_indexes, likes, count_music):
            model = NearestNeighbors(n_neighbors=1000, algorithm='ball_tree')
            data = self.transformed_data.iloc[data_indexes]
            model.fit(data)

            list_track = self.transformed_data.iloc[likes]
            neighbors = model.kneighbors(list_track, return_distance=False, n_neighbors=count_music)

            indexes = list(set(_flatten(list(map(list, neighbors)))))
            chosen_indexes = random.choices(indexes, k=recommend_size)
            data.reset_index(inplace=True)
            true_index = pd.DataFrame(data.iloc[chosen_indexes])[['index']].values
            true_index = list([val[0] for val in true_index])

            res = pd.DataFrame(self.initial_data.iloc[true_index])[['full_title']].values.tolist()
            return [(chosen_indexes[idx], res[idx][0]) for idx in range(len(res))]

        if len(list_ID) < 7:

            data_by_genres = self.initial_data[self.initial_data['genre'].isin(genres)]
            data_by_genres.reset_index(inplace=True)

            if len(list_ID) < 1:
                list_ID = random.sample(data_by_genres['index'].to_list(), recommend_size)

            return get_nearest_music_by_knn(data_by_genres['index'].to_list(), list_ID, gen_size)

        else:
            playlists = pd.read_csv('playlists.csv')['playlists'].apply(ast.literal_eval).to_list()
            given_playlist = list(map(int, list(list_ID)))
            unique_songs = list(set(song for playlist in playlists for song in playlist).union(set(given_playlist)))

            playlist_vectors = np.array(
                [self._create_playlist_vector(playlist, unique_songs) for playlist in playlists])
            given_playlist_vector = self._create_playlist_vector(given_playlist, unique_songs).reshape(1, -1)
            similarities = cosine_similarity(given_playlist_vector, playlist_vectors)[0]
            similar_playlist_indices = np.argsort(similarities)[::-1]
            musics_set = set(el for index in similar_playlist_indices[:gen_size] for el in playlists[index]) - set(
                given_playlist)

            return get_nearest_music_by_knn(given_playlist + list(musics_set), list_ID[-7:], gen_size // 7)

    def search(self, query, threshold=80):
        matches = process.extract(query, self.initial_data['full_title'], limit=10)
        matched_values = [match for match in matches if match[1] > threshold]
        matched_values = [match[0] for match in sorted(matched_values, key=lambda x: x[1], reverse=True)]
        matched_indexes = self.initial_data[self.initial_data['full_title'].isin(matched_values)].index.values.tolist()
        res = pd.DataFrame(self.initial_data.iloc[matched_indexes])[['full_title']].values.tolist()
        return [(matched_indexes[idx], res[idx][0]) for idx in range(len(matched_indexes))]

    @staticmethod
    def _create_playlist_vector(playlist, unique_songs):
        vector = np.zeros(max(unique_songs) + 1)
        for song in playlist:
            vector[song] = 1
        return vector
