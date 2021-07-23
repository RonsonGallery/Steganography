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
    message = input("enter hidden message: ")

    # splitting the image into 2
    crop("1.jpg", 2)

    imageFilename = "11.png"
    imageFilename2 = "12.png"
    img = Image.open(imageFilename)
    img2 = Image.open(imageFilename2)

    newImageFilename = "stego_11.png"
    newImageFilename2 = "stego_12.png"

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
