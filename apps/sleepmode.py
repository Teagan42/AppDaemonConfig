import appdaemon.appapi as appapi

#
# App to handle sleep mode
#
# Args:
#
# sensor: sensor to monitor e.g. sensor.upstairs_smoke
# idle_state - normal state of sensor e.g. Idle
# turn_on - scene or device to activate when sensor changes e.g. scene.house_bright
# Release Notes
#
# Version 1.0:
#   Initial Version


class SensorNotification(appapi.AppDaemon):

  def initialize(self):
    self.asleep = False
    self.sun = 'sun.sun'
    self.sensor = 'binary_sensor.adults_in_bed'
    self.sleep_script = 'script.sleep_mode'
    self.awake_script = 'script.awake_mode'
    
    self.listen_state(self.state_check_callback, self.sensor)
    self.run_at_sunset(self.state_check_callback)
    self.run_at_sunrise(self.state_check_callback)

  def state_check_callback(self, **kwargs):
    sun_state = self.get_state(self.sun)
    sensor_state = self.get_state(self.sensor)
    if sensor_state == 'on':
      if sun_state == 'below_horizon' and not self.asleep:
        enter_sleep_mode()
    else:
      if sun_state == 'above_horizon' and self.asleep:
        exit_sleep_mode()

  def enter_sleep_mode(self):
    self.asleep = True
    self.set_state(self.sleep_script, 'on')

  def exit_sleep_mode(self):
    self.asleep = False
    self.set_state(self.awake_script, 'on')
