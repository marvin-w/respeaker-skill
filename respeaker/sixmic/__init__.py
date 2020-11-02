"""Support for ReSpeaker 6-Mics Hat."""
import time

import RPi.GPIO as GPIO
from gpiozero import LED
from mycroft import Message

from ..fourmic import Respeaker4Mic


class Respeaker6Mic(Respeaker4Mic):
    """Strategy for respeaker 6 mic hat."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)
        self.power = LED(5)
        self.button = 26

    def startup(self):
        """Startup 6mic hat."""
        super().startup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button, GPIO.IN)

    def supports_button(self) -> bool:
        """Supports button presses."""
        return True

    def button_cb(self) -> None:
        """Button callback."""
        longpress_threshold = 2
        is_active = GPIO.input(self.button)

        if is_active:
            pressed_time = time.time()
            while is_active:
                time.sleep(0.2)
            pressed_time = time.time() - pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.bus.emit(Message("mycroft.stop"))

