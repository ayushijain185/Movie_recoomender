from flask import Flask, request, render_template
import pickle

# Load the movie list and cosine similarity matrix
with open('movie_list.pkl', 'rb') as f:
    df = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

app = Flask(__name__)

def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = df[df['title'].str.lower() == title.lower()].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices].tolist()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['title']
    recommendations = get_recommendations(title)
    return render_template('main.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
