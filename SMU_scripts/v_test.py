import time
from  keithley2600 import Keithley2600, ResultTable

k = Keithley2600('TCPIP0::192.168.2.121::INSTR')

# create ResultTable with two columns
rt = ResultTable(
    column_titles=['Voltage', 'Current'],
    units=['V', 'A'],
    params={'recorded': time.asctime(), 'sweep_type': 'iv'},
)

# create live plot which updates as data is added
rt.plot(live=True)

# measure some currents
for v in range(0, 20):
    k.apply_voltage(k.smua, 10)
    i = k.smua.measure.i()
    rt.append_row([v, i])

# save the data
rt.save('~/iv_curve.txt')