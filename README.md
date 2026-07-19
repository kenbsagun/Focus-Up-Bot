# Focus Up Bot

Focus Up Bot is an embedded Pomodoro study companion built using an Adafruit Metro M0 Express and CircuitPython. It guides students through a 15-minute focus session followed by a 5-minute break using an OLED display, animated expressions, a live progress bar, NeoPixel status lighting, and audible alerts.

## See It in Action

[![Watch the Focus Up Bot demo](https://img.youtube.com/vi/uJ1JSmlKQ8A/maxresdefault.jpg)](https://youtu.be/uJ1JSmlKQ8A)

## Inspiration

While studying for my AP exams, I found it inconvenient to repeatedly open YouTube and search for a 15/5 Pomodoro timer. Since I was already on YouTube, it was easy to get distracted by other videos or let my five-minute breaks last much longer than intended.

I wanted to create a physical device that could sit on my desk and be dedicated specifically to the 15/5 Pomodoro study method. By moving the timer away from my phone and computer, Focus Up Bot helps eliminate small but significant distractions during study sessions.

## What It Does

Focus Up Bot guides the user through a complete Pomodoro study cycle.

The device begins in an idle state. Pressing the button starts a 15-minute focus session. The OLED displays a focused expression and a progress bar that fills as time passes. The NeoPixel turns green to indicate that the focus session is active.

When the focus period finishes, the NeoPixel turns red and the buzzer plays an alert. The device then automatically begins a 5-minute break. During the break, the OLED expression changes and the NeoPixel turns purple. Once the break ends, the device returns to its blue idle state.

The button can also be used to cancel an active session and return the system to idle.

## How I Built It

The project is powered by an Adafruit Metro M0 Express running CircuitPython.

I connected a 128×64 SSD1306 OLED display using the I²C communication protocol. The OLED displays different facial expressions for the idle, focus, and break states, along with a live progress bar.

A pushbutton connected to a GPIO pin acts as the main user input. The button uses the Metro’s internal pull-up resistor, meaning the input reads `True` while unpressed and `False` while pressed.

The built-in NeoPixel provides color-coded feedback:

- Blue indicates idle mode.
- Green indicates focus mode.
- Purple indicates break mode.
- Red indicates that a timed phase has finished.

A passive buzzer is controlled using PWM to generate completion sounds.

The program is organized as a finite-state machine with three main states:

```text
IDLE → FOCUS → BREAK → IDLE
```

When a timed state begins, the program records its starting time using:

```python
start_time = time.monotonic()
```

The elapsed time is continuously calculated without stopping the rest of the program:

```python
elapsed_time = time.monotonic() - start_time
```

The progress bar is calculated by dividing the elapsed time by the total duration:

```python
progress = elapsed_time / phase_length
```

That ratio is then converted into the number of OLED pixels that should be filled:

```python
fill_width = int(progress * 108)
```

This approach allows the button, display, NeoPixel, buzzer, and timer to continue operating together without freezing the program.

## Challenges I Ran Into

One of the first challenges was correctly wiring the four-pin pushbutton. The button initially appeared to be permanently pressed because some of its legs are internally connected. I isolated the button from the rest of the program, printed its input value to the serial monitor, and tested different pin combinations until I determined that the signal and ground wires needed to be connected across the correct opposing legs.

Another challenge was working with the OLED display libraries. CircuitPython 10 uses `I2CDisplayBus` instead of the older `I2CDisplay` class, so I had to identify and correct a library-version mismatch before the OLED would display properly.

The largest challenge involved memory limitations on the Metro M0 Express. I originally planned to include a DHT11 temperature and humidity sensor that would temporarily display environmental warnings such as “TOO HOT” or “TOO COLD.”

The DHT11 worked correctly by itself, but combining its library with the OLED display system repeatedly caused `MemoryError` exceptions. I experimented with lighter text libraries, smaller display buffers, custom pixel-based text, and simplified graphics. Ultimately, I removed the temperature feature and prioritized a stable, reliable Pomodoro system.

This taught me that adding more features does not always produce a better embedded system. Hardware limitations, reliability, and project scope must also be considered.

## Accomplishments I’m Proud Of

I am proud that I successfully integrated several hardware and software systems into one complete device.

The project combines:

- A microcontroller
- I²C communication
- GPIO input
- An internal pull-up resistor
- PWM output
- NeoPixel control
- OLED graphics
- Non-blocking time tracking
- Finite-state-machine logic

I am also proud that I turned the initial idea into a functioning physical prototype rather than stopping after individual component tests.

## What I Learned

This project taught me that embedded development involves much more than writing code. I had to understand how physical components were wired, how communication protocols worked, how the program managed its current state, and how limited memory affected design decisions.

I learned how to:

- Program a microcontroller using CircuitPython
- Communicate with an OLED through I²C
- Read a pushbutton through GPIO
- Generate buzzer tones using PWM
- Control RGB status lighting
- Design a finite-state machine
- Measure elapsed time using `time.monotonic()`
- Draw graphics directly with OLED pixels
- Debug hardware and software separately
- Manage limited microcontroller memory
- Reduce project scope while preserving the core purpose

Most importantly, I learned that debugging is a major part of engineering. When a feature did not work, I had to isolate the problem, test individual components, interpret errors, and decide whether a feature was worth keeping.

## Features

- 15-minute focus session
- 5-minute break session
- Automatic focus-to-break transition
- OLED progress bar
- Animated OLED expressions
- Pushbutton start and cancel control
- NeoPixel status indicators
- Passive buzzer completion alerts
- Finite-state-machine architecture
- Non-blocking elapsed-time tracking

## Hardware

- Adafruit Metro M0 Express
- 128×64 SSD1306 OLED display
- Pushbutton
- Passive buzzer
- Breadboard
- Jumper wires
- Micro-USB cable

## Software

- CircuitPython 10.2.1
- Python
- `adafruit_displayio_ssd1306`
- `displayio`
- `i2cdisplaybus`
- `digitalio`
- `pwmio`
- `neopixel`
- `board`
- `time`

## Hardware Interfaces

### OLED Display

The OLED communicates with the Metro M0 Express using I²C through the SDA and SCL pins.

### Pushbutton

The pushbutton is connected to a digital GPIO pin and uses the Metro’s internal pull-up resistor:

```python
button.pull = digitalio.Pull.UP
```

This means:

```text
Unpressed = True
Pressed = False
```

### Passive Buzzer

The passive buzzer is controlled through PWM. Changing the PWM frequency produces different audible tones.

### NeoPixel

The Metro M0 Express’s built-in NeoPixel displays the device’s current state using RGB color values.

## Future Improvements

- Adjustable focus and break durations
- Pause and resume controls
- Additional physical buttons
- Session history and productivity statistics
- Environmental sensing using a board with more memory
- A custom 3D-printed enclosure
- Battery-powered operation
- Desktop or mobile synchronization
- Adaptive focus recommendations based on previous study sessions

## Project Structure

```text
Focus-Up-Bot/
├── code.py
├── README.md
├── LICENSE
├── images/
│   ├── final-build.jpg
│   ├── wiring.jpg
│   └── oled-demo.jpg
└── demo/
    └── demo-video-link.txt
```