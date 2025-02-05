import gpiod
chip = gpiod.Chip("/dev/gpiochip0")
line = chip.get_line(17)
line.request(consumer="LED_ON", type =gpiod.LINE_REQ_DIR_OUT)
line.set_value(0)