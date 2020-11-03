"""Support for ReSpeaker 6-Mics Hat."""
from gpiozero import Button
from mycroft import Message

from ..fourmic import Respeaker4Mic


class Respeaker6Mic(Respeaker4Mic):
    """Strategy for respeaker 6 mic hat."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)
        self.button = Button(26, hold_time=2)
        self.init_button()

    def supports_button(self) -> bool:
        """Supports button presses via reoccuring event."""
        return False

    def init_button(self):
        """Init Button."""
        def held():
            """Executed when held for 2 seconds."""
            self.bus.emit(Message("mycroft.stop"))

        def released():
            """Executed when released."""
            self.bus.emit(Message("mycroft.mic.listen"))

        self.button.when_held = held
        self.button.when_activated = released

