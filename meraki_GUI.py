from tkinter import *
from tkinter import filedialog as fd
from meraki_GUI_APIcall import *
import xlrd
import re

class MerakiWizard(Frame):

    ####MERAKI GUI INTERFACE####
    def __init__(self,parent,*args,**kwargs):
        self.parent=parent
        self.org_info=orgInfo()
        ####PROMPTS USER TO SELECT ORGANIZATION####
        self.org_title=Label(text="Select Organization")
        self.org_title.grid(row=0,column=0)
        #Org Listbox: takes Org Name, passes Org ID on button click to get list of networks
        self.orgMenu=Listbox(root,exportselection=False) 
        self.orgMenu.grid(row=1,column=0)
        for org_name in self.getOrgList():
            self.orgMenu.insert(END,org_name)
            self.orgMenu.bind("<<ListboxSelect>>", self.popuNetNames)
        ####PROMPTS USER TO SELECT NETWORK####
        self.net_title=Label(text="Select Network")
        self.net_title.grid(row=0, column=1)
        #Network Listbox: takes Network Name, passes Network ID on button click to get list of devices
        self.netMenu=Listbox(root,exportselection=False)
        self.netMenu.grid(row=1, column=1)
        self.netMenu.bind("<<ListboxSelect>>", self.popuDevNames)
        ####PROMPTS USER TO SELECT DEVICE####
        self.net_title=Label(text="Select Device")
        self.net_title.grid(row=0, column=2)
        #Device Listbox: Takes Device Name, passes Device 
        self.devMenu=Listbox(root,exportselection=False)
        self.devMenu.grid(row=1,column=2)
        self.devMenu.bind("<<ListboxSelect>>", self.devInfoClick)
        ####PROMPTS USER TO SELECT AN ACTION THEY WANT TO PERFORM####
        #Alteration OptionMenu: list of things to do on (1)org (2)network (3)device level
        self.commands=commandList()
        self.alter=StringVar(root)
        self.alter.set(self.commands[0])
        self.alterMenu=OptionMenu(root,self.alter,*self.commands)
        self.alterMenu.grid(row=4,column=0)
        #select button
        self.selectButton=Button(
            root,text='Select Action',command=self.AlterMenu, bg='#049fd9', fg='white')
        self.selectButton.grid(row=4,column=1)
    ####ALTERATION OPTIONMENU####
    def AlterMenu(self): #what to do depending on the option selected
        self.selected=self.alter.get()
        if self.selected=='Create Network':
            pass
        elif self.selected=='Delete Network': #deletes network and all devices
            deleteNetwork(self.getNetID())
        elif self.selected=='Add Device': #adds a single device to the network
            self.infoPopup()
        elif self.selected=='Bulk Add Devices': #automatically adds all devices on .xls file
            claimDevices(self.getNetID(),self.bulkAddExcel())
            self.bulkRenameExcel()
            self.popuDevNames()
        elif self.selected=='Rename Device': #renames a device that is selected from listbox
            self.infoPopup()
        ###BULK RENAME DEVICE in progress. takes device names, {show name}-{model}-(#) --> RSA-SW-1 ####
        elif self.selected=='Remove Device(s)': #removes the devices selected or all devices
            self.delDevices()
        elif self.selected=='Bulk Add Address': #adds the trade show or event address to all devices
            self.infoPopup()
        elif self.selected=='Add VLAN': #adds a VLAN given user input of required info
            self.infoPopup()
        ####BULK ADD DEFAULT VLANS in progress. Takes Vlan ID, Name, Subnet, Appliance IP from excel file and auto adds the vlans
        elif self.selected=='Delete VLAN': #deletes VLAN given the VLAN ID
            self.infoPopup()
        elif self.selected=='Swap MX Warm Spare': #switches primary and warm MX
            swapWarmSpare(self.getNetID()) 
        elif self.selected=='Blink LED': #blinks LED of chosen device
            blinkDevice(self.getDevSerial())
        elif self.selected=='Update Device Port': #updates port type for specefied port (and vlan on chosen device if not trunk)
            self.infoPopup()
    def infoPopup(self): #popup menu to get the user input of required parameters
        self.selected=self.alter.get()
        self.entry=Toplevel()
        if self.selected=='Add Device': #SN
            self.getInput=Label(self.entry,text='*Enter Device SN:')
            self.getInput.pack()
            self.devSnEntry=Entry(self.entry)
            self.devSnEntry.pack()
        elif self.selected=='Rename Device': #Name
            self.getInput=Label(self.entry,text='*Rename device to:')
            self.getInput.pack()
            self.renameEntry=Entry(self.entry)
            self.renameEntry.pack()   
        elif self.selected=='Bulk Add Address': #Address
            self.getInput=Label(self.entry,text='*Enter address:')
            self.getInput.pack()
            self.addrEntry=Entry(self.entry)
            self.addrEntry.pack()
        elif self.selected=='Add VLAN': #Vlan ID, name, subnet, appliance IP
            self.getID=Label(self.entry,text='*ID:')
            self.getID.pack()
            self.idEnt=Entry(self.entry)
            self.idEnt.pack()
            self.getName=Label(self.entry,text='*Name:')
            self.getName.pack()
            self.nameEnt=Entry(self.entry)
            self.nameEnt.pack()
            self.getSubnet=Label(self.entry,text='*Subnet:')
            self.getSubnet.pack()
            self.subEnt=Entry(self.entry)
            self.subEnt.pack()
            self.getAppIp=Label(self.entry,text='*Appliance IP:')
            self.getAppIp.pack()
            self.appEnt=Entry(self.entry)
            self.appEnt.pack()
        elif self.selected=='Delete VLAN': #Vlan ID
            self.getInput=Label(self.entry,text='*Enter VLAN ID:')
            self.getInput.pack()
            self.vlanIdEntry=Entry(self.entry)
            self.vlanIdEntry.pack()
        elif self.selected=='Update Device Port': #Port ID, type[access,trunk] *optional(VLAN ID)
            self.getId=Label(self.entry,text='*Enter port ID:')
            self.getId.pack()
            self.idEnt=Entry(self.entry)
            self.idEnt.pack()
            self.getType=Label(self.entry,text='*Enter port type [access/trunk]:')
            self.getType.pack()
            self.typeEnt=Entry(self.entry)
            self.typeEnt.pack()
            self.getVlan=Label(self.entry,text='Enter port VLAN ID (if access):')
            self.getVlan.pack()
            self.vlanEnt=Entry(self.entry)
            self.vlanEnt.pack()
        self.doneButton=Button(self.entry,text='Done',command=self.quitInput)
        self.doneButton.pack()     
    def quitInput(self): #on button click, takes the stored entries and calls method given the selected option
        self.selected=self.alter.get()
        if self.selected=='Add Device':
            self.addDevice()
        elif self.selected=='Rename Device': #do NOT name devices a name that exists currently, this will make the program bug out
            renameDevice(self.getDevSerial(),self.renameEntry.get())
            self.popuDevNames()
        elif self.selected=='Update Device Port':
            if self.vlanEnt.get(): #if changing to access port and want to change/Add associated VLAN
                updateDevSwitchportVLAN(
                    self.getDevSerial(),self.idEnt.get(),
                    self.typeEnt.get(),self.vlanEnt.get())
            else: #if changing to trunk/if no VLAN specified and want to change other info
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
    def getOrgList(self): #return the list of accessible org names
        self.org_list=sorted([org['name'] for org in self.org_info])
        return self.org_list
    def getOrgID(self,*args): #get org ID given org name, used to get all network names in org
        self.name=self.orgMenu.get(self.orgMenu.curselection())
        self.org_id=''
        for orgs in self.org_info:
            if orgs['name']==self.name:
                self.org_id+=orgs['id']
        return self.org_id
    def getOrgNetIDs(self): #get list all network IDs in an org given org ID
        self.net_ids=[]
        for nets in orgNetInfo(self.getOrgID()):
            if nets['organizationId']==self.getOrgID():
                self.net_ids.append(nets['id'])
        return self.net_ids
    def getOrgNetNames(self): #get list of all network names given list of netID
        self.net_names=[net['name'] for net in orgNetInfo(self.getOrgID())]
        return self.net_names
    def popuNetNames(self,*args): #populates listbox on click per orgNetwork button, refreshes each new click
        self.netMenu.delete(0,END)
        for name in self.getOrgNetNames():
            self.netMenu.insert(END,name)

    ####NETWORK FUNCTIONS####
    def getNetID(self,*args): #get net ID given net name
        self.org_nets=orgNetInfo(self.getOrgID())
        self.name=self.netMenu.get(self.netMenu.curselection())
        self.curr_net=''
        for nets in self.org_nets:
            if nets['name']==self.name:
                self.curr_net+=(nets['id'])
        return self.curr_net
    def getNetDevSerials(self): #gets SN of all network devices
        self.net_serials=[device['serial'] for device in deviceInfo(self.getNetID())]
        return self.net_serials

    ####DEVICE FUNCTIONS####
    def getDevNames(self): #gets list of device names in a network
        self.dev_names=[dev['name'] for dev in deviceInfo(self.getNetID())]
        return self.dev_names
    def popuDevNames(self,*args): #populates listbox on click of selecting network
        self.devMenu.delete(0,END)
        for name in self.getDevNames():
            self.devMenu.insert(END,name)
    def getDevSerial(self,*args): #gets the device SN given the listbox selection
        self.net_devs=deviceInfo(self.getNetID())
        self.name=self.devMenu.get(self.devMenu.curselection())
        self.curr_dev=''
        for devs in self.net_devs:
            if devs['name']==self.name:
                self.curr_dev+=devs['serial']
        return self.curr_dev
    def devInfoClick(self,*args):
        print(specDevInfo(self.getDevSerial()))
    def bulkAddExcel(self,*args): #Add devices given JLL .xlsx file
        self.pattern=re.compile(r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$") #xxxx-xxxx-xxxx Meraki SN format checker
        self.file_name=fd.askopenfilename(initialdir='/',title='Select A File',filetypes=(('.xlsx','*.xlsx'),('all files','.')))
        self.wb=xlrd.open_workbook(self.file_name)
        self.sheet=self.wb.sheet_by_index(0)
        self.meraki_devices=[]
        for row in range(self.sheet.nrows):
            if self.sheet.cell_value(row,40)!='Approved-Cancelled' and self.pattern.match(self.sheet.cell_value(row,24)):
                    self.meraki_devices.append(self.sheet.cell_value(row,24))
        return self.meraki_devices
    def bulkRenameExcel(self,*args):
        self.net_devs=deviceInfo(self.getNetID())
        for device in self.net_devs:
            self.name=device['model']+'_'+device['serial'][-4:]
            renameDevice(device['serial'],self.name)
    def addDevice(self,*args): #adds a specific device given
        self.to_add=[] #the SN passed into the API call is supposed to be a tuple
        self.to_add.append(str(self.devSnEntry.get()))
        claimDevices(self.getNetID(),self.to_add)
        self.popuDevNames()
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