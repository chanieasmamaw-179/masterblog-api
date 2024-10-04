from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This is the third post."}
]

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)

@app.route('/api/posts/<int:post_id>', methods=['GET'])  # Fixed the route here
def get_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post:
        return jsonify(post)
    else:
        return jsonify({'message': 'Post not found'}), 404  # Corrected the spelling

# Create a new post with error handling
@app.route('/api/posts', methods=['POST'])
def create_post():
    new_post = request.get_json()

    # Check if title and content are provided
    if not new_post or 'title' not in new_post or 'content' not in new_post:
        return jsonify({'message': 'Bad Request: Missing title or content'}), 400

    # Auto-increment ID
    new_post['id'] = POSTS[-1]['id'] + 1 if POSTS else 1
    POSTS.append(new_post)
    return jsonify(new_post), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
