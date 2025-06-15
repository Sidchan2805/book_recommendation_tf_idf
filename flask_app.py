from flask import Flask, request, jsonify
from recommender import recommend_books

app = Flask(__name__)

@app.route('/')
def home():
    return "📚 Welcome to the Book Recommender API!"

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    top_n = int(request.args.get('top_n', 5))
    
    if not title:
        return jsonify({"error": "Please provide a book title."}), 400
    
    result = recommend_books(title, top_n)
    
    if isinstance(result, str):
        return jsonify({"message": result}), 404
    else:
        return jsonify(result.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
