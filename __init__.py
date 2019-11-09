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
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import LOG
from mycroft import intent_file_handler

from pixel_ring import pixel_ring
from gpiozero import LED

class ReSpeaker_4mic_hat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

        #self.main_blue = 0x22A7F0
        #self.tertiary_blue = 0x4DE0FF
        #self.tertiary_green = 0x40DBB0

        power = LED(5)
        power.on()
        pixel_ring.set_brightness(10)

    def initialize(self):
        LOG.debug("initialising")
        pixel_ring.wakeup()
        try:
            self.add_event('recognizer_loop:record_begin',
                            self.handle_listener_started)
            self.add_event('recognizer_loop:record_end',
                            self.handle_listener_ended)
            self.add_event('mycroft.speech.recognition.unknown',
                            self.handle_failed_stt)

            self.bus.on('mycroft.skill.handler.start',
                        self.on_handler_started)
            self.bus.on('mycroft.skill.handler.complete',
                        self.on_handler_complete)

            self.bus.on('recognizer_loop:audio_output_start',
                         self.on_handler_audio_start)
            self.bus.on('recognizer_loop:audio_output_end',
                         self.handle_listener_off)
        except Exception as e:
            LOG.debug("exception while setting up pixel_ring: {}".format(e))
        finally:
            pixel_ring.off()

    def shutdown(self):
        LOG.debug("shutdown")
        self.bus.remove('mycroft.skill.handler.start',
                         self.on_handler_started)
        self.bus.remove('mycroft.skill.handler.complete',
                         self.on_handler_complete)
        self.bus.remove('recognizer_loop:audio_output_start',
                         self.on_handler_audio_start)
        self.bus.remove('recognizer_loop:audio_output_end',
                         self.on_handler_audio_end)
        pixel_ring.off()

    def handle_listener_started(self, message):
        LOG.debug("wakeup")
        #pixel_ring.set_color_palette(self.main_blue, self.main_blue)
        pixel_ring.listen()

    def handle_listener_ended(self, message):
        LOG.debug("off")
        pixel_ring.off()

    def handle_failed_stt(self, message):
        LOG.debug("unkown")
        pixel_ring.off()


    def on_handle_started(self, message):
        LOG.debug("think")
        #pixel_ring.set_color_palette(self.main_blue, self.tertiary_green)
        pixel_ring.think()

    def on_handle_complete(self, message):
        LOG.debug("complete")
        pixel_ring.off()

    def on_handler_audio_start(self, message):
        LOG.debug("speak")
        #pixel_ring.set_color_palette(self.main_blue, self.tertiary_blue)
        pixel_ring.speak()

    def on_handler_audio_end(self, message):
        LOG.debug("stop")
        pixel_ring.off()


    @intent_file_handler('ring.pixel.respeaker.intent')
    def handle_ring_pixel_respeaker(self, message):
        self.speak_dialog('ring.pixel.respeaker')


def create_skill():
    return ReSpeaker_4mic_hat()
