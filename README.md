# SROS Rootifier <small>{BETA}</small>

> Safe command is a `/`-based command!

When an engineer configures remote device via telnet/ssh it is **safer** to use configuration commands
in a _full-context_ fashion. This best-practice comes from a sad fact that large configuration snippets may render corrupted
while pasting large chunks of data procedure in the terminal window. Chances are you end up with an inconsistent configuration or even an
outage.
With this script one can transform tree-based config into full-context (aka display-set) in a blink of an eye.

## Usage
Script takes just one argument which is a input config file.
```shell
python rootify.py input.cfg
```
and prints _rootified_ commands to `stdout` and output file: `rootified_<inputFname>`

For example, for an input file with a name input.cfg and contents:
```
# TiMOS-C-12.0.R12 cpm/hops64 ALCATEL SR 7750 Copyright (c) 2000-2015 Alcatel-Lucent.
# All rights reserved. All use subject to applicable license agreements.
# Built on Wed Sep 2 13:59:32 PDT 2015 by builder in /rel12.0/b1/R12/panos/main

# Generated MON APR 04 23:00:17 2016 UTC

exit all
configure
#--------------------------------------------------
echo "System Configuration"
#--------------------------------------------------
    system
        name "VV000446-BBR02"
        chassis-mode d
        dns
        exit
        snmp
            streaming
                no shutdown
            exit
            packet-size 9216
        exit
        time
            ntp
                ntp-server
                server 10.80.0.2 prefer
                server 10.81.0.2
                no shutdown
            exit
            sntp
                shutdown
            exit
            zone UTC10 10
        exit
        thresholds
            rmon
            exit
        exit
        lldp
            tx-interval 10
            tx-hold-multiplier 2
            reinit-delay 5
            notification-interval 10
        exit
    exit
```
script will produce output file with a name `rooted_input.cfg` and contents:
```
/configure system name "VV000446-BBR02"
/configure system chassis-mode d
/configure system dns
/configure system snmp streaming no shutdown
/configure system snmp packet-size 9216
/configure system time ntp ntp-server
/configure system time ntp server 10.80.0.2 prefer
/configure system time ntp server 10.81.0.2
/configure system time ntp no shutdown
/configure system time sntp shutdown
/configure system time zone UTC10 10
/configure system thresholds rmon
/configure system lldp tx-interval 10
/configure system lldp tx-hold-multiplier 2
/configure system lldp reinit-delay 5
/configure system lldp notification-interval 10
```

## Assumptions
- Code is sensible to indentation. Paste the configuration code as you see it on a router
- Script will take into account only the lines starting with **4 spaces**.

You can pass as input something like this:
```
#--------------------------------------------------
echo "System Configuration"
#--------------------------------------------------
    system
        name "MPLS-078-2878-BH02"
        snmp
            packet-size 9216
        exit
        login-control
            pre-login-message "MPLS-078-2878-BH02"
        exit
```
or this:
```
    port 1/1/2
        shutdown
        ethernet
        exit
    exit
    port 1/1/3
        shutdown
        ethernet
        exit
    exit
```
or even the whole configuration file!

But you can't paste configuration statements which are not nested under `configure` section.
For example this will produce erroneous output:
```
            lldp
                dest-mac nearest-bridge
                    admin-status tx-rx
                    notification
                    tx-tlvs port-desc sys-cap
                    tx-mgmt-address system
                exit
            exit
```
# Author
Roman Dodin [@noshut_ru](https://twitter.com/noshut_ru)
