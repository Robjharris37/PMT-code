'''
Copyright (c) 2018 Robert J. Harris & Marcelo Tala
    
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
    
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
    
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

TBD

Check code works properly
'''

import serial   #import python serial module

class pmt(object):
    '''
    The PMT class for control
    '''

    def __init__(self,):
        ''' intialise the PMT, set the initial values'''

        self.com_port = "COM5"

        try:
            self.control = serial.Serial(self.com_port)
        except:
            print("Oh dear, that didn't work so well, lets try manually")
            self.find_com_port()

        #setup initial parameters

        self.control.write(b"R01\r")
        print("setting R = 01")

        self.control.write(b"P10\r")
        print("setting P = 10")
        #Set sequence of readings to 1 self.pmt. "R\x01\r", 3, "setting R = 01");
        #Set number of intervals to sum - send_cmd_and_chk( "P\x0a\r", 3, "setting P = 10");

    def find_com_port(self):
        '''Maybe we will need to find the com port
        so taken from
        https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        '''

        import serial.tools.list_ports
        list_ports = serial.tools.list_ports.comports()
        connected = [port.device for port in serial.tools.list_ports.comports()]
        print("Connected COM ports: " + str(connected))

        self.com_port = str(input("Please type selected port:"))

        return

    def voltage_off(self):

         #"V\x00\x00\r", 4, "shutting off HV"
        self.control.write(b"V00r")
        self.check_command()
        print('High voltage off')

    def voltage_on(self):

        #"V\x03\xe8\r" from C code
        self.control.write(b"D\r")
        self.check_command()
        print('High voltage on')


    def set_voltage(self, voltage, min_v = 300, max_v = 1200):

        #check if between max and min
        if voltage > min_v and voltage < max_v:
            self.control.write(b"V{}\r".format(voltage))
            self.check_command()
        else:
            print("Invalid command entered")

    def set_integration_time(self, int_time, min_i = 0, max_i = 100):

        #check if between max and min
        if int_time > min_i and int_time < max_i:
            self.control.write(b"P{}\r".format(int_time))
            self.check_command()
        else:
            print("Invalid command entered")

    def set_sequence_readings(self,min_r = 1, max_r = 255):

        #check if between max and min
        if int_time > min_r and int_time < max_r:
            self.control.write(b"R{}\r".format(int_time)) #lowercase hex format - might need to be in seperate lines!!!
            self.check_command()
        else:
            print("Invalid command entered")
        #set command

    def check_command(self):
        no_bytes = self.inWaiting()
        if no_bytes != 0:
            test = self.control.read(no_bytes)
            if test == "VA":
                print('Boom, that worked!')
            else:
                print("That didn't work,returned {}".format(test))

if __name__ == '__main__':

    pmt_test = pmt() #initialise PMT
    
