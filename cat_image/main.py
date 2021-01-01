from flask import Flask, request

# from flask_cors import CORS

from cat_image.validation_data import ValidationData
from cat_image.categorization.processing_images import ProcessingImages
from cat_image.categorization.categorization import Categorization

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
    if request.method == 'GET':
        return {'status': 'error', 'message': 'GET Method Not Allowed'}, 405

    if request.method == 'POST':
        reply_message = {}
        images_data = request.get_json()
        if not ValidationData.is_images_number_valid(images_data):
            reply_message['status'] = 'error'
            reply_message['message'] = 'Incorrect images quantity'
            return reply_message, 400

        try:
            processing_images = ProcessingImages(images_data)
            decoded_images = processing_images.decoding()  # decode images and return in a list
        except:
            reply_message['status'] = 'error'
            reply_message['message'] = 'Decoding failed'
            return reply_message, 500

        try:
            wrong_images_id = ValidationData.images_format_validation(decoded_images)
        except:
            reply_message['status'] = 'error'
            reply_message['message'] = 'images_format_validation failed'
            return reply_message, 500

        if len(wrong_images_id) > 0:
            reply_message['status'] = 'error'
            reply_message['message'] = 'Incorrect images format'
            reply_message['wrong_images_id'] = wrong_images_id
            return reply_message, 400
        else:
            try:
                categorization = Categorization()
                categorization.load_input_images()  # read images from dir and put in self.images list
                result = categorization.use_template()  # analyze self.images list and return results
            except:
                reply_message['status'] = 'error'
                reply_message['message'] = 'Categorization failed'
                return reply_message, 500

            reply_message['status'] = 'OK'
            reply_message['message'] = 'Categorization successfully processed'
            reply_message['result'] = result
            try:
                ProcessingImages.empty_folder()
            except:
                # send OK response with the categorization results, despite the empty_folder being unsuccessful
                reply_message['message'] = 'Categorization successfully processed, but empty_folder failed'
                return reply_message, 200
            return reply_message, 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
