import io
from flask import Flask, request, redirect, render_template, send_file, make_response
import mosaic
import pdf_converter
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form.get('option')
        if option == 'option2':
            # Option 1 logic
            image = request.files['image']
            print(image)
            rows = int(request.form.get('rows'))
            if image and allowed_file(image.filename):
                mosaic_image = mosaic.ImageProcessor(image, rows)
                mosaic_bytes = mosaic_image.process()
                return send_file(
                    io.BytesIO(mosaic_bytes),
                    mimetype='image/jpeg',
                    as_attachment=True,
                    download_name='mosaic.jpeg'
                )
        elif option == 'option3':
            images = request.files.getlist("images")
            pd = pdf_converter.ImageToPDF(images=images, filename="output.pdf")
            pdf = pd.convert()
            response = make_response(pdf.output(dest='S').encode('latin1'))
            response.headers.set('Content-Disposition', 'attachment', filename='output.pdf')
            response.headers.set('Content-Type', 'application/pdf')
            return response
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    freezer.freeze()
