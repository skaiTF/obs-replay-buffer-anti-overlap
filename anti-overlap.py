import obspython as obs
import time

hotkey_id = obs.OBS_INVALID_HOTKEY_ID

def on_smart_save_pressed(pressed):
    if not pressed:
        return

    if not obs.obs_frontend_replay_buffer_active():
        print("Replay buffer not active")
        return

    print("Save replay")

    obs.obs_frontend_replay_buffer_save()
    # Wait 500ms before stopping the buffer to allow save to complete
    obs.timer_add(stop_replay_buffer_after_save, 500)


def stop_replay_buffer_after_save():
    obs.obs_frontend_replay_buffer_stop()
    obs.timer_remove(stop_replay_buffer_after_save)
    obs.timer_add(wait_for_buffer_stop_and_restart, 50)



# Retry logic
restart_attempts = 0
MAX_RESTART_ATTEMPTS = 10

def restart_replay_buffer():
    global restart_attempts
    print("Restart buffer")
    obs.obs_frontend_replay_buffer_start()
    if obs.obs_frontend_replay_buffer_active():
        print("Replay buffer restarted successfully")
        obs.timer_remove(wait_for_buffer_stop_and_restart)
        restart_attempts = 0
    else:
        restart_attempts += 1
        if restart_attempts < MAX_RESTART_ATTEMPTS:
            obs.timer_add(wait_for_buffer_stop_and_restart, 200)
        else:
            print("Failed to restart replay buffer after multiple attempts.")
            obs.timer_remove(wait_for_buffer_stop_and_restart)
            restart_attempts = 0


# Wait for the replay buffer to stop before restarting
def wait_for_buffer_stop_and_restart():
    if not obs.obs_frontend_replay_buffer_active():
        restart_replay_buffer()


def script_load(settings):
    global hotkey_id

    hotkey_id = obs.obs_hotkey_register_frontend(
        "SmartReplay.Save", 
        "Smart Save Replay",
        on_smart_save_pressed
    )
    # Load bind data if available
    hotkey_array = obs.obs_data_get_array(settings, "smart_save_hotkey")
    obs.obs_hotkey_load(hotkey_id, hotkey_array)
    obs.obs_data_array_release(hotkey_array)
    print("Bind registered")



def script_save(settings):
    # Save bind 
    if hotkey_id != obs.OBS_INVALID_HOTKEY_ID:
        hotkey_array = obs.obs_hotkey_save(hotkey_id)
        obs.obs_data_set_array(settings, "smart_save_hotkey", hotkey_array)
        obs.obs_data_array_release(hotkey_array)

def script_unload():
    if hotkey_id != obs.OBS_INVALID_HOTKEY_ID:
        obs.obs_hotkey_unregister(hotkey_id)
    print("Bind unregistered")