
# FUD Backend

The code in this repository:
* generates a static weather GEOJSON file and associated metadata that are read by the system (this happens in a separate cron job)
* runs the simulation as a series of threads which control the market, the dialog, and the 


### restarting the service file
```
systemctl --user restart simulation
systemctl --user daemon-reload
```