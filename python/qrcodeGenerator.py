import qrcode

def generate(message):
    img = qrcode.make(message)

    print(type(img))
    print(img.size)
    img.save('qrcode_test.png')
    return img