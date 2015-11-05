What is JLoad?

JLoad is a template loading program that was adapted from a YouTube video. The purpose of this program is to deploy a configuration change to multiple devices. The template represents the configuration and the CSV contains the data that will go into each device. Each line in the CSV represents a unique chassis.

Using JLoad

Prerequisites:
- Host with python and standard PyEZ libraries (pip install junos-eznc)
- Juniper Router(s)
- Account on chassis
- Enable netconf access (set system services netconf ssh port 830)


1. Create a CSV file template
2. Add the CSV template to the "csv" folder in jload
3. Create a template file
4. Add the template file to the "template" folder in jload
5. Run script file > python jload.py
6. Follow instructions