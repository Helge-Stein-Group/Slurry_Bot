from xarm.wrapper import XArmAPI
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Config laden ─────────────────────────────────────────────
def load_config(filename="config.txt"):
    """
    Loads all configuration from config.txt.
    Returns: fixed_points, gripper_positions, racks
    """
    fixed_points      = {}
    gripper_positions = {}
    racks             = {}

    filepath = os.path.join(BASE_DIR, "Positions", filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")

    current_rack_custom = None

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue

            parts = line.split()

            if parts[0] == "FIXED":
                name = parts[1]
                if len(parts) == 3:
                    fixed_points[name] = float(parts[2])
                elif len(parts) == 8:
                    fixed_points[name] = [float(v) for v in parts[2:8]]

            elif parts[0] == "GRIPPER":
                gripper_positions[parts[1]] = int(parts[2])

            elif parts[0] == "RACK":
                name      = parts[1]
                ref_file  = parts[2]
                spacing_x = float(parts[3])
                spacing_y = float(parts[4])
                count     = int(parts[5])

                racks[name] = {
                    "ref_file":  ref_file,
                    "spacing_x": spacing_x,
                    "spacing_y": spacing_y,
                    "count":     count
                }
                current_rack_custom = None

    print(f"✓ Config loaded: "
          f"{len(fixed_points)} fixed | "
          f"{len(gripper_positions)} gripper | "
          f"{len(racks)} racks")

    return fixed_points, gripper_positions, racks


fixed_points, gripper_positions, racks = load_config()


class Robot():

    def __init__(self):
        self.arm        = XArmAPI('192.168.1.200')
        self.savedegree = 0

    # ── Core movement function ───────────────────────────────
    def move_from_file(self, filename, speed=50, offset_x=0, offset_y=0, offset_z=0):
        """
        Loads and executes a position file.
        Optional offset shifts all cartesian coordinates.
        Execution order per point: move → gripper → track
        Only sets gripper/track if value changed from previous point.
        """
        filepath = os.path.join(BASE_DIR, "Positions", filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Position file not found: {filepath}")

        with open(filepath, "r") as f:
            lines = [
                l for l in f.readlines()
                if l.strip() != "" and not l.strip().startswith("#")
            ]

        prev_gripper = None
        prev_track   = None
        i            = 0

        while i < len(lines):
            try:
                _, cart_vals = lines[i].split(" cartesian: ", 1)
                cartesian    = eval(cart_vals.strip())

                _, ang_vals  = lines[i+1].split(" angular: ", 1)
                angular      = eval(ang_vals.strip())

                _, grip_val  = lines[i+2].split(": ", 1)
                gripper      = int(grip_val.strip())

                _, track_val = lines[i+3].split(": ", 1)
                track        = int(track_val.strip())

                _, type_val  = lines[i+4].split(": ", 1)
                point_type   = type_val.strip()

                # Offset anwenden
                cartesian[0] += offset_x
                cartesian[1] += offset_y
                cartesian[2] += offset_z

                # 1. Bewegen
                if point_type == "linear":
                    self.arm.set_position(
                        *cartesian,
                        speed=speed, wait=True
                    )
                elif point_type == "angular":
                    self.arm.set_servo_angle(
                        angle=angular,
                        speed=speed, wait=True
                    )

                # 2. Greifer – nur wenn geändert
                if gripper != prev_gripper:
                    self.arm.set_gripper_position(gripper, wait=True)
                    prev_gripper = gripper

                # 3. Schiene – nur wenn geändert
                if track != prev_track:
                    self.arm.set_linear_track_pos(track, wait=True)
                    prev_track = track

                i += 5

            except Exception as e:
                print(f"⚠️  Could not parse line {i} in {filename}: {e}")
                i += 1

    # ── Helper ───────────────────────────────────────────────
    def GripperAction(self, name):
        """Sets gripper to named position from config.txt"""
        self.arm.set_gripper_position(gripper_positions[name], wait=True)

    # ── Setup ────────────────────────────────────────────────
    def restart(self):
        self.arm.disconnect()
        self.arm.connect()
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)

    def hangle_err_warn_changed(item):
        print('ErrorCode: {}, WarnCode: {}'.format(
            item['error_code'], item['warn_code']))

    def initialize(self):
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(state=0)
        self.arm.set_gripper_enable(True)
        self.arm.set_gripper_mode(0)
        self.arm.set_initial_point([-400, 0, 133, 0, 90, 180])
        self.arm.connect()
        self.arm.set_position(
            x=-400, y=0, z=133, roll=0, pitch=90, yaw=180,
            speed=20, wait=True)
        self.arm.set_linear_track_back_origin(wait=True)
        self.arm.set_linear_track_enable(True)
        self.arm.set_linear_track_speed(200)

    def close(self):
        self.arm.disconnect()

    # ── Movements ────────────────────────────────────────────
    def GoTo_InitialPoint(self, speedfactor=1):
        self.move_from_file("initial_point.txt",
                            speed=20*speedfactor)

    def PickUpVial(self, vial_number, speedfactor=1):
        if vial_number in ["Vial1", "Vial2", "Vial3"]:
            rack  = racks["VialRackFront"]
            index = int(vial_number[-1]) - 1
        elif vial_number in ["Vial4", "Vial5", "Vial6"]:
            rack  = racks["VialRackBack"]
            index = int(vial_number[-1]) - 4
        else:
            raise ValueError(f"Unknown vial: {vial_number}")

        self.move_from_file(
            filename = rack["ref_file"],
            offset_x = rack["spacing_x"] * index,
            offset_y = rack["spacing_y"] * index,
            speed    = 60*speedfactor
        )

    def VialToScale(self, speedfactor=1):
        self.move_from_file("vial_to_scale.txt",
                            speed=80*speedfactor)

    def ScaleToLiquidRestPoint(self, speedfactor=1):
        self.move_from_file("scale_to_liquid_rest.txt",
                            speed=80*speedfactor)

    def PickUpPipette(self, speedfactor=1):
        self.move_from_file("pipette_pickup.txt",
                            speed=50*speedfactor)

    def PuttingBackPipette(self, speedfactor=1):
        self.move_from_file("putting_back_pipette.txt",
                            speed=100*speedfactor)

    def GettingPipetteTip(self, tip_number, speedfactor=1):
        rack  = racks["TipGet"]
        index = int(tip_number) - 1
        self.move_from_file(
            filename = rack["ref_file"],
            offset_x = rack["spacing_x"] * index,
            offset_y = rack["spacing_y"] * index,
            speed    = 30*speedfactor
        )

    def TakingLiquid(self, tip_number, speedfactor=1):
        rack  = racks["TipTakeLiquid"]
        index = int(tip_number) - 1
        self.move_from_file(
            filename = rack["ref_file"],
            offset_x = rack["spacing_x"] * index,
            offset_y = rack["spacing_y"] * index,
            speed    = 30*speedfactor
        )

    def LiquidToVial(self, tip_number, speedfactor=1):
        rack  = racks["TipLiquidToVial"]
        index = int(tip_number) - 1
        self.move_from_file(
            filename = rack["ref_file"],
            offset_x = rack["spacing_x"] * index,
            offset_y = rack["spacing_y"] * index,
            speed    = 30*speedfactor
        )

    def PuttingBackPipetteTip(self, tip_number, speedfactor=1):
        rack  = racks["TipPutback"]
        index = int(tip_number) - 1
        self.move_from_file(
            filename = rack["ref_file"],
            offset_x = rack["spacing_x"] * index,
            offset_y = rack["spacing_y"] * index,
            speed    = 30*speedfactor
        )

    def PlaceFunnel(self, speedfactor=1):
        self.move_from_file("place_funnel.txt", speed=70*speedfactor)

    def ReplaceFunnel(self, speedfactor=1):
        self.move_from_file("replace_funnel.txt", speed=70*speedfactor)

    def PickupLargeSpatula(self, speedfactor=1):
        self.move_from_file("pickup_large.txt", speed=80*speedfactor)

    def ReplaceLargeSpatula(self, speedfactor=1):
        self.move_from_file("replace_big_spatula.txt", speed=70*speedfactor)

    def PickupMediumSpatula(self, speedfactor=1):
        self.move_from_file("pickup_medium.txt", speed=80*speedfactor)

    def ReplaceMediumSpatula(self, speedfactor=1):
        self.move_from_file("replace_medium_spatula.txt", speed=70*speedfactor)

    def ScoopBigMiddle(self, speedfactor=1):
        self.move_from_file("scoop_big_middle.txt", speed=30*speedfactor)

    def ScoopBigLeft(self, speedfactor=1):
        self.move_from_file("scoop_big_left.txt", speed=30*speedfactor)

    def ScoopBigRight(self, speedfactor=1):
        self.move_from_file("scoop_big_right.txt", speed=30*speedfactor)

    def ScoopMediumLeft(self, speedfactor=1):
        self.move_from_file("scoop_medium_left.txt", speed=30*speedfactor)

    def ScoopMediumRight(self, speedfactor=1):
        self.move_from_file("scoop_medium_right.txt", speed=30*speedfactor)

    def ScoopMediumMiddle(self, speedfactor=1):
        self.move_from_file("scoop_medium_middle.txt", speed=30*speedfactor)

    def ScoopMediumFarleft(self, speedfactor=1):
        self.move_from_file("scoop_medium_farleft.txt", speed=30*speedfactor)

    def ScoopTiny(self, speedfactor=1):
        self.move_from_file("scoop_tiny.txt", speed=30*speedfactor)

    def ScoopTinyLeft(self, speedfactor=1):
        self.move_from_file("scoop_tiny_left.txt", speed=30*speedfactor)

    def ScoopTinyRight(self, speedfactor=1):
        self.move_from_file("scoop_tiny_right.txt", speed=30*speedfactor)
