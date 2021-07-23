from PIL import Image

import LsbSteg

from CaesarCipher import CaesarCipher

def crop(filename, number):
    im = Image.open(filename)
    w, h = im.size
    # unit is the size per slice
    unit = w // 2
    for n in range(number):
        im1 = im.crop((unit * n, 0, unit * (n + 1), h))
        im1.save(filename[:-4] + str(n + 1) + ".png")


# CaesarCipher key
key = 5
# splitting the image into 2
crop("merged_images.png", 2)

# TODO fix the image split
imageFilename = "merged_images1.png"
imageFilename2 = "merged_images2.png"
img = Image.open(imageFilename)
img2 = Image.open(imageFilename)

newImageFilename = "stego_merged_images1"
newImageFilename2 = "stego_merged_images2"

# decoding the encrypted message from the 2 halves
print("Decoding...")
rawMessage1 = LsbSteg.decodeLSB("stego_merged_images1.png")
# print("Message1 before cipher decrypt:", rawMessage1)
message = CaesarCipher.decrypt(rawMessage1, key)
# print("Final message from 1: ", message)
rawMessage2 = LsbSteg.decodeLSB("stego_merged_images2.png")
# print("Message2 before cipher decrypt:", rawMessage2)
message2 = CaesarCipher.decrypt(rawMessage2, key)
# print("Final message from 2: ", message2)

# check if both halves returned the same message
if message == message2:
    print("Final message is:", message)
else:
    print("Messages don't match")
