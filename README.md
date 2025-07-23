## OBS Replay Buffer Anti-Overlap Script

This prevents the replay buffer saves from overlapping by restarting the buffer (and therefore the buffer counter) everytime a clip is saved.

---

## Installation

1. **Download the script**
   - Download or copy the `anti-overlap.py` file

2. **Add the script to OBS**
   - Open OBS
   - Go to `Tools` > `Scripts`
   - Click the `+` button and select the `anti-overlap.py` file

3. **Set Up the Hotkey**
   - Go to `Settings` > `Hotkeys`
   - Find `Smart Save Replay` in the list and assign a key to it