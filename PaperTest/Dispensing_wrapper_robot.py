
import numpy as np
import time
import os
import csv

from Robot_wrapper import *

class Calibration:
    def __init__(self, acceleration, speed, material, version_inside, version_outside, motor, scale, robot):
        self.acceleration = acceleration
        self.speed = speed
        self.material = material
        self.version_inside = version_inside
        self.version_outside = version_outside
        self.date = None
        self.calibration_weights = None
        self.g_o_f = None #goodness of fit R^2
        self.slope = None
        self.y_intercept = None
        self.step_range = None
        self.weight_range = None
        self.avg_weights = None
        self.std_error_weights = None
        self.relative_std_error_weights = None
        self.repeat = None
        self.steps = None
        self.motor = motor
        self.scale = scale
        self.robot = robot

    def test_function(self):
        print("Test successful")
    

    def calibrate(self, steps, repeat, vial_number):
        weights = np.zeros((len(steps), repeat))  # Initialize array to store weights
        first_action = True

        # Create a file to save raw data
        raw_data_filename = f'raw_calibration_data_{self.material}_{self.version_inside}.csv'
        with open(raw_data_filename, 'w', newline='') as raw_file:
            writer = csv.writer(raw_file)
            writer.writerow(["Step", "Weight"])
            
        for i in range(repeat):
            if i == 5:
                time.sleep(20)
            print(f"Repeat: {i+1}")
            for idx, step in enumerate(steps):
                self.scale.open()
                print("Scale opened")
                if first_action == True:
                    # Move vial from Storage on scale
                    self.robot.PickUpVial(vial_number)
                    self.robot.VialToScale()
                    first_action = False
                time.sleep(2)
                self.scale.tare()
                # Move vial from scale under dispensing unit 
                self.robot.ScaleToDispenser1()
                time.sleep(2)
                self.motor.move(step)
                time.sleep(2)
                # Move vial from dispensing unit on scale
                self.robot.Dispenser1ToScale()
                time.sleep(2)
                weight = self.scale.measure_stable().value
                weights[idx, i] = weight
                #weights[idx, i] = self.scale.measure_stable().value
                print(f"Step: {step}, Weight: {weights[idx, i]}")
                # Save the raw data immediately after each measurement

                with open(raw_data_filename, 'a', newline='') as raw_file:
                    writer = csv.writer(raw_file)
                    writer.writerow([step, weight])

                self.scale.close()
                print("Scale closed")
                time.sleep(2)

        # Move vial from scale to storage
        self.robot.ScaleToVialRestPoint()
        self.robot.GoTo_Point("VialRestPoint", 20)
        self.robot.GoTo_InitialPoint()
        # Fitting
        avg_weights = np.mean(weights, axis=1)
        steps_matrix = np.vstack((steps, np.ones_like(steps))).T  # Formatting steps properly
        self.slope, self.y_intercept = np.linalg.lstsq(steps_matrix, avg_weights, rcond=None)[0]  # Corrected line
        residuals = avg_weights - (self.slope * np.array(steps) + self.y_intercept)
        self.g_o_f = 1 - (np.sum(residuals ** 2))/(np.sum((avg_weights - np.mean(avg_weights))**2))
        self.calibration_weights = weights
        self.date = time.ctime()
        self.step_range = [min(steps), max(steps)]
        self.weight_range = [min(avg_weights), max(avg_weights)]
        self.avg_weights = avg_weights
        self.std_error_weights = np.std(weights, axis=1)  # Standard error for each line
        self.relative_std_error_weights = self.std_error_weights / self.avg_weights
        self.repeat = repeat
        self.steps = steps

    def calibration_report(self):
        if self.calibration_weights is None:
            return "Calibration data is not available. Please run calibration first."
        report = f"Calibration Report:\nDate: {self.date}\n"
        report += f"Material: {self.material}\nVersion Inside: {self.version_inside}\nVersion Outside: {self.version_outside}\n"
        report += "Calibration:\n"
        report += f"Slope: {self.slope}, y-intercept: {self.y_intercept}, R_square = {self.g_o_f}"
        return report

    def save_calibration(self):
        # Overview_File
        if not os.path.exists('Calibration_File.csv'):
            headers = ["Calibration ID", "Date", "Acceleration", "Speed", "Material",
                       "Version Inside", "Version Outside", "Slope", "Y-intercept",
                       "Goodness of Fit", "Weight Range", "Step Range", "Repeat"]
            with open('Calibration_File.csv', 'w', newline='') as cal_file:
                writer = csv.writer(cal_file)
                writer.writerow(headers)
            cal_id = 1
        else:
            with open('Calibration_File.csv', 'r') as cal_file:
                reader = csv.reader(cal_file)
                last_row = list(reader)[-1]
                cal_id = 1 + int(last_row[0])

        csv_line = [cal_id, self.date, self.acceleration, self.speed, self.material, self.version_inside, 
                    self.version_outside, self.slope, self.y_intercept, self.g_o_f, str(self.weight_range), str(self.step_range), self.repeat]

        with open('Calibration_File.csv', 'a', newline='') as cal_file:
            writer = csv.writer(cal_file)
            writer.writerow(csv_line)

        # Calibration_Report_File
        # Format the date and time string to replace spaces and colons
        formatted_date = self.date.replace(' ', '_').replace(':', '')

        # Construct the report filename with the formatted date
        report_filename = f'report_cal_id_{cal_id}_{formatted_date}.csv'
        headers = ["Steps", "AVG_weight", "STD_weight", "STD_rel_weight"]
        with open(report_filename, 'w', newline='') as report_file:
            writer = csv.writer(report_file)
            writer.writerow(headers)
            for i in range(len(self.steps)):
                writer.writerow([self.steps[i], self.avg_weights[i], self.std_error_weights[i], self.relative_std_error_weights[i]])

class Dispensing:
    def __init__(self, motor, scale, robot):
        self.motor = motor
        self.scale = scale
        self.robot = robot

    def dispense(self, weight:float, cal_id:int):
        #assumes initial vial position on scale
        with open('Calibration_File.csv', 'r') as cal_file:
            reader = csv.DictReader(cal_file)
            for row in reader:
                if int(row['Calibration ID']) == cal_id:
                    slope = float(row['Slope'])
                    y_intercept = float(row['Y-intercept'])
                    speed = float(row['Speed'])
                    acceleration = float(row['Acceleration'])
                    break
            else:
                raise ValueError("No matching ID found")
        calc_steps = int(round((weight-y_intercept)/slope))
        time.sleep(2)
        self.scale.tare()
        time.sleep(2)
        # move vial from scale under dispensing unit
        self.robot.ScaleToDispenser1()
        time.sleep(2)
        self.motor.move(calc_steps)
        time.sleep(2)
        self.robot.Dispenser1ToScale()
        time.sleep(2)
        weight_dispensed = self.scale.measure_stable().value
        return weight_dispensed

    def dispense_precisely(desired_weight:float, cal_id:int, vial_number):
        with open('Calibration_File.csv', 'r') as cal_file:
            reader = csv.DictReader(cal_file)
            for row in reader:
                if int(row['Calibration ID']) == cal_id:
                    date = row['Date']  # No need to use time.strftime here
                    break
            else:
                raise ValueError("No matching ID found")
        
        formatted_date = date.replace(' ', '_').replace(':', '')
        with open(f'report_cal_id_{cal_id}_{formatted_date}.csv', 'r') as report_file:
            reader = csv.DictReader(report_file)
            AVG_weights = []
            STD_rel_weight = []
            STD_weight = []
            for row in reader:
                AVG_weights.append(float(row['AVG_weight']))
                STD_rel_weight.append(float(row['STD_rel_weight']))
                STD_weight.append(float(row['STD_weight']))
        
        weight = desired_weight
        self.scale.tare()
        first_action = True
        time.sleep(2)
        # Move vial from storage on scale
        self.robot.PickUpVial(vial_number)
        self.robot.VialToScale()
        time.sleep(1)
        mass_netto = self.scale.measure_stable().value
        # Aprroximation
        weight_dispensed = 0
        improvement_expected = True
        while improvement_expected:
            weight -= weight_dispensed
            closest = AVG_weights[0]
            closest_index = 0
            for i, AVG_weight in enumerate(AVG_weights):
                if abs (AVG_weight - weight) < abs(closest - weight):
                    closest_index = i
            weight_current_step = (1-3*STD_rel_weight[closest_index]) * weight #3-sigma criterion
            weight_dispensed = dispense(weight=weight_current_step,cal_id=cal_id,motor=self.motor,scale=self.scale, robot=self.robot)
            #weight_dispensed, first_cycle = dispense(weight=weight_current_step,cal_id=cal_id,motor=motor,scale=scale, robot=robot)
            
            if abs(weight - weight_dispensed) < 3 * STD_rel_weight[closest_index]*weight:
                improvement_expected = False
                weight -= weight_dispensed
                break

            #to pervent statistical understimation: addition of the missing part
        if weight > 0:
            weight_dispensed = self.dispense(weight=weight,cal_id=cal_id,motor=self.motor,scale=self.scale, robot=self.robot)

        # robot pickup vial from scale and keep it (maybe storage directly located next to scale)
        self.robot.LiftVial()
        time.sleep(2)
        self.scale.tare()
        time.sleep(2)
        # robot place vial on scale again
        self.robot.DropVial()
        mass_brutto = self.scale.measure_stable().value
        weight_dispensed = mass_brutto-mass_netto
        relative_weighing_error = (weight_dispensed-desired_weight)/desired_weight
        absolute_weighing_error = weight_dispensed - desired_weight
        # robot return vial in storage
        self.robot.ScaleToVialRestPoint()
        return weight_dispensed, relative_weighing_error, absolute_weighing_error
