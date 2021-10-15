#Keithley2634B Voltage Sweep with Switch
#this program is intended to source voltage and measure current for a diode, bjt, or mosfet
#note: the channels of the screw terminal panel on the switch are being used
#note: however, the switch commands are not yet automated
#note: the diode and bjt code in general is complete, but the mosfet plots need revisions

#start of program
#------------------------------------------------

import numpy as np
import pyvisa
import time
#  import numpy
import matplotlib.pyplot as my_graph  # this is to plot directly in python
from keithley2600 import Keithley2600

rm = pyvisa.ResourceManager('')

# set up the two instruments
System_Switch = rm.open_resource('TCPIP0::169.254.000.001::inst0::INSTR')  # 3706System_Switch system switch
Source_meter = Keithley2600('TCPIP0::169.254.025.226::inst0::INSTR')  # 2634B source meter

# query the two instruments to ensure proper connection
#  print(System_Switch.query("*IDN?"))
#  Source_meter.smua.source.output = Source_meter.smua.OUTPUT_OFF

l_steps = 25
l_curr = [0] * l_steps
l_volt = [0] * l_steps


# diode characterization
def diode_vsweep(vlevel, start, stop):
    l_vrange = 2
    l_vlevel = vlevel
    l_icmpl = 1
    l_nplc = 1
    #l_start = start
    #l_stop = stop
    # l_steps = steps
    l_delay = 0.001
    # changed 1_start &1_stop to pull directly from the inputs
    l_step = (stop - start) / (l_steps - 1)
    l_source_val = start
    l_v = 1

#initialize SMU a& b
    Source_meter.smua.reset()
    Source_meter.smub.reset()
    Source_meter.errorqueue.clear()

#Source meter functions
    Source_meter.display.smua.measure.func = Source_meter.display.MEASURE_DCAMPS
    Source_meter.smua.source.func = Source_meter.smua.OUTPUT_DCVOLTS
    Source_meter.smua.source.autorangev = Source_meter.smua.AUTORANGE_ON
    Source_meter.smua.source.levelv = l_vlevel
    Source_meter.smua.source.limiti = l_icmpl
    Source_meter.smua.measure.autorangei = Source_meter.smua.AUTORANGE_ON
    Source_meter.smua.measure.nplc = l_nplc
    Source_meter.smua.source.output = Source_meter.smua.OUTPUT_ON

#
    for l_v in range(1, l_steps):
        Source_meter.delay(l_delay)
        l_volt[l_v] = Source_meter.smua.measure.v()
        l_curr[l_v] = Source_meter.smua.measure.i()
        l_source_val = l_source_val + l_step
        Source_meter.smua.source.levelv = l_source_val

    Source_meter.smua.source.output = Source_meter.smua.OUTPUT_OFF
    Source_meter.smua.source.levelv = l_vlevel

    print('Current Data (System_Switch):')
    for l_v in range(1, l_steps):
        print(l_curr[l_v])
    print('')
    print('Source Voltage Data (V):')
    for l_v in range(1, l_steps):
        print(l_volt[l_v])


# this is to REMOVE the first data point from each set
# this should be revised so we don't have to remove each time
def graph_diode():
    n = 2
    xvals = [0] * (l_steps - 1)
    for x in range(1, l_steps - 1):
        xvals[x] = l_volt[n]
        n = n + 1
    m = 2
    yvals = [0] * (l_steps - 1)
    for y in range(1, l_steps - 1):
        yvals[y] = l_curr[m]
        m = m + 1
    # print diode plot
    plt.plot(xvals, yvals)
    plt.show()


l_vbesteps = 50
l_vb = [0] * l_vbesteps
l_ic = [0] * l_vbesteps
l_ib = [0] * l_vbesteps


# bjt characterization
def bjt_vsweep(vbestart, vbestop, vcebias):
    l_icmpl = 100E-3
    l_nplc = 1
    l_vbestart = vbestart
    l_vbestop = vbestop

    l_vce_bias = vcebias

    if l_vbestart is None:
        l_vbestart = 0
    if l_vbestart > 100E-6:
        l_vbestart = 100E-6
    if l_vbestop is None:
        l_vbestop = 700E-3
    if l_vbestop > 1:
        l_vbestop = 1

    l_vbestep = (l_vbestop - l_vbestart) / (l_vbesteps - 1)
    l_vbesource_val = l_vbestart
    l_vbe_i = 1

    if l_vce_bias is None:
        l_vce_bias = 10
    if l_vce_bias > 40:
        l_vce_bias = 40

    # Data tables
    Source_meter.smua.reset()
    Source_meter.smub.reset()
    Source_meter.errorqueue.clear()

    # Configure Collector/Emitter (SMUA) source and measure settings
    Source_meter.smua.source.func = Source_meter.smua.OUTPUT_DCVOLTS
    Source_meter.smua.source.autorangev = Source_meter.smua.AUTORANGE_ON
    Source_meter.smua.source.levelv = 0
    Source_meter.smua.source.limiti = l_icmpl
    Source_meter.smua.measure.autorangei = Source_meter.smua.AUTORANGE_ON

    Source_meter.smua.measure.autozero = Source_meter.smua.AUTOZERO_AUTO
    Source_meter.smua.measure.nplc = l_nplc

    Source_meter.smua.source.output = Source_meter.smua.OUTPUT_ON

    # Configure Base (SMUB) source and measure settings
    Source_meter.smub.source.func = Source_meter.smub.OUTPUT_DCVOLTS
    Source_meter.smub.source.autorangev = Source_meter.smub.AUTORANGE_ON
    Source_meter.smub.source.levelv = 0
    Source_meter.smub.source.limiti = l_icmpl
    Source_meter.smub.measure.autorangev = Source_meter.smub.AUTORANGE_ON

    Source_meter.smub.measure.autozero = Source_meter.smub.AUTOZERO_AUTO
    Source_meter.smub.measure.nplc = l_nplc

    Source_meter.smub.source.output = Source_meter.smub.OUTPUT_ON
    Source_meter.smua.source.levelv = l_vce_bias

    # Execute sweep
    for l_vbe_i in range(1, l_vbesteps):
        if l_vbe_i == 1:
            l_vbesource_val = l_vbestart

        Source_meter.delay(0.01)
        l_vb[l_vbe_i] = Source_meter.smub.measure.v()
        l_ib[l_vbe_i] = Source_meter.smub.measure.i()
        l_ic[l_vbe_i] = Source_meter.smua.measure.i()
        l_vbesource_val = l_vbesource_val + l_vbestep

        if l_vbe_i == l_vbesteps:
            l_vbesource_val = l_vbestart

        Source_meter.smub.source.levelv = l_vbesource_val

    Source_meter.smua.source.output = Source_meter.smua.OUTPUT_OFF
    Source_meter.smub.source.output = Source_meter.smub.OUTPUT_OFF
    Source_meter.smua.source.levelv = 0
    Source_meter.smub.source.levelv = 0

    print('')
    print('Vce', l_vce_bias)
    print('Vbe (V)', 'Ic (A)', 'Ib (A)')
    for l_vbe_i in range(1, l_vbesteps):
        print(l_vb[l_vbe_i], l_ic[l_vbe_i], l_ib[l_vbe_i])


# print gummel plot for bjt
def graph_bjt():
    my_graph.semilogy(l_vb, l_ic, 'b', l_vb, l_ib, 'r')
    # my_graph.legend('Vbe vs. Ib' 'Vbe vs. Ic')
    my_graph.xlabel('Vbe (Volts)')
    my_graph.ylabel('Current (Amps)')
    my_graph.title('Gummel Plot (BC5478 BJT)')
    my_graph.show()


#  define number of steps - might only need vgs steps but not sure
l_vdssteps = 25
l_vgssteps = 25
num_steps = 25

# create data tables
l_vgs_data = np.zeros([l_vgssteps, l_vgssteps])
l_vds_data = np.zeros([l_vgssteps, l_vgssteps])
l_id_data = np.zeros([l_vgssteps, l_vgssteps])

xvals_1 = np.zeros([l_vgssteps, 1])
xvals_2 = np.zeros([l_vgssteps, 1])
xvals_3 = np.zeros([l_vgssteps, 1])
xvals_4 = np.zeros([l_vgssteps, 1])
xvals_5 = np.zeros([l_vgssteps, 1])
xvals_6 = np.zeros([l_vgssteps, 1])
xvals_7 = np.zeros([l_vgssteps, 1])
xvals_8 = np.zeros([l_vgssteps, 1])
xvals_9 = np.zeros([l_vgssteps, 1])
xvals_10 = np.zeros([l_vgssteps, 1])
xvals_11 = np.zeros([l_vgssteps, 1])
xvals_12 = np.zeros([l_vgssteps, 1])
xvals_13 = np.zeros([l_vgssteps, 1])
xvals_14 = np.zeros([l_vgssteps, 1])
xvals_15 = np.zeros([l_vgssteps, 1])
xvals_16 = np.zeros([l_vgssteps, 1])
xvals_17 = np.zeros([l_vgssteps, 1])
xvals_18 = np.zeros([l_vgssteps, 1])
xvals_19 = np.zeros([l_vgssteps, 1])
xvals_20 = np.zeros([l_vgssteps, 1])
xvals_21 = np.zeros([l_vgssteps, 1])
xvals_22 = np.zeros([l_vgssteps, 1])
xvals_23 = np.zeros([l_vgssteps, 1])
xvals_24 = np.zeros([l_vgssteps, 1])
xvals_25 = np.zeros([l_vgssteps, 1])

yvals_1 = np.zeros([l_vgssteps, 1])
yvals_2 = np.zeros([l_vgssteps, 1])
yvals_3 = np.zeros([l_vgssteps, 1])
yvals_4 = np.zeros([l_vgssteps, 1])
yvals_5 = np.zeros([l_vgssteps, 1])
yvals_6 = np.zeros([l_vgssteps, 1])
yvals_7 = np.zeros([l_vgssteps, 1])
yvals_8 = np.zeros([l_vgssteps, 1])
yvals_9 = np.zeros([l_vgssteps, 1])
yvals_10 = np.zeros([l_vgssteps, 1])
yvals_11 = np.zeros([l_vgssteps, 1])
yvals_12 = np.zeros([l_vgssteps, 1])
yvals_13 = np.zeros([l_vgssteps, 1])
yvals_14 = np.zeros([l_vgssteps, 1])
yvals_15 = np.zeros([l_vgssteps, 1])
yvals_16 = np.zeros([l_vgssteps, 1])
yvals_17 = np.zeros([l_vgssteps, 1])
yvals_18 = np.zeros([l_vgssteps, 1])
yvals_19= np.zeros([l_vgssteps, 1])
yvals_20 = np.zeros([l_vgssteps, 1])
yvals_21 = np.zeros([l_vgssteps, 1])
yvals_22 = np.zeros([l_vgssteps, 1])
yvals_23 = np.zeros([l_vgssteps, 1])
yvals_24 = np.zeros([l_vgssteps, 1])
yvals_25 = np.zeros([l_vgssteps, 1])

def mosfet_vsweep(vgsstart, vgsstop, vdsstart, vdsstop):
    Source_meter.errorqueue.clear()
    l_vrange = 40
    l_icmpl = 1
    l_nplc = 1

    if vgsstart is None:
        vgsstart = 0
    if vgsstart > 10:
        vgsstart = 10
    if vgsstop is None:
        vgsstop = 10
    if vgsstop > 10:
        vgsstop = 10

    l_vgsstep = (vgsstop - vgsstart) / (l_vgssteps - 1)
    l_vgssource_val = vgsstart
    l_vgs_iteration = 1

    if vdsstart is None:
        vdsstart = 0
    if vdsstart > 10:
        vdsstart = 10
    if vdsstop is None:
        vdsstop = 10
    if vdsstop > 40:
        vdsstop = 40

    l_vdsstep = (vdsstop - vdsstart) / (l_vdssteps - 1)
    l_vdssource_val = vdsstart
    l_vds_iteration = 1

    # reset smua and clear error queue
    Source_meter.smua.reset()
    Source_meter.smub.reset()
    Source_meter.errorqueue.clear()

    # Configure Drain-Source (SMUA) source and measure settings - DRAIN (left leg) is SMUA
    Source_meter.smua.source.func = Source_meter.smua.OUTPUT_DCVOLTS
    Source_meter.smua.source.autorangev = Source_meter.smua.AUTORANGE_ON
    Source_meter.smua.source.levelv = 0
    Source_meter.smua.source.limiti = l_icmpl
    Source_meter.smua.measure.autorangei = Source_meter.smua.AUTORANGE_ON

    Source_meter.smua.measure.autozero = Source_meter.smua.AUTOZERO_AUTO
    Source_meter.smua.measure.nplc = l_nplc

    print('turn output on')
    Source_meter.smua.source.output = Source_meter.smua.OUTPUT_ON

    # Configure Gate-Source (SMUB) source and measure settings - GATE (middle leg) is SMUB
    Source_meter.smub.source.func = Source_meter.smub.OUTPUT_DCVOLTS
    Source_meter.smub.source.autorangev = Source_meter.smub.AUTORANGE_ON
    Source_meter.smub.source.levelv = 0
    Source_meter.smub.source.limiti = l_icmpl
    Source_meter.smub.measure.autorangei = Source_meter.smub.AUTORANGE_ON

    Source_meter.smub.measure.autozero = Source_meter.smub.AUTOZERO_AUTO
    Source_meter.smub.measure.nplc = l_nplc

    Source_meter.smub.source.output = Source_meter.smub.OUTPUT_ON

    #  Execute sweep
    for l_vgs_iteration in range(1, l_vgssteps):
        Source_meter.smub.source.levelv = l_vgssource_val

        l_vgs_data[l_vgs_iteration] = Source_meter.smub.measure.v()  # Measure gate-source voltage
        for l_vds_iteration in range(1, l_vdssteps):
            if l_vds_iteration == 1:
                l_vdssource_val = vdsstart

            l_vds_data[l_vgs_iteration][l_vds_iteration] = Source_meter.smua.measure.v()  # Measure sourced voltage
            l_id_data[l_vgs_iteration][l_vds_iteration] = Source_meter.smua.measure.i()  # Measure current
            l_vdssource_val = l_vdssource_val + l_vdsstep

            if l_vds_iteration == l_vdssteps:
                l_vdssource_val = vdsstart
                l_vdssource_val = vdsstart  # Reinitialize voltage value after last iteration

            Source_meter.smua.source.levelv = l_vdssource_val  # Increment source

        l_vgssource_val = l_vgssource_val + l_vgsstep  # Calculate new source value

    Source_meter.smua.source.output = Source_meter.smua.OUTPUT_OFF
    Source_meter.smub.source.output = Source_meter.smub.OUTPUT_OFF
    Source_meter.smua.source.levelv = 0
    Source_meter.smub.source.leveli = 0

    l_vgs_iteration = 1
    l_vds_iteration = 1
    #  make column with x vals
    # make column with y vals
    # by appending

    next_pos = 0
    for l_vgs_iteration in range(1, l_vgssteps):
        print("")
        print("Gate-source Bias (V)")
        print(l_vgs_data[l_vgs_iteration])
        print("Drain-source Voltage (V)", "Drain-source Current (A)")
        for l_vds_iteration in range(1, l_vdssteps):
            print(l_vds_data[l_vgs_iteration][l_vds_iteration], l_id_data[l_vgs_iteration][l_vds_iteration])
            if l_vgs_iteration == 1:
                xvals_1[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_1[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 2:
                xvals_2[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_2[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 3:
                xvals_3[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_3[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 4:
                xvals_4[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_4[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 5:
                xvals_5[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_5[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 6:
                xvals_6[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_6[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 7:
                xvals_7[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_7[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 8:
                xvals_8[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_8[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 9:
                xvals_9[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_9[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 10:
                xvals_10[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_10[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 11:
                xvals_11[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_11[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 12:
                xvals_12[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_12[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 13:
                xvals_13[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_13[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 14:
                xvals_14[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_14[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 15:
                xvals_15[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_15[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 16:
                xvals_16[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_16[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 17:
                xvals_17[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_17[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 18:
                xvals_18[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_18[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 19:
                xvals_19[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_19[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 20:
                xvals_20[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_20[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 21:
                xvals_21[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_21[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 22:
                xvals_22[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_22[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 23:
                xvals_23[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_23[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 24:
                xvals_24[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_24[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            elif l_vgs_iteration == 25:
                xvals_25[next_pos] = l_vds_data[l_vgs_iteration][l_vds_iteration]
                yvals_25[next_pos] = l_id_data[l_vgs_iteration][l_vds_iteration]
            next_pos = next_pos + 1

def graph_mosfet():
    next_color = ['y', 'm', 'c', 'r', 'g', 'b', 'k']
    next_color_index = 0


    # my_graph.legend('Vbe vs. Ib' 'Vbe vs. Ic')
    my_graph.xlabel('Drain Voltage (Volts)')
    my_graph.ylabel('Drain Current (Amps)')
    my_graph.title('BS170 MOSFET Gate Bias Characterization')
    my_graph.show()

# DIODE CHARACTERIZATION - automated (for loop)
num_devices = 2
next_device = 6000
# for i in range(14, 14):
 #   new_position = next_device + i
 #   print(new_position)
 #   System_Switch.write('channel.open("allslots")')
 #   System_Switch.write('channel.close("new_position")')
 #   diode_vsweep(1, -1, 1)  # fix parameters
 #   System_Switch.write('waitcomplete()')
 #   graph_diode()
 #   System_Switch.write('channel.open("allslots")')

# BJT CHARACTERIZATION - automated (for loop)
# for i in range(14, 14):
#    System_Switch.write('channel.open("allslots")')
#    System_Switch.write('channel.close("6014")')
#    System_Switch.write('channel.close("6029")')
#    bjt_vsweep(1, 4, 5)  # fix parameters
#    System_Switch.write('waitcomplete()')
#    graph_bjt()
#    System_Switch.write('channel.open("allslots")')

# MOSFET CHARACTERIZATION - automated (for loop)
#for i in range(14, 14):
# System_Switch.write('channel.open("allslots")')
# System_Switch.write('channel.close("6014")')
# System_Switch.write('channel.close("6029")')
#mosfet_vsweep(1, 5, 1, 5)  # fix parameters
  #  System_Switch.write('waitcomplete()')
  #  System_Switch.write('channel.open("allslots")')

#graph_mosfet()

