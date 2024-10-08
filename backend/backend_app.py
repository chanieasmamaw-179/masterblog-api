from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

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


# Search a post by title or content using a GET request
@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    query = request.args.get('q')  # Get the search query from the URL
    if not query:
        return jsonify({'message': 'Bad Request: Missing search query'}), 400

    # Search for posts by title or content
    results = [post for post in POSTS if
               query.lower() in post['title'].lower() or query.lower() in post['content'].lower()]

    if results:
        return jsonify(results), 200
    else:
        return jsonify({'message': 'No matching posts found'}), 404


# Sort posts by title or content
@app.route('/api/posts/sort', methods=['GET'])
def sort_posts():
    sort_by = request.args.get('sort_by', 'title')  # Get the sorting field, default to 'title'
    direction = request.args.get('direction', 'asc')  # Get the sorting direction, default to ascending

    if sort_by not in ['title', 'content']:
        return jsonify({'message': 'Invalid sorting field. Must be either "title" or "content".'}), 400

    sorted_posts = sorted(POSTS, key=lambda post: post[sort_by].lower(), reverse=(direction == 'desc'))

    return jsonify(sorted_posts), 200

"""
usage: http://192.168.179.163:5002/static/masterblog.json
"""
SWAGGER_URL="/api/docs"  # Swagger endpoint
API_URL="/static/masterblog.json"  # Path to the API definition


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'backend_app.py': 'Masterblog API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

