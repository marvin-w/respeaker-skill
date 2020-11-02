"""ReSpeaker library."""
import subprocess

from .strategy import RespeakerStrategy


def obtain_strategy(pattern, bus) -> RespeakerStrategy:
    """Get the supported strategy."""
    result = subprocess.run(['ls', '-al', '/etc/asound.conf'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if '2mic' in result:
        raise NotImplementedError
    if '4mic' in result:
        from .fourmic import Respeaker4Mic
        return Respeaker4Mic(pattern, bus)
    if '6mic' in result:
        from .sixmic import Respeaker6Mic
        return Respeaker6Mic(pattern, bus)

    result = subprocess.run(['uname', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    if 'respeaker' in result:
        from .corev2 import CoreV2
        return CoreV2(pattern, bus)

    #  TODO: We should catch this and speak a dialog to the user in this case.
    raise NotImplementedError("Your system does not support this skill. Please make sure you installed all neccessary "
                              "drivers.")
