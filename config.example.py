class Config(object):
    DEBUG = False

    # Application root path
    APPLICATION_ROOT = '/api'

    # File restrictions
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 megabytes
    ALLOWED_FILE_EXTENSIONS = ['mp3', 'wav', 'opus']

    # Upload files directory
    UPLOAD_DIRECTORY = '/tmp/upload'
