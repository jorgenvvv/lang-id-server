import os
import json
import ffmpeg

from flask import Blueprint, jsonify, request, g
from flask import current_app as app
from werkzeug.utils import secure_filename

from .constants import Constants
from .language_identifier import LanguageIdentifier

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/identify-language', methods=['POST'])
def identify_language():
    file = get_request_file(request)
    filename = secure_filename(file.filename)

    errors = validate_file(filename)
    if (len(errors)):
        return jsonify(errors), 400

    file_save_path = os.path.join(app.config['UPLOAD_DIRECTORY'], filename)
    file.save(file_save_path)

    processed_file_path = preprocess_audio(file_save_path)

    with app.app_context():
        predictions = app.language_identifier.identify_language(
            processed_file_path)
    language_info = get_language_info()

    for prediction in predictions:
        prediction['language'] = language_info['ALL_LANGUAGES'][prediction['language']]

    os.remove(file_save_path)
    
    return jsonify(predictions)

@api.route('/languages')
def available_languages():
    with app.app_context():
        languages = app.language_identifier.model.chunk_dataset_factory.label2id

    available_language_codes = list(languages.keys())
    language_info = get_language_info()

    available_languages = []
    for code in available_language_codes:
        available_languages.append(language_info['ALL_LANGUAGES'][code])

    return jsonify(available_languages)

def create_error(error_code, message) -> dict:
    return {
        'code': error_code,
        'message': message,
    }

def get_request_file(request):
    if 'file' not in request.files:
        return jsonify(create_error(Constants.FILE_NOT_FOUND_ERROR, Constants.FILE_NOT_FOUND_ERROR_TEXT)), 400

    file = request.files['file']

    if not file:
        return jsonify(create_error(Constants.FILE_NOT_FOUND_ERROR, Constants.FILE_NOT_FOUND_ERROR_TEXT)), 400

    return file

def preprocess_audio(input_file_path: str) -> str:
    input_file = os.path.basename(input_file_path)
    output_file_name = os.path.splitext(input_file)[0] + '.converted.wav'

    output_file_path = os.path.join(
        os.path.dirname(input_file_path), output_file_name)

    # Convert to 1 channel, 16k bitrate wav file
    out, err = (
        ffmpeg
        .input(input_file_path)
        .output(output_file_path, format='wav', ac=1, ar='16k')
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )

    return output_file_path


def validate_file_type(file_name: str) -> bool:
    file_extension = os.path.splitext(file_name)[1].replace('.', '')

    if file_extension not in app.config['ALLOWED_FILE_EXTENSIONS']:
        return False

    return True


def validate_file(file_path: str) -> list:
    errors = []

    file_name = os.path.basename(file_path)

    if not validate_file_type(file_name):
        errors.append(create_error(
            Constants.INVALID_FILE_TYPE_ERROR, Constants.INVALID_FILE_TYPE_ERROR_TEXT))

    return errors

def get_language_info(lang_code: str = None) -> dict:
    with app.open_resource('languages.json') as fin:
        data = json.load(fin)

    if lang_code is None:
        return data        
    else:
        return NotImplementedError
