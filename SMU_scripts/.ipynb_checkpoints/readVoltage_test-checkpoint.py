import pytest
from keithley2600 import Keithley2600, ResultTable

k = Keithley2600('TCPIP2::169.254.0.1::INSTR')
r1=1800
def voltage_measure(y):
    k.apply_voltage(k.smua, y)
    x = k.measure_current(k.smua) * r1
    return x #k.measure_voltage(k.smua, input)
    
def test_voltage_measure():
    assert voltage_measure(10) == pytest.approx(10)

# def capital_case(x):
#     return x

# def test_capital_case():
#     assert capital_case(10) == 10