from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_free_id():
    """Return the first free id in the POSTS list."""
    free_id = 1
    used_ids = [post["id"] for post in POSTS]
    while free_id in used_ids:
        free_id += 1
    return free_id


def get_post_by_id(post_id):
    """Return the post with the given id."""
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


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    if "title" in data:
        post["title"] = data["title"]
    if "content" in data:
        post["content"] = data["content"]
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    search_query = request.args
    title_query = search_query.get("title")
    content_query = search_query.get("content")
    if title_query or content_query:
        result = []
        for post in POSTS:
            # If both title and content are provided, we will search for posts that match both
            if title_query and content_query:
                if title_query.lower() in post["title"].lower() and content_query.lower() in post["content"].lower():
                    result.append(post)
            # If only title is provided, we will search for posts that match the title
            elif title_query:
                if title_query.lower() in post["title"].lower():
                    result.append(post)
            # If only content is provided, we will search for posts that match the content
            elif content_query:
                if content_query.lower() in post["content"].lower():
                    result.append(post)
        return jsonify(list(result)), 200
    return jsonify({"error": "'title' or 'content' query parameter is required"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
