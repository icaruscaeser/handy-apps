#Author : Icarus Caeser
#File created on 11 Aug 2020 6:49 AM

from flask import Flask, render_template, request, send_file, after_this_request
import os
import download_images_bunch
import file_operations


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
        return 'Expected the arguments are url, extension, from, to   -- \n download-consecutive-images?extension=jpg&&url=https://images.com/hello&&from=1&&to=2'

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



@app.route('/')
def index():
    return render_template('index.html')


if '__main__' == __name__:
    port = int(os.environ.get('PORT', 11000))
    app.run(host='0.0.0.0', port=port, debug=True)