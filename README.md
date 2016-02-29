# JLOAD 

### Juniper Configuration Deployment Script

# ABOUT

What is JLoad?

JLoad is a template loading program that was adapted from a YouTube video. The purpose of this program is to deploy a configuration change to multiple devices. The script uses a template and csv file to assemble and push configurations to devices. It will accept both "set" and "bracketed" template formats. The template represents the configuration and the CSV contains the data that will go into each device. Each line in the CSV represents a unique chassis.

# DEPENDENCIES

- Host with python and standard PyEZ libraries (pip install junos-eznc)
- Juniper Router(s)
- Account on chassis
- Enable netconf access (set system services netconf ssh port 830)

# USAGE

1. Create a CSV file template
2. Add the CSV template to the "csv" folder in jload
3. Create a template file
4. Add the template file to the "template" folder in jload
5. Run script file > python jload.py

# CONTRIBUTORS

[Tyler Jordan](https://github.com/tjordan) - Creator
[Steve Steiner](https://github.com/ntwrkguru) - Ported to Docker

