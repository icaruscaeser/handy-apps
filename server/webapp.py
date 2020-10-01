#Author : Icarus Caeser
#File created on 11 Aug 2020 6:49 AM

from flask import Flask, render_template, request, send_file, after_this_request, make_response
import os
import download_images_bunch
import file_operations
import crypt_utils

UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')

app = Flask(__name__)

@app.route('/icarus')
def icarus():
    return "At your service master!!"

@app.route('/download-images')
def download_images():
    return render_template('download-images.html')

@app.route('/download-consecutive-images')
def download_consecutive_images_api():
    try:
        url = request.args['url']
        extension = request.args['extension']
        from_index = int(request.args['from'])
        to_index = int(request.args['to'])

    except Exception as exc:
        print(exc)
        return 'Expected the arguments are url, extension, from, to   -- <a href="download-consecutive-images?extension=jpg&&from=1&&to=2&&url=https://images.com/hello">click me for ease of use</a>'

    zip_file_dest = download_images_bunch.download_consecutive_images_as_zip(url, extension, from_index, to_index)
    zip_file_dest = os.path.abspath(zip_file_dest)

    @after_this_request
    def remove_the_file(response):
        file_operations.clean_dir_and_zip(zip_file_dest)
        return response


    print(zip_file_dest)

    # def stream_and_remove_file(file_path):
    #     print(file_path)
    #     file_handle = open(file_path, 'rb')
    #     yield from file_handle
    #     file_handle.close()
    #     file_operations.clean_dir_and_zip(file_path)
    #
    # return app.response_class(
    #     stream_and_remove_file(zip_file_dest),
    #     headers = {'Content-Disposition': 'attachment', 'filename': 'hello.zip'})
    return send_file(os.path.abspath(zip_file_dest), attachment_filename=zip_file_dest)

@app.route('/aes')
def aes():
    return render_template('aes.html')

@app.route('/aes/encrypt', methods=['post'])
def encrypt():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)
    encrypted_file_path = crypt_utils.encrypt_file(file_path)
    response = make_response(send_file(encrypted_file_path))
    response.headers['filename'] = os.path.basename(encrypted_file_path)

    @after_this_request
    def remove_files(response):
        os.remove(encrypted_file_path)
        os.remove(file_path)
        return response

    return response



@app.route('/aes/decrypt', methods=['post'])
def decrypt():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)
    decrypted_file_path = crypt_utils.decrypt_file(file_path)
    response = make_response(send_file(decrypted_file_path))
    response.headers['filename'] = os.path.basename(decrypted_file_path)

    @after_this_request
    def remove_files(response):
        os.remove(decrypted_file_path)
        os.remove(file_path)
        return response

    return response


@app.route('/')
def index():
    return render_template('index.html')


if '__main__' == __name__:

    if not os.path.exists(UPLOAD_DIR):
        os.mkdir(UPLOAD_DIR)

    port = int(os.environ.get('PORT', 11000))
    app.run(host='0.0.0.0', port=port, debug=True)