import qrcode

def generate(message):
  img = qrcode.make(message)

  print(type(img))
  print(img.size)
  # <class 'qrcode.image.pil.PilImage'>
  # (290, 290)
  img.save('qrcode_test.png')
  return img