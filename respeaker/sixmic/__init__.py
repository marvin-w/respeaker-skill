"""Support for ReSpeaker 6-Mics Hat."""
from gpiozero import Button
from mycroft import Message

from ..fourmic import Respeaker4Mic


class Respeaker6Mic(Respeaker4Mic):
    """Strategy for respeaker 6 mic hat."""

    def __init__(self, bus, pattern) -> None:
        """Init."""
        super().__init__(bus, pattern)
        self.button = Button(26)
        self.init_button()

    def init_button(self):
        """Init Button."""
        def released():
            """Executed when released."""
            self.bus.emit(Message("mycroft.mic.listen"))

        self.button.when_activated = released

