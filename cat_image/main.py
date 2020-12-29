from flask import Flask, request

# from flask_cors import CORS

from cat_image.validation_data import ValidationData

app = Flask(__name__)  # create the Flask app
'''CORS(app, origins="http://localhost:8080", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)'''


# Route for handling the login page logic
@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    reply_message = {}
    if not ValidationData.is_username_valid(login_data):
        reply_message['status'] = 'error'
        reply_message['message'] = 'Incorrect username or email'
        return reply_message, 400
    elif not ValidationData.is_password_valid(login_data):
        reply_message['status'] = 'error'
        reply_message['message'] = 'Incorrect password'
        return reply_message, 400
    else:
        return {'status': 'OK'}, 200


# Route for handling the upload page logic
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return {'status': 'OK'}, 200
    else:
        return {'status': 'error', 'message': 'GET Method Not Allowed'}, 405


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
