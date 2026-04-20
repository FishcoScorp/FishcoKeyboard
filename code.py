import time

import board
import busio
import digitalio
import keypad
import rotaryio
import usb_hid

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


ROW_PINS = (
    board.IO4,
    board.IO5,
    board.IO6,
    board.IO7,
    board.IO8,
    board.IO9,
)

COL_PINS = (
    board.IO10,
    board.IO11,
    board.IO12,
    board.IO13,
    board.IO14,
    board.IO15,
    board.IO16,
    board.IO17,
    board.IO18,
    board.IO21,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39,
    board.IO40,
    board.IO41,
    board.IO42,
)

ENCODER_A = board.IO47
ENCODER_B = board.IO48
ENCODER_BUTTON = board.IO1

OLED_SCL = board.IO3
OLED_SDA = board.IO2

ROW_COUNT = len(ROW_PINS)
COL_COUNT = len(COL_PINS)


def build_keymap():
    no = None
    action = lambda name: ("action", name)

    rows = [
        [
            no,
            Keycode.ESCAPE,
            Keycode.F1,
            Keycode.F2,
            Keycode.F3,
            Keycode.F4,
            Keycode.F5,
            Keycode.F6,
            Keycode.F7,
            Keycode.F8,
            Keycode.F9,
            Keycode.F10,
            Keycode.F11,
            Keycode.F12,
            action("ALT_F4_MACRO"),
            no,
            no,
            no,
        ],
        [
            no,
            Keycode.GRAVE_ACCENT,
            Keycode.ONE,
            Keycode.TWO,
            Keycode.THREE,
            Keycode.FOUR,
            Keycode.FIVE,
            Keycode.SIX,
            Keycode.SEVEN,
            Keycode.EIGHT,
            Keycode.NINE,
            Keycode.ZERO,
            Keycode.MINUS,
            Keycode.EQUALS,
            Keycode.BACKSPACE,
            action("MEDIA_PREV"),
            action("MEDIA_PLAY_PAUSE"),
            action("MEDIA_NEXT"),
        ],
        [
            action("UNASSIGNED_1"),
            Keycode.TAB,
            Keycode.Q,
            Keycode.W,
            Keycode.E,
            Keycode.R,
            Keycode.T,
            Keycode.Y,
            Keycode.U,
            Keycode.I,
            Keycode.O,
            Keycode.P,
            Keycode.LEFT_BRACKET,
            Keycode.RIGHT_BRACKET,
            Keycode.BACKSLASH,
            action("OPEN_SETTINGS"),
            action("OPEN_DISCORD"),
            action("OPEN_SPOTIFY"),
        ],
        [
            action("UNASSIGNED_2"),
            Keycode.CAPS_LOCK,
            Keycode.A,
            Keycode.S,
            Keycode.D,
            Keycode.F,
            Keycode.G,
            Keycode.H,
            Keycode.J,
            Keycode.K,
            Keycode.L,
            Keycode.SEMICOLON,
            Keycode.QUOTE,
            Keycode.ENTER,
            no,
            action("MEDIA_MUTE"),
            action("DISCORD_DEAFEN"),
            action("LEDS_TOGGLE"),
        ],
        [
            action("UNASSIGNED_3"),
            Keycode.LEFT_SHIFT,
            Keycode.Z,
            Keycode.X,
            Keycode.C,
            Keycode.V,
            Keycode.B,
            Keycode.N,
            Keycode.M,
            Keycode.COMMA,
            Keycode.PERIOD,
            Keycode.FORWARD_SLASH,
            Keycode.RIGHT_SHIFT,
            Keycode.UP_ARROW,
            no,
            no,
            action("COPY"),
            action("PASTE"),
        ],
        [
            action("UNASSIGNED_4"),
            no,
            no,
            no,
            Keycode.LEFT_CONTROL,
            Keycode.LEFT_GUI,
            Keycode.LEFT_ALT,
            Keycode.SPACEBAR,
            Keycode.RIGHT_ALT,
            action("FN_LAYER"),
            Keycode.RIGHT_CONTROL,
            Keycode.LEFT_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.RIGHT_ARROW,
            no,
            no,
            no,
            no,
            no,
            no,
        ],
    ]

    flattened = [code for row in rows for code in row]
    if len(flattened) != ROW_COUNT * COL_COUNT:
        raise ValueError("Keymap dimensions do not match matrix size")
    return flattened


KEYMAP = build_keymap()


def key_number_to_keycode(key_number):
    return KEYMAP[key_number]


def setup_display():
    try:
        import displayio
        import terminalio
        from adafruit_display_text import label
        from adafruit_displayio_ssd1306 import SSD1306
    except ImportError:
        return None

    displayio.release_displays()

    i2c = busio.I2C(OLED_SCL, OLED_SDA)
    display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
    display = SSD1306(display_bus, width=128, height=32)

    splash = displayio.Group()
    text = label.Label(terminalio.FONT, text="HELLO WORLD", color=0xFFFFFF, x=8, y=16)
    splash.append(text)
    display.root_group = splash
    return display


keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)

matrix = keypad.KeyMatrix(
    row_pins=ROW_PINS,
    column_pins=COL_PINS,
    columns_to_anodes=True,
)

encoder = rotaryio.IncrementalEncoder(ENCODER_A, ENCODER_B)
last_encoder_position = encoder.position

encoder_button = digitalio.DigitalInOut(ENCODER_BUTTON)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP
last_button_value = encoder_button.value

display = setup_display()
pressed_counts = {}


def send_combo(*keycodes):
    keyboard.press(*keycodes)
    keyboard.release_all()


def handle_custom_action(action_name):
    if action_name.startswith("UNASSIGNED_"):
        # Reserved side buttons; assign behavior here later.
        return

    if action_name == "ALT_F4_MACRO":
        send_combo(Keycode.LEFT_ALT, Keycode.F4)
    elif action_name == "MEDIA_PREV":
        consumer.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
    elif action_name == "MEDIA_PLAY_PAUSE":
        consumer.send(ConsumerControlCode.PLAY_PAUSE)
    elif action_name == "MEDIA_NEXT":
        consumer.send(ConsumerControlCode.SCAN_NEXT_TRACK)
    elif action_name == "OPEN_SETTINGS":
        send_combo(Keycode.LEFT_GUI, Keycode.I)
    elif action_name == "OPEN_DISCORD":
        # Placeholder for host-side automation or remapping.
        return
    elif action_name == "OPEN_SPOTIFY":
        # Placeholder for host-side automation or remapping.
        return
    elif action_name == "FN_LAYER":
        # Placeholder for an additional layer later.
        return
    elif action_name == "MEDIA_MUTE":
        consumer.send(ConsumerControlCode.MUTE)
    elif action_name == "DISCORD_DEAFEN":
        # Placeholder for host-side automation or remapping.
        return
    elif action_name == "LEDS_TOGGLE":
        # Placeholder for lighting control later.
        return
    elif action_name == "COPY":
        send_combo(Keycode.LEFT_CONTROL, Keycode.C)
    elif action_name == "PASTE":
        send_combo(Keycode.LEFT_CONTROL, Keycode.V)


def press_key(keycode):
    if keycode is None:
        return

    if isinstance(keycode, tuple) and keycode[0] == "action":
        handle_custom_action(keycode[1])
        return

    count = pressed_counts.get(keycode, 0)
    if count == 0:
        keyboard.press(keycode)
    pressed_counts[keycode] = count + 1


def release_key(keycode):
    if keycode is None:
        return

    if isinstance(keycode, tuple) and keycode[0] == "action":
        return

    count = pressed_counts.get(keycode, 0)
    if count <= 1:
        pressed_counts.pop(keycode, None)
        keyboard.release(keycode)
    else:
        pressed_counts[keycode] = count - 1


def handle_matrix_events():
    while True:
        event = matrix.events.get()
        if event is None:
            return

        keycode = key_number_to_keycode(event.key_number)
        if event.pressed:
            press_key(keycode)
        elif event.released:
            release_key(keycode)


def handle_encoder():
    global last_encoder_position

    position = encoder.position
    delta = position - last_encoder_position
    if delta > 0:
        for _ in range(delta):
            consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif delta < 0:
        for _ in range(-delta):
            consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
    last_encoder_position = position


def handle_encoder_button():
    global last_button_value

    current_value = encoder_button.value
    if last_button_value and not current_value:
        consumer.send(ConsumerControlCode.MUTE)
    last_button_value = current_value


while True:
    handle_matrix_events()
    handle_encoder()
    handle_encoder_button()
    time.sleep(0.001)
