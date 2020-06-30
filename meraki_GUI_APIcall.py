import meraki
import os

def commandList():
    commands=[
        'Create Network',
        'Delete Network', 
        'Add Device(s)', #done
        'Remove Device(s)', #done
        'Rename Device',
        'Bulk Add Address', #done
        'Add VLAN',
        'Delete VLAN', #done
        'Swap MX Warm Spare', #done
        'Blink LED', #done
        'Update Device Port'
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

#getNetworkDevices() API call
def deviceInfo(net_id):
    getNetDevices=dashboard.networks.getNetworkDevices(net_id)
    return getNetDevices

def specDevInfo(serial):
    devInfo=dashboard.devices.getDevice(serial)
    return devInfo

#getNetworkApplianceVlans() API call
def getNetVlan(net_id):
    getNetVlan=dashboard.appliance.getNetworkApplianceVlans(network_id)
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


#swapNetworkApplianceWamSpare() API call
def swapWarmSpare(net_id):
    dashboard.appliance.swapNetworkApplianceWarmSpare(net_id)

#createVLAN() API call
def createVLAN(net_id,id,name,subnet,ip):
    dashboard.appliance.createNetworkApplianceVlan(
        net_id,id,name,subnet,ip)

#blinkDeviceLeds() API call
def blinkDevice(serial):
    dashboard.devices.blinkDeviceLeds(serial, duration=20, period=160, duty=50)

def setAddress(serials,address): #bulk change address
    dashboard.devices.updateDevice(serials,address=address)

# def updateDevSwitchport():
#     dashboard.switch.updateDeviceSwitchPort(
#         serial, port_id, 
#         name='My switch port', 
#         tags=['tag1', 'tag2'], 
#         enabled=True, 
#         type='access', 
#         vlan=10, 
#         voiceVlan=20, 
#         poeEnabled=True, 
#         isolationEnabled=False, 
#         rstpEnabled=True, 
#         stpGuard='disabled', 
#         linkNegotiation='Auto negotiate', 
#         portScheduleId='1234', 
#         udld='Alert only', 
#         accessPolicyType='Sticky MAC whitelist', 
#         stickyMacWhitelist=['34:56:fe:ce:8e:b0', '34:56:fe:ce:8e:b1'], 
#         stickyMacWhitelistLimit=5, 
#         stormControlEnabled=True
#     )

#updateNetworkApplianceVlan() API call
# def updateVLAN():
#     response = dashboard.appliance.updateNetworkApplianceVlan(
#     network_id, vlan_id, 
#     name='My VLAN', 
#     subnet='192.168.1.0/24', 
#     applianceIp='192.168.1.2', 
#     groupPolicyId='101', 
#     dhcpHandling='Run a DHCP server', 
#     dhcpLeaseTime='1 day', 
#     dhcpBootOptionsEnabled=False, 
#     dhcpBootNextServer=None, 
#     dhcpBootFilename=None, 
#     fixedIpAssignments={'22:33:44:55:66:77': {'ip': '1.2.3.4', 'name': 'Some client name'}}, 
#     reservedIpRanges=[{'start': '192.168.1.0', 'end': '192.168.1.1', 'comment': 'A reserved IP range'}], 
#     dnsNameservers='google_dns', 
#     dhcpOptions=[{'code': 5, 'type': 'text', 'value': 'five'}]
# )

def removeVLAN(net_id,vlan_id):
    dashboard.appliance.deleteNetworkApplianceVlan(net_id, vlan_id)