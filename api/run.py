import os, sys

from api.controller.article_controller import app

if __name__ == "__main__":
    # configure folder for uploaded article files
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploaded')

    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER, 777)
    elif not os.path.isdir(UPLOAD_FOLDER):
        app.log_exception("UPLOAD_FOLDER is not a directory")
        exit(1)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print(app.config['UPLOAD_FOLDER'])

    app.run(host='0.0.0.0', port=5000, debug=True)
