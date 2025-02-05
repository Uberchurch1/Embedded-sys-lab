from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board
import busio
import time
import psutilWIDTH = 128
HEIGHT = 64

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# textbbox
try:
    font = ImageFont.truetype("arial.ttf", 14)
except IOError:
    font = ImageFont.load_default()  
    
emoji_font_path = "NotoEmoji-VariableFont_wght.ttf"
emoji_font = ImageFont.truetype(emoji_font_path, 10)


## get CPU temp
def get_cpu_temperature():
    """Get the CPU temperature (if no external sensor)."""
    try:
        temp = psutil.sensors_temperatures()
        if "cpu_thermal" in temp:
            return temp["cpu_thermal"][0].current
        return 0.0  
    except Exception:
        return 0.0  

while True:
    image = Image.new("1", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    current_time = time.strftime("%H:%M:%S")

    temperature = get_cpu_temperature()
    temp_text = f"Temp: {temperature:.1f}°C"

    text = "Hello World"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    time_bbox = draw.textbbox((0, 0), current_time, font=font)
    time_width = time_bbox[2] - time_bbox[0]

    temp_bbox = draw.textbbox((0, 0), temp_text, font=font)
    temp_width = temp_bbox[2] - temp_bbox[0]

    x_text = (WIDTH - text_width) // 2
    x_time = (WIDTH - time_width) // 2
    x_temp = (WIDTH - temp_width) // 2

    draw.text((x_text, 5), text, font=font, fill=255)        
    draw.text((x_time, 25), current_time, font=font, fill=255)  
    draw.text((x_temp, 45), temp_text, font=font, fill=255)  
    draw.text((0,15), "\U0001F346", font=emoji_font, fill=255)

    oled.image(image)
    oled.show()

    time.sleep(1)