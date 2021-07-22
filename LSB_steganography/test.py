from PIL import Image

import LsbSteg

from CaesarCipher import CaesarCipher

import canny_edge_detector


def crop(filename, number):
    im = Image.open(filename)
    w, h = im.size
    # unit is the size per slice
    unit = w // 2
    for n in range(number):
        im1 = im.crop((unit * n, 0, unit * (n + 1), h))
        im1.save(filename[:-4] + str(n + 1) + ".png")


if __name__ == "__main__":
    # CaesarCipher key
    key = 5
    message = "I am a message"

    # splitting the image into 2
    crop("stars_background.jpg", 2)

    imageFilename = "stars_background1.png"
    imageFilename2 = "stars_background2.png"
    img = Image.open(imageFilename)
    img2 = Image.open(imageFilename)

    newImageFilename = "stego_stars_background1"
    newImageFilename2 = "stego_stars_background2"

    # CaesarCipher encryption on the imbedded message
    encMessage = CaesarCipher.encrypt(message, key)
    print("Message after cipher encrypt:", encMessage)

    # running canny edge detection on the image
    img = Image.open(imageFilename)
    detect = canny_edge_detector.cannyEdgeDetector(img)

    # embedding the encrypted message into the 2 halves
    newImg = LsbSteg.encodeLSB(encMessage, imageFilename, newImageFilename)
    if not newImg is None:
        print("Stego image1 created.")
    newImg = LsbSteg.encodeLSB(encMessage, imageFilename2, newImageFilename2)
    if not newImg is None:
        print("Stego image2 created.")

    # getting image size
    size1 = img.size
    size2 = img2.size

    # combining back the split images
    new_image = Image.new('RGB', (2 * size1[0], size1[1]), (250, 250, 250))
    new_image.paste(img, (0, 0))
    new_image.paste(img2, (size1[0], 0))
    new_image.save("merged_images.png", "PNG")
    new_image.show()

    # decoding the encrypted message from the 2 halves
    print("Decoding...")
    rawMessage1 = LsbSteg.decodeLSB("stego_stars_background1.png")
    # print("Message1 before cipher decrypt:", rawMessage1)
    message = CaesarCipher.decrypt(rawMessage1, key)
    # print("Final message from 1: ", message)
    rawMessage2 = LsbSteg.decodeLSB("stego_stars_background2.png")
    # print("Message2 before cipher decrypt:", rawMessage2)
    message2  = CaesarCipher.decrypt(rawMessage2, key)
    # print("Final message from 2: ", message2)

    # check if both halfs returned the same message
    if message == message2:
        print("Final message is:", message)
    else:
        print("Messages don't match")
