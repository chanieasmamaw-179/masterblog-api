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


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post:
        return jsonify(post)
    else:
        return jsonify({'message': 'Post not found'}), 404


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


# Delete a post by ID
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS
    post = next((post for post in POSTS if post['id'] == post_id), None)

    if post:
        POSTS = [p for p in POSTS if p['id'] != post_id]  # Remove the post from the list
        return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Post not found'}), 404


# Update a post by ID
@app.route('/api/posts/<int:update_id>', methods=['PUT'])  # Use 'PUT' for updates
def update_post(update_id):
    global POSTS
    post = next((post for post in POSTS if post['id'] == update_id), None)

    if post:
        updated_data = request.get_json()  # Get the updated data from the request
        # Check if title and content are provided
        if not updated_data or 'title' not in updated_data or 'content' not in updated_data:
            return jsonify({'message': 'Bad Request: Missing title or content'}), 400

        # Update the post
        post['title'] = updated_data['title']
        post['content'] = updated_data['content']
        return jsonify({'message': f'Post with id {update_id} has been updated successfully.'}), 200
    else:
        return jsonify({'message': 'Post not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
