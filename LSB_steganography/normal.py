# an example with black and white image using normal method
from PIL import Image

import LsbSteg

from CaesarCipher import CaesarCipher

import canny_edge_detector

if __name__ == "__main__":
    message = input("enter hidden message: ")
    # message = "I am a message"

    imageFilename = "BW-using-curves.jpg"
    img = Image.open(imageFilename)
    newImageFilename = "stego_BW-using-curves3"

    # running canny edge detection on the image
    detect = canny_edge_detector.cannyEdgeDetector(img)

    # embedding the encrypted message into the 2 halves
    newImg = LsbSteg.encodeLSB(message, imageFilename, newImageFilename)
    if not newImg is None:
        print("Stego image created.")

    # newImg.show()

    # decoding the encrypted message from the 2 halves
    print("Decoding...")
    message = LsbSteg.decodeLSB("stego_BW-using-curves3.png")
    print("Final message: ", message)
