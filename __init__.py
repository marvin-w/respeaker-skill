# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# All credits go to domcross (Github https://github.com/domcross)

import time

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
from mycroft.util.log import LOG
from mycroft import intent_file_handler

from pixel_ring import pixel_ring
from gpiozero import LED

class ReSpeaker_4mic_hat(MycroftSkill):
    
    def __init__(self):
        super(ReSpeaker_4mic_hat, self).__init__(name="ReSpeaker_4mic_hat")

    def initialize(self):
	power = LED(5)
        power.on()
        pixel_ring.set_brightness(10)

        pixel_ring.wakeup()
	self.enable()

    def enable(self):
        LOG.debug("initializing")

        self.add_event('recognizer_loop:record_begin',
                        self.handle_listener_wakeup)
        self.add_event('recognizer_loop:record_end',
                        self.handle_listener_off)

        self.add_event('mycroft.skill.handler.start',
                        self.handler_listener_think)
        self.add_event('mycroft.skill.handler.complete',
                        self.handler_listener_off)

        self.add_event('recognizer_loop:audio_output_start',
                        self.handler_listener_speak)
        self.add_event('recognizer_loop:audio_output_end',
                        self.handle_listener_off)

        pixel_ring.off()

    def disable(self):
        LOG.debug("shutdown")
        self.remove_event('recognizer_loop:record_begin')
        self.remove_event('recognizer_loop:record_end')
        self.remove_event('recognizer_loop:audio_output_start')
        self.remove_event('recognizer_loop:audio_output_end')
        self.remove_event('mycroft.skill.handler.start')
        self.remove_event('mycroft.skill.handler.complete')

     def shutdown(self):
        pixel_ring.off()

    def handle_listener_wakeup(self, message):
        LOG.debug("wakeup")
        pixel_ring.listen()

    def handle_listener_off(self, message):
        LOG.debug("off")
        pixel_ring.off()

    def handle_listener_think(self, message):
        LOG.debug("think")
        pixel_ring.think()

    def handler_listener_speak(self, message):
        LOG.debug("speak")
        pixel_ring.speak()

    @intent_handler(IntentBuilder("").require("EnablePixelRing"))
    def handle_enable_pixel_ring_intent(self, message):
        self.enable()
        self.speak_dialog("EnablePixelRing")

    @intent_handler(IntentBuilder("").require("DisablePixelRing"))
    def handle_disable_pixel_ring_intent(self, message):
        self.disable()
        self.speak_dialog("DisablePixelRing")

def create_skill():
    return ReSpeaker_4mic_hat()
