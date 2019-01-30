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
from pixel_ring import pixel_ring
from gpiozero import LED
from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG


class ReSpeaker_4mic_hat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        LOG.debug("initialising")

        power = LED(5)
        power.on()

        pixel_ring.set_brightness(10)
        pixel_ring.wakeup()

        self.add_event('recognizer_loop:record_begin',
                       self.handle_listener_wakeup)
        self.add_event('recognizer_loop:record_end', self.handle_listener_off)
        self.add_event('recognizer_loop:audio_output_start',
                       self.handle_listener_speak)
        self.add_event('recognizer_loop:audio_output_end',
                       self.handle_listener_off)
        self.add_event('mycroft.skill.handler.start',
                       self.handle_listener_think)
        self.add_event('mycroft.skill.handler.complete',
                       self.handle_listener_off)
        pixel_ring.off()

    def shutdown(self):
        LOG.debug("shutdown")
        pixel_ring.off()
        self.en.write(1)

    def handle_listener_wakeup(self, message):
        LOG.debug("wakeup")
        pixel_ring.wakeup()

    def handle_listener_think(self, message):
        LOG.debug("think")
        pixel_ring.think()

    def handle_listener_speak(self, message):
        LOG.debug("speak")
        pixel_ring.speak()

    def handle_listener_off(self, message):
        LOG.debug("off")
        pixel_ring.off()

    @intent_file_handler('ring.pixel.respeaker.intent')
    def handle_ring_pixel_respeaker(self, message):
        self.speak_dialog('ring.pixel.respeaker')


def create_skill():
    return ReSpeaker_4mic_hat()
