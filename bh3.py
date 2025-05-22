# coding=utf-8
import baseFunctions as bf
import cv2
import time
import numpy as np
from PIL import ImageGrab as ig

# Global Image Definitions
IMG_01_START = cv2.imread("bh3/01.png", cv2.IMREAD_GRAYSCALE)
IMG_02_MUMU = cv2.imread("bh3/02.png", cv2.IMREAD_GRAYSCALE)
IMG_03_BENG = cv2.imread("bh3/03.png", cv2.IMREAD_GRAYSCALE)
IMG_04_LOGIN = cv2.imread("bh3/04.png", cv2.IMREAD_GRAYSCALE)
IMG_05_BASE_MENU_BUTTON = cv2.imread("bh3/05.png", cv2.IMREAD_GRAYSCALE)
IMG_06_COIN_ICON = cv2.imread("bh3/06.png", cv2.IMREAD_GRAYSCALE)
IMG_07_CONFIRM_COINS = cv2.imread("bh3/07.png", cv2.IMREAD_GRAYSCALE)
IMG_08_BACK_BUTTON = cv2.imread("bh3/08.png", cv2.IMREAD_GRAYSCALE)
IMG_09_MESSAGE = cv2.imread("bh3/09.png", cv2.IMREAD_GRAYSCALE)
IMG_10_GOTO_BUTTON = cv2.imread("bh3/10.png", cv2.IMREAD_GRAYSCALE)
IMG_11_REFRESH_BUTTON = cv2.imread("bh3/11.png", cv2.IMREAD_GRAYSCALE)
IMG_12_ONEKEY_BUTTON = cv2.imread("bh3/12.png", cv2.IMREAD_GRAYSCALE)
IMG_13_CONFIRM_ADVENTURE = cv2.imread("bh3/13.png", cv2.IMREAD_GRAYSCALE)
IMG_14_ADVENTURE_BUTTON = cv2.imread("bh3/14.png", cv2.IMREAD_GRAYSCALE)
IMG_16_HOME_BUTTON = cv2.imread("bh3/16.png", cv2.IMREAD_GRAYSCALE)
IMG_17_DAILY_REWARD_BUTTON = cv2.imread("bh3/17.png", cv2.IMREAD_GRAYSCALE)
IMG_18_CONFIRM_DAILY = cv2.imread("bh3/18.png", cv2.IMREAD_GRAYSCALE)


def openBh3Auto():
    # Images are now global: IMG_01_START, IMG_02_MUMU, etc.

    # Get screen dimensions for ROI
    try:
        screen_width, screen_height = ig.grab().size
    except Exception as e:
        print(f"Error getting screen dimensions: {e}. Defaulting to 1920x1080.")
        screen_width, screen_height = 1920, 1080


    print("opening application...")
    # For IMG_01_START, it's likely a desktop icon, so full screen search is probably best.
    # A screen_image could be used here if desired, but often these initial clicks are less performance critical.
    # For now, let's keep it as is to focus on post-app-launch optimizations.
    start_menu = bf.findLocWithKp(IMG_01_START) 
    bf.animateMoveAndClick(bf.getCurPos(), start_menu)
    time.sleep(2) # Wait for potential UI changes

    # Screen capture after clicking start menu icon
    screen_capture_pil = ig.grab()
    # Define ROI for MuMu Player icon - assuming it appears in the central area of the screen.
    roi_mumu = (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)
    print(f"Using ROI for MuMu icon (IMG_02_MUMU): {roi_mumu}")
    mumu = bf.findLocWithKp(IMG_02_MUMU, screen_image=screen_capture_pil, roi=roi_mumu)
    if mumu[0] == 0 and mumu[1] == 0:
        print("MuMu icon not found with ROI, trying full screen.")
        mumu = bf.findLocWithKp(IMG_02_MUMU, screen_image=screen_capture_pil) # Fallback to full screen

    if mumu[0] == 0 and mumu[1] == 0:
        print("MuMu icon not found even with full screen search. Exiting.")
        exit()
        
    bf.animateMoveAndClick(bf.getCurPos(), mumu)
    
    counter = 0
    # ROI for bengbengbeng (game loading screen) - likely central
    roi_beng = (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)
    print(f"Using ROI for game loading (IMG_03_BENG): {roi_beng}")
    while True:
        screen_capture_pil = ig.grab() # Capture fresh screen for each attempt in loop
        print("waiting for game to load (IMG_03_BENG)...")
        counter += 1
        # Pass screen_capture_pil directly, findLocWithKp will handle conversion
        bengbengbeng = bf.findLocWithKp(IMG_03_BENG, screen_image=screen_capture_pil, roi=roi_beng)
        if bengbengbeng[0] != 0 and bengbengbeng[1] != 0:
            print("Game loading image found.")
            break
        if counter > 15: # Timeout after 15 attempts (approx 15 seconds)
            print("Timeout waiting for game loading image.")
            exit()
        time.sleep(1) # Reduced sleep time
    print("opening game...")

    bf.animateMoveAndClick(bf.getCurPos(), bengbengbeng)
    
    counter = 0
    # ROI for login button - often central on the login screen
    roi_login = (screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 2) # Central area, slightly taller
    print(f"Using ROI for login screen (IMG_04_LOGIN): {roi_login}")
    while True:
        screen_capture_pil = ig.grab() # Capture fresh screen
        print("waiting for login screen (IMG_04_LOGIN)...")
        # login = bf.findLocWithKp(IMG_04_LOGIN) # Original
        login = bf.findLocWithKp(IMG_04_LOGIN, screen_image=screen_capture_pil, roi=roi_login)
        if login[0] != 0 and login[1] != 0:
            print("Login image found.")
            break
        if counter > 15: # Timeout
            print("Timeout waiting for login image.")
            exit()
        time.sleep(1) # Reduced sleep time
    # Click a bit to the right of the found login image center
    bf.animateMoveAndClick(bf.getCurPos(), (login[0] + 300, login[1])) 
    time.sleep(8) # Wait for game to load to main interface

    # After login, game interface loads, capture a new screen
    screen_after_login_pil = ig.grab()

    # ROI for message box - typically modal, often central
    roi_message = (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)
    print(f"Using ROI for message box (IMG_09_MESSAGE): {roi_message}")
    message_box = bf.findLocWithKp(IMG_09_MESSAGE, screen_image=screen_after_login_pil, roi=roi_message)
    if message_box[0] != 0 and message_box[1] != 0:
        print("Message box found, clicking.")
        bf.animateMoveAndClick(bf.getCurPos(), message_box)
        time.sleep(2) # Wait for message box to close or animate
        screen_after_login_pil = ig.grab() # Re-capture screen as message box might overlay daily
    else:
        print("Message box not found or already dismissed.")


    # ROI for daily login reward button - location can vary, assuming bottom-right quadrant for now
    # This is a guess and might need adjustment based on actual UI
    roi_daily = (screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2)
    print(f"Using ROI for daily reward (IMG_17_DAILY_REWARD_BUTTON): {roi_daily}")
    daily = bf.findLocWithKp(IMG_17_DAILY_REWARD_BUTTON, screen_image=screen_after_login_pil, roi=roi_daily)
    if daily[0] != 0 and daily[1] != 0:
        print("Daily reward button found, clicking.")
        bf.animateMoveAndClick(bf.getCurPos(), daily)
        time.sleep(1) # Wait for confirm dialog
        
        screen_after_daily_click_pil = ig.grab() # Capture screen for confirm button
        # ROI for confirm button - usually central to a dialog
        roi_confirm = (screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 3)
        print(f"Using ROI for confirm button (IMG_18_CONFIRM_DAILY): {roi_confirm}")
        confirm_loc = bf.findLocWithKp(IMG_18_CONFIRM_DAILY, screen_image=screen_after_daily_click_pil, roi=roi_confirm) # Renamed confirm to confirm_loc
        if confirm_loc[0] != 0 and confirm_loc[1] != 0: # Use confirm_loc
            print("Confirm button found, clicking.")
            bf.animateMoveAndClick(bf.getCurPos(), confirm_loc) # Use confirm_loc
        else:
            print("Confirm button not found after clicking daily.")
    else:
        print("Daily reward button not found.")
    time.sleep(8) # Final wait


def collectCoinsAuto():
    # Images are now global: IMG_05_BASE_MENU_BUTTON, IMG_06_COIN_ICON, etc.

    # Get screen dimensions for ROI
    try:
        screen_width, screen_height = ig.grab().size
    except Exception as e:
        print(f"Error getting screen dimensions: {e}. Defaulting to 1920x1080.")
        screen_width, screen_height = 1920, 1080

    counter = 0
    # Assuming IMG_05_BASE_MENU_BUTTON is on the main game screen, often a button on a persistent menu.
    # Let's define a wide ROI for the bottom half of the screen where menus often are.
    roi_base = (0, screen_height // 2, screen_width, screen_height // 2) 
    print(f"Using ROI for base button (IMG_05_BASE_MENU_BUTTON): {roi_base}")

    # Capture screen once before the loop assuming the screen state is stable until IMG_05_BASE_MENU_BUTTON appears or is found.
    screen_capture_pil_initial = ig.grab()
    screen_capture_cv_initial = cv2.cvtColor(np.asarray(screen_capture_pil_initial), cv2.COLOR_RGB2GRAY)

    while True:
        print("waiting for base button (IMG_05_BASE_MENU_BUTTON)...")
        counter += 1
        # Use the initially captured and converted screen for searching IMG_05_BASE_MENU_BUTTON.
        base = bf.findLocWithKp(IMG_05_BASE_MENU_BUTTON, screen_image=screen_capture_cv_initial, roi=roi_base)
        if base[0] != 0 and base[1] != 0:
            print("Base button found.")
            break
        if counter > 15: # Timeout after 15 attempts (approx 15 seconds)
            print("Timeout waiting for base button.")
            # Try one last time with full screen without ROI if not found
            print("Retrying base button search on full screen...")
            base = bf.findLocWithKp(IMG_05_BASE_MENU_BUTTON, screen_image=screen_capture_cv_initial) # Use converted
            if base[0] != 0 and base[1] != 0:
                print("Base button found on full screen attempt.")
                break
            else:
                print("Base button not found even on full screen. Exiting collectCoinsAuto.")
                return # Exit the function if base is not found
        time.sleep(1) # Reduced sleep time

    bf.animateMoveAndClick(bf.getCurPos(), base)
    time.sleep(2) # Wait for UI to react after clicking base

    # After clicking base, new UI elements appear. Capture fresh screen for coins.
    screen_after_base_pil = ig.grab()
    screen_after_base_cv = cv2.cvtColor(np.asarray(screen_after_base_pil), cv2.COLOR_RGB2GRAY)
    # IMG_06_COIN_ICON is likely within a specific area of the new screen. Assume top-left or general menu area.
    # For example, a quarter of the screen from top-left.
    roi_coin = (0, 0, screen_width // 2, screen_height // 2) 
    print(f"Using ROI for coins (IMG_06_COIN_ICON): {roi_coin}")
    coins = bf.findLocWithKp(IMG_06_COIN_ICON, screen_image=screen_after_base_cv, roi=roi_coin)
    if coins[0] == 0 and coins[1] == 0:
        print("Coins not found with ROI, trying full screen.")
        coins = bf.findLocWithKp(IMG_06_COIN_ICON, screen_image=screen_after_base_cv)

    if coins[0] != 0 and coins[1] != 0:
        print("Coins found, clicking.")
        bf.animateMoveAndClick(bf.getCurPos(), coins)
        time.sleep(2) # Wait for confirm dialog to appear

        # After clicking coins, a confirmation dialog is expected. Capture fresh screen.
        screen_after_coin_pil = ig.grab()
        screen_after_coin_cv = cv2.cvtColor(np.asarray(screen_after_coin_pil), cv2.COLOR_RGB2GRAY)
        # Confirm buttons are often central.
        roi_confirm_coins = (screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 3)
        print(f"Using ROI for confirm button (IMG_07_CONFIRM_COINS): {roi_confirm_coins}")
        confirm_loc = bf.findLocWithKp(IMG_07_CONFIRM_COINS, screen_image=screen_after_coin_cv, roi=roi_confirm_coins)
        if confirm_loc[0] == 0 and confirm_loc[1] == 0:
            print("Confirm button not found with ROI, trying full screen.")
            confirm_loc = bf.findLocWithKp(IMG_07_CONFIRM_COINS, screen_image=screen_after_coin_cv)

        if confirm_loc[0] != 0 and confirm_loc[1] != 0:
            print("Confirm button found, clicking.")
            bf.animateMoveAndClick(bf.getCurPos(), confirm_loc)
            time.sleep(2) # Wait for confirm action
        else:
            print("Confirm button not found after clicking coins.")
            # Decide if to proceed or return, for now, let's assume we might still want to go back.
    else:
        print("Coins not found.")
        # If coins are not found, we probably can't confirm, but might still want to go back.

    # After confirm (or if coins/confirm not found), try to go back. Capture fresh screen.
    screen_after_confirm_pil = ig.grab()
    screen_after_confirm_cv = cv2.cvtColor(np.asarray(screen_after_confirm_pil), cv2.COLOR_RGB2GRAY)
    # Back buttons are often top-left or top-right. Let's try a broad top area.
    roi_back_coins = (0, 0, screen_width, screen_height // 4)
    print(f"Using ROI for back button (IMG_08_BACK_BUTTON): {roi_back_coins}")
    back_loc = bf.findLocWithKp(IMG_08_BACK_BUTTON, screen_image=screen_after_confirm_cv, roi=roi_back_coins)
    if back_loc[0] == 0 and back_loc[1] == 0:
        print("Back button not found with ROI, trying full screen.")
        back_loc = bf.findLocWithKp(IMG_08_BACK_BUTTON, screen_image=screen_after_confirm_cv)

    if back_loc[0] != 0 and back_loc[1] != 0:
        print("Back button found, clicking.")
        bf.animateMoveAndClick(bf.getCurPos(), back_loc)
        time.sleep(2) # Wait for back action
    else:
        print("Back button not found.")


def adventureAuto():
    # Images are now global: IMG_05_BASE_MENU_BUTTON, IMG_14_ADVENTURE_BUTTON, etc.

    # Get screen dimensions for ROI
    try:
        screen_width, screen_height = ig.grab().size
    except Exception as e:
        print(f"Error getting screen dimensions: {e}. Defaulting to 1920x1080.")
        screen_width, screen_height = 1920, 1080

    # Initial screen state (assuming this function is called from main game screen)
    screen_before_base_pil = ig.grab()
    screen_before_base_cv = cv2.cvtColor(np.asarray(screen_before_base_pil), cv2.COLOR_RGB2GRAY)
    
    # Define ROI for base button on main screen (similar to collectCoinsAuto)
    roi_base_adv = (0, screen_height // 2, screen_width, screen_height // 2) 
    print(f"Using ROI for base button (IMG_05_BASE_MENU_BUTTON): {roi_base_adv}")
    base = bf.findLocWithKp(IMG_05_BASE_MENU_BUTTON, screen_image=screen_before_base_cv, roi=roi_base_adv)
    if base[0] == 0 and base[1] == 0:
        print("Base button (adventure) not found with ROI, trying full screen.")
        base = bf.findLocWithKp(IMG_05_BASE_MENU_BUTTON, screen_image=screen_before_base_cv)
    
    if base[0] == 0 and base[1] == 0:
        print("Base button (adventure) not found. Exiting adventureAuto.")
        return
    bf.animateMoveAndClick(bf.getCurPos(), base)
    time.sleep(2) # Wait for UI to change to base screen

    # Screen after clicking base button
    screen_after_base_pil = ig.grab()
    screen_after_base_cv = cv2.cvtColor(np.asarray(screen_after_base_pil), cv2.COLOR_RGB2GRAY)
    
    # Define ROI for adventure button on base screen (e.g., central part of the screen)
    roi_adventure = (screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)
    print(f"Using ROI for adventure button (IMG_14_ADVENTURE_BUTTON): {roi_adventure}")
    venture = bf.findLocWithKp(IMG_14_ADVENTURE_BUTTON, screen_image=screen_after_base_cv, roi=roi_adventure, numKps=5000) # Keep numKps=5000
    if venture[0] == 0 and venture[1] == 0:
        print("Adventure button not found with ROI, trying full screen.")
        venture = bf.findLocWithKp(IMG_14_ADVENTURE_BUTTON, screen_image=screen_after_base_cv, numKps=5000)

    if venture[0] == 0 and venture[1] == 0:
        print("Adventure button not found. Exiting adventureAuto.")
        return
    bf.animateMoveAndClick(bf.getCurPos(), venture)
    time.sleep(2) # Wait for adventure screen to load

    # Screen after clicking adventure button (this is the screen with task list)
    screen_after_adventure_pil = ig.grab()
    screen_after_adventure_cv = cv2.cvtColor(np.asarray(screen_after_adventure_pil), cv2.COLOR_RGB2GRAY)

    # Define ROIs for back and refresh buttons on adventure screen (e.g., top corners)
    roi_back_adv = (0, 0, screen_width // 4, screen_height // 4) # Top-left quarter
    roi_refresh_adv = (screen_width * 3 // 4, 0, screen_width // 4, screen_height // 4) # Top-right quarter

    print(f"Using ROI for back button (IMG_08_BACK_BUTTON): {roi_back_adv}")
    loc1 = bf.findLocWithKp(IMG_08_BACK_BUTTON, screen_image=screen_after_adventure_cv, roi=roi_back_adv)
    if loc1[0] == 0 and loc1[1] == 0: loc1 = bf.findLocWithKp(IMG_08_BACK_BUTTON, screen_image=screen_after_adventure_cv) # Fallback

    print(f"Using ROI for refresh button (IMG_11_REFRESH_BUTTON): {roi_refresh_adv}")
    loc2 = bf.findLocWithKp(IMG_11_REFRESH_BUTTON, screen_image=screen_after_adventure_cv, roi=roi_refresh_adv)
    if loc2[0] == 0 and loc2[1] == 0: loc2 = bf.findLocWithKp(IMG_11_REFRESH_BUTTON, screen_image=screen_after_adventure_cv) # Fallback

    if loc1[0] == 0 or loc2[0] == 0: # Check if critical elements for y-range are found
        print("Could not find back or refresh buttons for adventure task y-range. Exiting.")
        return

    y_start = loc1[1]
    y_end = loc2[1]
    print(f"y_start (back button y): {y_start}, y_end (refresh button y): {y_end}")
    if y_end <= y_start: # Sanity check
        print("Refresh button y is not below back button y. Cannot calculate y_range. Exiting.")
        return
    y_range = y_end - y_start

    task1_y_start = int(y_start + 0.194 * y_range)
    task1_y_end = int(y_start + (0.194 + 0.225) * y_range)
    task2_y_start = int(y_start + 0.434 * y_range)
    task3_y_start = int(y_start + 0.673 * y_range)

    # task1_img is a slice of screen_after_adventure_cv
    task1_img_roi = screen_after_adventure_cv[task1_y_start:task1_y_end, :] 
    
    # Using siftFlannMatch with its default numKps (2000 for img1, 1500 for img2)
    # Or we can specify, e.g. numKps=3000 to align with findLocWithKp's default
    print("Attempting to match IMG_10_GOTO_BUTTON within task1_img_roi using siftFlannMatch.")
    _, kp_task1 = bf.siftFlannMatch(IMG_10_GOTO_BUTTON, task1_img_roi) # Using default numKps for siftFlannMatch
    
    if not kp_task1: # Check if kp_task1 is empty
        print("No keypoints found for IMG_10_GOTO_BUTTON in the first task area. Exiting.")
        return

    mean_x_task = sum(pt[0] for pt in kp_task1) / len(kp_task1)
    mean_y_task = sum(pt[1] for pt in kp_task1) / len(kp_task1)

    # Targets are relative to the full screen, but mean_y_task is relative to task1_img_roi
    target1 = (int(mean_x_task), int(task1_y_start + mean_y_task))
    # For target2 and target3, x-coordinate is assumed to be the same as target1
    # The y-coordinates for task2_img and task3_img would be task2_y_start + mean_y_task_from_its_own_roi etc.
    # The original code reuses mean_y_task from task1 for all targets, which might be an oversimplification
    # if the "goto" button shifts vertically within each task item.
    # For now, replicating original logic for target calculation.
    # A more robust way would be to match img_goto for each task slice.
    target2 = (int(mean_x_task), int(task2_y_start + mean_y_task)) # Replicates original logic
    target3 = (int(mean_x_task), int(task3_y_start + mean_y_task)) # Replicates original logic

    # ROIs for onekey, confirm, home - assuming they appear in predictable locations after clicks
    roi_onekey_adv = (screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 3) # Central dialog
    roi_confirm_adv = (screen_width // 3, screen_height // 3, screen_width // 3, screen_height // 3) # Central dialog
    roi_home_adv = (0, 0, screen_width // 4, screen_height // 5) # Top-left for home button

    # Process Task 1
    print(f"Clicking target1: {target1}")
    bf.animateMoveAndClick(bf.getCurPos(), target1)
    time.sleep(2)
    screen_after_target1_pil = ig.grab()
    screen_after_target1_cv = cv2.cvtColor(np.asarray(screen_after_target1_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for onekey (IMG_12_ONEKEY_BUTTON): {roi_onekey_adv}")
    onekey_loc = bf.findLocWithKp(IMG_12_ONEKEY_BUTTON, screen_image=screen_after_target1_cv, roi=roi_onekey_adv)
    if onekey_loc[0] == 0 and onekey_loc[1] == 0: onekey_loc = bf.findLocWithKp(IMG_12_ONEKEY_BUTTON, screen_image=screen_after_target1_cv) # Fallback
    if onekey_loc[0] == 0 and onekey_loc[1] == 0: print("Onekey button not found for task 1."); return
    bf.animateMoveAndClick(bf.getCurPos(), onekey_loc)
    time.sleep(2)
    screen_after_onekey1_pil = ig.grab()
    screen_after_onekey1_cv = cv2.cvtColor(np.asarray(screen_after_onekey1_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for confirm (IMG_13_CONFIRM_ADVENTURE): {roi_confirm_adv}")
    confirm_loc = bf.findLocWithKp(IMG_13_CONFIRM_ADVENTURE, screen_image=screen_after_onekey1_cv, roi=roi_confirm_adv)
    if confirm_loc[0] == 0 and confirm_loc[1] == 0: confirm_loc = bf.findLocWithKp(IMG_13_CONFIRM_ADVENTURE, screen_image=screen_after_onekey1_cv) # Fallback
    if confirm_loc[0] == 0 and confirm_loc[1] == 0: print("Confirm button not found for task 1."); return
    bf.animateMoveAndClick(bf.getCurPos(), confirm_loc)
    time.sleep(2)

    # Process Task 2
    print(f"Clicking target2: {target2}")
    bf.animateMoveAndClick(bf.getCurPos(), target2) # Assumes target2 is clickable from current screen
    time.sleep(2)
    screen_after_target2_pil = ig.grab()
    screen_after_target2_cv = cv2.cvtColor(np.asarray(screen_after_target2_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for onekey (IMG_12_ONEKEY_BUTTON): {roi_onekey_adv}")
    onekey_loc = bf.findLocWithKp(IMG_12_ONEKEY_BUTTON, screen_image=screen_after_target2_cv, roi=roi_onekey_adv)
    if onekey_loc[0] == 0 and onekey_loc[1] == 0: onekey_loc = bf.findLocWithKp(IMG_12_ONEKEY_BUTTON, screen_image=screen_after_target2_cv) # Fallback
    if onekey_loc[0] == 0 and onekey_loc[1] == 0: print("Onekey button not found for task 2."); return
    bf.animateMoveAndClick(bf.getCurPos(), onekey_loc)
    time.sleep(2)
    screen_after_onekey2_pil = ig.grab()
    screen_after_onekey2_cv = cv2.cvtColor(np.asarray(screen_after_onekey2_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for confirm (IMG_13_CONFIRM_ADVENTURE): {roi_confirm_adv}")
    confirm_loc = bf.findLocWithKp(IMG_13_CONFIRM_ADVENTURE, screen_image=screen_after_onekey2_cv, roi=roi_confirm_adv)
    if confirm_loc[0] == 0 and confirm_loc[1] == 0: confirm_loc = bf.findLocWithKp(IMG_13_CONFIRM_ADVENTURE, screen_image=screen_after_onekey2_cv) # Fallback
    if confirm_loc[0] == 0 and confirm_loc[1] == 0: print("Confirm button not found for task 2."); return
    bf.animateMoveAndClick(bf.getCurPos(), confirm_loc)
    time.sleep(2)

    # Process Task 3
    print(f"Clicking target3: {target3}")
    bf.animateMoveAndClick(bf.getCurPos(), target3) # Assumes target3 is clickable
    time.sleep(2)
    screen_after_target3_pil = ig.grab()
    screen_after_target3_cv = cv2.cvtColor(np.asarray(screen_after_target3_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for onekey (IMG_12_ONEKEY_BUTTON): {roi_onekey_adv}")
    onekey_loc = bf.findLocWithKp(IMG_12_ONEKEY_BUTTON, screen_image=screen_after_target3_cv, roi=roi_onekey_adv)
    if onekey_loc[0] == 0 and onekey_loc[1] == 0: onekey_loc = bf.findLocWithKp(IMG_12_ONEKEY_BUTTON, screen_image=screen_after_target3_cv) # Fallback
    if onekey_loc[0] == 0 and onekey_loc[1] == 0: print("Onekey button not found for task 3."); return
    bf.animateMoveAndClick(bf.getCurPos(), onekey_loc)
    time.sleep(2)
    screen_after_onekey3_pil = ig.grab()
    screen_after_onekey3_cv = cv2.cvtColor(np.asarray(screen_after_onekey3_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for confirm (IMG_13_CONFIRM_ADVENTURE): {roi_confirm_adv}")
    confirm_loc = bf.findLocWithKp(IMG_13_CONFIRM_ADVENTURE, screen_image=screen_after_onekey3_cv, roi=roi_confirm_adv)
    if confirm_loc[0] == 0 and confirm_loc[1] == 0: confirm_loc = bf.findLocWithKp(IMG_13_CONFIRM_ADVENTURE, screen_image=screen_after_onekey3_cv) # Fallback
    if confirm_loc[0] == 0 and confirm_loc[1] == 0: print("Confirm button not found for task 3."); return
    bf.animateMoveAndClick(bf.getCurPos(), confirm_loc)
    time.sleep(2)

    # After all tasks, find home button
    screen_after_all_tasks_pil = ig.grab()
    screen_after_all_tasks_cv = cv2.cvtColor(np.asarray(screen_after_all_tasks_pil), cv2.COLOR_RGB2GRAY)
    print(f"Using ROI for home button (IMG_16_HOME_BUTTON): {roi_home_adv}")
    home_loc = bf.findLocWithKp(IMG_16_HOME_BUTTON, screen_image=screen_after_all_tasks_cv, roi=roi_home_adv)
    if home_loc[0] == 0 and home_loc[1] == 0: home_loc = bf.findLocWithKp(IMG_16_HOME_BUTTON, screen_image=screen_after_all_tasks_cv) # Fallback
    if home_loc[0] == 0 and home_loc[1] == 0: print("Home button not found after tasks."); return
    bf.animateMoveAndClick(bf.getCurPos(), home_loc)
    time.sleep(2)


if __name__ == '__main__':
    import time # Make sure time is imported

    # It's good practice to ensure the game/emulator is ready before starting.
    # Consider adding a small initial delay or a prompt for the user.
    print("Script starting in 5 seconds... Please ensure the game environment is ready.")
    time.sleep(5) 

    overall_start_time = time.time()

    print("Starting openBh3Auto...")
    start_time_open = time.time()
    openBh3Auto()
    end_time_open = time.time()
    duration_open = end_time_open - start_time_open
    print(f"openBh3Auto took: {duration_open:.2f} seconds")

    print("\nStarting collectCoinsAuto...")
    start_time_collect = time.time()
    collectCoinsAuto()
    end_time_collect = time.time()
    duration_collect = end_time_collect - start_time_collect
    print(f"collectCoinsAuto took: {duration_collect:.2f} seconds")

    print("\nStarting adventureAuto...")
    start_time_adventure = time.time()
    adventureAuto()
    end_time_adventure = time.time()
    duration_adventure = end_time_adventure - start_time_adventure
    print(f"adventureAuto took: {duration_adventure:.2f} seconds")

    overall_end_time = time.time()
    total_duration = overall_end_time - overall_start_time
    # This total_duration includes the time.sleep(5) at the beginning if calculated from overall_start_time.
    # A more accurate sum of individual functions is:
    # total_function_time = duration_open + duration_collect + duration_adventure
    # print(f"Total function execution time: {total_function_time:.2f} seconds")
    print(f"Total script execution time (including initial delay): {total_duration:.2f} seconds")
