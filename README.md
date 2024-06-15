# SMC_project
Repository for final project on Social Media Computing course

# Recommendation model
We use music from [this](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019) and [this](https://www.kaggle.com/datasets/adityak80/spotify-millions-playlist/download-directory/ZdREpgVPkaZKRnAoQJIa%2Fversions%2FSen9PNopSfICPMRO4yJI%2Fdirectories%2Fspotify?datasetVersionNumber=2) datasets.

For text preprocessing we use [google universal sentence encoder](https://www.kaggle.com/models/google/universal-sentence-encoder).
It is a model that encodes text into 512-dimensional vectors that can be used for different natural language tasks.

For recommendations we first ask the user to select their favorite genres, until the user has at least 1 like, random recommendations based on the selected genre are given. Then, until there are 8 likes we recommend similar songs using KNN.
Because of the large number of features, we use KNN, which is based on ball trees (for more details see. [docs](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbor-algorithms:~:text=using%20nearest%20neighbors.-,1.6.4.%20Nearest%20Neighbor%20Algorithms,-%23). 
When we have 8 tracks, we first look for a few similar playlists and take unique tracks from them.


In "app" folder you can find a simple web application, based on [flask framework](https://flask.palletsprojects.com/en/3.0.x/).
For local run you need to first initialize a user database by running `init.sh` script.
After that you can run application on localhost by command `flask run`.


Powered by [Дегтярев Виктор](https://github.com/DeVictoria), [Ситкина Алёна](https://github.com/a-ct-seal) и [Ерёмин Владимир](https://github.com/deytenit)
