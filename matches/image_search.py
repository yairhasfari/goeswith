from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('AIzaSyC06aIvaVsRDOIMu0mvp5djCxGHmWaKJM0', '011315890042780505025:22h6vrpxwns')

search_params = {
    'q': 'mango png',
    'num': 2,
    'safe': 'high',
    'fileType': 'png',
    'imgType': 'clipart',
    'imgSize': 'icon',
    'searchType': 'image',
    }
for image in gis.result():
    image.download('.')
    image.resize(500, 500)