from BaseComponent import BaseComponent

class FXComponent(BaseComponent):
    'Handles sends controls'
    __module__ = __name__

    def __init__(self, parent, assign_track=0, *args, **kwargs):

        buttonnames = ['_gain_encoder',
                       '_touchpad_x', '_touchpad_y',
                       '_touchpad_x_shift', '_touchpad_y_shift',
                       '_fx_on_off', '_warp_mode', '_warping', '_pitch_up', '_pitch_down']

        super(FXComponent, self).__init__(parent, buttonnames, assign_track)

        self._fx_on = False

    def _gain_encoder_listener(self, value):
        self.send_value(value, send_id=0)

    def _touchpad_x_listener(self, value):
        if self._fx_on:
            self.send_value(value, send_id=1)

    def _touchpad_y_listener(self, value):
        if self._fx_on:
            self.send_value(value, send_id=2)

    def _touchpad_x_shift_listener(self, value):
        if self._fx_on:
            self.send_value(value, send_id=3)

    def _touchpad_y_shift_listener(self, value):
        if self._fx_on:
            self.send_value(value, send_id=4)

    def _fx_on_off_listener(self, value):
        if value ==127:
            self._fx_on = True
        else:
            self._fx_on = False

    def _pitch_up_listener(self, value):
        clip = self.get_current_clip()
        if value > 0:
            clip.pitch_coarse += 1

    def _pitch_down_listener(self, value):
        clip = self.get_current_clip()
        if value > 0:
            clip.pitch_coarse -= 1

    def _warping_listener(self, value):
        clip = self.get_current_clip()
        if value > 0:
            if clip.warping == True:
                clip.warping = False
            else:
                clip.warping = True

    def _warp_mode_listener(self, value):
        clip = self.get_current_clip()
        warp_modes = [i for i in clip.available_warp_modes]
        try:
            warp_index = warp_modes.index(clip.warp_mode)
        except:
            warp_index = 0

        if value > 0:
            clip.warp_mode = warp_modes[(warp_index + 1)%len(warp_modes)]





    def send_value(self, value, send_id=0):
        sends = self._track.mixer_device.sends
        if send_id < len(sends):
            self._track.mixer_device.sends[send_id].value = value / 127.

