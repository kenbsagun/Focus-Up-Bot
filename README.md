# Focus-Up-Bot

Focus Up Bot is an embedded Pomodoro study companion built with a
Metro M0 Express and CircuitPython.

## See It in Action

[Watch the Focus Up Bot demo on YouTube](https://youtu.be/uJ1JSmlKQ8A)

## Features

- 15-minute focus session
- 5-minute break
- OLED animated expressions
- OLED progress bar
- Button-controlled start and cancel
- NeoPixel status feedback
- Passive buzzer completion alert
- Automatic transition from focus to break

## Status Colors

- Blue: Idle
- Green: Focus
- Purple: Break
- Red: Session complete

## Hardware

- Adafruit Metro M0 Express
- 128x64 SSD1306 OLED
- Pushbutton
- Passive buzzer
- Breadboard and jumper wires

## How It Works

The program operates as a finite-state machine with three states:
Idle, Focus, and Break. Timing is handled with `time.monotonic()`.
The OLED communicates with the Metro using I2C.

## Challenges

The original design included environmental monitoring with a DHT11.
Due to the Metro M0's memory constraints, the final design prioritized
a reliable and polished Pomodoro system.

## Future Improvements

- Adjustable session lengths
- Pause and resume
- Temperature monitoring on a board with more RAM
- Session statistics
- Custom enclosure