from .menu_reset import reset_menu
import pygame as pg

def settings_update(back_to_game_state, menu_ui_settings, menu_ui, menu_ui_save, menu_ui_load, menu_ui_inventory, menu_ui_skills, menu_ui_achievement, new_size, display, dt, current_time, platform, key, mobile_key, input, pygame_event):
    new_sound_volume = menu_ui_settings.sound_slider.save_value/100
    menu_ui.select_sfx.set_volume(new_sound_volume)
    menu_ui.open_menu_sfx.set_volume(new_sound_volume)
    menu_ui_save.select_sfx.set_volume(new_sound_volume)
    menu_ui_load.select_sfx.set_volume(new_sound_volume)
    menu_ui_inventory.select_sfx.set_volume(new_sound_volume)
    menu_ui_skills.select_sfx.set_volume(new_sound_volume)
    menu_ui_achievement.select_sfx.set_volume(new_sound_volume)
    new_music_volume = menu_ui_settings.music_slider.save_value/100
    pg.mixer.music.set_volume(new_music_volume)
    select_submenu = False
    if new_size:
        reset_menu(menu_ui_settings, display, cursor = menu_ui_settings.cursor)
    slide_in = menu_ui_settings.draw(display, dt, current_time)
    if not slide_in:
        match platform:
            case 'pc':
                select_submenu = menu_ui_settings.update_for_pc(key, input.joysticks, dt, current_time, input)
            case 'android':
                select_submenu = menu_ui_settings.update_for_android(mobile_key, [], dt, current_time, input)
            case 'web':
                select_submenu = menu_ui_settings.update_for_pc(key, input.joysticks, dt, current_time, input)
    if select_submenu:
        match select_submenu:
            case 'Back':
                reset_menu(menu_ui_settings, display)
                reset_menu(menu_ui, display, 5)
                pygame_event.game_state = back_to_game_state
