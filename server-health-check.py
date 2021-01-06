""" MFW Status Report """
import sys
import os
import platform
import requests

# Add local lib path
pathname = os.path.dirname(sys.argv[0])
sys.path.append(os.path.abspath(pathname) + "/modules/")

# --------------------------------------------------------------------- #
# Import General modules
from mfw_lib_status import *
from mfw_lib_general import *

# --------------------------------------------------------------------- #
# Define
SLACKBOT_WEBHOOK = "https://piclickbot.herokuapp.com/gathering"
SLACKBOT_WEBHOOK_DEBUG = "http://localhost:5000/gathering"

# --------------------------------------------------------------------- #

def gather_info():
    """ gather_info """
    DATE      = get_timestamp()
    IPADDRESS = f"{get_network_ip()}/{get_external_ip()}"
    HOSTNAME  = get_hostname()
    CPULOAD   = get_cpuload()
    PROCESS   = get_processcount()
    MEMFREE   = get_memfree(get_memfreeb())
    MEMUSED   = get_memused(get_memusedb(get_memtotalb(), get_memfreeb()))
    MEMTOTAL  = get_memtotal(get_memtotalb())
    SWAPFREE  = get_swapfree(get_swapfreeb())
    SWAPUSED  = get_swapused(get_swapusedb(get_swaptotalb(), get_swapfreeb()))
    SWAPTOTAL = get_swaptotal(get_swaptotalb()) if get_swaptotal(get_swaptotalb()) != 0.0 else 1
    ROOTFREE  = get_rootfree(get_rootfreeb())
    ROOTUSED  = get_rootused(get_rootusedb())
    ROOTTOTAL = get_roottotal(get_roottotalb())

    MESSAGE  = f"CPU Load : {CPULOAD}\n"
    MESSAGE += f"Memory : Free: {MEMFREE} GB ({round(float(MEMFREE)/float(MEMTOTAL),2)*100}%), Used: {MEMUSED} GB ({round(float(MEMUSED)/float(MEMTOTAL),2)*100}%), Total: {MEMTOTAL} GB \n" 
    MESSAGE += f"Swap : Free: {SWAPFREE} GB ({round(float(SWAPFREE)/float(SWAPTOTAL),2)*100}%), Used: {SWAPUSED} GB ({round(float(SWAPUSED)/float(SWAPTOTAL),2)*100}%), Total: {SWAPTOTAL} GB \n"
    MESSAGE += f"Root : Free:{ROOTFREE} GB ({get_rootfreeperc(get_rootusedperc())}%), Used: {ROOTUSED} GB ({get_rootusedperc()}%), Total: {ROOTTOTAL} GB \n"
    MESSAGE += f"Processes : {PROCESS}\n"

    return {
        "DATE": DATE,
        "IPADDRESS": IPADDRESS,
        "HOSTNAME": HOSTNAME,
        "MESSAGE": MESSAGE
    }

def exec_interval():
  requests.post(SLACKBOT_WEBHOOK, data=gather_info())


# --------------------------------------------------------------------- #
if __name__ == "__main__":
  exec_interval()
