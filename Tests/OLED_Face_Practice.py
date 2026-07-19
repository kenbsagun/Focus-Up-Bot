import board
import displayio
import i2cdisplaybus
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c = board.I2C()

#Device_Address = 0x3C is corret

display_bus = i2cdisplaybus.I2CDisplayBus(i2c,device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(display_bus,width=128,height=64)

bitmap = displayio.Bitmap(128, 64, 2)
palette = displayio.Palette(2)

palette[0] = 0x000000
palette[1] = 0xFFFFFF

tile_grid = displayio.TileGrid(bitmap,pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)

display.root_group = group

# Left eye
for x in range(37, 43):
    for y in range(25, 31):
        bitmap[x, y] = 1

# Right eye
for x in range(85, 91):
    for y in range(25, 31):
        bitmap[x, y] = 1

# Mouth
for x in range(48, 80):
    bitmap[x, 45] = 1

while True:
    pass