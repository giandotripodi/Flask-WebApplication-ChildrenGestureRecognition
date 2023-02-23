from flask import Flask, render_template, request, redirect, send_file, url_for
import subprocess

ALLOWED_EXTENSIONS = {'MOV', 'mp4', 'avi', 'mpeg', 'mpeg-2'}
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/video_feed", methods=['POST', 'GET'])
def video_feed():
    if request.method == 'POST':
        if 'select_file' not in request.files:
            return render_template('index.html')
        file = request.files['select_file']
        if file.filename == '':
            return render_template('index.html')
        if file and allowed_file(file.filename):
            # running children detection/hand model script with the selected file
            subprocess.run(['python', 'detection.py', file.filename])
            clustering_filename = file.filename[:-4] + '.csv'
            # running clustering model script
            subprocess.run(['python', 'clustering.py', clustering_filename])
            return render_template('done.html', videoname=request.files['select_file'].filename)
        return render_template('index.html')


@app.route("/videoplayer", methods=['POST', 'GET'])
def videoplayer():
    if request.method == 'POST':
        # getting video file name from the form in done.html
        videoname = request.form.get('videoname')
        module_path = "C:/Java/javafx-sdk-19/lib"
        add_modules = "javafx.base,javafx.controls,javafx.fxml,javafx.graphics,javafx.media"
        # running video player
        subprocess.call(
            ["java", "--module-path", module_path, "--add-modules", add_modules, "-jar", "PointingPlayer.jar",
             videoname])
        return render_template('done.html', videoname=videoname)
