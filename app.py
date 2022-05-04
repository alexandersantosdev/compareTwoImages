from PIL import Image
from PIL import ImageChops
import requests
from io import BytesIO
import math
from flask import Flask, request


def compare_images(urlImg1, urlImg2):

    response = requests.get(urlImg1)
    img1 = Image.open(BytesIO(response.content))

    response = requests.get(urlImg2)
    img2 = Image.open(BytesIO(response.content))

    h = ImageChops.difference(img2, img1).histogram()

    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(img1.size[0] * img1.size[1]))
    msg = ''
    if rms < 8:
        msg = 'Images are similar'
    else:
        msg = 'Images are different'
    return msg


app = Flask(__name__)


@app.post('/compare_images')
def compare():
    data = request.get_json()
    if data:
        try:
            url1 = data['url1']
            url2 = data['url2']
            return compare_images(url1, url2)
        except Exception as e:
            return 'Error: ' + str(e)
    return 'No urls data provided'


if __name__ == '__main__':
    app.run(debug=True)
