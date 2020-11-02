"""Support for ReSpeaker 6-Mics Hat."""
import time

import RPi.GPIO as GPIO
from mycroft import Message

from ..fourmic import Respeaker4Mic


class Respeaker6Mic(Respeaker4Mic):
    """Strategy for respeaker 6 mic hat."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)
        self.button = 26

    def supports_button(self) -> bool:
        """Supports button presses."""
        return True

    def button_cb(self) -> None:
        """Button callback."""
        longpress_threshold = 2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button, GPIO.IN)

        if GPIO.input(self.button):
            pressed_time = time.time()
            while GPIO.input(self.button):
                time.sleep(0.2)
            pressed_time = time.time() - pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.bus.emit(Message("mycroft.stop"))

