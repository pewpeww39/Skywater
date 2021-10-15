import pytest
from keithley2600 import Keithley2600, ResultTable

k = Keithley2600('TCPIP::169.254.0.1::INSTR')

def voltage_measure (input)
    k.measure_voltage(k.smua, input)
    
def test_voltage_measure()
    assert k.measure_voltage(10) == 10