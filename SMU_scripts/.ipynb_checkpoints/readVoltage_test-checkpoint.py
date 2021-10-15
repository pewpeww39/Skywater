import pytest
from keithley2600 import Keithley2600, ResultTable

k = Keithley2600('TCPIP::169.254.0.1::INSTR')
r1=1500
def voltage_measure(y):
    apply_voltage(k.smub, y)
    x = k.measure_current(k.smua) * r1
    return x #k.measure_voltage(k.smua, input)
    
def test_voltage_measure():
    assert voltage_measure(10) == apporx(10)

# def capital_case(x):
#     return x

# def test_capital_case():
#     assert capital_case(10) == 10