import qrcode
img = qrcode.make('https://www.bioxsystems.com/')
type(img) # qrcode.image.pil.PilImage
img.save("access_biox_systems.png")

