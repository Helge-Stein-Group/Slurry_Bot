"""
Slurrybot Visual Jogger
PyQt5 desktop app for teaching and editing robot position files.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QLabel, QPushButton, QFrame, QStatusBar, QSizePolicy,
    QScrollArea, QGroupBox, QGridLayout, QLineEdit, QSlider,
    QDoubleSpinBox, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QFileDialog,
    QStyledItemDelegate, QMenu, QAction
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QPalette

# ──────────────────────────────────────────────────────────────────────────────
# Theme
# ──────────────────────────────────────────────────────────────────────────────

C_BG        = "#0d1117"
C_CARD      = "#161b22"
C_ELEVATED  = "#1c2333"
C_BORDER    = "#30363d"
C_TEXT      = "#e6edf3"
C_MUTED     = "#8b949e"
C_ACCENT    = "#58a6ff"   # blue  – cartesian
C_PURPLE    = "#bc8cff"   # purple – rotation / angular capture
C_GREEN     = "#3fb950"   # green  – linear capture / connected
C_ORANGE    = "#e3b341"   # orange – track
C_RED       = "#f85149"   # red    – disconnected / gripper close
C_JOINT     = "#79c0ff"   # light blue – joints

APP_STYLESHEET = f"""
QMainWindow, QDialog {{ background: {C_BG}; }}
QWidget {{ color: {C_TEXT}; font-family: "Segoe UI", "SF Pro Text", Arial, sans-serif; font-size: 12px; background: transparent; }}
QMainWindow > QWidget, QScrollArea > QWidget > QWidget {{ background: {C_BG}; }}

QGroupBox {{
    background: {C_CARD};
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    padding: 10px 8px 8px 8px;
    margin-top: 4px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 6px;
    color: {C_MUTED};
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 0.8px;
}}

QPushButton {{
    background: {C_ELEVATED};
    color: {C_TEXT};
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton:hover {{ background: #262d38; border-color: {C_ACCENT}; color: {C_ACCENT}; }}
QPushButton:pressed {{ background: #1a2133; }}
QPushButton:disabled {{ background: {C_CARD}; color: #3d444d; border-color: #21262d; }}

QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {{
    background: {C_ELEVATED};
    border: 1px solid {C_BORDER};
    border-radius: 6px;
    padding: 3px 6px;
    color: {C_TEXT};
    selection-background-color: #1f6feb;
}}
QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {{ border-color: {C_ACCENT}; }}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background: {C_BORDER}; border: none; width: 16px;
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{ border-radius: 0 5px 0 0; }}
QSpinBox::down-button, QDoubleSpinBox::down-button {{ border-radius: 0 0 5px 0; }}

QTableWidget {{
    background: {C_BG};
    alternate-background-color: {C_CARD};
    gridline-color: #21262d;
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    selection-background-color: rgba(31,111,235,0.25);
    selection-color: {C_TEXT};
    outline: none;
}}
QTableWidget::item {{ padding: 2px 4px; border: none; }}
QTableWidget::item:selected {{ background: rgba(31,111,235,0.25); }}
QHeaderView {{ background: transparent; border: none; }}
QHeaderView::section {{
    background: {C_CARD};
    color: {C_MUTED};
    border: none;
    border-right: 1px solid #21262d;
    border-bottom: 1px solid {C_BORDER};
    padding: 5px 8px;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

QScrollBar:vertical {{ background: transparent; width: 6px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {C_BORDER}; border-radius: 3px; min-height: 24px; }}
QScrollBar::handle:vertical:hover {{ background: {C_ACCENT}; }}
QScrollBar:horizontal {{ background: transparent; height: 6px; margin: 0; }}
QScrollBar::handle:horizontal {{ background: {C_BORDER}; border-radius: 3px; min-width: 24px; }}
QScrollBar::add-line, QScrollBar::sub-line,
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; border: none; }}

QScrollArea {{ border: none; background: transparent; }}
QSplitter::handle {{ background: {C_BORDER}; }}
QSplitter::handle:horizontal {{ width: 1px; }}

QComboBox::drop-down {{ border: none; padding: 0 4px; }}
QComboBox QAbstractItemView {{
    background: {C_ELEVATED};
    border: 1px solid {C_ACCENT};
    border-radius: 6px;
    selection-background-color: #1f6feb;
    color: {C_TEXT};
    padding: 2px;
}}

QStatusBar {{
    background: {C_CARD};
    color: {C_MUTED};
    border-top: 1px solid {C_BORDER};
    font-size: 11px;
    padding: 0 8px;
}}
QToolTip {{
    background: {C_ELEVATED};
    color: {C_TEXT};
    border: 1px solid {C_ACCENT};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
}}
QMenu {{
    background: {C_ELEVATED};
    border: 1px solid {C_BORDER};
    border-radius: 8px;
    padding: 4px;
}}
QMenu::item {{ padding: 6px 20px 6px 12px; border-radius: 4px; }}
QMenu::item:selected {{ background: #1f6feb; color: #fff; }}
QMenu::separator {{ height: 1px; background: {C_BORDER}; margin: 4px 6px; }}
QMessageBox {{ background: {C_CARD}; }}
"""


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

ROBOT_IP = "192.168.1.200"
POSITIONS_DIR = os.path.join(os.path.dirname(__file__), "..", "Positions")
POLL_INTERVAL_MS = 200

POSITION_COLS = ["#", "Name", "X", "Y", "Z", "Roll", "Pitch", "Yaw", "Gripper", "Track", "Type"]
COL_IDX = {name: i for i, name in enumerate(POSITION_COLS)}

AT_POSITION_TOLERANCE_MM = 1.0
AT_POSITION_TOLERANCE_DEG = 1.0


# ──────────────────────────────────────────────────────────────────────────────
# Mock robot for when no hardware is connected
# ──────────────────────────────────────────────────────────────────────────────

class MockArm:
    """Simulates basic xArm responses so the UI works without hardware."""

    def __init__(self):
        self._position = [0.0, 0.0, 200.0, 180.0, 0.0, 0.0]  # x,y,z,roll,pitch,yaw
        self._joints = [0.0] * 6
        self._gripper = 500
        self._track = 500
        self.connected = False

    # position
    def get_position(self):
        return 0, self._position[:]

    def get_servo_angle(self):
        return 0, self._joints[:]

    def get_gripper_position(self):
        return 0, self._gripper

    def get_linear_track_pos(self):
        return 0, self._track

    # motion – just update internal state
    def set_position(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None,
                     speed=20, is_radian=False, wait=False):
        if x is not None: self._position[0] = x
        if y is not None: self._position[1] = y
        if z is not None: self._position[2] = z
        if roll is not None: self._position[3] = roll
        if pitch is not None: self._position[4] = pitch
        if yaw is not None: self._position[5] = yaw
        return 0

    def set_servo_angle(self, angle=None, servo_id=None, speed=10, wait=False):
        if servo_id is not None and angle is not None:
            idx = servo_id - 1
            if 0 <= idx < 6:
                self._joints[idx] = angle
        return 0

    def set_gripper_position(self, pos, speed=2000, wait=False):
        self._gripper = max(0, min(850, int(pos)))
        return 0

    def set_linear_track_pos(self, pos, speed=200, wait=False):
        self._track = max(0, min(1000, int(pos)))
        return 0

    # connection / setup stubs
    def connect(self): self.connected = True
    def disconnect(self): self.connected = False
    def clean_error(self): pass
    def clean_warn(self): pass
    def motion_enable(self, en): pass
    def set_mode(self, m): pass
    def set_state(self, s): pass
    def set_gripper_enable(self, en): pass
    def set_gripper_mode(self, m): pass
    def set_linear_track_enable(self, en): pass
    def set_linear_track_speed(self, s): pass


# ──────────────────────────────────────────────────────────────────────────────
# Robot worker thread
# ──────────────────────────────────────────────────────────────────────────────

class RobotWorker(QObject):
    """Runs robot commands in a background thread so the UI never blocks."""

    position_updated = pyqtSignal(list, list, int, int)  # [x,y,z,r,p,y], [j1..j6], gripper, track
    connected = pyqtSignal(bool)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.arm = MockArm()
        self._is_connected = False

    # ── connection ────────────────────────────────────────────────────────────

    def connect_robot(self):
        try:
            import logging
            logging.getLogger("xarm").setLevel(logging.ERROR)
            from xarm.wrapper import XArmAPI
            arm = XArmAPI(ROBOT_IP)
            arm.connect()
            arm.clean_error()
            arm.clean_warn()
            arm.motion_enable(True)
            arm.set_mode(0)
            arm.set_state(0)
            arm.set_gripper_enable(True)
            arm.set_gripper_mode(0)
            arm.set_linear_track_enable(True)
            arm.set_linear_track_speed(200)
            self.arm = arm
            self._is_connected = True
            self.connected.emit(True)
        except Exception as e:
            self.error.emit(f"Connection failed: {e}")
            self.connected.emit(False)

    def disconnect_robot(self):
        try:
            self.arm.disconnect()
        except Exception:
            pass
        self.arm = MockArm()
        self._is_connected = False
        self.connected.emit(False)

    # ── polling ───────────────────────────────────────────────────────────────

    def poll_position(self):
        try:
            _, pos = self.arm.get_position()
            if pos is None:
                pos = [0.0] * 6
            _, joints = self.arm.get_servo_angle()
            if joints is None:
                joints = [0.0] * 6
            _, gripper = self.arm.get_gripper_position()
            if gripper is None:
                gripper = 0
            _, track = self.arm.get_linear_track_pos()
            if track is None:
                track = 0
            self.position_updated.emit(
                [float(v) for v in pos[:6]],
                [float(v) for v in joints[:6]],
                int(gripper),
                int(track),
            )
        except Exception:
            pass

    # ── motion commands ───────────────────────────────────────────────────────

    def jog_cartesian(self, axis, delta, speed=20):
        try:
            _, pos = self.arm.get_position()
            if pos is None:
                return
            pos = list(pos[:6])
            axis_map = {"x": 0, "y": 1, "z": 2, "roll": 3, "pitch": 4, "yaw": 5}
            pos[axis_map[axis]] += delta
            self.arm.set_position(
                x=pos[0], y=pos[1], z=pos[2],
                roll=pos[3], pitch=pos[4], yaw=pos[5],
                speed=speed, wait=False,
            )
        except Exception as e:
            self.error.emit(str(e))

    def jog_joint(self, joint_idx, delta, speed=10):
        try:
            _, angles = self.arm.get_servo_angle()
            if angles is None:
                return
            angles = list(angles[:6])
            angles[joint_idx] += delta
            self.arm.set_servo_angle(
                servo_id=joint_idx + 1,
                angle=angles[joint_idx],
                speed=speed,
                wait=False,
            )
        except Exception as e:
            self.error.emit(str(e))

    def set_gripper(self, value):
        try:
            self.arm.set_gripper_position(value, wait=False)
        except Exception as e:
            self.error.emit(str(e))

    def jog_track(self, delta, speed=200):
        try:
            _, track = self.arm.get_linear_track_pos()
            if track is None:
                track = 0
            new_pos = max(0, min(1000, int(track) + int(delta)))
            self.arm.set_linear_track_pos(new_pos, speed=speed, wait=False)
        except Exception as e:
            self.error.emit(str(e))

    def go_to_position(self, point, speed=20):
        """Drive robot to a position-list point dict."""
        try:
            self.arm.set_mode(0)
            self.arm.set_state(0)
            if point.get("type", "linear").lower() == "angular":
                # Angular: replay recorded joint angles exactly
                joints = point.get("joints", [0.0] * 6)
                self.arm.set_servo_angle(
                    angle=joints,
                    speed=speed, mvacc=50, wait=False,
                )
            else:
                # Linear: move in Cartesian space
                self.arm.set_position(
                    x=point["x"], y=point["y"], z=point["z"],
                    roll=point["roll"], pitch=point["pitch"], yaw=point["yaw"],
                    speed=speed, wait=False,
                )
            self.arm.set_gripper_position(point.get("gripper", 500), wait=False)
            self.arm.set_linear_track_pos(point.get("track", 500), wait=False)
        except Exception as e:
            self.error.emit(str(e))


# ──────────────────────────────────────────────────────────────────────────────
# Position data model
# ──────────────────────────────────────────────────────────────────────────────

def empty_point(name=""):
    return {
        "name": name,
        "x": 0.0, "y": 0.0, "z": 200.0,
        "roll": 180.0, "pitch": 0.0, "yaw": 0.0,
        "joints": [0.0] * 6,
        "gripper": 500,
        "track": 500,
        "type": "linear",
    }


def parse_positions_file(path):
    """Parse a position txt file into a list of point dicts."""
    points = []
    with open(path, "r") as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

    i = 0
    while i < len(lines):
        # skip blank lines
        if not lines[i].strip():
            i += 1
            continue

        try:
            # line 0: point_N cartesian: [x,y,z,roll,pitch,yaw]
            cart_line = lines[i]; i += 1
            # line 1: point_N angular: [j1..j6]
            ang_line = lines[i]; i += 1
            # line 2: Gripper: N
            grip_line = lines[i]; i += 1
            # line 3: Track: N
            track_line = lines[i]; i += 1
            # line 4: Type: linear/angular
            type_line = lines[i]; i += 1

            name = cart_line.split(" cartesian:")[0].strip()

            def parse_list(s):
                s = s[s.index("[") + 1: s.index("]")]
                return [float(v.strip()) for v in s.split(",")]

            cart = parse_list(cart_line)
            ang = parse_list(ang_line)
            gripper = int(grip_line.split(":")[-1].strip())
            track = int(track_line.split(":")[-1].strip())
            ptype = type_line.split(":")[-1].strip().lower()

            points.append({
                "name": name,
                "x": cart[0], "y": cart[1], "z": cart[2],
                "roll": cart[3], "pitch": cart[4], "yaw": cart[5],
                "joints": ang,
                "gripper": gripper,
                "track": track,
                "type": ptype,
            })
        except (IndexError, ValueError):
            break

    return points


def serialize_positions(points):
    """Serialize list of point dicts to the required txt format."""
    lines = []
    for idx, pt in enumerate(points, start=1):
        n = f"point_{idx}"
        cart = [pt["x"], pt["y"], pt["z"], pt["roll"], pt["pitch"], pt["yaw"]]
        ang = pt.get("joints", [0.0] * 6)
        lines.append(f"{n} cartesian: {cart}")
        lines.append(f"{n} angular: {ang}")
        lines.append(f"Gripper: {pt['gripper']}")
        lines.append(f"Track: {pt['track']}")
        lines.append(f"Type: {pt['type']}")
        lines.append("")  # blank separator
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────────
# Snap helper
# ──────────────────────────────────────────────────────────────────────────────

SNAP_ANGLES = [0, 45, 90, 135, 180, -45, -90, -135, -180]

def snap_value(value, is_rotation):
    if is_rotation:
        return min(SNAP_ANGLES, key=lambda a: abs(a - value))
    return round(value)


# ──────────────────────────────────────────────────────────────────────────────
# UI helpers
# ──────────────────────────────────────────────────────────────────────────────

def _section_label(text):
    lbl = QLabel(text)
    lbl.setFont(QFont("Arial", 9, QFont.Bold))
    lbl.setStyleSheet("color: #aaa; margin-top: 6px;")
    return lbl


def _jog_button(text, tooltip=""):
    btn = QPushButton(text)
    btn.setFixedSize(48, 32)
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


DPAD_STYLE = f"""
    QPushButton {{
        background: {C_ELEVATED};
        color: {C_TEXT};
        border: 1px solid {C_BORDER};
        border-radius: 6px;
    }}
    QPushButton:hover  {{ background: #1f3358; border-color: {C_ACCENT}; color: {C_ACCENT}; }}
    QPushButton:pressed {{ background: #0d1f3c; border-color: #388bfd; }}
    QPushButton:disabled {{ background: {C_CARD}; color: #3d444d; border-color: #21262d; }}
"""

def _dpad_button(symbol, label, tooltip=""):
    btn = QPushButton(f"{symbol}\n{label}")
    btn.setFixedSize(48, 52)
    btn.setStyleSheet(DPAD_STYLE + "QPushButton { font-size: 13px; line-height: 1; }")
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


def _step_box(default, suffix="mm", decimals=1, min_val=0.1, max_val=500.0):
    sb = QDoubleSpinBox()
    sb.setDecimals(decimals)
    sb.setMinimum(min_val)
    sb.setMaximum(max_val)
    sb.setValue(default)
    sb.setSuffix(f" {suffix}")
    sb.setFixedWidth(80)
    return sb


# ──────────────────────────────────────────────────────────────────────────────
# Left panel – live position display
# ──────────────────────────────────────────────────────────────────────────────

class LivePositionPanel(QGroupBox):
    def __init__(self):
        super().__init__("Live Position")
        self._labels = {}
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        fields = [
            ("X", "mm"), ("Y", "mm"), ("Z", "mm"),
            ("Roll", "°"), ("Pitch", "°"), ("Yaw", "°"),
            ("Gripper", ""), ("Track", "mm"),
        ]
        for name, unit in fields:
            row = QHBoxLayout()
            key_lbl = QLabel(f"{name}:")
            key_lbl.setFixedWidth(55)
            val_lbl = QLabel("—")
            val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            val_lbl.setStyleSheet("font-family: monospace; font-size: 13px;")
            unit_lbl = QLabel(unit)
            unit_lbl.setFixedWidth(20)
            row.addWidget(key_lbl)
            row.addWidget(val_lbl, 1)
            row.addWidget(unit_lbl)
            layout.addLayout(row)
            self._labels[name] = val_lbl

        layout.addStretch()

    def update_position(self, pos, gripper, track):
        keys = ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]
        for i, key in enumerate(keys):
            self._labels[key].setText(f"{pos[i]:>10.1f}")
        self._labels["Gripper"].setText(f"{gripper:>10d}")
        self._labels["Track"].setText(f"{track:>10d}")


# ──────────────────────────────────────────────────────────────────────────────
# Center panel – jog controls
# ──────────────────────────────────────────────────────────────────────────────

class JogPanel(QScrollArea):
    # signals to robot worker
    jog_requested = pyqtSignal(str, float)        # axis, delta
    jog_joint_requested = pyqtSignal(int, float)  # joint_idx, delta
    gripper_requested = pyqtSignal(int)
    track_jog_requested = pyqtSignal(float)
    capture_linear_requested = pyqtSignal()
    capture_angular_requested = pyqtSignal()
    prev_point_requested = pyqtSignal()
    next_point_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        inner = QWidget()
        self.setWidget(inner)
        self._layout = QVBoxLayout(inner)
        self._layout.setAlignment(Qt.AlignTop)
        self._build()
        self.set_enabled(False)

    def _build(self):
        lay = self._layout

        # ── Cartesian ────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Cartesian"))
        cart_box = QGroupBox()
        cart_outer = QHBoxLayout(cart_box)
        cart_outer.setSpacing(12)

        # PS-style d-pad for X/Y
        dpad_widget = QWidget()
        dpad_grid = QGridLayout(dpad_widget)
        dpad_grid.setSpacing(2)
        dpad_grid.setContentsMargins(0, 0, 0, 0)

        xp = _dpad_button("▲", "X+")
        xm = _dpad_button("▼", "X−")
        yp = _dpad_button("◀", "Y+")
        ym = _dpad_button("▶", "Y−")
        xp.clicked.connect(lambda: self._jog_cart("x", +1))
        xm.clicked.connect(lambda: self._jog_cart("x", -1))
        yp.clicked.connect(lambda: self._jog_cart("y", +1))
        ym.clicked.connect(lambda: self._jog_cart("y", -1))

        # centre spacer with axis labels
        centre = QLabel("")
        centre.setFixedSize(48, 52)

        dpad_grid.addWidget(xp,     0, 1)
        dpad_grid.addWidget(yp,     1, 0)
        dpad_grid.addWidget(centre, 1, 1)
        dpad_grid.addWidget(ym,     1, 2)
        dpad_grid.addWidget(xm,     2, 1)
        cart_outer.addWidget(dpad_widget)

        # Z column: label + up/down pair
        z_widget = QWidget()
        z_lay = QVBoxLayout(z_widget)
        z_lay.setSpacing(2)
        z_lay.setContentsMargins(0, 0, 0, 0)
        z_lbl = QLabel("Z")
        z_lbl.setAlignment(Qt.AlignCenter)
        z_lbl.setStyleSheet("color:#888; font-size:9px;")
        zp = _dpad_button("▲", "Z+")
        zm = _dpad_button("▼", "Z−")
        zp.clicked.connect(lambda: self._jog_cart("z", +1))
        zm.clicked.connect(lambda: self._jog_cart("z", -1))
        z_lay.addWidget(zp)
        z_lay.addWidget(z_lbl)
        z_lay.addWidget(zm)
        cart_outer.addWidget(z_widget)
        cart_outer.addStretch()

        # Step / Speed row below both d-pad and Z
        cart_wrap = QVBoxLayout()
        cart_wrap.setSpacing(4)
        cart_wrap.addWidget(cart_box)
        step_row = QHBoxLayout()
        step_row.addWidget(QLabel("Step:"))
        self._cart_step = _step_box(5.0, "mm")
        self._cart_speed = _step_box(20.0, "mm/s", min_val=1.0, max_val=500.0)
        step_row.addWidget(self._cart_step)
        step_row.addWidget(QLabel("Speed:"))
        step_row.addWidget(self._cart_speed)
        step_row.addStretch()
        cart_wrap.addLayout(step_row)
        lay.addLayout(cart_wrap)

        # store all dpad buttons so set_enabled covers them
        self._dpad_buttons = [xp, xm, yp, ym, zp, zm]

        # ── Rotation ─────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Rotation"))
        rot_box = QGroupBox()
        rot_lay = QGridLayout(rot_box)
        rot_lay.setSpacing(4)

        self._rot_step = _step_box(45.0, "°", min_val=1.0, max_val=360.0)

        rot_axes = ["roll", "pitch", "yaw"]
        for col, axis in enumerate(rot_axes):
            plus_btn = _jog_button(f"{axis.capitalize()}+")
            minus_btn = _jog_button(f"{axis.capitalize()}-")
            plus_btn.clicked.connect(lambda _, a=axis: self._jog_cart(a, +1))
            minus_btn.clicked.connect(lambda _, a=axis: self._jog_cart(a, -1))
            rot_lay.addWidget(plus_btn, 0, col)
            rot_lay.addWidget(minus_btn, 1, col)

        rot_step_row = QHBoxLayout()
        rot_step_row.addWidget(QLabel("Step:"))
        rot_step_row.addWidget(self._rot_step)
        rot_step_row.addStretch()
        rot_lay.addLayout(rot_step_row, 2, 0, 1, 3)
        lay.addWidget(rot_box)

        # ── Track ─────────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Linear Track"))
        track_box = QGroupBox()
        track_lay = QHBoxLayout(track_box)
        self._track_step = _step_box(10.0, "mm")
        track_plus = _jog_button("Track+")
        track_minus = _jog_button("Track-")
        track_plus.clicked.connect(lambda: self.track_jog_requested.emit(+self._track_step.value()))
        track_minus.clicked.connect(lambda: self.track_jog_requested.emit(-self._track_step.value()))
        track_lay.addWidget(track_minus)
        track_lay.addWidget(track_plus)
        track_lay.addWidget(QLabel("Step:"))
        track_lay.addWidget(self._track_step)
        track_lay.addStretch()
        lay.addWidget(track_box)

        # ── Gripper ───────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Gripper"))
        grip_box = QGroupBox()
        grip_lay = QHBoxLayout(grip_box)
        self._grip_input = QSpinBox()
        self._grip_input.setRange(0, 850)
        self._grip_input.setValue(500)
        self._grip_input.setFixedWidth(70)
        set_btn = QPushButton("Set")
        set_btn.setFixedWidth(40)
        set_btn.clicked.connect(lambda: self.gripper_requested.emit(self._grip_input.value()))
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(lambda: (self._grip_input.setValue(850), self.gripper_requested.emit(850)))
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(lambda: (self._grip_input.setValue(0), self.gripper_requested.emit(0)))
        grip_lay.addWidget(self._grip_input)
        grip_lay.addWidget(set_btn)
        grip_lay.addWidget(open_btn)
        grip_lay.addWidget(close_btn)
        grip_lay.addStretch()
        lay.addWidget(grip_box)

        # ── Joints ────────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Joints"))
        joint_box = QGroupBox()
        joint_lay = QGridLayout(joint_box)
        joint_lay.setSpacing(4)

        self._joint_step = _step_box(1.0, "°", min_val=0.1, max_val=180.0)

        for j in range(6):
            plus_btn = _jog_button(f"J{j+1}+")
            minus_btn = _jog_button(f"J{j+1}-")
            plus_btn.clicked.connect(lambda _, ji=j: self._jog_joint(ji, +1))
            minus_btn.clicked.connect(lambda _, ji=j: self._jog_joint(ji, -1))
            col = j % 3 * 2
            row = j // 3 * 2
            joint_lay.addWidget(plus_btn, row, col)
            joint_lay.addWidget(minus_btn, row + 1, col)

        jstep_row = QHBoxLayout()
        jstep_row.addWidget(QLabel("Step:"))
        jstep_row.addWidget(self._joint_step)
        jstep_row.addStretch()
        joint_lay.addLayout(jstep_row, 4, 0, 1, 6)
        lay.addWidget(joint_box)

        # ── Capture ───────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Capture"))
        cap_lin_btn = QPushButton("⊕  Capture Linear")
        cap_lin_btn.setFixedHeight(36)
        cap_lin_btn.setToolTip("Save cartesian position (playback via set_position)")
        cap_lin_btn.setStyleSheet(
            "background-color: #2a6; color: white; font-size: 12px; font-weight: bold; border-radius: 4px;"
        )
        cap_lin_btn.clicked.connect(self.capture_linear_requested)

        cap_ang_btn = QPushButton("⊕  Capture Angular")
        cap_ang_btn.setFixedHeight(36)
        cap_ang_btn.setToolTip("Save joint angles (playback via set_servo_angle)")
        cap_ang_btn.setStyleSheet(
            "background-color: #45a; color: white; font-size: 12px; font-weight: bold; border-radius: 4px;"
        )
        cap_ang_btn.clicked.connect(self.capture_angular_requested)

        lay.addWidget(cap_lin_btn)
        lay.addWidget(cap_ang_btn)

        # ── Navigate saved points ─────────────────────────────────────────────
        lay.addWidget(_section_label("Navigate Points"))
        nav_box = QWidget()
        nav_lay = QHBoxLayout(nav_box)
        nav_lay.setContentsMargins(0, 0, 0, 0)
        prev_btn = QPushButton("◀  Prev Point")
        next_btn = QPushButton("Next Point  ▶")
        prev_btn.setFixedHeight(32)
        next_btn.setFixedHeight(32)
        prev_btn.setToolTip("Go to previous point in list (like 'b' in keyboard jogger)")
        next_btn.setToolTip("Go to next point in list (like 'n' in keyboard jogger)")
        prev_btn.clicked.connect(self.prev_point_requested)
        next_btn.clicked.connect(self.next_point_requested)
        nav_lay.addWidget(prev_btn)
        nav_lay.addWidget(next_btn)
        lay.addWidget(nav_box)

        # keep refs for enable/disable
        self._jog_widgets = [
            rot_box, track_box, grip_box, joint_box,
            cap_lin_btn, cap_ang_btn, prev_btn, next_btn,
        ]

    def _jog_cart(self, axis, sign):
        if axis in ("roll", "pitch", "yaw"):
            step = self._rot_step.value() * sign
        else:
            step = self._cart_step.value() * sign
        self.jog_requested.emit(axis, step)

    def _jog_joint(self, idx, sign):
        step = self._joint_step.value() * sign
        self.jog_joint_requested.emit(idx, step)

    def set_enabled(self, enabled):
        for w in self._jog_widgets:
            w.setEnabled(enabled)
        for btn in self._dpad_buttons:
            btn.setEnabled(enabled)


# ──────────────────────────────────────────────────────────────────────────────
# Right panel – position table
# ──────────────────────────────────────────────────────────────────────────────

class TypeDelegate(QStyledItemDelegate):
    """Dropdown editor for the Type column."""

    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        cb.addItems(["linear", "angular"])
        return cb

    def setEditorData(self, editor, index):
        val = index.data(Qt.DisplayRole) or "linear"
        idx = editor.findText(val)
        if idx >= 0:
            editor.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)


class PositionTable(QWidget):
    go_to_requested = pyqtSignal(dict)
    capture_here_requested = pyqtSignal(int)   # row index
    row_selected = pyqtSignal(int)             # row index when user clicks a row

    def __init__(self):
        super().__init__()
        self._points = []   # list of point dicts
        self._current_pos = None
        self._dirty = False
        self._build()

    # ── build UI ──────────────────────────────────────────────────────────────

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        # toolbar
        toolbar = QHBoxLayout()
        self._snap_btn = QPushButton("Snap RPY")
        self._snap_btn.setToolTip(
            "Round Roll/Pitch/Yaw of the selected row to nearest 0°/±45°/±90°/±135°/±180°"
        )
        self._snap_btn.clicked.connect(self._snap_selected)

        add_btn = QPushButton("+ Add Row")
        add_btn.clicked.connect(self._add_row_below)

        toolbar.addWidget(self._snap_btn)
        toolbar.addWidget(add_btn)
        toolbar.addStretch()
        lay.addLayout(toolbar)

        # table
        self._table = QTableWidget(0, len(POSITION_COLS))
        self._table.setHorizontalHeaderLabels(POSITION_COLS)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(COL_IDX["Name"], QHeaderView.Stretch)
        self._table.verticalHeader().setVisible(False)
        self._table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self._table.setContextMenuPolicy(Qt.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._context_menu)
        self._table.itemChanged.connect(self._on_item_changed)
        self._table.itemSelectionChanged.connect(self._on_selection_changed)

        # type column delegate
        self._table.setItemDelegateForColumn(COL_IDX["Type"], TypeDelegate(self._table))

        # fix column widths
        for col in ["#", "Gripper", "Track", "Type"]:
            self._table.setColumnWidth(COL_IDX[col], 55)
        for col in ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]:
            self._table.setColumnWidth(COL_IDX[col], 65)

        lay.addWidget(self._table)

    # ── public interface ──────────────────────────────────────────────────────

    @property
    def points(self):
        return self._points

    @property
    def dirty(self):
        return self._dirty

    def mark_clean(self):
        self._dirty = False

    def load_points(self, points):
        self._points = points
        self._refresh_table()
        self._dirty = False

    def get_selected_row(self):
        rows = self._table.selectedIndexes()
        if not rows:
            return None
        return rows[0].row()

    def update_current_position(self, pos, gripper, track):
        self._current_pos = {"x": pos[0], "y": pos[1], "z": pos[2],
                             "roll": pos[3], "pitch": pos[4], "yaw": pos[5],
                             "gripper": gripper, "track": track}
        self._highlight_at_position()

    # ── internal helpers ──────────────────────────────────────────────────────

    def _refresh_table(self):
        self._table.blockSignals(True)
        self._table.setRowCount(0)
        for idx, pt in enumerate(self._points):
            self._insert_row(idx, pt)
        self._table.blockSignals(False)

    def _insert_row(self, row, pt):
        self._table.insertRow(row)
        data = [
            str(row + 1),
            pt.get("name", f"point_{row+1}"),
            f"{pt['x']:.2f}", f"{pt['y']:.2f}", f"{pt['z']:.2f}",
            f"{pt['roll']:.2f}", f"{pt['pitch']:.2f}", f"{pt['yaw']:.2f}",
            str(pt["gripper"]), str(pt["track"]),
            pt.get("type", "linear"),
        ]
        for col, val in enumerate(data):
            item = QTableWidgetItem(val)
            if col == COL_IDX["#"]:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
            self._table.setItem(row, col, item)

    def _renumber(self):
        self._table.blockSignals(True)
        for row in range(self._table.rowCount()):
            self._table.item(row, COL_IDX["#"]).setText(str(row + 1))
        self._table.blockSignals(False)

    def _row_to_point(self, row):
        def _fval(col):
            item = self._table.item(row, col)
            try:
                return float(item.text()) if item else 0.0
            except ValueError:
                return 0.0

        def _ival(col):
            item = self._table.item(row, col)
            try:
                return int(float(item.text())) if item else 0
            except ValueError:
                return 0

        name_item = self._table.item(row, COL_IDX["Name"])
        type_item = self._table.item(row, COL_IDX["Type"])
        # preserve stored joint angles (not shown in table columns)
        stored_joints = self._points[row].get("joints", [0.0] * 6) if row < len(self._points) else [0.0] * 6
        return {
            "name": name_item.text() if name_item else f"point_{row+1}",
            "x": _fval(COL_IDX["X"]),
            "y": _fval(COL_IDX["Y"]),
            "z": _fval(COL_IDX["Z"]),
            "roll": _fval(COL_IDX["Roll"]),
            "pitch": _fval(COL_IDX["Pitch"]),
            "yaw": _fval(COL_IDX["Yaw"]),
            "joints": stored_joints,
            "gripper": _ival(COL_IDX["Gripper"]),
            "track": _ival(COL_IDX["Track"]),
            "type": type_item.text().lower() if type_item else "linear",
        }

    def _sync_points_from_table(self):
        self._points = [self._row_to_point(r) for r in range(self._table.rowCount())]

    def _on_item_changed(self, item):
        if item.column() == COL_IDX["#"]:
            return
        self._sync_points_from_table()
        self._dirty = True

    def _on_selection_changed(self):
        row = self.get_selected_row()
        if row is not None:
            self.row_selected.emit(row)

    # ── snap ──────────────────────────────────────────────────────────────────

    def _snap_selected(self):
        row = self.get_selected_row()
        if row is None:
            return
        rpy_cols = [COL_IDX["Roll"], COL_IDX["Pitch"], COL_IDX["Yaw"]]
        self._table.blockSignals(True)
        for col in rpy_cols:
            item = self._table.item(row, col)
            if not item:
                continue
            try:
                val = float(item.text())
            except ValueError:
                continue
            snapped = snap_value(val, is_rotation=True)
            item.setText(f"{snapped:.2f}")
        self._table.blockSignals(False)
        self._sync_points_from_table()
        self._dirty = True

    # ── row actions ───────────────────────────────────────────────────────────

    def _add_row_below(self):
        row = self.get_selected_row()
        insert_at = (row + 1) if row is not None else self._table.rowCount()
        pt = empty_point(f"point_{insert_at+1}")
        self._table.blockSignals(True)
        self._insert_row(insert_at, pt)
        self._points.insert(insert_at, pt)
        self._renumber()
        self._table.blockSignals(False)
        self._dirty = True

    def _add_row_above(self):
        row = self.get_selected_row()
        insert_at = row if row is not None else 0
        pt = empty_point(f"point_{insert_at+1}")
        self._table.blockSignals(True)
        self._insert_row(insert_at, pt)
        self._points.insert(insert_at, pt)
        self._renumber()
        self._table.blockSignals(False)
        self._dirty = True

    def _delete_row(self):
        row = self.get_selected_row()
        if row is None:
            return
        self._table.blockSignals(True)
        self._table.removeRow(row)
        self._points.pop(row)
        self._renumber()
        self._table.blockSignals(False)
        self._dirty = True

    def _move_row(self, direction):
        row = self.get_selected_row()
        if row is None:
            return
        target = row + direction
        if target < 0 or target >= self._table.rowCount():
            return
        self._points[row], self._points[target] = self._points[target], self._points[row]
        self._table.blockSignals(True)
        self._refresh_table()
        self._table.selectRow(target)
        self._table.blockSignals(False)

    def _duplicate_row(self):
        row = self.get_selected_row()
        if row is None:
            return
        import copy
        pt = copy.deepcopy(self._row_to_point(row))
        insert_at = row + 1
        self._table.blockSignals(True)
        self._insert_row(insert_at, pt)
        self._points.insert(insert_at, pt)
        self._renumber()
        self._table.blockSignals(False)
        self._dirty = True

    def _go_to_row(self, row):
        pt = self._row_to_point(row)
        self.go_to_requested.emit(pt)

    def _capture_here(self, row):
        self.capture_here_requested.emit(row)

    # ── context menu ──────────────────────────────────────────────────────────

    def _context_menu(self, pos):
        row = self._table.rowAt(pos.y())
        menu = QMenu(self)

        if row >= 0:
            go_action = QAction("Go To", self)
            go_action.triggered.connect(lambda: self._go_to_row(row))
            menu.addAction(go_action)

            cap_action = QAction("Capture Here", self)
            cap_action.triggered.connect(lambda: self._capture_here(row))
            menu.addAction(cap_action)

            menu.addSeparator()

        add_above = QAction("Add Above", self)
        add_above.triggered.connect(self._add_row_above)
        menu.addAction(add_above)

        add_below = QAction("Add Below", self)
        add_below.triggered.connect(self._add_row_below)
        menu.addAction(add_below)

        if row >= 0:
            dup = QAction("Duplicate", self)
            dup.triggered.connect(self._duplicate_row)
            menu.addAction(dup)

            menu.addSeparator()

            move_up = QAction("Move Up", self)
            move_up.triggered.connect(lambda: self._move_row(-1))
            menu.addAction(move_up)

            move_down = QAction("Move Down", self)
            move_down.triggered.connect(lambda: self._move_row(+1))
            menu.addAction(move_down)

            menu.addSeparator()

            delete = QAction("Delete", self)
            delete.triggered.connect(self._delete_row)
            menu.addAction(delete)

        menu.exec_(self._table.viewport().mapToGlobal(pos))

    # ── highlight current position ────────────────────────────────────────────

    def _highlight_at_position(self):
        if self._current_pos is None:
            return
        cp = self._current_pos
        self._table.blockSignals(True)
        for row in range(self._table.rowCount()):
            pt = self._row_to_point(row)
            at = (
                abs(pt["x"] - cp["x"]) <= AT_POSITION_TOLERANCE_MM and
                abs(pt["y"] - cp["y"]) <= AT_POSITION_TOLERANCE_MM and
                abs(pt["z"] - cp["z"]) <= AT_POSITION_TOLERANCE_MM and
                abs(pt["roll"] - cp["roll"]) <= AT_POSITION_TOLERANCE_DEG and
                abs(pt["pitch"] - cp["pitch"]) <= AT_POSITION_TOLERANCE_DEG and
                abs(pt["yaw"] - cp["yaw"]) <= AT_POSITION_TOLERANCE_DEG
            )
            color = QColor("#1a4a1a") if at else QColor("transparent")
            for col in range(self._table.columnCount()):
                item = self._table.item(row, col)
                if item:
                    item.setBackground(color)
        self._table.blockSignals(False)

    # ── public: capture current position into a row ───────────────────────────

    def capture_into_row(self, row, pos, joints, gripper, track, ptype=None):
        existing = self._row_to_point(row)
        pt = {
            "name": existing["name"],
            "x": pos[0], "y": pos[1], "z": pos[2],
            "roll": pos[3], "pitch": pos[4], "yaw": pos[5],
            "joints": joints,
            "gripper": gripper, "track": track,
            "type": ptype if ptype is not None else existing["type"],
        }
        self._table.blockSignals(True)
        col_vals = [
            str(row + 1),
            pt["name"],
            f"{pt['x']:.2f}", f"{pt['y']:.2f}", f"{pt['z']:.2f}",
            f"{pt['roll']:.2f}", f"{pt['pitch']:.2f}", f"{pt['yaw']:.2f}",
            str(pt["gripper"]), str(pt["track"]),
            pt["type"],
        ]
        for col, val in enumerate(col_vals):
            item = self._table.item(row, col)
            if item:
                item.setText(val)
        self._table.blockSignals(False)
        self._points[row] = pt
        self._dirty = True

    def append_captured(self, pos, joints, gripper, track, ptype="linear"):
        pt = {
            "name": f"point_{self._table.rowCount()+1}",
            "x": pos[0], "y": pos[1], "z": pos[2],
            "roll": pos[3], "pitch": pos[4], "yaw": pos[5],
            "joints": joints,
            "gripper": gripper, "track": track,
            "type": ptype,
        }
        row = self._table.rowCount()
        self._table.blockSignals(True)
        self._insert_row(row, pt)
        self._points.append(pt)
        self._table.blockSignals(False)
        self._dirty = True
        self._table.scrollToBottom()


# ──────────────────────────────────────────────────────────────────────────────
# Main window
# ──────────────────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Slurrybot Visual Jogger")
        self.resize(1400, 800)

        self._current_file = None
        self._robot_connected = False
        self._last_pos = [0.0] * 6
        self._last_joints = [0.0] * 6
        self._last_gripper = 0
        self._last_track = 0
        self._nav_index = -1  # current navigated point index (-1 = none)

        # robot worker lives in its own thread
        self._robot_thread = QThread()
        self._robot = RobotWorker()
        self._robot.moveToThread(self._robot_thread)
        self._robot.position_updated.connect(self._on_position_updated)
        self._robot.connected.connect(self._on_connection_changed)
        self._robot.error.connect(self._on_robot_error)
        self._robot_thread.start()

        self._build_ui()
        self._start_poll_timer()

    # ── build UI ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── top bar ───────────────────────────────────────────────────────────
        top_bar = QWidget()
        top_lay = QHBoxLayout(top_bar)
        top_lay.setContentsMargins(6, 4, 6, 4)

        self._connect_btn = QPushButton("Connect")
        self._connect_btn.setFixedWidth(90)
        self._connect_btn.clicked.connect(self._toggle_connection)

        self._status_indicator = QLabel("●")
        self._status_indicator.setStyleSheet("color: red; font-size: 18px;")

        self._file_label = QLabel("No file loaded")
        self._file_label.setStyleSheet("color: #888;")

        open_btn = QPushButton("Open File")
        open_btn.clicked.connect(self._open_file)
        new_btn = QPushButton("New File")
        new_btn.clicked.connect(self._new_file)
        save_btn = QPushButton("Save All")
        save_btn.clicked.connect(self._save_file)

        top_lay.addWidget(self._status_indicator)
        top_lay.addWidget(self._connect_btn)
        top_lay.addSpacing(12)
        top_lay.addWidget(self._file_label, 1)
        top_lay.addWidget(open_btn)
        top_lay.addWidget(new_btn)
        top_lay.addWidget(save_btn)

        # ── panels ────────────────────────────────────────────────────────────
        self._live_panel = LivePositionPanel()
        self._live_panel.setMinimumWidth(180)
        self._live_panel.setMaximumWidth(220)

        self._jog_panel = JogPanel()
        self._jog_panel.setMinimumWidth(240)
        self._jog_panel.setMaximumWidth(320)

        self._pos_table = PositionTable()

        # connect jog signals to robot worker
        self._jog_panel.jog_requested.connect(
            lambda axis, delta: self._robot.jog_cartesian(axis, delta,
                                                          speed=self._jog_panel._cart_speed.value()))
        self._jog_panel.jog_joint_requested.connect(self._robot.jog_joint)
        self._jog_panel.gripper_requested.connect(self._robot.set_gripper)
        self._jog_panel.track_jog_requested.connect(self._robot.jog_track)
        self._jog_panel.capture_linear_requested.connect(self._capture_linear)
        self._jog_panel.capture_angular_requested.connect(self._capture_angular)
        self._jog_panel.prev_point_requested.connect(self._nav_prev)
        self._jog_panel.next_point_requested.connect(self._nav_next)

        # connect position table signals
        self._pos_table.go_to_requested.connect(self._robot.go_to_position)
        self._pos_table.capture_here_requested.connect(self._capture_here)
        self._pos_table.row_selected.connect(lambda row: setattr(self, "_nav_index", row))

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._live_panel)
        splitter.addWidget(self._jog_panel)
        splitter.addWidget(self._pos_table)
        splitter.setStretchFactor(2, 1)
        splitter.setSizes([200, 280, 900])

        # ── assemble ──────────────────────────────────────────────────────────
        central = QWidget()
        main_lay = QVBoxLayout(central)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #444;")

        main_lay.addWidget(top_bar)
        main_lay.addWidget(separator)
        main_lay.addWidget(splitter, 1)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())

    # ── polling timer ─────────────────────────────────────────────────────────

    def _start_poll_timer(self):
        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self._robot.poll_position)
        self._poll_timer.start(POLL_INTERVAL_MS)

    # ── slots ──────────────────────────────────────────────────────────────────

    def _on_position_updated(self, pos, joints, gripper, track):
        self._last_pos = pos
        self._last_joints = joints
        self._last_gripper = gripper
        self._last_track = track
        self._live_panel.update_position(pos, gripper, track)
        self._pos_table.update_current_position(pos, gripper, track)

    def _on_connection_changed(self, connected):
        self._robot_connected = connected
        if connected:
            self._status_indicator.setStyleSheet("color: #2d2; font-size: 18px;")
            self._connect_btn.setText("Disconnect")
            self.statusBar().showMessage("Robot connected")
        else:
            self._status_indicator.setStyleSheet("color: red; font-size: 18px;")
            self._connect_btn.setText("Connect")
            self.statusBar().showMessage("Robot disconnected")
        self._jog_panel.set_enabled(connected)

    def _on_robot_error(self, msg):
        self.statusBar().showMessage(f"Error: {msg}", 5000)

    def _toggle_connection(self):
        if self._robot_connected:
            self._robot.disconnect_robot()
        else:
            self._robot.connect_robot()

    # ── capture / go-to ───────────────────────────────────────────────────────

    def _capture_linear(self):
        self._pos_table.append_captured(
            self._last_pos, self._last_joints, self._last_gripper, self._last_track, "linear")
        self._nav_index = self._pos_table._table.rowCount() - 1

    def _capture_angular(self):
        self._pos_table.append_captured(
            self._last_pos, self._last_joints, self._last_gripper, self._last_track, "angular")
        self._nav_index = self._pos_table._table.rowCount() - 1

    def _capture_here(self, row):
        # preserve existing type when overwriting via context menu
        self._pos_table.capture_into_row(
            row, self._last_pos, self._last_joints, self._last_gripper, self._last_track)

    # ── point navigation (like b/n in keyboard jogger) ────────────────────────

    def _nav_prev(self):
        count = self._pos_table._table.rowCount()
        if count == 0:
            self.statusBar().showMessage("No points in list", 3000)
            return
        if self._nav_index <= 0:
            self.statusBar().showMessage("Already at first point", 3000)
            return
        self._nav_index -= 1
        self._nav_go(self._nav_index)

    def _nav_next(self):
        count = self._pos_table._table.rowCount()
        if count == 0:
            self.statusBar().showMessage("No points in list", 3000)
            return
        if self._nav_index >= count - 1:
            self.statusBar().showMessage("Already at last point", 3000)
            return
        self._nav_index += 1
        self._nav_go(self._nav_index)

    def _nav_go(self, index):
        pt = self._pos_table._row_to_point(index)
        self._pos_table._table.selectRow(index)
        self._robot.go_to_position(pt)
        self.statusBar().showMessage(
            f"Going to point {index + 1}/{self._pos_table._table.rowCount()}: {pt['name']}", 4000)

    # ── file management ───────────────────────────────────────────────────────

    def _open_file(self):
        if self._pos_table.dirty:
            ans = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Discard them?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if ans == QMessageBox.No:
                return

        start_dir = POSITIONS_DIR if os.path.isdir(POSITIONS_DIR) else os.path.expanduser("~")
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Position File", start_dir, "Text files (*.txt)"
        )
        if not path:
            return
        try:
            points = parse_positions_file(path)
            self._pos_table.load_points(points)
            self._current_file = path
            self._file_label.setText(path)
            self.statusBar().showMessage(f"Loaded {len(points)} points from {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{e}")

    def _new_file(self):
        if self._pos_table.dirty:
            ans = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Discard them?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if ans == QMessageBox.No:
                return

        start_dir = POSITIONS_DIR if os.path.isdir(POSITIONS_DIR) else os.path.expanduser("~")
        path, _ = QFileDialog.getSaveFileName(
            self, "New Position File", start_dir, "Text files (*.txt)"
        )
        if not path:
            return
        self._pos_table.load_points([])
        self._current_file = path
        self._file_label.setText(path)
        self.statusBar().showMessage("New file ready")

    def _save_file(self):
        if not self._current_file:
            start_dir = POSITIONS_DIR if os.path.isdir(POSITIONS_DIR) else os.path.expanduser("~")
            path, _ = QFileDialog.getSaveFileName(
                self, "Save Position File", start_dir, "Text files (*.txt)"
            )
            if not path:
                return
            self._current_file = path
            self._file_label.setText(path)

        try:
            content = serialize_positions(self._pos_table.points)
            with open(self._current_file, "w") as f:
                f.write(content)
            self._pos_table.mark_clean()
            self.statusBar().showMessage(
                f"Saved {len(self._pos_table.points)} points to {os.path.basename(self._current_file)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")

    # ── close guard ───────────────────────────────────────────────────────────

    def closeEvent(self, event):
        if self._pos_table.dirty:
            ans = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Save before exiting?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            )
            if ans == QMessageBox.Save:
                self._save_file()
                event.accept()
            elif ans == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
                return
        self._poll_timer.stop()
        self._robot_thread.quit()
        self._robot_thread.wait()
        event.accept()


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
    palette.setColor(QPalette.ToolTipBase, QColor(60, 60, 60))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(55, 55, 55))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
