"""
FP run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.term import makeTerm
#from minicps.mcps import MiniCPS
from topo import FPTopo

import time
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages')

from minicps.mcps import MiniCPS

class FPCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()
        net.pingAll()

        # start devices
        plc1, plc2, plc3, s1, attacker = self.net.get('plc1', 'plc2', 'plc3', 's1', 'attacker')
        
        s1.cmd('screen -dmSL power python physical_process.py')
        s1.cmd('screen -dmSL centrifuge python physical_process_centrifuge.py')
        plc3.cmd('screen -dmSL plc3 python plc3.py -Logfile')
        plc2.cmd('screen -dmSL plc2 python plc2.py -Logfile')
        plc1.cmd('screen -dmSL plc1 python plc1.py -Logfile')
        attacker.cmd('screen -dmSL attacker bash attack.sh')
        '''
        # to see the scripts running (xterm required),
        # uncomment the following lines (while removing the .cmd lines above)
        net.terms += makeTerm(s1, display=None, cmd='python physical_process.py')
        time.sleep(0.2)
        net.terms += makeTerm(s1, display=None, cmd='python physical_process_centrifuge.py')
        time.sleep(0.2)
        net.terms += makeTerm(plc3, display=None, cmd='python plc3.py')    # display=None
        time.sleep(0.2)
        net.terms += makeTerm(plc2, display=None, cmd='python plc2.py')
        time.sleep(0.2)
        net.terms += makeTerm(plc1, display=None, cmd='python plc1.py')
        '''
        CLI(self.net)
        # self.net.stop()


if __name__ == "__main__":

    topo = FPTopo()
    net = Mininet(topo=topo)

    fpcps = FPCPS(
        name='FPCPS',
        net=net)
