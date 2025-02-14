# Authors: Antoine Ginies <aginies@suse.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Prepare the Host system
"""

import uuid
import os
from string import Template
import pyudev
import virtscenario.template as template
import virtscenario.util as util
import virtscenario.sev as sev

def create_net_xml(file, net_data):
    """
    Create a libvirt XML for the network bridge
    """
    xml_template = template.NETWORK_TEMPLATE
    xml_net = {
        'network_uuid': str(uuid.uuid4()),
        'network_name': net_data['network_name'],
        'bridge': net_data['bridge'],
        'stp': net_data['stp'],
        'ip': net_data['ip'],
        'netmask': net_data['netmask'],
        'dhcp_start': '.'.join(net_data['ip'].split('.')[0:3]+[net_data['dhcp_start']]),
        'dhcp_end': '.'.join(net_data['ip'].split('.')[0:3]+[net_data['dhcp_end']]),
    }

    xml = Template(xml_template).substitute(xml_net)
    print("Create network bridge " +file)
    with open(file, 'w') as file_h:
        file_h.write(xml)

def create_storage_vol_xml(file, storage_data):
    """
    Create storage vol xml
    """
    xml_template = template.STORAGE_TEMPLATE
    xml_storage = {
        'storage_uuid': str(uuid.uuid4()),
        'storage_name': storage_data['storage_name'],
        'allocation': storage_data['allocation'],
        'unit': storage_data['unit'],
        'capacity': storage_data['capacity'],
        'path': storage_data['path']+'.'+storage_data['type'],
        'owner': storage_data['owner'],
        'group': storage_data['group'],
        'mode': storage_data['mode'],
        'label': storage_data['label'],
        }

    xml = Template(xml_template).substitute(xml_storage)
    print("Create storage volume " +file)
    with open(file, 'w') as file_h:
        file_h.write(xml)

def create_storage_image(storage_data):
    """
    Create the storage image
    """
    # TOFIX: prealloc metadata only for qcow2 image
    util.print_summary("\nCreating the Virtual Machine image")
    encryption = ""
    #ie: qemu-img create -f qcow2 Win2k.img 20G
    if os.path.isdir(storage_data['path']):
        print(storage_data['path'])
    else:
        util.print_warning(storage_data['path']+" Doesnt exist, creating it")
        try:
            os.makedirs(storage_data['path'], exist_ok=True)
        except Exception:
            util.print_error("Can't create "+storage_data['path']+" directory")
    filename = storage_data['path']+"/"+storage_data['storage_name']+"."+storage_data['format']
    cmd = "qemu-img create"

    # preallocation: off / metadata / falloc, full
    if storage_data['preallocation'] is False:
        preallocation = "preallocation=off"
    else:
        preallocation = "preallocation="+str(storage_data['preallocation'])

    # qcow2 related stuff
    if storage_data['format'] == "qcow2":
        # on / off VS True / False
        lazyref = ""
        if storage_data['lazy_refcounts'] is True:
            lazyref = "lazy_refcounts=on"
        else:
            lazyref = "lazy_refcounts=off"
        # cluster size: 512k / 2M
        clustersize = "cluster_size="+storage_data['cluster_size']
        # zlib zstd
        compression_type = "compression_type="+storage_data['compression_type']

        # encryption on
        if storage_data['encryption'] is True:
        # qemu-img create --object secret,id=sec0,data=123456 -f qcow2
        # -o encrypt.format=luks,encrypt.key-secret=sec0 base.qcow2 1G
            encryption = " --object secret,id=sec0,data="+storage_data['password']
            encryption += " -o "+"encrypt.format=luks,encrypt.key-secret=sec0"

        cmdall = cmd+" -o "+lazyref+","+clustersize+","+preallocation+","+compression_type
        cmdall += " -f "+storage_data['format']
        cmdall += encryption+" "+filename+" "+str(storage_data['capacity'])+storage_data['unit']
    else:
        # this is not a qcow2 format
        cmdoptions = " -o "+preallocation
        cmdoptions += " -f "+storage_data['format']+" "+filename
        cmdoptions += " "+str(storage_data['capacity'])+storage_data['unit']
        cmdall = cmd+" "+cmdoptions

    print(cmdall)
    out, errs = util.system_command(cmdall)
    if errs:
        print(errs)
    if not out:
        print(' No output... seems weird...')
    else:
        print(out)

def check_cpu_flag(flag):
    """
    check if a CPU flag is present
    """
    cpuinfo = open("/proc/cpuinfo")
    data = cpuinfo.read()
    test = data.find(flag)
    cpuinfo.close()
    return test

def sev_info():
    """
    grab the SEV information
    """
    sev_info = sev.SevInfo()
    sev_info.host_detect()

    return sev_info

def check_libvirt_sev(sev_info):
    """
    check that libvirt support sev
    """
    util.print_summary("\nCheck libvirt support SEV")
    if sev_info.supported() is True:
        util.print_ok("Libvirt support SEV")
    else:
        util.print_error("Libvirt does not Support SEV!")

def check_sev_enable():
    """
    check that sev is enable on this system
    """
    sevinfo = open("/sys/module/kvm_amd/parameters/sev")
    #sevinfo = open("/sys/module/kvm/supported")
    data = sevinfo.read()
    test = data.find("Y")
    sevinfo.close()
    return test

def check_in_container():
    """
    check if inside a container
    """
#    if os.environ['container'] != "":
#        return True
    out, errs = util.system_command("systemd-detect-virt -c")
    if errs:
        print(errs)
    if out.find("none") == -1:
        print("You are inside a container, you should do some stuff on the host system....")
        return True

def enable_sev():
    """
    enable sev on the system
    """
    if check_in_container() is True:
        print("Create: /etc/modprobe.d/sev.conf")
        print("options mem_encrypt=on kvm_amd sev=1 sev_es=1")
    else:
        sevconf = open("/etc/modprobe.d/sev.conf", "w")
        sevconf.write("options mem_encrypt=on kvm_amd sev=1 sev_es=1")
        sevconf.close()

def hugepages_enable():
    """
    check that vm.nr_hugepages is not 0
    reserve 1 GB (1,048,576 KB) for your VM Guest (2M hugepages)
    """
    hpconf = "/etc/sysctl.d/hugepages.conf"
    if check_in_container() is True:
        print("Create: /etc/sysctl.d/hugepages.conf")
        print("sysctl vm.nr_hugepages=512")
    else:
        if os.path.isfile(hpconf):
            print(hpconf+" Already exist")
            return True
        else:
            print("Creating "+hpconf)
            fdhp = open(hpconf, "w")
            fdhp.write("vm.nr_hugepages=512")
            fdhp.close()
            out, errs = util.system_command("sysctl vm.nr_hugepages=512")
            util.print_summary("\nSetting vm.nr_hugepages=512")
            if errs:
                print(errs)
            print(out)

def reprobe_kvm_amd_module():
    """
    reload the module
    """
    cmd = "modprobe -vr kvm_amd ; modprobe -v kvm_amd"
    if check_in_container() is True:
        print(cmd)
    else:
        out, errs = util.system_command(cmd)
        util.print_summary("\nReprobe the KVM module")
        if errs:
            print(errs)
        print(out)

def manage_ksm(todo, merge_across):
    """
    manage ksm
    """
    if todo == "enable":
        action = "start"
    else:
        action = "stop"
    cmd1 = "systemctl "+todo+" ksm"
    cmd2 = "systemctl "+action+" ksm"
    if merge_across == "enable":
        cmd3 = "echo 1 > /sys/kernel/mm/ksm/merge_across_nodes"
    elif merge_across == "disable":
        cmd3 = "echo 0 > /sys/kernel/mm/ksm/merge_across_nodes"
    else:
        cmd3 = ""
    util.print_summary("\nManaging KSM")
    if check_in_container() is True:
        for cmds in [cmd1, cmd2, cmd3]:
            print(cmds)
    else:
        for cmds in [cmd1, cmd2, cmd3]:
            out, errs = util.system_command(cmds)
            if errs:
                print(str(errs)+" "+str(out))
        if todo == "enable":
            print("KSM enabled")
        else:
            print("KSM disabled")

def swappiness(number):
    """
    swappiness
    """
    util.print_summary("\nSwappiness")
    #echo 35 > /proc/sys/vm/swappiness
    #/etc/systcl.conf
    #vm.swappiness = 35
    cmd = "echo "+number+"> /proc/sys/vm/swappiness"
    if check_in_container() is True:
        print(cmd)
    else:
        out, errs = util.system_command(cmd)
        if errs:
            print(str(errs)+" "+str(out))
        print(cmd)

def list_all_disk():
    """
    list all disks available
    """
    context = pyudev.Context()
    all_disk = []
    for device in context.list_devices(MAJOR='8'):
        if device.device_type == 'disk':
            #print("{}, ({})".format(device.device_node, device.device_type))
            onlydev = device.device_node.replace("/dev", "")
            all_disk.append(onlydev)
    return all_disk

def manage_ioscheduler(scheduler):
    """
    manage ioscheduler
    """
    util.print_summary("\nIO scheduler")
    listdisk = list_all_disk()
    cmdstart = "echo "+scheduler+" > /sys/block"
    cmdend = "/queue/scheduler"
    if check_in_container() is True:
        for disk in listdisk:
            print(cmdstart+disk+cmdend)
    else:
        for disk in listdisk:
            out, errs = util.system_command(cmdstart+disk+cmdend)
            if errs:
                print(str(errs)+" "+str(out))
            print(cmdstart+disk+cmdend)
        print("\nRecommended IO Scheduler inside VM guest is 'none'")

def kvm_amd_sev(sev_info):
    """
    be sure kvm_amd sev is enable if not enable it
    https://documentation.suse.com/sles/15-SP1/html/SLES-amd-sev/index.html
    """
    util.print_summary("Host section")
    util.print_summary("Enabling sev if needed")
    check_libvirt_sev(sev_info)
    flag = "sev"
    test_flag = check_cpu_flag(flag)
    if test_flag <= -1:
        util.print_error(" "+flag+" CPU flag not found...")
        util.print_error("WARNING: You can not do secure VM on this system (SEV)")
    else:
        util.print_ok("Found "+flag+" CPU flag")
        test_sev = check_sev_enable()
        if test_sev <= -1:
            util.print_error(" SEV not enabled on this system")
            enable_sev()
            reprobe_kvm_amd_module()
        else:
            util.print_ok(" SEV enabled on this system")

def hugepages():
    """
    prepare system to use hugepages
    https://documentation.suse.com/sles/15-SP4/single-html/SLES-virtualization-best-practices/#sec-vt-best-mem-huge-pages
    """
    #pdpe1gb pse
    util.print_summary("\nManaging Huge Pages")
    flaglist = ["pdpe1gb", "pse"]
    foundok = False
    for flag in flaglist:
        test_flag = check_cpu_flag(flag)
        if test_flag <= -1:
            util.print_error(" "+flag+" CPU flag not found...")
        else:
            util.print_ok("Found "+flag+" CPU flag")
            foundok = True
    if foundok is True:
        hugepages_enable()
    else:
        util.print_error("There is no hugepages support on this system")

def host_end(filename, toreport, conffile):
    """
    end of host configuration
    """
    util.print_summary_ok("\nHost Configuration is done")
    if len(toreport) != 6:
        util.print_summary("\nComparison table between user and recommended settings")
        util.print_warning("You are over writing scenario setting!")
        print("     Overwrite are from "+conffile+"\n")
        util.print_recommended(toreport)
    util.print_summary_ok("\nHow to use this on your system")
    util.print_ok("\nvirsh define "+filename+"\n")

# Net data
NET_DATA = {
    'network_name': "test_net",
    'bridge': "br0",
    'stp': "on",
    'ip': "192.168.12.1",
    'netmask': "255.255.255.0",
    'dhcp_start': "30",
    'dhcp_end': "254",
}
#create_net_xml("net.xml", NET_DATA)
