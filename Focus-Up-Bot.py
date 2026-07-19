import board
import displayio
import i2cdisplaybus
import digitalio
import adafruit_displayio_ssd1306
import pwmio
import time
import neopixel

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
# Buzzer Setup
# ----------------

buzzer = pwmio.PWMOut(board.D6, duty_cycle=0, frequency=1000)

# ----------------
# Pomodoro Setup
# ----------------

IDLE = 0
FOCUS = 1
BREAK = 2

current_mode = IDLE
start_time = 0

# 15 minutes
focus_length = 15 * 60

# 5 minutes
break_length = 5 * 60

last_progress_update = -1



# ----------------
# Drawing Functions
# ----------------

def draw_idle_face():
    bitmap.fill(0)

    # Left open eye
    for x in range(37, 43):
        for y in range(18, 24):
            bitmap[x, y] = 1

    # Right open eye
    for x in range(85, 91):
        for y in range(18, 24):
            bitmap[x, y] = 1

    # Mouth
    for x in range(48, 80):
        bitmap[x, 38] = 1


def draw_focus_face():
    bitmap.fill(0)

    # Left focused eye
    for x in range(37, 43):
        bitmap[x, 21] = 1

    # Right focused eye
    for x in range(85, 91):
        bitmap[x, 21] = 1

    # Mouth
    for x in range(48, 80):
        bitmap[x, 38] = 1


def draw_break_face():
    bitmap.fill(0)

    # Open eyes
    for x in range(37, 43):
        for y in range(18, 24):
            bitmap[x, y] = 1

    for x in range(85, 91):
        for y in range(18, 24):
            bitmap[x, y] = 1

    # Smile
    for x in range(48, 80):
        bitmap[x, 36] = 1

    for x in range(52, 76):
        bitmap[x, 40] = 1

    for y in range(36, 41):
        bitmap[48, y] = 1
        bitmap[79, y] = 1


def draw_progress_bar(progress):
    # Clear old progress bar area
    for x in range(8, 120):
        for y in range(51, 62):
            bitmap[x, y] = 0

    # Progress bar outline
    for x in range(8, 120):
        bitmap[x, 51] = 1
        bitmap[x, 61] = 1

    for y in range(51, 62):
        bitmap[8, y] = 1
        bitmap[119, y] = 1

    # Keep progress between 0 and 1
    if progress < 0:
        progress = 0

    if progress > 1:
        progress = 1

    # Fill progress bar
    fill_width = int(progress * 108)

    for x in range(10, 10 + fill_width):
        for y in range(53, 60):
            bitmap[x, y] = 1

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
# Mode Functions
# ----------------

def start_focus():
    global current_mode
    global start_time
    global last_progress_update

    current_mode = FOCUS
    start_time = time.monotonic()
    last_progress_update = -1

    draw_focus_face()
    draw_progress_bar(0)

    # Green = focus
    pixel[0] = (0, 255, 0)


def start_break():
    global current_mode
    global start_time
    global last_progress_update

    current_mode = BREAK
    start_time = time.monotonic()
    last_progress_update = -1

    draw_break_face()
    draw_progress_bar(0)

    # Purple = break
    pixel[0] = (150, 0, 255)


def return_to_idle():
    global current_mode
    global last_progress_update

    current_mode = IDLE
    last_progress_update = -1

    draw_idle_face()

    # Blue = idle
    pixel[0] = (0, 0, 255)

# ----------------
# Starting State
# ----------------

return_to_idle()

# ----------------
# Main Program Loop
# ----------------

while True:
    current_time = time.monotonic()

    # ----------------
    # Check Button
    # ----------------

    if not button.value:

        # Start focus session
        if current_mode == IDLE:
            start_focus()

        # Cancel focus or break
        else:
            return_to_idle()

        # Wait until button is released
        while not button.value:
            pass

        time.sleep(0.05)

    # ----------------
    # Focus Mode
    # ----------------

    if current_mode == FOCUS:
        elapsed_time = current_time - start_time
        elapsed_second = int(elapsed_time)

        # Update progress bar once per second
        if elapsed_second != last_progress_update:
            last_progress_update = elapsed_second
            progress = elapsed_time / focus_length
            draw_progress_bar(progress)

        # Focus session finished
        if elapsed_time >= focus_length:
            pixel[0] = (255, 0, 0)
            timer_finished_sound()
            time.sleep(1)

            # Automatically start break
            start_break()

    # ----------------
    # Break Mode
    # ----------------

    elif current_mode == BREAK:
        elapsed_time = current_time - start_time
        elapsed_second = int(elapsed_time)

        # Update progress bar once per second
        if elapsed_second != last_progress_update:
            last_progress_update = elapsed_second
            progress = elapsed_time / break_length
            draw_progress_bar(progress)

        # Break finished
        if elapsed_time >= break_length:
            pixel[0] = (255, 0, 0)
            timer_finished_sound()
            time.sleep(1)

            return_to_idle()