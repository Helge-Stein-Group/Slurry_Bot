import time
import os
from xarm.wrapper import XArmAPI
from pynput import keyboard

# ── Verbindung ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

arm = XArmAPI('192.168.1.200')
arm.connect()
arm.clean_error()
arm.clean_warn()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)

# Greifer initialisieren
arm.set_gripper_enable(True)
arm.set_gripper_mode(0)
arm.set_gripper_position(850, wait=True)

# Lineare Schiene initialisieren
arm.set_linear_track_enable(True)
arm.set_linear_track_speed(200)

# ── Globale Variablen ───────────────────────────────────────
txtfile          = ""
space_held       = False
active_key       = None
gripper_position = 850
track_position   = 0
last_saved_pos   = None
movestack        = []

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
    """Reads current linear track position."""
    code, pos = arm.get_linear_track_pos()
    if code == 0:
        return int(pos)
    return track_position  # fallback if read fails

def save_point(point_type: str) -> None:
    """
    Saves current position to txt file.
    Includes cartesian, angular, gripper AND track position.
    point_type: "linear" or "angular"
    """
    global last_saved_pos

    _, position = arm.get_position()
    _, angles   = arm.get_servo_angle()
    current_track = get_current_track_pos()
    movestack.clear()

    print(f"\nCartesian:  {[round(p,1) for p in position]}")
    print(f"Gripper:    {gripper_position}")
    print(f"Track:      {current_track}mm")
    print("Enter name for this point:")
    point_name = input("> ").strip()

    if point_name == "":
        print("No name entered – point NOT saved!")
        return

    with open(txtfile, "a") as f:
        f.write(f"{point_name} cartesian: {position}\n")
        f.write(f"{point_name} angular: {angles}\n")
        f.write(f"Gripper: {gripper_position}\n")
        f.write(f"Track: {current_track}\n")
        f.write(f"Type: {point_type}\n")
        f.write(f"\n")

    last_saved_pos = position
    print(f"✓ '{point_name}' saved ({point_type.upper()}) | "
          f"track: {current_track}mm | gripper: {gripper_position}")

def save_rack_ref_to_config(position) -> None:
    """
    Saves current position as RACK reference point in config.txt.
    Updates the first 6 values of the matching RACK line.
    """
    config_path = os.path.join(BASE_DIR, "Config", "config.txt")

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        return

    print("Enter RACK name to update (e.g. VialRackFront):")
    rack_name = input("> ").strip()

    if rack_name == "":
        print("Cancelled")
        return

    with open(config_path, "r") as f:
        lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(f"RACK {rack_name}"):
            parts     = stripped.split()
            spacing_x = parts[8]
            spacing_y = parts[9]
            count     = parts[10]
            lines[i]  = (
                f"RACK {rack_name:<20} "
                f"{position[0]:<8.1f} {position[1]:<8.1f} "
                f"{position[2]:<8.1f} "
                f"{position[3]:<8.1f} {position[4]:<8.1f} "
                f"{position[5]:<8.1f} "
                f"{spacing_x} {spacing_y} {count}\n"
            )
            found = True
            print(f"✓ Updated RACK {rack_name} in config.txt")
            break

    if not found:
        print(f"RACK '{rack_name}' not found in config.txt!")
        return

    with open(config_path, "w") as f:
        f.writelines(lines)

def reversal() -> None:
    """Reverses all moves since last saved point."""
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
    """Prints current position without saving."""
    _, position     = arm.get_position()
    _, angles       = arm.get_servo_angle()
    current_track   = get_current_track_pos()
    print(f"\nCartesian: {[round(p,1) for p in position]}")
    print(f"Angular:   {[round(a,1) for a in angles]}")
    print(f"Gripper:   {gripper_position}")
    print(f"Track:     {current_track}mm")
    print(f"Stepsize:  {controls['stepsize']}mm | "
          f"Track step: {controls['track_step']}mm | "
          f"Gripper step: {controls['gripper_step']}")

# ── Tastatur Callbacks ───────────────────────────────────────

def on_press(key):
    global space_held, active_key, gripper_position, track_position

    # OS Wiederholfilter
    if key == active_key:
        return
    active_key = key

    # Leertaste = Modifier
    if key == keyboard.Key.space:
        space_held = True
        return

    # ESC = Notausgang
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

        # ── Kartesische Bewegung x/y/z ──────────────────────
        if key.char in "xyz":
            if space_held:
                current_pos[controls[key.char]] -= controls["stepsize"]
            else:
                current_pos[controls[key.char]] += controls["stepsize"]
            arm.set_position(*current_pos, speed=20, wait=False)

        # ── Einzelne Gelenke 1-6 ────────────────────────────
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

        # ── Lineare Schiene t ────────────────────────────────
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

        # ── Punkt speichern l/j ──────────────────────────────
        elif key.char == "l":
            save_point("linear")

        elif key.char == "j":
            save_point("angular")

        # ── Zurück zum letzten Punkt r ───────────────────────
        elif key.char == "r":
            reversal()

        # ── Position anzeigen p ──────────────────────────────
        elif key.char == "p":
            print_current_position()

        # ── Rack-Referenz in config.txt speichern c ──────────
        elif key.char == "c":
            _, position = arm.get_position()
            save_rack_ref_to_config(position)

        # ── Greifer g ────────────────────────────────────────
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
            arm.set_gripper_position(gripper_position, wait=True)
            print(f"Gripper: {gripper_position}")

        # ── Greifer komplett auf/zu h/f ──────────────────────
        elif key.char == "h":
            gripper_position = GRIPPER_MAX
            arm.set_gripper_position(gripper_position, wait=True)
            print(f"Gripper: FULL OPEN ({GRIPPER_MAX})")

        elif key.char == "f":
            gripper_position = GRIPPER_MIN
            arm.set_gripper_position(gripper_position, wait=True)
            print(f"Gripper: FULL CLOSED ({GRIPPER_MIN})")

        # ── Schrittgröße +/- ─────────────────────────────────
        elif key.char == "+":
            if space_held:
                # Space++ = Track-Schrittgröße erhöhen
                controls["track_step"] = min(
                    controls["track_step"] * 2, 100
                )
                print(f"Track step: {controls['track_step']}mm")
            else:
                controls["stepsize"] = min(
                    controls["stepsize"] * 2, 100
                )
                print(f"Stepsize: {controls['stepsize']}mm")

        elif key.char == "-":
            if space_held:
                # Space+- = Track-Schrittgröße verringern
                controls["track_step"] = max(
                    controls["track_step"] / 2, 1
                )
                print(f"Track step: {controls['track_step']}mm")
            else:
                controls["stepsize"] = max(
                    controls["stepsize"] / 2, 0.5
                )
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
    except AttributeError:
        pass

# ── Main ─────────────────────────────────────────────────────

def main():
    global txtfile, controls

    print("\n=== Slurrybot Keyboard Jogger ===\n")

    # Positions-Ordner erstellen
    positions_dir = os.path.join(BASE_DIR, "Positions")
    os.makedirs(positions_dir, exist_ok=True)

    # Dateiname
    print("Enter name for this movement file")
    print("(e.g. 'pickup_vial1' → saves to Positions/pickup_vial1.txt):")
    filename = input("> ").strip()
    txtfile  = os.path.join(positions_dir, f"{filename}.txt")

    # Warnung wenn Datei schon existiert
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

    # Schrittgröße
    print(f"\nStep size in mm (default {controls['stepsize']}, "
          f"Enter to skip):")
    step_input = input("> ").strip()
    if step_input != "":
        try:
            controls["stepsize"] = float(step_input)
        except ValueError:
            print("Invalid – using default")

    # Track-Schrittgröße
    print(f"Track step size in mm (default {controls['track_step']}, "
          f"Enter to skip):")
    track_input = input("> ").strip()
    if track_input != "":
        try:
            controls["track_step"] = int(track_input)
        except ValueError:
            print("Invalid – using default")

    # Greifer-Schrittgröße
    print(f"Gripper step size (default {controls['gripper_step']}, "
          f"Enter to skip):")
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
  p                   print current position
  c                   save pos as RACK ref in config.txt

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
