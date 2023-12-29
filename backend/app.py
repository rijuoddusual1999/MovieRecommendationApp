import pandas as pd
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from flask import Flask, request, render_template, jsonify
import numpy as np 

app = Flask(__name__)
CORS(app)

cleaned = pd.read_csv("./imdb_top_1000.csv")
tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,3), min_df=3, analyzer='word')
cleaned['overview'] = cleaned['Gross'].fillna('')
tfidf_matrix = tfidf.fit_transform(cleaned['overview'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def similarity_function():
    return cleaned, cosine_sim

def allMovies():
    indices = pd.Series(cleaned.index, index=cleaned['Series_Title']).drop_duplicates()
    return indices

def get_recommendations(title, cosine_sim=cosine_sim, indices=None):
    if indices is None:
        indices = allMovies()

    if title not in indices:
        return "Sorry, the movie you typed is not present in the dataset."

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) 
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return cleaned['Series_Title'].iloc[movie_indices]

# print(get_recommendations('Psycho'))

@app.route('/api/movies', methods=['GET'])
@cross_origin()
def movies():
    # returns all the movies in the dataset
    movies = allMovies()
    result = {'arr': movies}
    return jsonify(result)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/similarity/<name>')
@cross_origin()
def similarity_route(name):
    movie = name
    recommendations = get_recommendations(movie)
    if type(recommendations) == type('string'):
        resultArray = recommendations.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)
    else:
        movieString = '---'.join(recommendations)
        resultArray = movieString.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)
    

@app.route('/api/similar_names/<partial_name>')
@cross_origin()
def similar_names(partial_name):
    partial_name = partial_name.lower()
    
    # Filter movie names that contain the given partial_name
    similar_names = [title for title in cleaned['Series_Title'] if partial_name in title.lower()]

    if not similar_names:
        return jsonify({'message': 'No similar names found.'})
    
    return jsonify({'similar_names': similar_names})


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
