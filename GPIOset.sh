#!/bin/sh

# This file configures the Serial Module port settings
#  Settings are as follows: RS485_RS232n (0, 4, 8, 12),  Half_Full (1, 5, 9 13), Termination (2, 6, 10, 14), Bias (3, 7, 11, 15)
#   RS485 Mode -> RS485_RS232n = 1
#   RS232 Mode -> RS485_RS232n = 0
#   Half Duplex -> Half_Fulln = 1
#   Full Duplex -> Half_Fulln = 0
#   120 Ohm Termination Enabled -> Termination = 1
#   120 Ohm Termination Disabled -> Termination = 0
#   Bias Enabled -> Bias = 1
#   Bias Disabled -> Bias = 0

#Configure for 8 port test
#Ports 1-7 are half duplex RS485, 8 is RS232

echo "Configuring serial ports for test"

#configure port 1 settings
gpioset gpiochip1 0=1 1=1 2=1 3=1
#configure port 2 settings
gpioset gpiochip1 4=1 5=1 6=1 7=1
#configure port 3 settings
gpioset gpiochip1 8=1 9=1 10=1 11=1
#configure port 4 settings
gpioset gpiochip1 12=1 13=1 14=1 15=1
#configure port 5 settings
gpioset gpiochip2 0=1 1=1 2=1 3=1
#configure port 6 settings
gpioset gpiochip2 4=1 5=1 6=1 7=1
#configure port 7 settings
gpioset gpiochip2 8=1 9=1 10=1 11=1
#configure port 8 settings
gpioset gpiochip2 12=0 13=0 14=0 15=0

exit 0

