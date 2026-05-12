import time
import os
import logging
from xarm.wrapper import XArmAPI
from pynput import keyboard

logging.getLogger('xarm').setLevel(logging.ERROR)

# ── Verbindung ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

arm = XArmAPI('192.168.1.200')
arm.connect()
arm.clean_error()
arm.clean_warn()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

arm.set_gripper_enable(True)
arm.set_gripper_mode(0)
arm.set_gripper_position(850, wait=True)

arm.set_linear_track_enable(True)
arm.set_linear_track_speed(200)

# ── Globale Variablen ───────────────────────────────────────
txtfile             = ""
space_held          = False
active_key          = None
gripper_position    = 850
track_position      = 0
movestack           = []
saved_points        = []
current_saved_index = -1

GRIPPER_MIN = 0
GRIPPER_MAX = 850
TRACK_MIN   = 0
TRACK_MAX   = 1000

controls = {
    "stepsize":      5,
    "step_angle":    1,
    "gripper_step":  25,
    "track_step":    10,
    "x": 0,
    "y": 2,
    "z": 1,
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
}

# ── Hilfsfunktionen ─────────────────────────────────────────

def get_current_track_pos():
    code, pos = arm.get_linear_track_pos()
    if code == 0:
        return int(pos)
    return track_position

def save_point(point_type: str) -> None:
    global current_saved_index

    _, position   = arm.get_position()
    _, angles     = arm.get_servo_angle()
    current_track = get_current_track_pos()
    movestack.clear()

    # Automatisch nummerieren
    point_name = f"point_{len(saved_points) + 1}"

    with open(txtfile, "a") as f:
        f.write(f"{point_name} cartesian: {position}\n")
        f.write(f"{point_name} angular: {angles}\n")
        f.write(f"Gripper: {gripper_position}\n")
        f.write(f"Track: {current_track}\n")
        f.write(f"Type: {point_type}\n")
        f.write(f"\n")

    saved_points.append({
        "name":     point_name,
        "angles":   angles,
        "position": position,
        "gripper":  gripper_position,
        "track":    current_track
    })
    current_saved_index = len(saved_points) - 1

    print(f"✓ '{point_name}' saved ({point_type.upper()}) | "
          f"pos: {[round(p,1) for p in position]} | "
          f"track: {current_track}mm | gripper: {gripper_position}")

def go_to_saved_point(index):
    """Moves robot to a saved point by index."""
    target = saved_points[index]
    print(f"Going to: '{target['name']}' "
          f"({index + 1}/{len(saved_points)})")
    arm.set_linear_track_pos(target["track"], wait=True)
    arm.set_servo_angle(angle=target["angles"], speed=20,
                        mvacc=50, wait=True)
    arm.set_gripper_position(target["gripper"], wait=False)
    print(f"✓ At point '{target['name']}'")

def reversal() -> None:
    if not movestack:
        print("Nothing to reverse!")
        return
    print(f"Reversing {len(movestack)} moves...")
    while movestack:
        target_angles = movestack.pop()
        arm.set_servo_angle(angle=target_angles, speed=10,
                            mvacc=50, wait=True)
    print("Reversal complete")

def print_current_position() -> None:
    _, position   = arm.get_position()
    _, angles     = arm.get_servo_angle()
    current_track = get_current_track_pos()
    print(f"\nCartesian: {[round(p,1) for p in position]}")
    print(f"Angular:   {[round(a,1) for a in angles]}")
    print(f"Gripper:   {gripper_position}")
    print(f"Track:     {current_track}mm")
    print(f"Stepsize:  {controls['stepsize']}mm | "
          f"Track step: {controls['track_step']}mm | "
          f"Gripper step: {controls['gripper_step']}")
    if saved_points:
        print(f"Saved points: {len(saved_points)} | "
              f"Current: {current_saved_index + 1}")

# ── Tastatur Callbacks ───────────────────────────────────────

def on_press(key):
    global space_held, active_key, gripper_position, track_position
    global current_saved_index

    if key == active_key:
        return
    active_key = key

    if key == keyboard.Key.space:
        space_held = True
        return

    elif key == keyboard.Key.esc:
        print("\nEMERGENCY STOP!")
        arm.set_state(4)
        arm.disconnect()
        return False

    try:
        code,   current_pos    = arm.get_position()
        code_2, current_angles = arm.get_servo_angle()

        if code != 0 or code_2 != 0:
            print("ERROR DETECTED – stopping!")
            arm.set_state(4)
            arm.disconnect()
            return False

        # ── Kartesische Bewegung ─────────────────────────────
        if key.char in "xyz":
            if space_held:
                current_pos[controls[key.char]] -= controls["stepsize"]
            else:
                current_pos[controls[key.char]] += controls["stepsize"]
            arm.set_position(*current_pos, speed=20, wait=False)

        # ── Gelenke ──────────────────────────────────────────
        elif key.char in "123456":
            if space_held:
                current_angles[controls[key.char]] -= controls["step_angle"]
            else:
                current_angles[controls[key.char]] += controls["step_angle"]
            arm.set_servo_angle(
                int(key.char),
                current_angles[controls[key.char]],
                speed=5, wait=False
            )

        # ── Schiene ──────────────────────────────────────────
        elif key.char == "t":
            track_position = get_current_track_pos()
            if space_held:
                track_position = max(
                    TRACK_MIN,
                    track_position - controls["track_step"]
                )
            else:
                track_position = min(
                    TRACK_MAX,
                    track_position + controls["track_step"]
                )
            arm.set_linear_track_pos(track_position, wait=True)
            print(f"Track: {track_position}mm")

        # ── Punkte speichern ─────────────────────────────────
        elif key.char == "l":
            save_point("linear")

        elif key.char == "j":
            save_point("angular")

        # ── Reversal ─────────────────────────────────────────
        elif key.char == "r":
            reversal()

        # ── Position anzeigen ────────────────────────────────
        elif key.char == "p":
            print_current_position()

        # ── Navigation zwischen gespeicherten Punkten ────────
        elif key.char == "b":
            if not saved_points:
                print("No saved points yet!")
            elif current_saved_index <= 0:
                print("Already at first saved point!")
            else:
                current_saved_index -= 1
                go_to_saved_point(current_saved_index)

        elif key.char == "n":
            if not saved_points:
                print("No saved points yet!")
            elif current_saved_index >= len(saved_points) - 1:
                print("Already at last saved point!")
            else:
                current_saved_index += 1
                go_to_saved_point(current_saved_index)

        # ── Greifer ──────────────────────────────────────────
        elif key.char == "g":
            if space_held:
                gripper_position = min(
                    gripper_position + controls["gripper_step"],
                    GRIPPER_MAX
                )
            else:
                gripper_position = max(
                    gripper_position - controls["gripper_step"],
                    GRIPPER_MIN
                )
            arm.set_gripper_position(gripper_position, wait=False)
            print(f"Gripper: {gripper_position}")

        elif key.char == "h":
            gripper_position = GRIPPER_MAX
            arm.set_gripper_position(gripper_position, wait=False)
            print(f"Gripper: FULL OPEN ({GRIPPER_MAX})")

        elif key.char == "f":
            gripper_position = GRIPPER_MIN
            arm.set_gripper_position(gripper_position, wait=False)
            print(f"Gripper: FULL CLOSED ({GRIPPER_MIN})")

        # ── Schrittgröße ─────────────────────────────────────
        elif key.char == "+":
            if space_held:
                controls["track_step"] = min(
                    controls["track_step"] * 2, 100)
                print(f"Track step: {controls['track_step']}mm")
            else:
                controls["stepsize"] = min(
                    controls["stepsize"] * 2, 100)
                print(f"Stepsize: {controls['stepsize']}mm")

        elif key.char == "-":
            if space_held:
                controls["track_step"] = max(
                    controls["track_step"] / 2, 1)
                print(f"Track step: {controls['track_step']}mm")
            else:
                controls["stepsize"] = max(
                    controls["stepsize"] / 2, 0.5)
                print(f"Stepsize: {controls['stepsize']}mm")

    except AttributeError:
        pass

def on_release(key):
    global space_held, active_key

    if key == keyboard.Key.space:
        space_held = False
        return
    try:
        if key.char in "xyz123456":
            active_key = None
            arm.set_state(4)
            arm.set_state(0)
            time.sleep(0.1)
            _, actual_angles = arm.get_servo_angle()
            movestack.append(actual_angles)

        elif key.char == "g":
            active_key = None

    except AttributeError:
        pass

# ── Main ─────────────────────────────────────────────────────

def main():
    global txtfile, controls

    print("\n=== Slurrybot Keyboard Jogger ===\n")

    positions_dir = os.path.join(BASE_DIR, "..", "Positions")
    os.makedirs(positions_dir, exist_ok=True)

    print("Enter name for this movement file")
    print("(e.g. 'pickup_vial1' → saves to Positions/pickup_vial1.txt):")
    filename = input("> ").strip()
    txtfile  = os.path.join(positions_dir, f"{filename}.txt")

    if os.path.exists(txtfile):
        print(f"\n⚠️  WARNING: '{filename}.txt' already exists!")
        print("  o = overwrite | a = append")
        choice = input("> ").strip().lower()
        if choice == "o":
            open(txtfile, "w").close()
            print("File cleared ✓")
        else:
            print("Appending to existing file ✓")
    else:
        print(f"Creating: {txtfile} ✓")

    print(f"\nStep size in mm (default {controls['stepsize']}, Enter to skip):")
    step_input = input("> ").strip()
    if step_input != "":
        try:
            controls["stepsize"] = float(step_input)
        except ValueError:
            print("Invalid – using default")

    print(f"Track step size in mm (default {controls['track_step']}, Enter to skip):")
    track_input = input("> ").strip()
    if track_input != "":
        try:
            controls["track_step"] = int(track_input)
        except ValueError:
            print("Invalid – using default")

    print(f"Gripper step size (default {controls['gripper_step']}, Enter to skip):")
    grip_input = input("> ").strip()
    if grip_input != "":
        try:
            controls["gripper_step"] = int(grip_input)
        except ValueError:
            print("Invalid – using default")

    print(f"\nSettings:")
    print(f"  File:         {txtfile}")
    print(f"  Step size:    {controls['stepsize']}mm")
    print(f"  Track step:   {controls['track_step']}mm")
    print(f"  Gripper step: {controls['gripper_step']}")

    print("""
Controls:
─────────────────────────────────────────────────
Movement:
  x / y / z           move cartesian (+)
  Space + x/y/z       move cartesian (-)
  1-6                 rotate joint (+)
  Space + 1-6         rotate joint (-)
  + / -               double/halve step size

Linear Track:
  t                   track forward (+)
  Space + t           track backward (-)
  Space + +/-         double/halve track step size

Gripper:
  g                   close gripper (one step)
  Space + g           open gripper (one step)
  f                   gripper fully closed (0)
  h                   gripper fully open (850)

Save & Navigate:
  l                   save point as LINEAR
  j                   save point as ANGULAR
  r                   revert to last saved point
  b                   go back to previous saved point
  n                   go forward to next saved point
  p                   print current position

  ESC                 emergency stop + exit
─────────────────────────────────────────────────
    """)

    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()

if __name__ == "__main__":
    main()
       
