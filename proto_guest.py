#!/usr/bin/env python3
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
Guest side definition
"""

import uuid
from string import Template
import template


def create_name(name_data):
    """
    name and uuid
    """
    xml_template = template.NAME_TEMPLATE
    xml_name = {
        'VM_name': name_data['VM_name'],
        'VM_uuid': str(uuid.uuid4()),
    }
    xml = Template(xml_template).substitute(xml_name)
    return xml

def create_metadata(metadata_data):
    """
    name and uuid
    """
    xml_template = template.METADATA_TEMPLATE
    #xml_metadata = { }
    #xml = Template(xml_template).substitute(xml_metadata)
    return xml_template

def create_memory(memory_data):
    """
    memory
    """
    xml_template = template.MEMORY_TEMPLATE
    xml_mem = {
        'mem_unit': memory_data['mem_unit'],
        'max_memory': memory_data['max_memory'],
        'current_mem_unit': memory_data['current_mem_unit'],
        'memory': memory_data['memory'],
    }
    xml = Template(xml_template).substitute(xml_mem)
    return xml

def create_cpu(cpu_data):
    """
    cpu
    """
    xml_template = template.CPU_TEMPLATE
    xml_cpu = {
        'vcpu': cpu_data['vcpu'],
    }
    xml = Template(xml_template).substitute(xml_cpu)
    return xml

def create_os(os_data):
    """
    os
    """
    xml_template = template.OS_TEMPLATE
    xml_os = {
        'arch': os_data['arch'],
        'machine': os_data['machine'],
        'boot_dev': os_data['boot_dev'],
    }
    xml = Template(xml_template).substitute(xml_os)
    return xml

def create_features(features_data):
    """
    features
    """
    xml_template = template.FEATURES_TEMPLATE
    xml_features = {
        'features': features_data['features'],
    }
    xml = Template(xml_template).substitute(xml_features)
    return xml

def create_cpumode(cpumode_data):
    """
    features
    """
    xml_template = template.CPUMODE_TEMPLATE
    xml_cpumode = {
        'cpu_mode': cpumode_data['cpu_mode'],
        'migratable': cpumode_data['migratable'],
    }
    xml = Template(xml_template).substitute(xml_cpumode)
    return xml

def create_clock(clock_data):
    """
    clock
    """
    xml_template = template.CLOCK_TEMPLATE
    xml_clock = {
        'clock_offset': clock_data['clock_offset'],
        'clock': clock_data['clock'],
    }
    xml = Template(xml_template).substitute(xml_clock)
    return xml

def create_on(on_data):
    """
    on power etc...
    """
    xml_template = template.ON_TEMPLATE
    xml_on = {
        'on_poweroff': on_data['on_poweroff'],
        'on_reboot': on_data['on_reboot'],
        'on_crash': on_data['on_crash'],
    }
    xml = Template(xml_template).substitute(xml_on)
    return xml

def create_power(power_data):
    """
    power
    """
    xml_template = template.POWER_TEMPLATE
    xml_power = {
        'suspend_to_mem': power_data['suspend_to_mem'],
        'suspend_to_disk': power_data['suspend_to_disk'],
    }
    xml = Template(xml_template).substitute(xml_power)
    return xml

def create_emulator(power_data):
    """
    power
    """
    xml_template = template.EMULATOR_TEMPLATE
    xml_emulator = {
        'emulator': power_data['emulator'],
        }
    xml = Template(xml_template).substitute(xml_emulator)
    return xml

def create_disk(disk_data):
    """
    disk
    """
    xml_template = template.DISK_TEMPLATE
    xml_disk = {
        'disk_type': disk_data['disk_type'],
        'disk_cache': disk_data['disk_cache'],
        'source_file': disk_data['source_file'],
        'disk_target': disk_data['disk_target'],
        'disk_bus': disk_data['disk_bus'],
    }
    xml = Template(xml_template).substitute(xml_disk)
    return xml

def create_interface(interface_data):
    """
    interface
    """
    xml_template = template.INTERFACE_TEMPLATE
    xml_interface = {
        'mac_address': interface_data['mac_address'],
        'network': interface_data['network'],
        'type': interface_data['type'],
    }
    xml = Template(xml_template).substitute(xml_interface)
    return xml

def create_channel(channel_data):
    """
    channel
    """
    xml_template = template.CHANNEL_TEMPLATE
    #xml_channel = { }
    #xml = Template(xml_template).substitute(xml_channel)
    return xml_template

def create_console(console_data):
    """
    console
    """
    xml_template = template.CONSOLE_TEMPLATE
    #xml_console = { }
    #xml = Template(xml_template).substitute(xml_console)
    return xml_template

def create_input(input_data):
    """
    input
    """
    xml_template = template.INPUT_TEMPLATE
    xml_input = {
        'type': input_data['type'],
        'bus': input_data['bus'],
    }
    xml = Template(xml_template).substitute(xml_input)
    return xml

def create_graphics(graphics_data):
    """
    graphics
    """
    xml_template = template.GRAPHICS_TEMPLATE
    #xml_graphics = { }
    #xml = Template(xml_template).substitute(xml_graphics)
    return xml_template

def create_audio(audio_data):
    """
    audio
    """
    xml_template = template.AUDIO_TEMPLATE
    xml_audio = {
        'model': audio_data['model'],
    }
    xml = Template(xml_template).substitute(xml_audio)
    return xml

def create_video(video_data):
    """
    video
    """
    xml_template = template.VIDEO_TEMPLATE
    #xml_video = { }
    #xml = Template(xml_template).substitute(xml_video)
    return xml_template

def create_watchdog(watchdog_data):
    """
    watchdog
    """
    xml_template = template.WATCHDOG_TEMPLATE
    xml_watchdog = {
        'model': watchdog_data['model'],
        'action': watchdog_data['action'],
    }
    xml = Template(xml_template).substitute(xml_watchdog)
    return xml

def create_memballoon(memballoon_data):
    """
    memballoon
    """
    xml_template = template.MEMBALLOON_TEMPLATE
    #xml_memballoon = { }
    #xml = Template(xml_template).substitute(xml_memballoon)
    return xml_template

def create_rng(rng_data):
    """
    rng
    """
    xml_template = template.RNG_TEMPLATE
    #xml_rng = { }
    #xml = Template(xml_template).substitute(xml_rng)
    return xml_template

def create_tpm(tpm_data):
    """
    tpm
    """
    xml_template = template.TPM_TEMPLATE
    xml_tpm = {
        'tpm_model': tpm_data['tpm_model'],
        'tpm_type': tpm_data['tpm_type'],
        'device_path': tpm_data['device_path'],
    }
    xml = Template(xml_template).substitute(xml_tpm)
    return xml
