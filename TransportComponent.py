#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Arturia/SessionComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.TransportComponent import TransportComponent as TransportComponentBase
from _Framework.Control import EncoderControl

from _Framework.SubjectSlot import subject_slot


class TransportComponent(TransportComponentBase):

    def __init__(self, _parent, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._parent = _parent


    # don't raise an not-imported error in here... not sure why this is necessary...
    @subject_slot(u'value')
    def _song_position_value(self, value):
        pass
