# Slurrybot System Documentation

## System Overview

The Slurrybot system consists of four components that work together:

```
keyboard_jogger.py    → teaches positions by jogging the robot manually
Robot_wrapper.py      → controls the robot, reads positions from txt files
Config/config.txt     → stores gripper values and rack spacings
Positions/*.txt       → store all robot positions (taught with jogger)
```

---

## Directory Structure

```
SlurryBot/
├── keyboard_jogger.py
├── Robot_wrapper.py
├── Config/
│   └── config.txt
├── Positions/
│   ├── initial_point.txt
│   ├── vial1_pickup.txt
│   ├── vial4_pickup.txt
│   ├── vial_to_scale.txt
│   ├── scale_to_liquid_rest.txt
│   ├── place_funnel.txt
│   ├── replace_funnel.txt
│   ├── pipette_pickup.txt
│   ├── putting_back_pipette.txt
│   ├── tip1_get.txt
│   ├── tip1_putback.txt
│   ├── tip1_take_liquid.txt
│   ├── tip1_liquid_to_vial.txt
│   ├── pickup_large.txt
│   ├── replace_big_spatula.txt
│   ├── pickup_medium.txt
│   ├── replace_medium_spatula.txt
│   ├── scoop_big_middle.txt
│   ├── scoop_big_left.txt
│   ├── scoop_big_right.txt
│   ├── scoop_medium_left.txt
│   ├── scoop_medium_right.txt
│   ├── scoop_medium_middle.txt
│   ├── scoop_medium_farleft.txt
│   ├── scoop_tiny.txt
│   ├── scoop_tiny_left.txt
│   └── scoop_tiny_right.txt
└── Testing/
    └── Testground.ipynb
```

---

## How Positions Work

Every movement the robot makes is stored in a txt file. Each point in the file has exactly 5 lines:

```
point_name cartesian: [x, y, z, roll, pitch, yaw]
point_name angular:   [j1, j2, j3, j4, j5, j6]
Gripper: <value>
Track:   <value>
Type:    linear / angular
```

The robot executes all points in a file sequentially. After each movement it automatically sets the gripper and track if their values changed from the previous point.

**Vials and Tips** are handled differently – only the reference position (Vial1, Tip1) needs to be taught. All other positions are calculated automatically from the spacing defined in `config.txt`:

```
Vial2 = Vial1 + 75.3mm in x
Vial3 = Vial1 + 150.6mm in x
Tip2  = Tip1  + 45mm in x
Tip3  = Tip1  + 45mm in y
Tip4  = Tip1  + 45mm in x and y
```

---

## config.txt

The config file stores two types of values:

**Gripper positions** – how far open/closed the gripper is (0 = fully closed, 850 = fully open):
```
GRIPPER GrabVial        250
GRIPPER ReleaseVial     500
GRIPPER ReleasePipette  850
GRIPPER GrabPipette     500
```

**Racks** – reference file and spacing for arrays of positions:
```
RACK VialRackFront   vial1_pickup.txt    75.3   0    3
RACK TipGet          tip1_get.txt        45    45    4
```

Only edit `config.txt` when gripper force needs adjusting or rack spacing changes. Then re-run Cell 1 in the notebook.

---

## Teaching New Positions

When a position needs to be re-taught (e.g. after the lab setup changes):

1. Open terminal in SlurryBot folder
2. Run: `python keyboard_jogger.py`
3. Enter filename (e.g. `vial_to_scale`)
4. Choose overwrite (`o`) or append (`a`)
5. Set step sizes or press Enter for defaults
6. Jog the robot to position using the keyboard:

| Key | Action |
|-----|--------|
| `x` / `y` / `z` | move cartesian (+) |
| `Space` + `x/y/z` | move cartesian (-) |
| `1`–`6` | rotate joints (+) |
| `Space` + `1`–`6` | rotate joints (-) |
| `+` / `-` | double/halve step size |
| `t` / `Space+t` | track forward/backward |
| `g` / `Space+g` | close/open gripper (one step) |
| `f` | gripper fully closed |
| `h` | gripper fully open |
| `l` | save point as LINEAR |
| `j` | save point as ANGULAR |
| `p` | print current position |
| `r` | revert to last saved point |
| `ESC` | emergency stop |

7. Re-run Cell 1 in the notebook to reload positions

---

## When to Re-teach Positions

| Situation | What to do |
|-----------|-----------|
| Something moved in the lab | Re-teach affected txt file → re-run Cell 1 |
| New vials with different height | Re-teach `vial1_pickup.txt` and `vial4_pickup.txt` → Vial2/3/5/6 update automatically |
| Tips moved | Re-teach `tip1_get.txt`, `tip1_putback.txt`, `tip1_take_liquid.txt`, `tip1_liquid_to_vial.txt` → Tip2/3/4 update automatically |
| Gripper force needs adjusting | Edit `config.txt` GRIPPER values → re-run Cell 1 |

---

## Running the Notebook

**Every session – run Cells 1–5 in order:**

```
Cell 1  → imports
Cell 2  → connect robot
Cell 3  → connect scale
Cell 4  → helper functions & logging
Cell 5  → weighing logic
```

**Then choose:**

```
Cell 6+7  → full automatic workflow
Cell 8    → calibration (first session or after position changes)
Cell 9    → individual movement tests
```

---

## Full Workflow

```python
weighing_workflow(vial_number="Vial1", target_weight=1.5)
```

This automatically:
1. Picks up Vial1 and places it on the scale
2. Places funnel over vial
3. Tares scale
4. Weighs powder using large then medium spatula
5. Replaces funnel
6. Prints run summary

---

## Testing Individual Movements

Always test in the correct order – the robot must be in the right position before each step.

> ⚠️ **After any error, always start here:**
> ```python
> robot.GoTo_InitialPoint()
> robot.restart()
> ```

### Vial Handling
```python
robot.PickUpVial("Vial1")    # picks up vial and moves towards scale
robot.VialToScale()           # places vial on scale
```

### Funnel
```python
# Vial must be on scale first!
robot.PlaceFunnel()
robot.ReplaceFunnel()
```

### Large Spatula
```python
# Always as a complete block!
robot.PickupLargeSpatula()
robot.ScoopBigMiddle()        # repeat as needed
robot.ScoopBigLeft()          # optional
robot.ScoopBigRight()         # optional
robot.ReplaceLargeSpatula()
```

### Medium Spatula
```python
# Always as a complete block!
robot.PickupMediumSpatula()
robot.ScoopMediumLeft()       # repeat as needed
robot.ScoopMediumMiddle()     # optional
robot.ScoopMediumRight()      # optional
robot.ScoopMediumFarleft()    # optional
robot.ScoopTiny()             # optional
robot.ScoopTinyLeft()         # optional
robot.ScoopTinyRight()        # optional
robot.ReplaceMediumSpatula()
```

### Scale to Rest & Pipette
```python
# Always in this order!
robot.ScaleToLiquidRestPoint()
robot.PickUpPipette()
robot.GettingPipetteTip("1")
robot.TakingLiquid("1")
robot.LiquidToVial("1")
robot.PuttingBackPipetteTip("1")
robot.PuttingBackPipette()
```

---

## Calibration

Run before the first weighing session or after positions have changed.
Compare your results with Aidan's reference values to check if positions are still correct:

| Spatula | Expected yield |
|---------|---------------|
| Big middle | ~1.0g |
| Big left | ~0.6g |
| Big right | ~0.5g |
| Medium left | ~0.3g |
| Medium middle | ~0.23g |
| Medium right | ~0.21g |
| Medium farleft | ~0.215g |
| Tiny | ~0.05–0.08g |

If your values differ significantly → re-teach the affected position files.

---

## If Something Goes Wrong

| Problem | Solution |
|---------|----------|
| Robot stops mid-movement | `robot.restart()` → `robot.GoTo_InitialPoint()` → check txt file |
| Scale not responding | Check COM port in Cell 3 → reconnect scale |
| Wrong position | Re-teach position file with jogger → re-run Cell 1 |
| Container empty (endless loop) | Refill powder container – safety limit will stop the robot automatically after 20 large or 30 medium scoops |

---

## Notes for Future Students

- The mixer functions have been removed pending hardware replacement. Once the new mixer is installed, teach new position files with the jogger and add corresponding functions to `Robot_wrapper.py`.
- All spatula positions (scoop_big_*, scoop_medium_*, scoop_tiny_*) were calibrated with flour. For different powders, run calibration first and adjust the weighing thresholds in `run_weighing_logic()` if needed.
- Never edit position txt files manually. Always use the keyboard jogger to re-teach positions.
