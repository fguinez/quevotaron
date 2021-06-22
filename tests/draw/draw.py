# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

from PIL import Image, ImageDraw, ImageFont
import sys




im = Image.open("foto.png") 
draw = ImageDraw.Draw(im)




# LETRAS
draw.text((50,50), "Hello HELLO", fill='#330000')

bold =  myFont = ImageFont.truetype('../../fonts/IBM-Plex-Sans/IBMPlexSans-Bold.ttf', 60)
draw.text((50,100), "Hello HELLO", font=bold, fill='#3344FF')




## FORMAS

draw.ellipse((100, 500, 200, 600), fill='#ff9900')

# triángulo
x, y, r = (300, 500, 50)
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FFFF55')
draw.regular_polygon(((300, 500+r*0.1628), 50), 3, fill='#119900')

# cuadrado
x, y, r = (400, 500, 50)
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FFFF55')
draw.regular_polygon(((400, 500), 50), 4, fill='#772266')

# pentágono
x, y, r = (500, 500, 50)
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FFFF55')
draw.regular_polygon(((500, 500), 50*0.95), 5, fill='#222299')

# circulo
x, y, r = (600, 500, 50)
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FFFF55')
r *= 0.8
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FF0033')
im.show()
# circulo
x, y, r = (700, 500, 50)
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FFFF55')
r *= 0.8
draw.ellipse((x-r, y-r, x+r, y+r), fill='#FF0033')
im.show()


im.save("foto_edited.png")