from tkinter import *
from tkinter import filedialog as fd
from meraki_GUI_APIcall import *
import xlrd
import numpy

class MerakiWizard(Frame):
    ####MERAKI GUI INTERFACE####
    def __init__(self,parent,*args,**kwargs):
        self.parent=parent
        self.org_info=orgInfo()
        #Select Organization label
        self.org_title=Label(text="Select Organization")
        self.org_title.grid(row=0,column=0)
        #Org Listbox: takes Org Name, passes Org ID on button click to get list of networks
        self.orgMenu=Listbox(root,exportselection=False) 
        self.orgMenu.grid(row=1,column=0)
        for org_name in self.getOrgList():
            self.orgMenu.insert(END,org_name)
            self.orgMenu.bind("<<ListboxSelect>>", self.popuNetNames)
        #Select Network label
        self.net_title=Label(text="Select Network")
        self.net_title.grid(row=0, column=1)
        #Network Listbox: takes Network Name, passes Network ID on button click to get list of devices
        self.netMenu=Listbox(root,exportselection=False)
        self.netMenu.grid(row=1, column=1)
        self.netMenu.bind("<<ListboxSelect>>", self.popuDevNames)
        #Select Devices label
        self.net_title=Label(text="Select Device")
        self.net_title.grid(row=0, column=2)
        #Device Listbox: Takes Device Name, passes Device 
        self.devMenu=Listbox(root,exportselection=False)
        self.devMenu.grid(row=1,column=2)
        self.devMenu.bind("<<ListboxSelect>>", self.getNetDevSerials)
        #network option menu
        self.commands=commandList()
        self.alter=StringVar(root)
        self.alter.set(self.commands[0])
        self.alterMenu=OptionMenu(root,self.alter,*self.commands)
        self.alterMenu.grid(row=4,column=0)
        #select button
        self.selectButton=Button(
            root,text='Select Action',command=self.AlterMenu, bg='#049fd9', fg='white')
        self.selectButton.grid(row=4,column=1)

    ####ALTERATION DROPDOWN MENU####
    def AlterMenu(self):
        self.selected=self.alter.get()
        if self.selected=='Create Network':
            pass
        elif self.selected=='Delete Network': #deletes network and all devices
            deleteNetwork(self.getNetID())
            self.popuNetNames()
        elif self.selected=='Add Device': #adds a single device to the network
            self.infoPopup()
            self.popuDevNames()
        elif self.selected=='Bulk Add Devices': #automatically adds all devices on .csv file
            claimDevices(self.getNetID(),self.getDevicesExcel())
            self.popuDevNames()
        elif self.selected=='Rename Device': #renames a device that is selected from listbox
            self.infoPopup()
            self.popuDevNames()
        elif self.selected=='Remove Device(s)': #removes the devices selected or all devices
            self.delDevices()
        elif self.selected=='Bulk Add Address': #adds the input address for all devices
            self.infoPopup()
        elif self.selected=='Add VLAN': #adds a VLAN given user input
            self.infoPopup()
        elif self.selected=='Delete VLAN': #deletes VLAN given the VLAN ID
            self.infoPopup()
        elif self.selected=='Swap MX Warm Spare': #switches primary and warm MX
            swapWarmSpare(self.getNetID()) 
        elif self.selected=='Blink LED': #blinks LED of chosen device
            blinkDevice(self.getDevSerial())
        elif self.selected=='Update Device Port': #updates port type and vlan on chosen device
            self.infoPopup()
    def infoPopup(self): #popup menu if needed for inputs required 
        self.selected=self.alter.get()
        self.entry=Toplevel()
        if self.selected=='Add Device':
            self.getInput=Label(self.entry,text='Enter Device SN:')
            self.getInput.pack()
            self.devSnEntry=Entry(self.entry)
            self.devSnEntry.pack()
        elif self.selected=='Rename Device':
            self.getInput=Label(self.entry,text='Rename device to:')
            self.getInput.pack()
            self.renameEntry=Entry(self.entry)
            self.renameEntry.pack()   
        elif self.selected=='Bulk Add Address':
            self.getInput=Label(self.entry,text='Enter address:')
            self.getInput.pack()
            self.addrEntry=Entry(self.entry)
            self.addrEntry.pack()
        elif self.selected=='Add VLAN':
            self.getID=Label(self.entry,text='ID:')
            self.getID.pack()
            self.idEnt=Entry(self.entry)
            self.idEnt.pack()
            self.getName=Label(self.entry,text='Name:')
            self.getName.pack()
            self.nameEnt=Entry(self.entry)
            self.nameEnt.pack()
            self.getSubnet=Label(self.entry,text='Subnet:')
            self.getSubnet.pack()
            self.subEnt=Entry(self.entry)
            self.subEnt.pack()
            self.getAppIp=Label(self.entry,text='Appliance IP:')
            self.getAppIp.pack()
            self.appEnt=Entry(self.entry)
            self.appEnt.pack()
        elif self.selected=='Delete VLAN':
            self.getInput=Label(self.entry,text='Enter VLAN ID:')
            self.getInput.pack()
            self.vlanIdEntry=Entry(self.entry)
            self.vlanIdEntry.pack()
        elif self.selected=='Update Device Port':
            self.getId=Label(self.entry,text='Enter port ID:')
            self.getId.pack()
            self.idEnt=Entry(self.entry)
            self.idEnt.pack()
            self.getType=Label(self.entry,text='Enter port type:')
            self.getType.pack()
            self.typeEnt=Entry(self.entry)
            self.typeEnt.pack()
            self.getVlan=Label(self.entry,text='Enter port VLAN:')
            self.getVlan.pack()
            self.vlanEnt=Entry(self.entry)
            self.vlanEnt.pack()
        self.doneButton=Button(self.entry,text='Done',command=self.quitInput)
        self.doneButton.pack()     
    def quitInput(self):
        self.selected=self.alter.get()
        if self.selected=='Add Device':
            self.to_add=[]
            self.to_add.append(str(self.devSnEntry.get()))
            claimDevices(self.getNetID(),self.to_add)
            self.popuDevNames()
        elif self.selected=='Rename Device': #do NOT name devices the same name, this will make the program bug out
            renameDevice(self.getDevSerial(),self.renameEntry.get())
            self.popuDevNames()
        elif self.selected=='Update Device Port': #if you specify trunk you shouldn't be adding a VLAN!!!
            if self.vlanEnt.get():
                updateDevSwitchportVLAN(
                    self.getDevSerial(),self.idEnt.get(),
                    self.typeEnt.get(),self.vlanEnt.get())
            else:
                updateDevSwitchport(
                    self.getDevSerial(),self.idEnt.get(),
                    self.typeEnt.get()) 
        elif self.selected=='Bulk Add Address':
            for device in self.getNetDevSerials():
                setAddress(device,self.addrEntry.get())  
        elif self.selected=='Add VLAN':
            createVLAN(
                self.getNetID(),self.idEnt.get(),self.nameEnt.get(),
                self.subEnt.get(),self.appEnt.get())
        elif self.selected=='Delete VLAN':
            removeVLAN(self.getNetID(),self.vlanIdEntry.get())  
        self.entry.destroy()

    ####ORG FUNCTIONS####
    def getOrgList(self): #return the list of accessible orgs
        self.the_orgs=[org['name'] for org in self.org_info]
        return self.the_orgs
    def getOrgID(self,*args): #get org ID given org name
        self.name=self.orgMenu.get(self.orgMenu.curselection())
        self.org_id=''
        for orgs in self.org_info:
            if orgs['name']==self.name:
               self.org_id+=orgs['id']
        return self.org_id

    ####NETWORK FUNCTIONS####
    def getNetID(self,*args): #get net ID given net name
        self.org_nets=orgNetInfo(self.getOrgID())
        self.name=self.netMenu.get(self.netMenu.curselection())
        self.curr_net=''
        for nets in self.org_nets:
            if nets['name']==self.name:
                self.curr_net+=(nets['id'])
        return self.curr_net
    def getOrgNetIDs(self): #get list all network IDs in an org given org ID
        self.net_info=orgNetInfo(self.getOrgID())
        self.net_ids=[]
        for nets in self.net_info:
            if nets['organizationId']==self.getOrgID():
                self.net_ids.append(nets['id'])
        return self.net_ids
    def getOrgNetNames(self): #get list of all network names given list of netID
        self.net_info=orgNetInfo(self.getOrgID())
        self.net_ids=self.getOrgNetIDs()
        self.net_names=[]
        for ident in self.net_ids:
            for nets in self.net_info:
                if nets['id']==ident:
                    self.net_names.append(nets['name'])
        return self.net_names
    def popuNetNames(self,*args): #populates listbox on click per orgNetwork button, refreshes each new click
        self.netMenu.delete(0,END)
        for name in self.getOrgNetNames():
            self.netMenu.insert(END,name)
    def getNetDevices(self,*args): #given selected network name, return dictlist of all devices in the network
        self.net_info=orgNetInfo(self.getOrgID())
        self.name=self.netMenu.get(self.netMenu.curselection())
        self.curr_net=''
        for nets in self.net_info:
            if nets['name']==self.name:
                self.curr_net+=(nets['id'])
        return deviceInfo(self.curr_net)
    def getNetDevSerials(self,*args): #gets SN of all network devices
        self.dev_info=self.getNetDevices()
        self.serial=[]
        for device in self.dev_info:
            self.serial.append(device['serial'])
        return self.serial

    ####DEVICE FUNCTIONS####
    def getDevNames(self): #gets list of device names in a network
        self.the_devs=[dev['name'] for dev in self.getNetDevices()]
        return self.the_devs
    def popuDevNames(self,*args): #populates listbox on click of selecting network
        self.devMenu.delete(0,END)
        for name in self.getDevNames():
            self.devMenu.insert(END,name)
    def getDevSerial(self,*args): #gets the device SN given the listbox selection
        self.net_devs=self.getNetDevices()
        self.curr_dev=''
        self.name=self.devMenu.get(self.devMenu.curselection())
        for devs in self.net_devs:
            if devs['name']==self.name:
                self.curr_dev+=devs['serial']
        return self.curr_dev
    def getDevicesExcel(self,*args): #Add devices given JLL .xls(x) file
        self.file_name=fd.askopenfilename(initialdir='/',title='Select A File',filetypes=(('.xls','*.xls'),('all files','.')))
        self.wb=xlrd.open_workbook(self.file_name)
        self.sheet=self.wb.sheet_by_index(0)
        self.meraki_devices=[]
        for row in range(self.sheet.nrows):
            if self.sheet.cell_value(row,40)!='Approved-Cancelled':
                self.meraki_devices.append(self.sheet.cell_value(row,24))
        return self.meraki_devices[3:]
        #needs to filter out only meraki devices
    def delDevices(self,*args): #deletes (1)selected device (2)all devices of selected network
        if self.devMenu.curselection():
            removeDevices(self.getNetID(),self.getDevSerial())
        else:
            for ser in self.getNetDevSerials():
                removeDevices(self.getNetID(),ser)
        self.popuDevNames()

if __name__=="__main__":
    root=Tk()
    root.title("Technology Experiences Meraki Wizard v0.1")
    MerakiWizard(root)
    root.mainloop()