from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board
import busio

WIDTH = 128
HEIGHT = 64

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

try:
    font = ImageFont.truetype("arial.ttf", 16)
except IOError:
    font = ImageFont.load_default()
    
text = "Hello World"
bbox = draw.textbbox((0,0), text, font=font)
text_width = bbox[2]-bbox[0]
text_height = bbox[3]-bbox[1]


x = (WIDTH - text_width) //2
y = (HEIGHT - text_height) //2

draw.text((x, y), text, font=font, fill=25)

oled.image(image)
oled.show()