"""
Slurrybot Visual Jogger
PyQt5 desktop app for teaching and editing robot position files.
"""

import sys
import os
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QLabel, QPushButton, QFrame, QStatusBar, QSizePolicy,
    QScrollArea, QGroupBox, QGridLayout, QLineEdit, QSlider,
    QDoubleSpinBox, QSpinBox, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QFileDialog,
    QStyledItemDelegate, QMenu, QAction, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject, QRectF, QPointF, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter, QPainterPath, QPen, QBrush

# ──────────────────────────────────────────────────────────────────────────────
# Theme system
# ──────────────────────────────────────────────────────────────────────────────

DARK_THEME = {
    "bg":       "#0d1117",
    "card":     "#161b22",
    "elevated": "#1c2333",
    "border":   "#30363d",
    "text":     "#e6edf3",
    "muted":    "#8b949e",
    "accent":   "#58a6ff",
    "purple":   "#bc8cff",
    "green":    "#3fb950",
    "orange":   "#e3b341",
    "red":      "#f85149",
    "joint":    "#79c0ff",
    "btn_hover":  "#262d38",
    "btn_press":  "#1a2133",
    "btn_dis_fg": "#3d444d",
    "btn_dis_bg": "#21262d",
    "sel_bg":   "rgba(31,111,235,0.25)",
    "grid":     "#21262d",
}

LIGHT_THEME = {
    "bg":       "#f6f8fa",
    "card":     "#ffffff",
    "elevated": "#eaeef2",
    "border":   "#d0d7de",
    "text":     "#1f2328",
    "muted":    "#636c76",
    "accent":   "#0969da",
    "purple":   "#8250df",
    "green":    "#1a7f37",
    "orange":   "#9a6700",
    "red":      "#cf222e",
    "joint":    "#0550ae",
    "btn_hover":  "#dde3e9",
    "btn_press":  "#c8d0d8",
    "btn_dis_fg": "#8c959f",
    "btn_dis_bg": "#eaeef2",
    "sel_bg":   "rgba(9,105,218,0.15)",
    "grid":     "#e1e4e8",
}

# mutable current theme – update in-place to switch
T = dict(LIGHT_THEME)


def build_stylesheet():
    return f"""
QMainWindow, QDialog {{ background: {T['bg']}; }}
QWidget {{ color: {T['text']}; font-family: "Segoe UI", "SF Pro Text", Arial, sans-serif; font-size: 13px; background: transparent; }}
QMainWindow > QWidget, QScrollArea > QWidget > QWidget {{ background: {T['bg']}; }}

QGroupBox {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    padding: 10px 8px 8px 8px;
    margin-top: 4px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 6px;
    color: {T['muted']};
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 0.8px;
}}

QPushButton {{
    background: {T['elevated']};
    color: {T['text']};
    border: 1px solid {T['border']};
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 500;
}}
QPushButton:hover {{ background: {T['btn_hover']}; border-color: {T['accent']}; color: {T['accent']}; }}
QPushButton:pressed {{ background: {T['btn_press']}; }}
QPushButton:disabled {{ background: {T['btn_dis_bg']}; color: {T['btn_dis_fg']}; border-color: {T['border']}; }}

QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit {{
    background: {T['elevated']};
    border: 1px solid {T['border']};
    border-radius: 6px;
    padding: 3px 6px;
    color: {T['text']};
    selection-background-color: {T['accent']};
}}
QSpinBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {{ border-color: {T['accent']}; }}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background: {T['border']}; border: none; width: 16px;
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{ border-radius: 0 5px 0 0; }}
QSpinBox::down-button, QDoubleSpinBox::down-button {{ border-radius: 0 0 5px 0; }}

QTableWidget {{
    background: {T['bg']};
    alternate-background-color: {T['card']};
    gridline-color: {T['grid']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    selection-background-color: {T['sel_bg']};
    selection-color: {T['text']};
    outline: none;
}}
QTableWidget::item {{ padding: 2px 4px; border: none; }}
QTableWidget::item:selected {{ background: {T['sel_bg']}; }}
QHeaderView {{ background: transparent; border: none; }}
QHeaderView::section {{
    background: {T['card']};
    color: {T['muted']};
    border: none;
    border-right: 1px solid {T['grid']};
    border-bottom: 1px solid {T['border']};
    padding: 5px 8px;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

QScrollBar:vertical {{ background: transparent; width: 6px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {T['border']}; border-radius: 3px; min-height: 24px; }}
QScrollBar::handle:vertical:hover {{ background: {T['accent']}; }}
QScrollBar:horizontal {{ background: transparent; height: 6px; margin: 0; }}
QScrollBar::handle:horizontal {{ background: {T['border']}; border-radius: 3px; min-width: 24px; }}
QScrollBar::add-line, QScrollBar::sub-line,
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; border: none; }}

QScrollArea {{ border: none; background: transparent; }}
QSplitter::handle {{ background: {T['border']}; }}
QSplitter::handle:horizontal {{ width: 1px; }}

QComboBox::drop-down {{ border: none; padding: 0 4px; }}
QComboBox QAbstractItemView {{
    background: {T['elevated']};
    border: 1px solid {T['accent']};
    border-radius: 6px;
    selection-background-color: {T['accent']};
    color: {T['text']};
    padding: 2px;
}}

QStatusBar {{
    background: {T['card']};
    color: {T['muted']};
    border-top: 1px solid {T['border']};
    font-size: 11px;
    padding: 0 8px;
}}
QToolTip {{
    background: {T['elevated']};
    color: {T['text']};
    border: 1px solid {T['accent']};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 11px;
}}
QMenu {{
    background: {T['elevated']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    padding: 4px;
}}
QMenu::item {{ padding: 6px 20px 6px 12px; border-radius: 4px; }}
QMenu::item:selected {{ background: {T['accent']}; color: #fff; }}
QMenu::separator {{ height: 1px; background: {T['border']}; margin: 4px 6px; }}
QMessageBox {{ background: {T['card']}; }}
"""


# Convenience accessors so code can read T["key"] without a long dict lookup
def _t(key):
    return T[key]


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

    def emergency_stop(self):
        try:
            self.arm.set_state(4)
        except Exception as e:
            self.error.emit(str(e))

    def set_manual_mode(self):
        try:
            self.arm.set_mode(2)
            self.arm.set_state(0)
        except Exception as e:
            self.error.emit(str(e))

    def set_normal_mode(self):
        try:
            self.arm.set_mode(0)
            self.arm.set_state(0)
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

# One color per joint (J1–J6)
JOINT_COLORS = ["#ff8c00", "#e05252", "#4caf50", "#2196f3", "#9c27b0", "#e91e96"]


# ──────────────────────────────────────────────────────────────────────────────
# UI helpers
# ──────────────────────────────────────────────────────────────────────────────

class ThemedLabel(QLabel):
    """Section header label that re-styles itself on apply_theme()."""
    def __init__(self, text, color_key="accent"):
        super().__init__(text.upper())
        self._color_key = color_key
        self.apply_theme()

    def apply_theme(self):
        c = T[self._color_key]
        self.setStyleSheet(f"""
            color: {c};
            font-size: 9px;
            font-weight: bold;
            letter-spacing: 1.5px;
            padding: 4px 0 2px 8px;
            border-left: 2px solid {c};
            margin-top: 8px;
        """)


def _section_label(text, color_key="accent"):
    return ThemedLabel(text, color_key)


def _jog_button(text, tooltip=""):
    btn = QPushButton(text)
    btn.setFixedHeight(30)
    btn.setMinimumWidth(58)
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


def dpad_style():
    return f"""
    QPushButton {{
        background: {T['elevated']};
        color: {T['text']};
        border: 1px solid {T['border']};
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }}
    QPushButton:hover  {{ background: {T['btn_hover']}; border-color: {T['accent']}; color: {T['accent']}; }}
    QPushButton:pressed {{ background: {T['btn_press']}; }}
    QPushButton:disabled {{ background: {T['btn_dis_bg']}; color: {T['btn_dis_fg']}; border-color: {T['border']}; }}
"""

def _dpad_button(symbol, label, tooltip=""):
    btn = QPushButton(f"{symbol}\n{label}")
    btn.setMinimumSize(54, 54)
    btn.setStyleSheet(dpad_style())
    if tooltip:
        btn.setToolTip(tooltip)
    return btn


def _hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return ", ".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))


def _step_box(default, suffix="mm", decimals=1, min_val=0.1, max_val=500.0):
    sb = QDoubleSpinBox()
    sb.setDecimals(decimals)
    sb.setMinimum(min_val)
    sb.setMaximum(max_val)
    sb.setValue(default)
    sb.setSuffix(f" {suffix}")
    sb.setMinimumWidth(90)
    return sb


# ──────────────────────────────────────────────────────────────────────────────
# Circular compass d-pad widget
# ──────────────────────────────────────────────────────────────────────────────

class CompassPad(QWidget):
    """Circular 4-way d-pad drawn with QPainter. Clicks on each sector emit a signal."""

    north_clicked = pyqtSignal()
    south_clicked = pyqtSignal()
    west_clicked  = pyqtSignal()
    east_clicked  = pyqtSignal()

    def __init__(self, north_label="N", south_label="S", west_label="W", east_label="E"):
        super().__init__()
        self._labels = {"north": north_label, "south": south_label,
                        "west": west_label,   "east":  east_label}
        self._hovered = None
        self._pressed = None
        self.setMouseTracking(True)
        self.setMinimumSize(148, 148)
        self.setMaximumSize(160, 160)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    # ── geometry helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _pt(cx, cy, r, angle_deg):
        """Screen point on circle of radius r at angle_deg (CCW from right, 90=up)."""
        rad = math.radians(angle_deg)
        return cx + r * math.cos(rad), cy - r * math.sin(rad)

    def _radii(self):
        cx, cy = self.width() / 2.0, self.height() / 2.0
        r_out = min(cx, cy) * 0.88
        r_in  = r_out * 0.24
        return cx, cy, r_out, r_in

    def _sector_path(self, cx, cy, r_out, r_in, start_deg, span_deg):
        """Build a donut-slice QPainterPath sector."""
        path = QPainterPath()
        ix0, iy0 = self._pt(cx, cy, r_in, start_deg)
        ox0, oy0 = self._pt(cx, cy, r_out, start_deg)
        path.moveTo(ix0, iy0)
        path.lineTo(ox0, oy0)
        outer_rect = QRectF(cx - r_out, cy - r_out, 2*r_out, 2*r_out)
        path.arcTo(outer_rect, start_deg, span_deg)
        end_deg = start_deg + span_deg
        ix1, iy1 = self._pt(cx, cy, r_in, end_deg)
        path.lineTo(ix1, iy1)
        inner_rect = QRectF(cx - r_in, cy - r_in, 2*r_in, 2*r_in)
        path.arcTo(inner_rect, end_deg, -span_deg)
        path.closeSubpath()
        return path

    # ── hit testing ───────────────────────────────────────────────────────────

    def _sector_at(self, x, y):
        cx, cy, r_out, r_in = self._radii()
        dx, dy = x - cx, y - cy
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < r_in or dist > r_out:
            return None
        # atan2 in screen coords: dy positive = down, so up = negative dy → atan2 gives -90° for up
        angle = math.degrees(math.atan2(dy, dx))
        if -135 <= angle < -45:
            return "north"
        if -45 <= angle < 45:
            return "east"
        if 45 <= angle < 135:
            return "south"
        return "west"

    # ── events ────────────────────────────────────────────────────────────────

    def mouseMoveEvent(self, e):
        sector = self._sector_at(e.x(), e.y()) if self.isEnabled() else None
        if sector != self._hovered:
            self._hovered = sector
            self.update()

    def mousePressEvent(self, e):
        if not self.isEnabled() or e.button() != Qt.LeftButton:
            return
        self._pressed = self._sector_at(e.x(), e.y())
        self.update()

    def mouseReleaseEvent(self, e):
        if not self.isEnabled() or e.button() != Qt.LeftButton:
            return
        sector = self._sector_at(e.x(), e.y())
        if sector and sector == self._pressed:
            getattr(self, f"{sector}_clicked").emit()
        self._pressed = None
        self.update()

    def leaveEvent(self, e):
        self._hovered = None
        self._pressed = None
        self.update()

    # ── painting ──────────────────────────────────────────────────────────────

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        cx, cy, r_out, r_in = self._radii()
        enabled = self.isEnabled()

        # Each sector: (arcTo_start, arcTo_span, label_center_angle_deg)
        SECTORS = {
            "north": (45,  90,  90),
            "east":  (-45, 90,  0),
            "south": (225, 90, 270),
            "west":  (135, 90, 180),
        }

        for name, (start, span, label_angle) in SECTORS.items():
            path = self._sector_path(cx, cy, r_out, r_in, start, span)

            if not enabled:
                fill = QColor(T["btn_dis_bg"])
                text_color = QColor(T["btn_dis_fg"])
            elif name == self._pressed:
                fill = QColor(T["btn_press"])
                text_color = QColor(T["accent"])
            elif name == self._hovered:
                c = QColor(T["accent"])
                c.setAlpha(55)
                fill = c
                text_color = QColor(T["accent"])
            else:
                fill = QColor(T["elevated"])
                text_color = QColor(T["text"])

            p.setPen(QPen(QColor(T["border"]), 1.2))
            p.setBrush(QBrush(fill))
            p.drawPath(path)

            # Label text
            lbl = self._labels.get(name, "")
            if lbl:
                lx, ly = self._pt(cx, cy, r_out * 0.60, label_angle)
                p.setPen(QPen(text_color))
                p.setFont(QFont("Segoe UI", 9, QFont.Bold))
                p.drawText(QRectF(lx - 28, ly - 14, 56, 28), Qt.AlignCenter, lbl)

        # Inner circle
        p.setPen(QPen(QColor(T["border"]), 1.2))
        p.setBrush(QBrush(QColor(T["card"])))
        p.drawEllipse(QRectF(cx - r_in, cy - r_in, 2*r_in, 2*r_in))


# ──────────────────────────────────────────────────────────────────────────────
# Per-joint slider row
# ──────────────────────────────────────────────────────────────────────────────

class JointSliderRow(QWidget):
    """One row per joint: colored label + display slider + angle value + -/+ buttons."""

    jog_requested = pyqtSignal(int, float)  # joint_idx, delta_degrees

    def __init__(self, joint_idx, step_fn, color):
        super().__init__()
        self._idx = joint_idx
        self._step_fn = step_fn
        self._color = color
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(2, 1, 2, 1)
        lay.setSpacing(5)

        lbl = QLabel(f"J{self._idx + 1}")
        lbl.setFixedWidth(22)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(
            f"color: {self._color}; font-weight: bold; font-size: 11px; background: transparent;")

        self._minus = QPushButton("−")
        self._minus.setMinimumSize(32, 30)
        self._minus.setMaximumWidth(36)
        self._minus.setStyleSheet("font-size: 16px; font-weight: bold; padding: 0 4px;")
        self._minus.clicked.connect(
            lambda: self.jog_requested.emit(self._idx, -self._step_fn()))

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(-3600, 3600)
        self._slider.setValue(0)
        self._slider.setEnabled(False)   # display only
        self._slider.setMinimumWidth(60)
        self._apply_slider_style()

        self._plus = QPushButton("+")
        self._plus.setMinimumSize(32, 30)
        self._plus.setMaximumWidth(36)
        self._plus.setStyleSheet("font-size: 16px; font-weight: bold; padding: 0 4px;")
        self._plus.clicked.connect(
            lambda: self.jog_requested.emit(self._idx, +self._step_fn()))

        self._val_lbl = QLabel("   0.0°")
        self._val_lbl.setFixedWidth(62)
        self._val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._val_lbl.setStyleSheet(
            f"color: {self._color}; font-family: 'Courier New', monospace; "
            f"font-size: 12px; font-weight: bold; background: transparent;")

        lay.addWidget(lbl)
        lay.addWidget(self._minus)
        lay.addWidget(self._slider, 1)
        lay.addWidget(self._plus)
        lay.addWidget(self._val_lbl)

    def _apply_slider_style(self):
        c = self._color
        self._slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {T['grid']}; height: 4px; border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {c}; width: 10px; height: 10px;
                border-radius: 5px; margin: -3px 0;
            }}
            QSlider::sub-page:horizontal {{
                background: {c}; border-radius: 2px;
            }}
            QSlider:disabled::groove:horizontal {{ background: {T['grid']}; }}
            QSlider:disabled::sub-page:horizontal {{ background: {T['border']}; }}
            QSlider:disabled::handle:horizontal {{ background: {T['border']}; }}
        """)

    def update_value(self, angle):
        self._slider.setValue(int(angle * 10))
        self._val_lbl.setText(f"{angle:+6.1f}°")

    def set_jog_enabled(self, enabled):
        self._minus.setEnabled(enabled)
        self._plus.setEnabled(enabled)

    def apply_theme(self):
        self._apply_slider_style()
        self._val_lbl.setStyleSheet(
            f"color: {self._color}; font-family: 'Courier New', monospace; "
            f"font-size: 12px; font-weight: bold; background: transparent;")


# ──────────────────────────────────────────────────────────────────────────────
# 3D coordinate axes reference diagram
# ──────────────────────────────────────────────────────────────────────────────

class CoordDiagram(QWidget):
    """Minimal 3D coordinate axes drawn in 2.5D: X forward, Y right, Z up."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 72)
        self.setMaximumHeight(88)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def sizeHint(self):
        return QSize(160, 80)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = float(self.width()), float(self.height())

        # Background
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(T["card"])))
        p.drawRoundedRect(QRectF(0, 0, w, h), 6, 6)

        # Origin — slightly left of center, lower half
        ox = w * 0.38
        oy = h * 0.64
        arm = min(w, h) * 0.36

        def draw_axis(vx, vy, color, label):
            mag = math.sqrt(vx*vx + vy*vy)
            ux, uy = vx / mag, vy / mag
            ex = ox + ux * arm
            ey = oy + uy * arm

            pen = QPen(QColor(color), 2, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen)
            p.drawLine(QPointF(ox, oy), QPointF(ex, ey))

            # Arrowhead
            hlen = arm * 0.22
            hside = arm * 0.12
            nx, ny = -uy, ux          # perpendicular
            p.drawLine(QPointF(ex, ey),
                       QPointF(ex - hlen*ux + hside*nx, ey - hlen*uy + hside*ny))
            p.drawLine(QPointF(ex, ey),
                       QPointF(ex - hlen*ux - hside*nx, ey - hlen*uy - hside*ny))

            # Label beyond tip
            lx = ex + ux * 9
            ly = ey + uy * 9
            p.setPen(QPen(QColor(color)))
            p.setFont(QFont("Segoe UI", 9, QFont.Bold))
            p.drawText(QRectF(lx - 9, ly - 9, 18, 18), Qt.AlignCenter, label)

        # X: forward diagonal (lower-left in screen = depth/forward direction)
        draw_axis(-0.65,  0.52, T["accent"], "X")
        # Y: to the right
        draw_axis( 1.0,   0.0,  T["green"],  "Y")
        # Z: straight up
        draw_axis( 0.0,  -1.0,  T["orange"], "Z")

        # Origin dot
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(T["muted"])))
        p.drawEllipse(QRectF(ox - 3, oy - 3, 6, 6))


# ──────────────────────────────────────────────────────────────────────────────
# Left panel – live position display
# ──────────────────────────────────────────────────────────────────────────────

class LivePositionPanel(QGroupBox):
    def __init__(self):
        super().__init__()
        self._labels = {}
        self._title_lbl = None
        self._group_lbls = []     # (label, color_key)
        self._key_lbls = []       # (label,)
        self._val_lbls = []       # (label, color_key)
        self._unit_lbls = []
        self._row_widgets = []
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(10, 12, 10, 10)

        self._title_lbl = QLabel("LIVE POSITION")
        layout.addWidget(self._title_lbl)
        layout.addSpacing(6)

        groups = [
            ("CARTESIAN", [("X","mm"), ("Y","mm"), ("Z","mm")], "accent"),
            ("ROTATION",  [("Roll","°"), ("Pitch","°"), ("Yaw","°")], "purple"),
            ("DEVICE",    [("Gripper",""), ("Track","mm")], "orange"),
        ]

        for group_name, fields, color_key in groups:
            grp_lbl = QLabel(group_name)
            self._group_lbls.append((grp_lbl, color_key))
            layout.addWidget(grp_lbl)

            for name, unit in fields:
                row_w = QWidget()
                self._row_widgets.append(row_w)
                row = QHBoxLayout(row_w)
                row.setContentsMargins(6, 3, 6, 3)
                row.setSpacing(4)

                key_lbl = QLabel(name)
                key_lbl.setMinimumWidth(52)
                self._key_lbls.append(key_lbl)

                val_lbl = QLabel("—")
                val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self._val_lbls.append((val_lbl, color_key))

                unit_lbl = QLabel(unit)
                unit_lbl.setMinimumWidth(20)
                self._unit_lbls.append(unit_lbl)

                row.addWidget(key_lbl)
                row.addWidget(val_lbl, 1)
                row.addWidget(unit_lbl)
                layout.addWidget(row_w)
                layout.addSpacing(2)
                self._labels[name] = val_lbl

        layout.addStretch()
        self.apply_theme()

    def apply_theme(self):
        self._title_lbl.setStyleSheet(
            f"color: {T['muted']}; font-size: 9px; font-weight: bold; letter-spacing: 1.5px;")
        for grp_lbl, ck in self._group_lbls:
            grp_lbl.setStyleSheet(
                f"color: {T[ck]}; font-size: 8px; font-weight: bold; letter-spacing: 1px; margin-top: 6px;")
        for row_w in self._row_widgets:
            row_w.setStyleSheet(f"background: {T['elevated']}; border-radius: 4px;")
        for key_lbl in self._key_lbls:
            key_lbl.setStyleSheet(f"color: {T['muted']}; font-size: 11px; background: transparent;")
        for val_lbl, ck in self._val_lbls:
            val_lbl.setStyleSheet(
                f"color: {T[ck]}; font-family: 'Courier New', monospace; font-size: 13px; font-weight: bold; background: transparent;")
        for unit_lbl in self._unit_lbls:
            unit_lbl.setStyleSheet(f"color: {T['muted']}; font-size: 10px; background: transparent;")

    def update_position(self, pos, gripper, track):
        keys = ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]
        for i, key in enumerate(keys):
            self._labels[key].setText(f"{pos[i]:.1f}")
        self._labels["Gripper"].setText(str(gripper))
        self._labels["Track"].setText(str(track))


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

        # ── Capture ───────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Capture", "green"))

        cap_lin_btn = QPushButton("⊕  Capture Linear")
        cap_lin_btn.setFixedHeight(40)
        cap_lin_btn.setToolTip("Save cartesian position (playback via set_position)")
        cap_lin_btn.clicked.connect(self.capture_linear_requested)
        self._cap_lin_btn = cap_lin_btn

        cap_ang_btn = QPushButton("⊕  Capture Angular")
        cap_ang_btn.setFixedHeight(40)
        cap_ang_btn.setToolTip("Save joint angles (playback via set_servo_angle)")
        cap_ang_btn.clicked.connect(self.capture_angular_requested)
        self._cap_ang_btn = cap_ang_btn

        lay.addWidget(cap_lin_btn)
        lay.addWidget(cap_ang_btn)

        # ── Navigate saved points ─────────────────────────────────────────────
        lay.addWidget(_section_label("Navigate", "muted"))
        nav_box = QWidget()
        nav_lay = QHBoxLayout(nav_box)
        nav_lay.setContentsMargins(0, 0, 0, 0)
        nav_lay.setSpacing(4)
        prev_btn = QPushButton("← Previous Point")
        next_btn = QPushButton("Next Point →")
        prev_btn.setFixedHeight(32)
        next_btn.setFixedHeight(32)
        prev_btn.setToolTip("Drive robot to previous point in list (jump back one step)")
        next_btn.setToolTip("Drive robot to next point in list (jump forward one step)")
        prev_btn.clicked.connect(self.prev_point_requested)
        next_btn.clicked.connect(self.next_point_requested)
        nav_lay.addWidget(prev_btn)
        nav_lay.addWidget(next_btn)
        lay.addWidget(nav_box)

        lay.addSpacing(6)

        # ── Cartesian ────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Cartesian", "accent"))
        cart_box = QGroupBox()
        cart_outer = QHBoxLayout(cart_box)
        cart_outer.setSpacing(10)
        cart_outer.setContentsMargins(6, 6, 6, 6)

        self._xy_pad = CompassPad("X+", "X−", "Y+", "Y−")
        self._xy_pad.north_clicked.connect(lambda: self._jog_cart("x", +1))
        self._xy_pad.south_clicked.connect(lambda: self._jog_cart("x", -1))
        self._xy_pad.west_clicked.connect(lambda: self._jog_cart("y", +1))
        self._xy_pad.east_clicked.connect(lambda: self._jog_cart("y", -1))
        cart_outer.addWidget(self._xy_pad)

        z_widget = QWidget()
        z_lay = QVBoxLayout(z_widget)
        z_lay.setSpacing(4)
        z_lay.setContentsMargins(0, 0, 0, 0)
        zp = _jog_button("Z+")
        zm = _jog_button("Z−")
        zp.clicked.connect(lambda: self._jog_cart("z", +1))
        zm.clicked.connect(lambda: self._jog_cart("z", -1))
        z_lay.addWidget(zp)
        z_lay.addStretch()
        z_lay.addWidget(zm)
        self._z_up_btn = zp
        self._z_dn_btn = zm
        cart_outer.addWidget(z_widget)
        cart_outer.addStretch()

        cart_step_row = QHBoxLayout()
        cart_step_row.addWidget(QLabel("Step:"))
        self._cart_step = _step_box(5.0, "mm")
        cart_step_row.addWidget(self._cart_step)
        cart_step_row.addStretch()

        cart_wrap = QVBoxLayout()
        cart_wrap.setSpacing(4)
        cart_wrap.addWidget(cart_box)
        cart_wrap.addLayout(cart_step_row)
        lay.addLayout(cart_wrap)

        # ── Rotation ─────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Rotation", "purple"))
        rot_box = QGroupBox()
        rot_outer = QHBoxLayout(rot_box)
        rot_outer.setSpacing(10)
        rot_outer.setContentsMargins(6, 6, 6, 6)

        # RX (Roll) = west/east, RY (Pitch) = north/south
        self._rp_pad = CompassPad("RY+", "RY−", "RX−", "RX+")
        self._rp_pad.north_clicked.connect(lambda: self._jog_cart("pitch", +1))
        self._rp_pad.south_clicked.connect(lambda: self._jog_cart("pitch", -1))
        self._rp_pad.west_clicked.connect(lambda: self._jog_cart("roll", -1))
        self._rp_pad.east_clicked.connect(lambda: self._jog_cart("roll", +1))
        rot_outer.addWidget(self._rp_pad)

        # RZ (Yaw) as a horizontal button pair
        rz_widget = QWidget()
        rz_lay = QVBoxLayout(rz_widget)
        rz_lay.setSpacing(4)
        rz_lay.setContentsMargins(0, 0, 0, 0)
        rz_row = QHBoxLayout()
        rz_row.setSpacing(4)
        rzm = _jog_button("RZ−")
        rzp = _jog_button("RZ+")
        rzm.clicked.connect(lambda: self._jog_cart("yaw", -1))
        rzp.clicked.connect(lambda: self._jog_cart("yaw", +1))
        rz_row.addWidget(rzm)
        rz_row.addWidget(rzp)
        rz_lay.addStretch()
        rz_lay.addLayout(rz_row)
        rz_lay.addStretch()
        self._rz_m_btn = rzm
        self._rz_p_btn = rzp
        rot_outer.addWidget(rz_widget)
        rot_outer.addStretch()

        self._rot_step = _step_box(45.0, "°", min_val=1.0, max_val=360.0)
        rot_step_row = QHBoxLayout()
        rot_step_row.addWidget(QLabel("Step:"))
        rot_step_row.addWidget(self._rot_step)
        rot_step_row.addStretch()

        rot_wrap = QVBoxLayout()
        rot_wrap.setSpacing(4)
        rot_wrap.addWidget(rot_box)
        rot_wrap.addLayout(rot_step_row)
        lay.addLayout(rot_wrap)

        # Coordinate axes reference diagram
        self._coord_diagram = CoordDiagram()
        lay.addWidget(self._coord_diagram)

        # ── Track ─────────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Linear Track", "orange"))
        track_box = QGroupBox()
        track_inner = QVBoxLayout(track_box)
        track_inner.setSpacing(3)
        track_inner.setContentsMargins(8, 8, 8, 8)

        # Slider row: [-] [○--------] [+]  600mm
        track_row = QWidget()
        tr_lay = QHBoxLayout(track_row)
        tr_lay.setContentsMargins(2, 1, 2, 1)
        tr_lay.setSpacing(5)

        self._track_minus = QPushButton("−")
        self._track_minus.setMinimumSize(32, 30)
        self._track_minus.setMaximumWidth(36)
        self._track_minus.setStyleSheet("font-size: 16px; font-weight: bold; padding: 0 4px;")
        self._track_minus.clicked.connect(
            lambda: self.track_jog_requested.emit(-self._track_step.value()))

        self._track_slider = QSlider(Qt.Horizontal)
        self._track_slider.setRange(0, 1000)
        self._track_slider.setValue(500)
        self._track_slider.setEnabled(False)
        self._track_slider.setMinimumWidth(60)

        self._track_plus = QPushButton("+")
        self._track_plus.setMinimumSize(32, 30)
        self._track_plus.setMaximumWidth(36)
        self._track_plus.setStyleSheet("font-size: 16px; font-weight: bold; padding: 0 4px;")
        self._track_plus.clicked.connect(
            lambda: self.track_jog_requested.emit(+self._track_step.value()))

        self._track_val_lbl = QLabel(" 500mm")
        self._track_val_lbl.setFixedWidth(64)
        self._track_val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        tr_lay.addWidget(self._track_minus)
        tr_lay.addWidget(self._track_slider, 1)
        tr_lay.addWidget(self._track_plus)
        tr_lay.addWidget(self._track_val_lbl)
        track_inner.addWidget(track_row)

        self._track_step = _step_box(10.0, "mm")
        tstep_row = QHBoxLayout()
        tstep_row.addWidget(QLabel("Track step:"))
        tstep_row.addWidget(self._track_step)
        tstep_row.addStretch()
        track_inner.addLayout(tstep_row)
        lay.addWidget(track_box)

        # ── Gripper ───────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Gripper", "green"))
        grip_box = QGroupBox()
        grip_inner = QVBoxLayout(grip_box)
        grip_inner.setSpacing(4)
        grip_inner.setContentsMargins(8, 8, 8, 8)
        # Row 1: value input + Set button
        grip_row1 = QHBoxLayout()
        self._grip_input = QSpinBox()
        self._grip_input.setRange(0, 850)
        self._grip_input.setValue(500)
        self._grip_input.setMinimumWidth(80)
        set_btn = QPushButton("Set")
        set_btn.setMinimumWidth(52)
        set_btn.clicked.connect(lambda: self.gripper_requested.emit(self._grip_input.value()))
        grip_row1.addWidget(QLabel("Value (0–850):"))
        grip_row1.addWidget(self._grip_input)
        grip_row1.addWidget(set_btn)
        grip_row1.addStretch()
        grip_inner.addLayout(grip_row1)
        # Row 2: Open / Close buttons
        grip_row2 = QHBoxLayout()
        open_btn = QPushButton("Completely Open (850)")
        open_btn.clicked.connect(lambda: (self._grip_input.setValue(850), self.gripper_requested.emit(850)))
        close_btn = QPushButton("Completely Closed (0)")
        close_btn.clicked.connect(lambda: (self._grip_input.setValue(0), self.gripper_requested.emit(0)))
        grip_row2.addWidget(open_btn)
        grip_row2.addWidget(close_btn)
        grip_inner.addLayout(grip_row2)
        lay.addWidget(grip_box)

        # ── Joints ────────────────────────────────────────────────────────────
        lay.addWidget(_section_label("Joints", "joint"))
        joint_box = QGroupBox()
        joint_inner = QVBoxLayout(joint_box)
        joint_inner.setSpacing(3)
        joint_inner.setContentsMargins(8, 8, 8, 8)

        self._joint_step = _step_box(1.0, "°", min_val=0.1, max_val=180.0)
        self._joint_rows = []
        for j in range(6):
            row = JointSliderRow(j, lambda: self._joint_step.value(), JOINT_COLORS[j])
            row.jog_requested.connect(self.jog_joint_requested)
            self._joint_rows.append(row)
            joint_inner.addWidget(row)

        jstep_row = QHBoxLayout()
        jstep_row.addWidget(QLabel("Joint step:"))
        jstep_row.addWidget(self._joint_step)
        jstep_row.addStretch()
        joint_inner.addSpacing(4)
        joint_inner.addLayout(jstep_row)
        lay.addWidget(joint_box)

        # refs for enable/disable
        self._jog_widgets = [
            rot_box, track_box, grip_box, joint_box,
            prev_btn, next_btn,
        ]
        self._capture_widgets = [cap_lin_btn, cap_ang_btn]
        self._extra_jog_btns = [zp, zm, rzm, rzp]
        self._dpad_buttons = []  # kept for backward-compat; compass pads are self-managing

    def _jog_cart(self, axis, sign):
        if axis in ("roll", "pitch", "yaw"):
            step = self._rot_step.value() * sign
        else:
            step = self._cart_step.value() * sign
        self.jog_requested.emit(axis, step)

    def _jog_joint(self, idx, sign):
        step = self._joint_step.value() * sign
        self.jog_joint_requested.emit(idx, step)

    def update_joints(self, joints):
        """Update joint slider displays with current robot angles."""
        for i, row in enumerate(self._joint_rows):
            if i < len(joints):
                row.update_value(joints[i])

    def update_track(self, track_pos):
        """Update track slider display with current track position."""
        self._track_slider.setValue(int(track_pos))
        self._track_val_lbl.setText(f"{int(track_pos):4d}mm")

    def apply_theme(self):
        # extra jog buttons (Z, RZ)
        for btn in self._extra_jog_btns:
            btn.setStyleSheet(dpad_style())
        # compass pads repaint using T directly
        self._xy_pad.update()
        self._rp_pad.update()
        # coord diagram
        self._coord_diagram.update()
        # track slider (single handle, no filled bar)
        oc = T["orange"]
        self._track_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {T['grid']}; height: 4px; border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {oc}; width: 12px; height: 12px;
                border-radius: 6px; margin: -4px 0;
                border: 2px solid {T['card']};
            }}
            QSlider::sub-page:horizontal {{ background: transparent; }}
            QSlider::add-page:horizontal {{ background: transparent; }}
            QSlider:disabled::handle:horizontal {{ background: {T['muted']}; }}
        """)
        self._track_val_lbl.setStyleSheet(
            f"color: {T['orange']}; font-family: 'Courier New', monospace; "
            f"font-size: 12px; font-weight: bold; background: transparent;")
        # joint rows
        for row in self._joint_rows:
            row.apply_theme()
        # tinted capture buttons
        for btn, ck in [(self._cap_lin_btn, "green"), (self._cap_ang_btn, "purple")]:
            c = T[ck]
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: rgba({_hex_to_rgb(c)}, 0.15);
                    color: {c};
                    border: 1px solid rgba({_hex_to_rgb(c)}, 0.4);
                    border-radius: 6px; font-size: 12px; font-weight: bold; padding: 0 10px;
                }}
                QPushButton:hover {{ background: rgba({_hex_to_rgb(c)}, 0.28); border-color: {c}; }}
                QPushButton:pressed {{ background: rgba({_hex_to_rgb(c)}, 0.4); }}
                QPushButton:disabled {{ background: {T['btn_dis_bg']}; color: {T['btn_dis_fg']}; border-color: {T['border']}; }}
            """)
        # section labels
        for w in self.widget().findChildren(ThemedLabel):
            w.apply_theme()

    def set_enabled(self, enabled):
        for w in self._jog_widgets:
            w.setEnabled(enabled)
        for w in self._capture_widgets:
            w.setEnabled(enabled)
        for btn in self._extra_jog_btns:
            btn.setEnabled(enabled)
        self._xy_pad.setEnabled(enabled)
        self._rp_pad.setEnabled(enabled)
        self._track_minus.setEnabled(enabled)
        self._track_plus.setEnabled(enabled)
        for row in self._joint_rows:
            row.set_jog_enabled(enabled)

    def set_capture_enabled(self, enabled):
        """Enable only the capture buttons (used in manual mode)."""
        for w in self._capture_widgets:
            w.setEnabled(enabled)


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

        # column widths
        self._table.setColumnWidth(COL_IDX["#"],       34)
        self._table.setColumnWidth(COL_IDX["Gripper"], 68)
        self._table.setColumnWidth(COL_IDX["Track"],   68)
        self._table.setColumnWidth(COL_IDX["Type"],    72)
        for col in ["X", "Y", "Z", "Roll", "Pitch", "Yaw"]:
            self._table.setColumnWidth(COL_IDX[col], 72)

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

    def commit_editor(self):
        """Close any open cell editor and commit its value to the table item.

        Call this before any Go To / navigation action so that in-progress edits
        are never silently discarded.
        """
        editor = self._table.focusWidget()
        if editor and editor is not self._table:
            # Closing the persistent editor via the index is the Qt-recommended way.
            idx = self._table.currentIndex()
            if idx.isValid():
                self._table.commitData(editor)
                self._table.closeEditor(editor,
                                        QStyledItemDelegate.SubmitModelCache)
        # Now force a sync so self._points is up to date.
        self._sync_points_from_table()

    def get_point(self, row):
        """Return the current (live) point dict for *row*, always reading from
        the table widget so that any manual edits are included.

        Always call ``commit_editor()`` first if an editor might be open.
        """
        return self._row_to_point(row)

    def update_current_position(self, pos, gripper, track):
        self._current_pos = {"x": pos[0], "y": pos[1], "z": pos[2],
                             "roll": pos[3], "pitch": pos[4], "yaw": pos[5],
                             "gripper": gripper, "track": track}
        self._highlight_at_position()

    def apply_theme(self):
        for row in range(self._table.rowCount()):
            type_item = self._table.item(row, COL_IDX["Type"])
            num_item  = self._table.item(row, COL_IDX["#"])
            if type_item:
                ck = "purple" if type_item.text() == "angular" else "accent"
                type_item.setForeground(QColor(T[ck]))
            if num_item:
                num_item.setForeground(QColor(T["muted"]))

    # ── internal helpers ──────────────────────────────────────────────────────

    def _refresh_table(self):
        self._table.blockSignals(True)
        self._table.setRowCount(0)
        for idx, pt in enumerate(self._points):
            self._insert_row(idx, pt)
        self._table.blockSignals(False)

    def _insert_row(self, row, pt):
        self._table.insertRow(row)
        ptype = pt.get("type", "linear")
        data = [
            str(row + 1),
            pt.get("name", f"point_{row+1}"),
            f"{pt['x']:.2f}", f"{pt['y']:.2f}", f"{pt['z']:.2f}",
            f"{pt['roll']:.2f}", f"{pt['pitch']:.2f}", f"{pt['yaw']:.2f}",
            str(pt["gripper"]), str(pt["track"]),
            ptype,
        ]
        type_color = QColor(T["purple"]) if ptype == "angular" else QColor(T["accent"])
        for col, val in enumerate(data):
            item = QTableWidgetItem(val)
            if col == COL_IDX["#"]:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                item.setForeground(QColor(T["muted"]))
            elif col == COL_IDX["Type"]:
                item.setForeground(type_color)
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
        self.commit_editor()
        pt = copy.deepcopy(self.get_point(row))
        insert_at = row + 1
        self._table.blockSignals(True)
        self._insert_row(insert_at, pt)
        self._points.insert(insert_at, pt)
        self._renumber()
        self._table.blockSignals(False)
        self._dirty = True

    def _go_to_row(self, row):
        self.commit_editor()            # flush any in-progress cell edit first
        pt = self.get_point(row)        # read live table values
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

        def _read_float(row, col):
            item = self._table.item(row, col)
            try:
                return float(item.text()) if item else 0.0
            except ValueError:
                return 0.0

        # Compute which rows are "at position" BEFORE blocking signals,
        # so self._points is never read inside the blocked window.
        highlights = []
        for row in range(self._table.rowCount()):
            at = (
                abs(_read_float(row, COL_IDX["X"])     - cp["x"])     <= AT_POSITION_TOLERANCE_MM and
                abs(_read_float(row, COL_IDX["Y"])     - cp["y"])     <= AT_POSITION_TOLERANCE_MM and
                abs(_read_float(row, COL_IDX["Z"])     - cp["z"])     <= AT_POSITION_TOLERANCE_MM and
                abs(_read_float(row, COL_IDX["Roll"])  - cp["roll"])  <= AT_POSITION_TOLERANCE_DEG and
                abs(_read_float(row, COL_IDX["Pitch"]) - cp["pitch"]) <= AT_POSITION_TOLERANCE_DEG and
                abs(_read_float(row, COL_IDX["Yaw"])   - cp["yaw"])   <= AT_POSITION_TOLERANCE_DEG
            )
            highlights.append(at)

        # Apply background colours with signals blocked so itemChanged
        # (background role) doesn't trigger a spurious _sync_points_from_table.
        self._table.blockSignals(True)
        for row, at in enumerate(highlights):
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
# Compact horizontal live position bar (sits below the position table)
# ──────────────────────────────────────────────────────────────────────────────

class LivePositionBar(QWidget):
    """Two-row live position readout shown below the position table."""

    def __init__(self):
        super().__init__()
        self.setFixedHeight(80)
        self._val_labels = {}   # key → QLabel
        self._theme_items = []  # (role, widget, color_key?)
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Row 1: cartesian + rotation + device ─────────────────────────────
        row1_w = QWidget()
        lay = QHBoxLayout(row1_w)
        lay.setContentsMargins(12, 4, 12, 2)
        lay.setSpacing(0)

        def add_title(text, layout):
            lbl = QLabel(text)
            self._theme_items.append(("title", lbl))
            layout.addWidget(lbl)
            layout.addSpacing(16)

        def add_field(key, display, unit, ck, layout):
            k = QLabel(display)
            self._theme_items.append(("key", k))
            v = QLabel("—")
            self._val_labels[key] = v
            self._theme_items.append(("val", v, ck))
            layout.addWidget(k)
            layout.addSpacing(3)
            layout.addWidget(v)
            if unit:
                u = QLabel(unit)
                self._theme_items.append(("unit", u))
                layout.addSpacing(2)
                layout.addWidget(u)
            layout.addSpacing(14)

        def add_sep(layout, height=28):
            f = QFrame()
            f.setFrameShape(QFrame.VLine)
            f.setFixedHeight(height)
            self._theme_items.append(("sep", f))
            layout.addWidget(f)
            layout.addSpacing(12)

        add_title("LIVE", lay)
        add_field("X",     "X",          "mm", "accent",  lay)
        add_field("Y",     "Y",          "mm", "accent",  lay)
        add_field("Z",     "Z",          "mm", "accent",  lay)
        add_sep(lay)
        add_field("Roll",  "Roll / RX",  "°",  "purple",  lay)
        add_field("Pitch", "Pitch / RY", "°",  "purple",  lay)
        add_field("Yaw",   "Yaw / RZ",   "°",  "purple",  lay)
        add_sep(lay)
        add_field("Gripper", "Gripper",  "",   "orange",  lay)
        add_field("Track",   "Track",    "mm", "orange",  lay)
        lay.addStretch()
        outer.addWidget(row1_w)

        # ── Divider ───────────────────────────────────────────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setFixedHeight(1)
        self._theme_items.append(("hdiv", div))
        outer.addWidget(div)

        # ── Row 2: joint values ───────────────────────────────────────────────
        row2_w = QWidget()
        lay2 = QHBoxLayout(row2_w)
        lay2.setContentsMargins(12, 2, 12, 4)
        lay2.setSpacing(0)

        jt_title = QLabel("JOINTS")
        self._theme_items.append(("title", jt_title))
        lay2.addWidget(jt_title)
        lay2.addSpacing(16)

        for i, label in enumerate(["J1", "J2", "J3", "J4", "J5", "J6"]):
            color = JOINT_COLORS[i]
            k = QLabel(label)
            self._theme_items.append(("jkey", k, color))
            v = QLabel("—")
            self._val_labels[label] = v
            self._theme_items.append(("jval", v, color))
            lay2.addWidget(k)
            lay2.addSpacing(3)
            lay2.addWidget(v)
            u = QLabel("°")
            self._theme_items.append(("unit", u))
            lay2.addSpacing(2)
            lay2.addWidget(u)
            lay2.addSpacing(14)

        lay2.addStretch()
        outer.addWidget(row2_w)

        self.apply_theme()

    def update_position(self, pos, gripper, track):
        for key, idx in [("X",0),("Y",1),("Z",2),("Roll",3),("Pitch",4),("Yaw",5)]:
            self._val_labels[key].setText(f"{pos[idx]:.1f}")
        self._val_labels["Gripper"].setText(str(gripper))
        self._val_labels["Track"].setText(str(track))

    def update_joints(self, joints):
        for i, label in enumerate(["J1", "J2", "J3", "J4", "J5", "J6"]):
            if i < len(joints):
                self._val_labels[label].setText(f"{joints[i]:.1f}")

    def apply_theme(self):
        self.setStyleSheet(
            f"background: {T['card']}; border-top: 1px solid {T['border']};")
        for item in self._theme_items:
            role = item[0]
            w    = item[1]
            if role == "title":
                w.setStyleSheet(
                    f"color: {T['muted']}; font-size: 9px; font-weight: bold; "
                    f"letter-spacing: 1px; background: transparent;")
            elif role == "key":
                w.setStyleSheet(
                    f"color: {T['muted']}; font-size: 10px; background: transparent;")
            elif role == "val":
                ck = item[2]
                w.setStyleSheet(
                    f"color: {T[ck]}; font-family: 'Courier New', monospace; "
                    f"font-size: 13px; font-weight: bold; background: transparent;")
            elif role == "unit":
                w.setStyleSheet(
                    f"color: {T['muted']}; font-size: 10px; background: transparent;")
            elif role == "sep":
                w.setStyleSheet(f"color: {T['border']}; background: transparent;")
            elif role == "hdiv":
                w.setStyleSheet(f"background: {T['border']};")
            elif role == "jkey":
                color = item[2]
                w.setStyleSheet(
                    f"color: {color}; font-size: 10px; font-weight: bold; background: transparent;")
            elif role == "jval":
                color = item[2]
                w.setStyleSheet(
                    f"color: {color}; font-family: 'Courier New', monospace; "
                    f"font-size: 13px; font-weight: bold; background: transparent;")


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
        self._manual_mode = False

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
        top_bar.setStyleSheet(f"background: {T['card']}; border-bottom: 1px solid {T['border']};")
        top_bar.setFixedHeight(52)
        top_lay = QHBoxLayout(top_bar)
        top_lay.setContentsMargins(14, 0, 14, 0)
        top_lay.setSpacing(10)

        # app name
        app_name = QLabel("SLURRYBOT")
        sub_name = QLabel("Visual Jogger")
        self._app_name_lbl = app_name
        self._sub_name_lbl = sub_name
        name_col = QVBoxLayout()
        name_col.setSpacing(0)
        name_col.addWidget(app_name)
        name_col.addWidget(sub_name)

        # status dot
        self._status_indicator = QLabel("●")
        self._status_indicator.setStyleSheet(f"color: {T['red']}; font-size: 14px; background: transparent;")
        self._status_indicator.setToolTip("Robot connection status")

        # connect button — initial style applied by apply_theme() at end of _build_ui
        self._connect_btn = QPushButton("Connect")
        self._connect_btn.setFixedSize(100, 32)
        self._connect_btn.clicked.connect(self._toggle_connection)

        # speed label + slider
        speed_lbl = QLabel("Speed:")
        speed_lbl.setStyleSheet("background: transparent;")
        self._speed_lbl = speed_lbl
        self._speed_slider = QSlider(Qt.Horizontal)
        self._speed_slider.setRange(1, 200)
        self._speed_slider.setValue(20)
        self._speed_slider.setFixedWidth(100)
        self._speed_slider.setToolTip("Jog speed (mm/s or °/s)")
        self._speed_val_lbl = QLabel("20")
        self._speed_val_lbl.setFixedWidth(32)
        self._speed_val_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._speed_slider.valueChanged.connect(
            lambda v: self._speed_val_lbl.setText(str(v)))

        # file area
        self._file_label = QLabel("No file loaded")

        def _header_btn(text):
            btn = QPushButton(text)
            btn.setFixedHeight(30)
            return btn

        open_btn = _header_btn("Open")
        open_btn.clicked.connect(self._open_file)
        new_btn = _header_btn("New")
        new_btn.clicked.connect(self._new_file)
        save_btn = _header_btn("Save")
        save_btn.clicked.connect(self._save_file)
        self._save_btn = save_btn

        # STOP button — large, red, always visible
        self._stop_btn = QPushButton("■  STOP")
        self._stop_btn.setFixedSize(90, 36)
        self._stop_btn.setToolTip(
            "Halt all robot motion (arm.set_state(4)).\n"
            "After stopping, use Disconnect → Connect to resume."
        )
        self._stop_btn.clicked.connect(self._emergency_stop)

        # Manual Mode toggle button
        self._manual_btn = QPushButton("✋  Manual Mode")
        self._manual_btn.setFixedHeight(36)
        self._manual_btn.setMinimumWidth(140)
        self._manual_btn.setCheckable(True)
        self._manual_btn.setToolTip(
            "Enable Manual Mode: move the arm by hand.\n"
            "Jog buttons are disabled. Use Capture to save positions."
        )
        self._manual_btn.clicked.connect(self._toggle_manual_mode)
        self._manual_btn.setEnabled(False)  # enabled only when robot is connected

        self._theme_btn = QPushButton("🌙")
        self._theme_btn.setFixedSize(30, 30)
        self._theme_btn.setToolTip("Switch to dark mode")
        self._theme_btn.clicked.connect(self._toggle_theme)

        top_lay.addLayout(name_col)
        top_lay.addSpacing(20)
        top_lay.addWidget(self._status_indicator)
        top_lay.addWidget(self._connect_btn)
        top_lay.addSpacing(12)
        top_lay.addWidget(speed_lbl)
        top_lay.addWidget(self._speed_slider)
        top_lay.addWidget(self._speed_val_lbl)
        top_lay.addSpacing(8)
        top_lay.addWidget(self._file_label, 1)
        top_lay.addWidget(open_btn)
        top_lay.addWidget(new_btn)
        top_lay.addWidget(save_btn)
        top_lay.addSpacing(8)
        top_lay.addWidget(self._manual_btn)
        top_lay.addSpacing(6)
        top_lay.addWidget(self._stop_btn)
        top_lay.addSpacing(4)
        top_lay.addWidget(self._theme_btn)

        # ── panels ────────────────────────────────────────────────────────────
        self._jog_panel = JogPanel()
        self._jog_panel.setMinimumWidth(310)
        self._jog_panel.setMaximumWidth(460)

        self._pos_table = PositionTable()
        self._live_bar = LivePositionBar()

        # connect jog signals to robot worker
        self._jog_panel.jog_requested.connect(
            lambda axis, delta: self._robot.jog_cartesian(axis, delta,
                                                          speed=self._speed_slider.value()))
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

        # Right side: table on top, live bar pinned to bottom
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(0)
        right_lay.addWidget(self._pos_table, 1)
        right_lay.addWidget(self._live_bar)
        self._right_widget = right_widget

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._jog_panel)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([380, 1020])

        self._top_bar = top_bar

        # Manual Mode banner (hidden by default)
        self._manual_banner = QLabel("✋  MANUAL MODE ACTIVE  —  Move arm by hand, then press Capture")
        self._manual_banner.setAlignment(Qt.AlignCenter)
        self._manual_banner.setFixedHeight(32)
        self._manual_banner.setVisible(False)
        self._manual_banner.setObjectName("ManualBanner")

        content = QWidget()
        self._content = content
        content_lay = QVBoxLayout(content)
        content_lay.setContentsMargins(8, 8, 8, 8)
        content_lay.setSpacing(0)
        content_lay.addWidget(splitter)

        # ── assemble ──────────────────────────────────────────────────────────
        central = QWidget()
        self._central = central
        main_lay = QVBoxLayout(central)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)
        main_lay.addWidget(top_bar)
        main_lay.addWidget(self._manual_banner)
        main_lay.addWidget(content, 1)

        self.setCentralWidget(central)
        self.setStatusBar(QStatusBar())
        self.apply_theme()

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
        self._live_bar.update_position(pos, gripper, track)
        self._live_bar.update_joints(joints)
        self._pos_table.update_current_position(pos, gripper, track)
        self._jog_panel.update_joints(joints)
        self._jog_panel.update_track(track)

    def _on_connection_changed(self, connected):
        self._robot_connected = connected
        self._apply_connect_btn_style(connected)
        self.statusBar().showMessage("Robot connected" if connected else "Robot disconnected")
        self._manual_btn.setEnabled(connected)
        if not connected and self._manual_mode:
            # Exit manual mode silently when robot disconnects
            self._manual_mode = False
            self._apply_manual_mode_ui()
        elif connected:
            self._jog_panel.set_enabled(True)
        else:
            self._jog_panel.set_enabled(False)

    def _apply_manual_btn_default_style(self):
        c = T["orange"]
        self._manual_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba({_hex_to_rgb(c)}, 0.12); color: {c};
                border: 1px solid rgba({_hex_to_rgb(c)}, 0.4);
                border-radius: 6px; font-weight: bold; font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba({_hex_to_rgb(c)}, 0.25); border-color: {c}; }}
            QPushButton:pressed {{ background: rgba({_hex_to_rgb(c)}, 0.4); }}
        """)

    def _apply_connect_btn_style(self, connected):
        dot_color = T["green"] if connected else T["red"]
        btn_color = T["red"] if connected else T["green"]
        label     = "Disconnect" if connected else "Connect"
        self._status_indicator.setStyleSheet(
            f"color: {dot_color}; font-size: 14px; background: transparent;")
        self._connect_btn.setText(label)
        self._connect_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba({_hex_to_rgb(btn_color)}, 0.15);
                color: {btn_color};
                border: 1px solid rgba({_hex_to_rgb(btn_color)}, 0.4);
                border-radius: 6px; font-weight: bold; font-size: 12px;
            }}
            QPushButton:hover {{
                background: rgba({_hex_to_rgb(btn_color)}, 0.28);
                border-color: {btn_color};
            }}
        """)

    def _on_robot_error(self, msg):
        self.statusBar().showMessage(f"Error: {msg}", 5000)

    # ── theme ─────────────────────────────────────────────────────────────────

    def _toggle_theme(self):
        is_light = T["bg"] == LIGHT_THEME["bg"]
        T.update(DARK_THEME if is_light else LIGHT_THEME)
        self._theme_btn.setText("☀" if is_light else "🌙")
        self._theme_btn.setToolTip("Switch to light mode" if is_light else "Switch to dark mode")
        QApplication.instance().setStyleSheet(build_stylesheet())
        self.apply_theme()

    def apply_theme(self):
        # top bar
        self._top_bar.setStyleSheet(
            f"background: {T['card']}; border-bottom: 1px solid {T['border']};")
        self._central.setStyleSheet(f"background: {T['bg']};")
        self._content.setStyleSheet(f"background: {T['bg']};")
        self._app_name_lbl.setStyleSheet(
            f"color: {T['accent']}; font-size: 15px; font-weight: bold; letter-spacing: 2px; background: transparent;")
        self._sub_name_lbl.setStyleSheet(
            f"color: {T['muted']}; font-size: 11px; background: transparent;")
        self._file_label.setStyleSheet(
            f"color: {T['muted']}; font-size: 11px; background: transparent;")
        self._speed_lbl.setStyleSheet(f"color: {T['muted']}; font-size: 11px; background: transparent;")
        self._speed_val_lbl.setStyleSheet(f"color: {T['text']}; font-size: 11px; background: transparent;")
        # speed slider
        m = T["muted"]
        self._speed_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {T['grid']}; height: 4px; border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {T['accent']}; width: 12px; height: 12px;
                border-radius: 6px; margin: -4px 0;
            }}
            QSlider::sub-page:horizontal {{ background: {T['accent']}; border-radius: 2px; }}
        """)
        # STOP button — always red
        r = T["red"]
        self._stop_btn.setStyleSheet(f"""
            QPushButton {{
                background: {r}; color: #ffffff;
                border: none; border-radius: 6px;
                font-weight: bold; font-size: 13px;
            }}
            QPushButton:hover {{ background: rgba({_hex_to_rgb(r)}, 0.82); }}
            QPushButton:pressed {{ background: rgba({_hex_to_rgb(r)}, 0.65); }}
        """)
        # save btn tinted
        a = T["accent"]
        self._save_btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba({_hex_to_rgb(a)}, 0.15); color: {a};
                border: 1px solid rgba({_hex_to_rgb(a)}, 0.4);
                border-radius: 6px; padding: 4px 12px; font-weight: bold; height: 30px;
            }}
            QPushButton:hover {{ background: rgba({_hex_to_rgb(a)}, 0.28); border-color: {a}; }}
        """)
        # connection button
        self._apply_connect_btn_style(self._robot_connected)
        # manual mode button (re-apply correct style for current state)
        if self._manual_mode:
            self._apply_manual_mode_ui()
        else:
            self._apply_manual_btn_default_style()
        # right widget background
        self._right_widget.setStyleSheet(f"background: {T['bg']};")
        # sub-panels
        self._live_bar.apply_theme()
        self._jog_panel.apply_theme()
        # re-color type column cells
        self._pos_table.apply_theme()

    def _toggle_connection(self):
        if self._robot_connected:
            self._robot.disconnect_robot()
        else:
            self._robot.connect_robot()

    def _toggle_manual_mode(self):
        if not self._manual_mode:
            # Activating — no confirmation needed
            self._manual_mode = True
            self._robot.set_manual_mode()
            self._apply_manual_mode_ui()
        else:
            # Deactivating — ask for confirmation to avoid accidental exit
            reply = QMessageBox.question(
                self, "Exit Manual Mode",
                "Deactivate Manual Mode and return to normal jog control?\n\n"
                "The arm will be set back to position mode (mode 0).",
                QMessageBox.Yes | QMessageBox.Cancel,
                QMessageBox.Cancel,
            )
            if reply == QMessageBox.Yes:
                self._manual_mode = False
                self._robot.set_normal_mode()
                self._apply_manual_mode_ui()
            else:
                # User cancelled — keep button checked
                self._manual_btn.setChecked(True)

    def _apply_manual_mode_ui(self):
        active = self._manual_mode
        g = T["green"]

        # Banner visibility
        self._manual_banner.setVisible(active)

        # Button style
        if active:
            self._manual_btn.setChecked(True)
            self._manual_btn.setStyleSheet(f"""
                QPushButton {{
                    background: {g}; color: #ffffff;
                    border: none; border-radius: 6px;
                    font-weight: bold; font-size: 13px;
                }}
                QPushButton:hover {{ background: rgba({_hex_to_rgb(g)}, 0.82); }}
                QPushButton:pressed {{ background: rgba({_hex_to_rgb(g)}, 0.65); }}
            """)
            self._manual_banner.setStyleSheet(
                f"background: {g}; color: #ffffff; "
                f"font-size: 13px; font-weight: bold; letter-spacing: 0.5px;")
        else:
            self._manual_btn.setChecked(False)
            self._apply_manual_btn_default_style()

        # When manual mode is active: disable jog controls but keep captures enabled
        if self._robot_connected:
            if active:
                self._jog_panel.set_enabled(False)
                self._jog_panel.set_capture_enabled(True)
            else:
                self._jog_panel.set_enabled(True)

    def _emergency_stop(self):
        self._robot.emergency_stop()
        self.statusBar().showMessage("EMERGENCY STOP sent", 5000)

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
        # Commit any open cell editor and sync _points before reading values.
        self._pos_table.commit_editor()
        pt = self._pos_table.get_point(index)   # always live table values
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

    def _apply_palette():
        palette = QPalette()
        palette.setColor(QPalette.Window,          QColor(T["card"]))
        palette.setColor(QPalette.WindowText,      QColor(T["text"]))
        palette.setColor(QPalette.Base,            QColor(T["bg"]))
        palette.setColor(QPalette.AlternateBase,   QColor(T["card"]))
        palette.setColor(QPalette.Text,            QColor(T["text"]))
        palette.setColor(QPalette.Button,          QColor(T["elevated"]))
        palette.setColor(QPalette.ButtonText,      QColor(T["text"]))
        palette.setColor(QPalette.Highlight,       QColor(T["accent"]))
        palette.setColor(QPalette.HighlightedText, QColor(T["text"]))
        palette.setColor(QPalette.ToolTipBase,     QColor(T["elevated"]))
        palette.setColor(QPalette.ToolTipText,     QColor(T["text"]))
        app.setPalette(palette)

    _apply_palette()
    app.setStyleSheet(build_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
