from flask import Flask, request, jsonify
from flask_cors import CORS
# import app

import xmltodict

import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
import python_server

from pyaadhaar.utils import Qr_img_to_text, isSecureQr
from pyaadhaar.decode import AadhaarSecureQr

# import qr_scanner

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/get_image": {"origins": "http://localhost:3000"}}

# data = qr_scanner.main()

ext_data2 = {}
ext_data3 = {}


@app.route("/upload", methods=["POST"])
def upload_image():
    try:
        # Check if the POST request contains a file with the key 'image'
        if "image" not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image = request.files["image"]

        # Check if the file is an image (you may want to enhance this validation)
        if not image.filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
            return jsonify({"error": "Invalid image format"}), 400

        # Save the image to a folder (you should create this folder)
        image.save("uploads/" + image.filename)

        li = []
        # fp=python_server.upload_image.image
        fp = image.filename
        # image = Image.open(fp)
        # image.show()
        image = cv2.imread(fp)

        barcodes = decode(image)
        decoded = barcodes[0]
        # print(decoded)
        url: bytes = decoded.data
        url = url.decode()
        # print(url)

        rect = decoded.rect
        # print(rect)

        poly = decoded.polygon
        # print(centroid(poly))
        for barcode in barcodes:
            # print(barcode.rect)
            (x, y, w, h) = barcode.rect
            r = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)

            Cx = x + 0.5 * (w)
            Cy = y + 0.5 * (h)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(
                image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
            )

            li.append([barcodeData, (Cx, Cy)])
            # print("[INFO] Found [{},{}] barcode: {}".format(x, y, barcodeData))
            isSecureQR = isSecureQr(barcodeData[0])
            # if isSecureQR:
            obj = AadhaarSecureQr(int(barcodeData))
            # decoded_secure_qr_data = secure_qr.decodeddata()
            ext_data = obj.decodeddata()

            ext_data2.update(ext_data)

            print(ext_data)

            out_file = open("myfile.json", "w")

            json.dump(ext_data, out_file, indent=6)

            out_file.close()
            # else:
                # ext_data = barcodeData
                # ext_data2 = xmltodict.parse(barcodeData)
                # print(ext_data2)
                # ext_data3.update(ext_data)

        return jsonify({"message": "Image uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


image_urls = [
    "/uploads/gray_gray_shazrin_ic.jpg",
    # 'http://example.com/image2.jpg',
    # Add more image URLs here
]


# def main():
#     li = []
#     # fp=python_server.upload_image.image
#     fp = "adhar8.jpg"
#     # image = Image.open(fp)
#     # image.show()
#     image = cv2.imread(fp)

#     barcodes = decode(image)
#     decoded = barcodes[0]
#     # print(decoded)
#     url: bytes = decoded.data
#     url = url.decode()
#     # print(url)

#     rect = decoded.rect
#     # print(rect)

#     poly = decoded.polygon
#     # print(centroid(poly))
#     for barcode in barcodes:
#         # print(barcode.rect)
#         (x, y, w, h) = barcode.rect
#         r = barcode.rect
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)

#         Cx = x + 0.5 * (w)
#         Cy = y + 0.5 * (h)

#         barcodeData = barcode.data.decode("utf-8")
#         barcodeType = barcode.type

#         text = "{} ({})".format(barcodeData, barcodeType)
#         cv2.putText(
#             image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
#         )

#         li.append([barcodeData, (Cx, Cy)])
#         # print("[INFO] Found [{},{}] barcode: {}".format(x, y, barcodeData))

#         obj = AadhaarSecureQr(int(barcodeData))
#         # decoded_secure_qr_data = secure_qr.decodeddata()
#         ext_data = obj.decodeddata()
#         print(ext_data)

#         out_file = open("myfile.json", "w")

#         json.dump(ext_data, out_file, indent=6)

#         out_file.close()
#     # print(li)
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)


# main()


@app.route("/get_image", methods=["GET"])
def get_image():
    # You can replace this logic with fetching images from a database or other sources
    image_url = image_urls[0]
    f = open("myfile.json")
    data = json.load(f)
    f.close()
    return jsonify(ext_data2)


if __name__ == "__main__":
    app.run(debug=True)
