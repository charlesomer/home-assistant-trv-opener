# Home Assistant TRV Opener
_Tested with the Drayton Wiser Heating System_

## Requirements
 - Pyscript for Home Assistant
 - Heating system needs to be integrated with Home Assistant.

## Setup/Notes

Once Pyscript is installed, add the script from this repo to the Pyscript folder (e.g. `volumes/home-assistant/pyscript/trv-script.py`). If you are not using the Wiser heat system, you may need to change the variables set at the beginning to work with your system.

By default, this script will increase the temperature of TRVs which are above temperature to 25 degrees to force them open and will then reset them back to the schedule once all minimum temperatures have been reached. This value can be changed in the script.

Then, Home Assistant needs to know when to run this script. For now, I am running it every minute but it would be nicer if it could be run only when the TRVs detect a change in temperature for example.

To run every minute:
 1. Navigate to the Home Assistant GUI
 2. Configuration
 3. Automations
 4. Add Automation
 5. Start with an empty automation
 6. Edit via the YAML and use something like this or configure using the GUI (using time pattern).
 ```
alias: TRV Monitor
description: ''
trigger:
- platform: time_pattern
    minutes: /5
condition: []
action:
- service: pyscript.trv_monitor
    data: {}
mode: single
 ```
You may need to go to Developer Tools > Services > Look for `Pyscript.reload` and call this service before the `trv_monitor` function appears.