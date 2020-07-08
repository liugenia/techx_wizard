import meraki
import os

def commandList():
    commands=[
        # 'Create Network', ####NEED FULL ORG ADMIN ACCESS FOR THIS####
        # 'Delete Network', 
        'Add Device', #done
        'Bulk Add Devices', #done
        'Rename Device', #done
        'Bulk Rename Device',
        'Remove Device(s)', #done
        'Update Device Port', #done
        'Bulk Add Address', #done
        'Add VLAN', #done
        'Delete VLAN', #done
        'Swap MX Warm Spare', #done
        'Blink LED', #done
        'Reboot Device'
        ]
    return commands

####GETTING INFORMATION####
#API key and dashboard
API_KEY=os.environ.get('Meraki_API')
dashboard=meraki.DashboardAPI(API_KEY, output_log=False, print_console=False)
# dashboard=meraki.DashboardAPI(API_KEY)

#getOrganizations() API call
def orgInfo():
    getOrg=dashboard.organizations.getOrganizations()
    return getOrg

#getOrganizationNetworks() API call
def orgNetInfo(org_id):
    getOrgNet=dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
    return getOrgNet

#getNetwork() API call
def netInfo(net_id):
    dashboard.networks.getNetwork(net_id)

def netVlanInfo(net_id):
    dashboard.appliance.getNetworkApplianceVlans(net_id)

#getNetworkDevices() API call
def deviceInfo(net_id):
    getNetDevices=dashboard.networks.getNetworkDevices(net_id)
    return getNetDevices

def specDevInfo(serial):
    devInfo=dashboard.devices.getDevice(serial)
    return devInfo

#getNetworkApplianceVlans() API call
def getNetVlan(net_id):
    getNetVlan=dashboard.appliance.getNetworkApplianceVlans(net_id)
    return getNetVlan

####MAKING CHANGES TO THE NETWORK####
#createOrganizationNetwork() API call
def createNetwork(org_id,net_name,prod_types):
    dashboard.organizations.createOrganizationNetwork(
    org_id, net_name, prod_types)

def deleteNetwork(net_id):
    dashboard.networks.deleteNetwork(net_id)

#claimNetworkDevices() API call
def claimDevices(net_id,serials):
    dashboard.networks.claimNetworkDevices(net_id, serials)

#removeNetworkDevices() API call
def removeDevices(net_id,serial):
    dashboard.networks.removeNetworkDevices(net_id,serial)

#renames device
def renameDevice(serial,dev_name):
    dashboard.devices.updateDevice(serial,name=dev_name)

#bulk adds address when called for each SN in network
def setAddress(serials,address):
    dashboard.devices.updateDevice(serials,address=address)

#swapNetworkApplianceWamSpare() API call
def swapWarmSpare(net_id):
    dashboard.appliance.swapNetworkApplianceWarmSpare(net_id)

#createVLAN() API call
def createVLAN(net_id,id,name,subnet,ip):
    dashboard.appliance.createNetworkApplianceVlan(
        net_id,id,name,subnet,ip
        )

#blinkDeviceLeds() API call
def blinkDevice(serial):
    dashboard.devices.blinkDeviceLeds(serial, duration=20, period=160, duty=50)

#if no VLAN input aka trunk port update or access port with unchanged VLAN ID
def updateDevSwitchport(serial,id,port_type):
    dashboard.switch.updateDeviceSwitchPort(
        serial, id, 
        type=port_type,
    )

#if there is a VLAN input aka access port update
def updateDevSwitchportVLAN(serial,id,port_type,vlan):
    dashboard.switch.updateDeviceSwitchPort(
        serial, id, 
        type=port_type, 
        vlan=vlan
    )

#updateNetworkApplianceVlan() API call
def updateVLAN(vlan_id,ip):
    dashboard.appliance.updateNetworkApplianceVlan(vlan_id,ip)

#deleteNetworkApplianceVlan() API call
def removeVLAN(net_id,vlan_id):
    dashboard.appliance.deleteNetworkApplianceVlan(net_id, vlan_id)

def rebootDevice(serial):
    dashboard.devices.rebootDevice(serial)