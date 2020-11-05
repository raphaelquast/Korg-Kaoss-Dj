# General

This is a **MIDI Remote Script** for **Ableton Live 10** and the **Korg Kaoss DJ** controller.
Use it, modify it, do whatever you want with it!  (any comments and suggestions are highly welcome!)

## ... it works like this:

- the **first track** is assigned to the **"left-side"** of the controller,  
  the **second track** is assigned to the **"right-side"** of the controller

- ALL controls will always target the **currently playing** scene of the associated tracks!  
  (they do **NOT** follow the selected track)
  
  - why? because in this way you can select another track and use a second midi-controller to do fancy stuff on it while still being able to control the basic elements of the first 2 tracks from the DJ controller.

- **Basic track-control**
  
  - start-stop, control volume, move playing position, move start marker
  
  - toggle pre-listen state, change global set bpm

- **Looping**
  
  - toggle loop, change length, change position
  
  - activate loop at current playing position
  
  - indicate if a loop is active with the center-led  
    (targets playing track or if none is playing the selected track)

- **Basic navigation**
  
  - browse scenes, activate track 1 or 2

# Installation

To use this script, simply copy the contents into a folder named "KorgKaossDJ" within the MIDI Remote Scripts folder of Ableton Live  (located at `..install-dir..\Resources\MIDI Remote Scripts`) and then select the **KorgKaossDJ** device as control-surface in the MIDI-tab of the preferences. (make sure to activate both `track`and `remote` for this device!)

# Button assignments:

## Loop buttons (loop-light on)

| <mark>LEFT</mark>        | <mark>MIDDLE</mark>                            | <mark>RIGHT</mark>        |
|:------------------------:|:----------------------------------------------:|:-------------------------:|
| half loop length         | toggle loop                                    | double loop length        |
|                          | <mark>**WITH SHIFT**</mark>                    |                           |
| move loop left (4 beats) | start a 32 beats loop at the  playing position | move loop right (4 beats) |

## Hot Cue buttons (HotCue light on)

| <mark>LEFT</mark>            | <mark>MIDDLE</mark>                            | <mark>RIGHT</mark>           |
|:----------------------------:|:----------------------------------------------:|:----------------------------:|
| reduce loop length by 1 beat | toggle loop                                    | extend loop length by 1 beat |
|                              | **<mark>WITH SHIFT</mark>**                    |                              |
| move loop left (1 beat)      | start a 16 beats loop at the  playing position | move loop right (1 beat)     |

## Tempo fader

| <mark>LEFT</mark>      | adjust the global bpm setting between 60 and 200                         |
| ---------------------- | ------------------------------------------------------------------------ |
| <mark>**RIGHT**</mark> | adjust the global bpm setting in a fine-scale (approx. plus-minus 1 bpm) |

## Loudness fader

- adjust the volume of the left/right track

## Gain knobs

- adjust "**Send A**" (e.g. the first return track) of the left/right track

## Pre-listen buttons

- toggle pre-listen mode of left/right track

- NOTE:
  
  - you must set the cue-out to a different output than the main-out track
  
  - you must activate pre-listen mode (instead of solo-mode) in the main-out track

## Jog wheels

| <mark><u>LOOPING OFF</u></mark>    | <mark>NORMAL</mark>                         | <mark>WITH SHIFT</mark>                |
| ---------------------------------- | ------------------------------------------- | -------------------------------------- |
| <mark>**LIGHT ON**</mark>          | scrobble track (e.g. move playing position) | move track start marker (coarse scale) |
| <mark>**LIGHT OFF**</mark>         | move track start marker (fine scale)        | move track start marker (coarse scale) |
| <mark>**<u>LOOPING ON</u>**</mark> |                                             |                                        |
| <mark>**LIGHT ON**</mark>          | scrobble track (e.g. move playing position) | move loop position (coarse scale)      |
| <mark>**LIGHT OFF**</mark>         | move loop position (fine scale)             | move loop position (coarse scale)      |

- moving the start-marker of a playing track will also adjust the current playing position!

- scrobbling a track will start playback!

## Further buttons & knobs (located in the center)

| <mark>A button</mark>        | activate (e.g. focus) the left track  |
|:----------------------------:|:-------------------------------------:|
| <mark>**B button**</mark>    | activate (e.g. focus) the right track |
| <mark>**Browse knob**</mark> | move clip-selection up-down           |

## ... THANKS to

- Julien Bayle for the awesome [PythonLiveAPI_documentation](https://julienbayle.studio/PythonLiveAPI_documentation/) and some more info's [here](https://julienbayle.studio/ableton-live-midi-remote-scripts/)

- Hanz Petrov for his [Introduction to the Framework-classes](https://livecontrol.q3f.org/ableton-liveapi/articles/introduction-to-the-framework-classes/) and the corresponding [remotescripts-blog](http://remotescripts.blogspot.com)

- azuki for introducing the basics here: [Writing Custom Control Surfaces for Ableton](https://blog.azuki.vip/ableton-midi/)

- willrjmarshall for his ideas within the [AbletonDJTemplate](https://github.com/willrjmarshall/AbletonDJTemplateUnsupported)
