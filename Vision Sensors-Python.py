#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT14, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_inertial = Inertial(Ports.PORT20)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 398.98, 320, 254, MM, 1)
controller_1 = Controller(PRIMARY)
# vex-vision-config:begin
vision_6__TRIBALL = Signature(1, -5773, -3697, -4735,-5635, -4063, -4849,0.6, 0)
vision_6__SIG_2 = Signature(2, 0, 0, 0,0, 0, 0,3, 0)
vision_6 = Vision(Ports.PORT6, 50, vision_6__TRIBALL, vision_6__SIG_2)
# vex-vision-config:end


# wait for rotation sensor to fully initialize
wait(30, MSEC)

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller_1.axis3.position() + controller_1.axis1.position()
            drivetrain_right_side_speed = controller_1.axis3.position() - controller_1.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

vexcode_vision_6_objects = []
vexcode_brain_precision = 0
vexcode_console_precision = 0
vexcode_controller_1_precision = 0
vexcode_vision_6_object_index = 0
myVariable = 0

def onauton_autonomous_0():
    global myVariable, vexcode_vision_6_objects, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision, vexcode_vision_6_object_index
    drivetrain.set_stopping(HOLD)
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.drive_for(REVERSE, 150, MM)
    drivetrain.stop()
    wait(5, MSEC)
    vexcode_vision_6_objects = vision_6.take_snapshot(vision_6__TRIBALL)
  #vision sensors
    while True:
        while not brain.timer.time(SECONDS) > 57:
            vexcode_vision_6_objects = vision_6.take_snapshot(vision_6__TRIBALL)
            if vexcode_vision_6_objects and len(vexcode_vision_6_objects) > 0:
                if vexcode_vision_6_objects[vexcode_vision_6_object_index].height > 0 and vexcode_vision_6_objects[vexcode_vision_6_object_index].height < 77 and vexcode_vision_6_objects[vexcode_vision_6_object_index].centerX > 100 and vexcode_vision_6_objects[vexcode_vision_6_object_index].centerX < 148:
                    drivetrain.drive(FORWARD)
                if vexcode_vision_6_objects[vexcode_vision_6_object_index].height > 0 and vexcode_vision_6_objects[vexcode_vision_6_object_index].height < 77 and vexcode_vision_6_objects[vexcode_vision_6_object_index].centerX < 100:
                    drivetrain.turn(LEFT)
                if vexcode_vision_6_objects[vexcode_vision_6_object_index].height > 0 and vexcode_vision_6_objects[vexcode_vision_6_object_index].height < 77 and vexcode_vision_6_objects[vexcode_vision_6_object_index].centerX > 148:
                    drivetrain.turn(RIGHT)
            else:
                drivetrain.stop()
        wait(5, MSEC)
        wait(5, MSEC)
    drivetrain.drive_for(REVERSE, 5, INCHES)
    drivetrain.stop()

def when_started1():
    global myVariable, vexcode_vision_6_objects, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision, vexcode_vision_6_object_index
    brain.timer.clear()
    drivetrain.set_drive_velocity(100, PERCENT)
    controller_1.screen.print(brain.timer.time(SECONDS), precision=6 if vexcode_controller_1_precision is None else vexcode_controller_1_precision)

# create a function for handling the starting and stopping of all autonomous tasks
def vexcode_auton_function():
    # Start the autonomous control tasks
    auton_task_0 = Thread( onauton_autonomous_0 )
    # wait for the driver control period to end
    while( competition.is_autonomous() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the autonomous control tasks
    auton_task_0.stop()

def vexcode_driver_function():
    # Start the driver control tasks

    # wait for the driver control period to end
    while( competition.is_driver_control() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the driver control tasks


# register the competition functions
competition = Competition( vexcode_driver_function, vexcode_auton_function )

# Calibrate the Drivetrain
calibrate_drivetrain()

when_started1()
