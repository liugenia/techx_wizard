from tkinter import *
from tkinter import filedialog as fd
from meraki_GUI_APIcall import *
import xlrd

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

    ####DROPDOWN ALTERATAION MENU####
    def AlterMenu(self):
        self.selected=self.alter.get()
        if self.selected=='Create Network':
            pass
        elif self.selected=='Delete Network':
            deleteNetwork(self.getNetID())
        elif self.selected=='Add Device(s)': #automatically adds all devices on .csv file
            claimDevices(self.getNetID(),self.getDevicesExcel())
            self.popuDevNames()
        elif self.selected=='Remove Device(s)': #removes the devices selected or all devices
            self.delDevices()
        elif self.selected=='Swap MX Warm Spare':
            swapWarmSpare(self.getNetID())
        elif self.selected=='Blink LED':
            blinkDevice(self.getDevSerial())

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

####INPUT POPUP WHEN SELECTED OPTION REQUIRES IT####
class InputPopup:
    def __init__(self,parent,*args,**kwargs):
        self.popup=Toplevel(root)


if __name__=="__main__":
    root=Tk()
    root.title("Technology Experiences Meraki Wizard v0.1")
    MerakiWizard(root)
    root.mainloop()