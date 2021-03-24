# Identifiers for TRV temperatures.
current_temperature_identifier = "current_temperature"
target_temperature_identifier  = "temperature"

service_name_to_set_temperatures = "set_temperature"

# The temperature to set TRVs to to force them open.
# I've found that 21 degrees is a good balance between forcing them open
# and rooms getting too hot but this may need adjusting based on your
# preference.
temperature_used_to_open_trv = 21

attribute_trv_when_manually_opened = "preset_mode"
attribute_trv_when_manually_opened_value = "Override"

attribute_demand_check = "percentage_demand"

service_to_use_to_reset_trvs       = "set_preset_mode"
service_to_use_to_reset_trvs_value = "Cancel Boost"

@service
def trv_monitor():
  # Get array of rooms with trvs.
  trv_rooms = state.names("climate")

  # We need to find out if any TRV is supposed to be on, i.e. if the current
  # temperature is below the target temperature.

  isHeatingRequired = False

  for room in trv_rooms:
    # Get attributes for the room.
    attributes = state.getattr(room)

    current_temperature = attributes[current_temperature_identifier]
    target_temperature  = attributes[target_temperature_identifier]

    if (
      current_temperature < target_temperature and
      attributes[attribute_trv_when_manually_opened] != attribute_trv_when_manually_opened_value and
      attributes[attribute_demand_check] > 0
    ):
      isHeatingRequired = True
      # There is a TRV which should be heating, we can now exit this loop
      # and loop again and this time set TRVs which aren't supposed to be
      # heating to a higher temperature to force them open.
      break

  if isHeatingRequired == True:
    log.info("Heating is required.")
    for room in trv_rooms:
      attributes = state.getattr(room)

      current_temperature = attributes[current_temperature_identifier]
      target_temperature  = attributes[target_temperature_identifier]

      # This time, if the current temperature is higher than the target
      # temperature (when the TRV will be off), we can increase the target
      # temperature to force the TRV open.
      if (
        current_temperature > target_temperature and
        attributes[attribute_trv_when_manually_opened] != attribute_trv_when_manually_opened_value and
        attributes[attribute_demand_check] == 0
      ):
        service.call("climate", service_name_to_set_temperatures,
          entity_id=room,
          temperature=temperature_used_to_open_trv
        )
        log.info("Setting TRV for: " + room)
  else:
    log.info("Heating is not required.")
    # Make sure to reset any TRVs that were previously set to a high
    # back to their defaults.
    for room in trv_rooms:
      attributes = state.getattr(room)
      if (
        attributes[attribute_trv_when_manually_opened] == attribute_trv_when_manually_opened_value
      ):
        service.call("climate", service_to_use_to_reset_trvs,
          entity_id=room,
          preset_mode=service_to_use_to_reset_trvs_value
        )
        log.info("Resetting TRV for: " + room)