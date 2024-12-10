from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_free_id():
    free_id = 1
    used_ids = [post["id"] for post in POSTS]
    while free_id in used_ids:
        free_id += 1
    return free_id


def get_post_by_id(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    return_data, status_code = {}, 400 # Default values
    if "title" not in data:
        if "error" not in return_data:
            return_data["error"] = {}
        return_data["error"]["title"] = "Title is required"
    if "content" not in data:
        if "error" not in return_data:
            return_data["error"] = {}
        return_data["error"]["content"] = "Content is required"

    if not return_data:
        new_post = {
            "id": get_free_id(),
            "title": data["title"],
            "content": data["content"],
        }
        POSTS.append(new_post)
        return_data, status_code = new_post, 201
    return jsonify(return_data), status_code


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = get_post_by_id(post_id)
    if post:
        POSTS.remove(post)
        return jsonify({
            "message": f"Post with id {post_id} has been deleted successfully."
        }), 200
    return jsonify({"error": "Post not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
