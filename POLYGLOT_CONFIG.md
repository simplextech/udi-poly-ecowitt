
# Configuration

Configure the GW1000 or other receiver per the manual.

This Nodeserver is a receiver for the data sent to it via a POST
http call from the GW1000.  If the GW1000 is on a different network (VLAN)
you will have to setup the routing/firewall rules for your environment.

There is no polling or discovery done by the NodeServer.  Devices are created
automatically from the data sent by the GW1000.

 1. After installing you need to configure the GW1000 per setup instructions and update the firmware.  Reference the GW1000 manual
 2. Go to Device List and select your device
 3. Touch More in the top right
 4. Touch Weather Services
 5. Touch Next (4 times) until you get to “Customized” option
 6. Select Enabled
 7. Protocol Type Same As = EcoWitt
 8. Server IP/Address = Polyglot IP
 9. Port: Port in configuration - default 8080
 10. Upload interval = How often to push data to the driver
