from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

# initialize flask app
app = Flask(__name__)

# simple in memory database to store user data
users = {}


# Define routes and methods for managing users
@app.route("/users", methods=["POST", "GET"])
@app.route("/users/<username>", methods=["GET", "PUT", "DELETE"])
def manage_users(username=None):
    # handle POST request to create a new user
    if request.method == "POST":
        # get Data sent with the POST request
        data = request.get_json()
        # hash the pw for security
        hashed_password = generate_password_hash(data["password"])
        # store the user in the dictionary with the hashed password
        users[data["username"]] = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "role": data["role"],
            "password": hashed_password,
        }
        # return a success message
        return jsonify({"message": "User added successfully"}), 201

    # handle get request to retrieve one or all users
    elif request.method == "GET":
        if username:
            # Retrieve a specific user by username
            user = users.get(username)
            if user:
                return jsonify(user), 200
            return jsonify({"message": "User not found"}), 404
        # return all users if no username is specified
        return jsonify(users), 200

    # handle PUT request to update an existing user
    elif request.method == "PUT":
        if username in users:
            # get the data for the update
            data = request.get_json()
            user = users[username]
            # update the user data based on provided JSON keeping existing data if
            # not specified
            user["first_name"] = data.get("first_name", user["first_name"])
            user["last_name"] = data.get("last_name", user["last_name"])
            user["role"] = data.get("role", user["role"])
            # update password if its included in the request
            if "password" in data:
                user["password"] = generate_password_hash(data["password"])
            return jsonify({"message": "User updated successfully"}), 200
        return jsonify({"message": "User not found"}), 404

    # handle DELETE request to remove a user
    elif request.method == "DELETE":
        if username in users:
            # Delete the user from the dictionary
            del users[username]
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"message": "User not found"}), 404


# Run the flask application if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
