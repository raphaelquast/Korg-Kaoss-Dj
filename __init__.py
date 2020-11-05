#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BeatStep/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
# import _Framework.Capabilities as caps
from .KorgKaossDJ import KorgKaossDJ

# def get_capabilities():
#     return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=2372, product_ids=[769], model_name=[u'Korg Kaoss DJ']),
#             caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT, caps.REMOTE]),
#                              caps.outport(props=[caps.SCRIPT])]}


def create_instance(c_instance):
    return KorgKaossDJ(c_instance)