import board
import displayio
import i2cdisplaybus
import digitalio
import adafruit_displayio_ssd1306
import time
import neopixel
import pwmio

# ----------------
# Buzzer Setup
# ----------------

buzzer = pwmio.PWMOut(board.D6, duty_cycle=0, frequency=4000)

# ----------------
# OLED Setup
# ----------------

displayio.release_displays()

i2c = board.I2C()

display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

bitmap = displayio.Bitmap(128, 64, 2)

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)

display.root_group = group

# ----------------
# Button Setup
# ----------------

button = digitalio.DigitalInOut(board.D5)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# ----------------
# NeoPixel Setup
# ----------------

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.2

# ----------------
# OLED Face Functions
# ----------------

def draw_idle_face():
    bitmap.fill(0)

    # Left open eye
    for x in range(37, 43):
        for y in range(25, 31):
            bitmap[x, y] = 1

    # Right open eye
    for x in range(85, 91):
        for y in range(25, 31):
            bitmap[x, y] = 1

    # Mouth
    for x in range(48, 80):
        bitmap[x, 45] = 1


def draw_focus_face():
    bitmap.fill(0)

    # Left closed eye
    for x in range(37, 43):
        bitmap[x, 27] = 1

    # Right closed eye
    for x in range(85, 91):
        bitmap[x, 27] = 1

    # Mouth
    for x in range(48, 80):
        bitmap[x, 45] = 1


# ----------------
# Buzzer Function
# ----------------

def timer_finished_sound():
    buzzer.duty_cycle = 32768
    time.sleep(0.2)

    buzzer.duty_cycle = 0
    time.sleep(0.15)

    buzzer.duty_cycle = 32768
    time.sleep(0.2)

    buzzer.duty_cycle = 0

# ----------------
# Timer Setup
# ----------------

# Blue = Idle
# Green = Timer running
# Red = Timer finished

timer_running = False
start_time = 0
focus_length = 10

# Start in idle mode
draw_idle_face()
pixel[0] = (0, 0, 255)

# ----------------
# Main Program Loop
# ----------------

while True:

    # Check if button is pressed
    if not button.value:
        timer_running = not timer_running

        # Start timer
        if timer_running:
            start_time = time.monotonic()
            draw_focus_face()
            pixel[0] = (0, 255, 0)

        # Cancel timer
        else:
            draw_idle_face()
            pixel[0] = (0, 0, 255)

        # Wait until button is released
        while not button.value:
            pass

    # Check timer progress
    if timer_running:
        elapsed_time = time.monotonic() - start_time

        # Timer finished
        if elapsed_time >= focus_length:
            timer_running = False

            draw_idle_face()

            # Glow red and play completion sound
            pixel[0] = (255, 0, 0)
            timer_finished_sound()
            time.sleep(3)

            # Return to idle blue
            pixel[0] = (0, 0, 255)