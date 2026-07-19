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


for x in range(20, 108):
    bitmap[x, 20] = 1
    bitmap[x, 44] = 1

for y in range(20, 45):
    bitmap[20, y] = 1
    bitmap[107, y] = 1

while True:
    pass