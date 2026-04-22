import time
from xarm.wrapper import XArmAPI
from pynput import keyboard
import os

# ── Verbindung ──────────────────────────────────────────────
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
arm.set_gripper_position(850, wait=True)  # startet offen

# ── Globale Variablen ───────────────────────────────────────
txtfile          = ""
space_held       = False
active_key       = None
gripper_position = 850    # aktueller Greiferwert
movestack        = []     # für Reversal-Funktion

GRIPPER_MIN = 0
GRIPPER_MAX = 850

controls = {
    "stepsize":      5,    # mm pro Tastendruck
    "step_angle":    1,    # Grad pro Tastendruck
    "gripper_step":  25,   # Greifer pro Tastendruck
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

def save_point(point_type: str) -> None:
    """
    Saves current position to txt file.
    Asks for a name so points are readable later.
    point_type: "linear" or "angular"
    """
    _, position = arm.get_position()
    _, angles   = arm.get_servo_angle()
    movestack.clear()

    print(f"\nCurrent position: {[round(p,1) for p in position]}")
    print(f"Current gripper:  {gripper_position}")
    print("Enter name for this point (e.g. 'approach_container'):")
    point_name = input("> ").strip()

    if point_name == "":
        print("No name entered – point NOT saved!")
        return

    with open(txtfile, "a") as file:
        file.write(
            f"{point_name} cartesian: {position}\n"
            f"{point_name} angular: {angles}\n"
            f"Gripper: {gripper_position}\n"
            f"Type: {point_type}\n"
            f"\n"  # Leerzeile zwischen Punkten
        )
    print(f"✓ '{point_name}' saved to {txtfile}")

def reversal() -> None:
    """Reverses all moves since last saved point."""
    if not movestack:
        print("Nothing to reverse!")
        return
    print(f"Reversing {len(movestack)} moves...")
    while movestack:
        target_angles = movestack.pop()
        arm.set_servo_angle(angle=target_angles, speed=10, mvacc=50, wait=True)
    print("Reversal complete")

def set_gripper(open: bool) -> None:
    """Opens or closes gripper by one step."""
    global gripper_position
    if open:
        gripper_position = min(gripper_position + controls["gripper_step"], GRIPPER_MAX)
    else:
        gripper_position = max(gripper_position - controls["gripper_step"], GRIPPER_MIN)
    arm.set_gripper_position(gripper_position, wait=True)
    print(f"Gripper: {gripper_position}")

def print_current_position() -> None:
    """Prints current position without saving."""
    _, position = arm.get_position()
    _, angles   = arm.get_servo_angle()
    print(f"\nPosition: {[round(p,1) for p in position]}")
    print(f"Angles:   {[round(a,1) for a in angles]}")
    print(f"Gripper:  {gripper_position}")
    print(f"Stepsize: {controls['stepsize']}mm")

# ── Tastatur Callbacks ───────────────────────────────────────

def on_press(key):
    global space_held, active_key, gripper_position

    # OS Wiederholfilter
    if key == active_key:
        return
    active_key = key

    # Leertaste = Modifier für negative Richtung
    if key == keyboard.Key.space:
        space_held = True
        return

    # ESC = Notausgang
    elif key == keyboard.Key.esc:
        print("\nEMERGENCY STOP – disconnecting!")
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

        # ── Kartesische Bewegung ────────────────────────────
        if key.char in "xyz":
            if space_held:
                current_pos[controls[key.char]] -= controls["stepsize"]
            else:
                current_pos[controls[key.char]] += controls["stepsize"]
            arm.set_position(*current_pos, speed=20, wait=False)

        # ── Einzelne Gelenke ────────────────────────────────
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

        # ── Punkt speichern ─────────────────────────────────
        elif key.char == "l":
            save_point("linear")

        elif key.char == "j":
            save_point("angular")

        # ── Zurück zum letzten Punkt ────────────────────────
        elif key.char == "r":
            reversal()

        # ── Greifer ─────────────────────────────────────────
        elif key.char == "g":
            # g = schließen, Space+g = öffnen
            set_gripper(open=space_held)

        elif key.char == "h":
            # h = komplett öffnen
            gripper_position = GRIPPER_MAX
            arm.set_gripper_position(gripper_position, wait=True)
            print(f"Gripper: FULL OPEN ({GRIPPER_MAX})")

        elif key.char == "f":
            # f = komplett schließen
            gripper_position = GRIPPER_MIN
            arm.set_gripper_position(gripper_position, wait=True)
            print(f"Gripper: FULL CLOSED ({GRIPPER_MIN})")

        # ── Schrittgröße ────────────────────────────────────
        elif key.char == "+":
            controls["stepsize"] = min(controls["stepsize"] * 2, 100)
            print(f"Stepsize: {controls['stepsize']}mm")

        elif key.char == "-":
            controls["stepsize"] = max(controls["stepsize"] / 2, 0.5)
            print(f"Stepsize: {controls['stepsize']}mm")

        # ── Position anzeigen ohne speichern ────────────────
        elif key.char == "p":
            print_current_position()

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
            arm.set_state(4)   # stopp
            arm.set_state(0)   # wieder bereit
            time.sleep(0.1)
            _, actual_angles = arm.get_servo_angle()
            movestack.append(actual_angles)
    except AttributeError:
        pass

# ── Main ─────────────────────────────────────────────────────

def main():
    global txtfile, controls

    print("\n=== Slurrybot Keyboard Jogger ===\n")

    # Positions-Ordner erstellen falls nicht vorhanden
    os.makedirs("Positions", exist_ok=True)

    # Dateiname eingeben
    print("Enter name for this movement file")
    print("(e.g. 'scoop_big_middle' → saves to Positions/scoop_big_middle.txt):")
    filename = input("> ").strip()
    txtfile = f"Positions/{filename}.txt"

    # Warnung wenn Datei schon existiert
    if os.path.exists(txtfile):
        print(f"\n⚠️  WARNING: '{txtfile}' already exists!")
        print("Options:")
        print("  o = overwrite (delete existing points)")
        print("  a = append (add to existing points)")
        choice = input("> ").strip().lower()
        if choice == "o":
            open(txtfile, "w").close()  # leeren
            print("File cleared ✓")
        else:
            print("Appending to existing file ✓")
    else:
        print(f"Creating new file: {txtfile} ✓")

    # Schrittgröße festlegen
    print(f"\nStep size in mm (default {controls['stepsize']}, Enter to skip):")
    step_input = input("> ").strip()
    if step_input != "":
        try:
            controls["stepsize"] = float(step_input)
        except ValueError:
            print("Invalid input – using default")

    # Greifer-Schrittgröße
    print(f"Gripper step size (default {controls['gripper_step']}, Enter to skip):")
    grip_input = input("> ").strip()
    if grip_input != "":
        try:
            controls["gripper_step"] = int(grip_input)
        except ValueError:
            print("Invalid input – using default")

    print(f"\nSettings:")
    print(f"  File:         {txtfile}")
    print(f"  Step size:    {controls['stepsize']}mm")
    print(f"  Gripper step: {controls['gripper_step']}")

    print("""
Controls:
─────────────────────────────────────────────
Movement:
  x / y / z         move along axis (+)
  Space + x/y/z     move along axis (-)
  1-6               rotate joint (+)
  Space + 1-6       rotate joint (-)
  + / -             double/halve step size

Gripper:
  g                 close gripper (one step)
  Space + g         open gripper (one step)
  f                 gripper fully closed
  h                 gripper fully open

Save & Navigate:
  l                 save point (linear/cartesian)
  j                 save point (angular/servo)
  r                 revert to last saved point
  p                 print current position

  ESC               emergency stop + exit
─────────────────────────────────────────────
    """)

    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()

if __name__ == "__main__":
    main()