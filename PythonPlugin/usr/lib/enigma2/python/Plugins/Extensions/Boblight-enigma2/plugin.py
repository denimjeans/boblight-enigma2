from __future__ import division
from __init__ import _

from Components.ActionMap import ActionMap, NumberActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import config, configfile, getConfigListEntry, ConfigSubsection, ConfigEnableDisable, ConfigSelection, ConfigSlider, ConfigDirectory, ConfigOnOff, ConfigNothing, ConfigInteger, ConfigYesNo
from Components.Label import Label
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens import Standby
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from time import localtime, time
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import ePicLoad, eConsoleAppContainer, getDesktop

from Components.Button import Button
from Components.FileList import FileList
from Components.Pixmap import Pixmap

import os, socket
import sys

from boblight import *

pluginversion = "Version: 0.5r12 beta1"

def DaemonToggle(session, **kwargs):
    container = eConsoleAppContainer()
    container.execute('/etc/init.d/boblight-control toggle')

def Enabled(session, **kwargs):
    container = eConsoleAppContainer()
    container.execute('/etc/init.d/boblight-control start')
            
def Disabled(session, **kwargs):
    container = eConsoleAppContainer()
    container.execute('/etc/init.d/boblight-control stop')
            
            
def Plugins(**kwargs):
    return [PluginDescriptor(name='Boblight Enigma2', description=_('Ambilight clone'), where=PluginDescriptor.WHERE_PLUGINMENU, icon='boblight.png', fnc=startSetup),
    PluginDescriptor(name='Boblight | On / Off', description=_('Ambilight clone'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon='boblight.png', fnc=DaemonToggle),
    PluginDescriptor(name='Boblight Menu', description=_('Ambilight clone'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon='boblight.png', fnc=startSetup)]

def main(session, **kwargs):
    session.open(startSetup)

def startSetup(session, **kwargs):
    print "[Boblight] start configuration"
    session.open(BoblightConfig)


class MoodLampConfigScreen(Screen, ConfigListScreen):

    skin = """
        <screen name="MoodlampSettings" position="%d,%d" size="600,300" title="Moodlamp Settings" >	
        <widget name="config" position="10,5" size="590,290" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>
        <ePixmap pixmap="skin_default/buttons/key_green.png" zPosition="2"  position="10,270" size="35,25" alphatest="on" />
        <ePixmap pixmap="skin_default/buttons/key_yellow.png" zPosition="2" position="200,270" size="35,25" alphatest="on" />
        <widget name="buttongreen" position="60,272" size="180,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
		<widget name="buttonyellow" position="250,272" size="450,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
		</screen>""" % (
			(DESKTOP_WIDTH - 600) / 2, (DESKTOP_HEIGHT - 300) / 2)

    def __init__(self,session):
        self.session = session
        Screen.__init__(self, session)
        self.createConfigList()
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self["buttongreen"] = Label(_("Save settings"))
        self["buttonyellow"] = Label(_("Send Settings to moodlamp"))
        self["moodActions"] = ActionMap(["ColorActions"],
			{
			"cancel": self.keyOk,
			"ok": self.keyOk,
			"yellow": self.keyYellow,
			"green": self.keyOk,
			}, -2)
	
    def createConfigList(self):
        self.list = []  
        self.list.append(getConfigListEntry(_('Enable moodlamp when boblight is disabled:'), config.plugins.Boblight_grab.moodlamp_onoff_standby))
        self.list.append(getConfigListEntry(_('Moodlamp Mode:'), config.plugins.Boblight_grab.moodlamp_mode))	      
            
        #Moodlamp staticmode
        if config.plugins.Boblight_grab.moodlamp_mode.value is str(0): 
            self.list.append(getConfigListEntry(_('Static Mode:'), config.plugins.Boblight_grab.moodlamp_static_profile))
            
            #Moodlamp static mode - custom color
            if config.plugins.Boblight_grab.moodlamp_static_profile.value is str(0):
                self.list.append(getConfigListEntry(_('Static Color R:'), config.plugins.Boblight_grab.moodlamp_static_color_r))
                self.list.append(getConfigListEntry(_('Static Color G:'), config.plugins.Boblight_grab.moodlamp_static_color_g))
                self.list.append(getConfigListEntry(_('Static Color B:'), config.plugins.Boblight_grab.moodlamp_static_color_b))

    def changedEntry(self): 
        #Ladybug
        if config.plugins.Boblight_grab.moodlamp_static_profile.value is str(1):
            config.plugins.Boblight_grab.moodlamp_static_color_r.setValue(165);
            config.plugins.Boblight_grab.moodlamp_static_color_g.setValue(42);
            config.plugins.Boblight_grab.moodlamp_static_color_b.setValue(40);
        
        #Blue
        if config.plugins.Boblight_grab.moodlamp_static_profile.value is str(2):
            config.plugins.Boblight_grab.moodlamp_static_color_r.setValue(25);
            config.plugins.Boblight_grab.moodlamp_static_color_g.setValue(67);
            config.plugins.Boblight_grab.moodlamp_static_color_b.setValue(190);
        
        #Ocean Blue
        if config.plugins.Boblight_grab.moodlamp_static_profile.value is str(3):
            config.plugins.Boblight_grab.moodlamp_static_color_r.setValue(28);
            config.plugins.Boblight_grab.moodlamp_static_color_g.setValue(107);
            config.plugins.Boblight_grab.moodlamp_static_color_b.setValue(160);
        
        config.plugins.Boblight_grab.moodlamp_static_color_r.save();
        config.plugins.Boblight_grab.moodlamp_static_color_g.save();
        config.plugins.Boblight_grab.moodlamp_static_color_b.save();
            
        self.createConfigList()
        self["config"].setList(self.list)
      
    def save(self):
        for x in self['config'].list:
            x[1].save()
        self.changedEntry() #Refresh list
        configfile.save() #save to file
    
    def keyOk(self):
        self.save()
        self.close()
    
    def keyYellow(self):
        if config.plugins.Boblight_grab.mode.value is str(2):
            self.ColorRestart()
        else:
            self.session.open(MessageBox, _('Mood Lamp is disabled!, you need to set mode, to [moodlamp] in menu....'), MessageBox.TYPE_WARNING, timeout=5)
    
    def ColorRestart(self):
        self.save()
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control restart_moodlamp')
        self.session.open(MessageBox, _('Reload moodlamp settings...'), MessageBox.TYPE_INFO, timeout=2)
        self.createConfigList()
        
class NetworkSettingsScreen(Screen, ConfigListScreen):

    skin = """
        <screen name="NetworkSettingsScreen" position="%d,%d" size="600,300" title="Network Settings" >	
        <widget name="config" position="10,5" size="590,290" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>
        <ePixmap pixmap="skin_default/buttons/key_green.png" zPosition="2"  position="10,270" size="35,25" alphatest="on" />
        <widget name="buttongreen" position="60,272" size="180,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
		</screen>""" % (
			(DESKTOP_WIDTH - 600) / 2, (DESKTOP_HEIGHT - 300) / 2)

    def __init__(self,session):
        self.session = session
        Screen.__init__(self, session)
        self.createConfigList()
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self["buttongreen"] = Label(_("Save settings"))
        self["networkActions"] = ActionMap(["ColorActions"],
			{
			"cancel": self.keyOk,
			"ok": self.keyOk,
			"green": self.keyOk,
			}, -2)
	
    def createConfigList(self):
        self.list = []  
        self.list.append(getConfigListEntry(_('Enable network mode (only client will be started):'), config.plugins.Boblight_grab.network_onoff))

        #Ip address
        if config.plugins.Boblight_grab.network_onoff.value is True: 
            self.list.append(getConfigListEntry(_('Deamon Ip address:'), config.plugins.Boblight_grab.address))
            self.list.append(getConfigListEntry(_('Deamon Port:'), config.plugins.Boblight_grab.port))
            
    def changedEntry(self): 
        self.createConfigList()
        self["config"].setList(self.list)
      
    def save(self):
        for x in self['config'].list:
            x[1].save()
        self.changedEntry() #Refresh list
        configfile.save() #save to file
    
    def keyOk(self):
        self.save()
        self.close()

class BoblightAboutScreen(Screen, ConfigListScreen):

    skin = """
        <screen name="BoblightAboutScreen" position="%d,%d" size="550,400" title="%s" >
			<widget name="pluginInfo" position="5,5" size="550,20" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>
			<widget name="daemonInfo" position="5,25" size="550,20" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="enigmaInfo" position="5,45" size="550,20" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>			
            <widget name="Empty"      position="5,65" size="550,20" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>			
            <widget name="ThanksInfo" position="5,95" size="550,20" valign="center" halign="left"  zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>			
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Boblight-enigma2/pic/boblight.png" zPosition="2" position="center,125" size="256,256" alphatest="on" />
		</screen>""" % (
			(DESKTOP_WIDTH - 550) / 2, (DESKTOP_HEIGHT - 400) / 2,
			_("About Boblight"),)

    def __init__(self,session):
        self.session = session
        Screen.__init__(self, session)
        self["aboutActions"] = ActionMap(["ColorActions"],
            {
            "cancel": self.exit,
            "ok": self.exit,
            }, -2)
        self["pluginInfo"] = Label("Plugin (v1.6) by Speedy1985.")
        self["daemonInfo"] = Label("Deamon (v2.0) by Bob Loosen.")
        self["enigmaInfo"] = Label("Boblight-Enigma2 (v0.5r12) by Speedy1985 / c@rstenpresser.")
        self["Empty"]      = Label("")
        self["ThanksInfo"] = Label("Special credits to: Nietgiftig, Stephan, Meega and Holymoly.")
    
    def exit(self):
        self.close()
        
class BoblightConfig(Screen, ConfigListScreen):
    skin = """
    <screen position="center,center" size="700,600" title="Boblight Config" >
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Boblight-enigma2/pic/logo.png" zPosition="2" position="10,10" size="680,120" alphatest="on" />
    <ePixmap pixmap="skin_default/div-v.png" position="225,135" size="1,600" zPosition="4" transparent="1" alphatest="on"/>
    
    <widget name="config" position="240,135" size="450,600" scrollbarMode="showOnDemand" />
	<ePixmap pixmap="skin_default/buttons/key_1.png"         zPosition="2" position="10,138" size="35,25" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/key_2.png"         zPosition="2" position="10,168" size="35,25" alphatest="on" />
	<ePixmap pixmap="skin_default/buttons/key_3.png"         zPosition="2" position="10,198" size="35,25" alphatest="on" />
    <ePixmap pixmap="skin_default/buttons/key_green.png"     zPosition="2" position="10,228" size="35,25" alphatest="on" />
    <ePixmap pixmap="skin_default/buttons/key_red.png"       zPosition="2" position="10,258" size="35,25" alphatest="on" />
    <ePixmap pixmap="skin_default/buttons/key_yellow.png"    zPosition="2" position="10,288" size="35,25" alphatest="on" />
    <ePixmap pixmap="skin_default/buttons/key_blue.png"      zPosition="2" position="10,318" size="35,25" alphatest="on" />
    <ePixmap pixmap="skin_default/buttons/key_info.png"      zPosition="2" position="10,348" size="35,25" alphatest="on" />

    <widget name="button1"      position="60,140" size="170,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    <widget name="button2"      position="60,170" size="170,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    <widget name="button3"      position="60,200" size="170,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>		
    <widget name="buttongreen"  position="60,230" size="150,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    <widget name="buttonred"    position="60,260" size="150,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    <widget name="buttonyellow" position="60,290" size="150,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    <widget name="buttonblue"   position="60,320" size="150,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    <widget name="buttoninfo"   position="60,350" size="150,20" valign="center" halign="left" zPosition="2" foregroundColor="white" font="Regular;18"/>
    </screen>"""

    def __init__(self,session):
        self.session = session
        Screen.__init__(self,session)
        self.createConfigList()
        
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self["button1"] = Label(_("Moodlamp settings"))
        self["button2"] = Label(_("Network settings"))
        self["button3"] = Label(_("Setup"))
        self["buttonred"] = Label(_("Stop"))
        self["buttongreen"] = Label(_("Start"))
        self["buttonyellow"] = Label(_("Send Settings"))
        self["buttonblue"] = Label(_("Default"))
        self["buttoninfo"] = Label(_("About"))
        self["setupActions"] = ActionMap(["ColorActions"],
            {
                "green": self.keyGreen,
                "red": self.keyRed,
                "yellow": self.keyYellow,
                "blue": self.keyBlue,
                "cancel": self.keyExit,
                "ok": self.keyOk,
                "info": self.AboutS,
                "key_1": self.Key1,
                "key_2": self.Key2,
                "key_3": self.Setup,
            }, -2)
        self.onShown.append(self.setWindowTitle)
        self.bob = '/usr/bin/boblight-dev.sh'
        
       
        
    def setWindowTitle(self):
        self.setTitle(_("Boblight Plugin - %s") % pluginversion)

    #Create configlist.
    def createConfigList(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Autostart on startup:'), config.plugins.Boblight_grab.autostart))
        self.list.append(getConfigListEntry(_('Stop client on standby:'), config.plugins.Boblight_grab.standby))

        self.list.append(getConfigListEntry(_('Mode:'), config.plugins.Boblight_grab.mode))
        if config.plugins.Boblight_grab.mode.value is str(1): 
            self.list.append(getConfigListEntry(_('Maximum intermediate-picture-size:'), config.plugins.Boblight_grab.pixels)) 
            self.list.append(getConfigListEntry(_('Blackbar detection:'), config.plugins.Boblight_grab.blackbar))
        self.list.append(getConfigListEntry(_('Profile:'), config.plugins.Boblight_grab.presets))

        #IF profile is custom
        if config.plugins.Boblight_grab.presets.value is str(0):
            self.list.append(getConfigListEntry(_('Interpolation:'), config.plugins.Boblight_grab.interpolation))        
            self.list.append(getConfigListEntry(_('Smoothness: '+str(config.plugins.Boblight_grab.speed.value)+'% '),config.plugins.Boblight_grab.speed))
            self.list.append(getConfigListEntry(_('Color Value: '+str(config.plugins.Boblight_grab.value.value)),config.plugins.Boblight_grab.value))
            self.list.append(getConfigListEntry(_('Color Value Min 0-1:'), config.plugins.Boblight_grab.valuemin))
            self.list.append(getConfigListEntry(_('Color Value Max 0-1:'), config.plugins.Boblight_grab.valuemax))
            self.list.append(getConfigListEntry(_('Saturation 0-20:'), config.plugins.Boblight_grab.saturation))
            self.list.append(getConfigListEntry(_('Saturation Min 0-1:'), config.plugins.Boblight_grab.saturationmin))
            self.list.append(getConfigListEntry(_('Saturation Max 0-1:'), config.plugins.Boblight_grab.saturationmax))
            self.list.append(getConfigListEntry(_('Gamma 1-10:'), config.plugins.Boblight_grab.gamma))
            #self.list.append(getConfigListEntry(_('Black value 0-255:'), config.plugins.Boblight_grab.threshold))
            
    def setProfile(self,saturation,value,speed,valuemax,valuemin,saturationmin,saturationmax,gamma,threshold):
        config.plugins.Boblight_grab.saturation.value = str(saturation);
        config.plugins.Boblight_grab.value.setValue(value);
        config.plugins.Boblight_grab.speed.setValue(speed);
        config.plugins.Boblight_grab.valuemax.value = str(valuemax);
        config.plugins.Boblight_grab.valuemin.value = str(valuemin);
        config.plugins.Boblight_grab.saturationmin.value = str(saturationmin);
        config.plugins.Boblight_grab.saturationmax.value = str(saturationmax);
        config.plugins.Boblight_grab.gamma.value = str(gamma);
        config.plugins.Boblight_grab.threshold.value = str(threshold);
        config.plugins.Boblight_grab.value.save()
        config.plugins.Boblight_grab.speed.save()
        config.plugins.Boblight_grab.saturation.save()
        config.plugins.Boblight_grab.valuemax.save()
        config.plugins.Boblight_grab.valuemin.save()
        config.plugins.Boblight_grab.saturationmin.save()
        config.plugins.Boblight_grab.saturationmax.save()
        config.plugins.Boblight_grab.gamma.save()
        config.plugins.Boblight_grab.threshold.save()
        
                
    def changedEntry(self):
        
        if config.plugins.Boblight_grab.presets.value is str(2):       #Profile verysmooth
            self.setProfile(1.2,10,30,1,0,0,1,2.2,10);
            
        if config.plugins.Boblight_grab.presets.value is str(1):       #Profile smooth
            self.setProfile(1.2,10,50,1,0,0,1,2.2,10);
            
        if config.plugins.Boblight_grab.presets.value is str(4):     #Profile smooth/action
            self.setProfile(1.2,10,80,1,0,0,1,2.2,15);
            
        if config.plugins.Boblight_grab.presets.value is str(3):     #Profile action
            self.setProfile(1.2,10,70,1,0,0,1,2.2,20);
            
        if config.plugins.Boblight_grab.presets.value is str(5):     #Profile Default
            self.setProfile(1.0,1,60,1,0,0,1,1.0,0);

        self.createConfigList()
        self["config"].setList(self.list)

    def save(self):
        for x in self['config'].list:
            x[1].save()
        self.changedEntry() #Refresh list

        configfile.save() #save to file
        RC_START_LINK = '/etc/rc3.d/S99boblight'
        
        if config.plugins.Boblight_grab.autostart.value is True:
            self.LinkFile('/etc/init.d/boblight-control', RC_START_LINK)
        
        if config.plugins.Boblight_grab.autostart.value is False:
            self.DeleteLink(RC_START_LINK)
        
            
    def keyOk(self):
        self.save()
        self.close(False,self.session)
        
    def keyYellow(self):
        if config.plugins.Boblight_grab.mode.value is str(2):
           self.ColorRestart()
        else:
           self.DaemonReload()

    #Moodlamp   
    def Key1(self):
		self.session.open(MoodLampConfigScreen)
	
	#Network
    def Key2(self):
        self.session.open(NetworkSettingsScreen)
	
    def Setup(self):
        startMsg = "Setup will install some drivers for boblight.\nYour settings will be reset\nDo you want continue ?"
        self.session.openWithCallback(self.StartSetup, MessageBox, _(startMsg), MessageBox.TYPE_YESNO)

    def installFinished(self):
        config.plugins.Boblight_grab.setup.value = str(1);
        config.plugins.Boblight_grab.setup.save();
        
        restartMsg = "You need to restart the GUI to load the new drivers.\nDo you want to Restart the GUI now?"
        self.session.openWithCallback(self.restartGUI, MessageBox, _(restartMsg), MessageBox.TYPE_YESNO)
        #self.close()
    
    # Restart the GUI if requested by the user.
    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

	# Start Setup
    def StartSetup(self, answer):
        if answer is True:
            self.session.openWithCallback(self.installFinished, Console, cmdlist = [self.bob], closeOnSuccess = True)
        else:
            self.close()
            	
    def AboutS(self):
		self.session.open(BoblightAboutScreen)
       
    def keyGreen(self):
        self.save()
        if config.plugins.Boblight_grab.mode.value is str(2):
            self.ColorStart()
        else:
            self.DaemonStart()
        
    def keyBlue(self):
        self.revert()

    def keyRed(self):
        self.DaemonStop()
        
    def keyExit(self):
        self.confirm = False
        for x in self['config'].list:
            self.confirm = (self.confirm or x[1].isChanged())

        if (self.confirm and self.session.openWithCallback(self.SaveConfirm, MessageBox, _('Save changes?'))):
            pass
        self.close(False, self.session)
            
    def SaveConfirm(self, result):
        if result is None or result is False:
            print "[Boblight] Save not confirmed. exit.."
            for x in self["config"].list:
                x[1].cancel()
        else:
            print "[Boblight] Save confirmed. Configchanges will be saved."
            self.save()

    def revert(self):
        self.session.openWithCallback(self.keyYellowConfirm, MessageBox, _("Reset Boblight settings to defaults?"), MessageBox.TYPE_YESNO, timeout = 20, default = True)

    def keyYellowConfirm(self, confirmed):
        if not confirmed:
            print "[Boblight] Reset to defaults not confirmed."
        else:
            print "[Boblight] Setting Configuration to defaults."
            config.plugins.Boblight_grab.blackbar.setValue(False)
            config.plugins.Boblight_grab.autostart.setValue(False)
            config.plugins.Boblight_grab.presets.setValue(0)
            config.plugins.Boblight_grab.pixels.setValue(128)
            config.plugins.Boblight_grab.saturation.setValue(1)
            config.plugins.Boblight_grab.saturationmax.setValue(1)
            config.plugins.Boblight_grab.saturationmin.setValue(0)
            config.plugins.Boblight_grab.speed.setValue(50)
            config.plugins.Boblight_grab.chase_speed.setValue(45)
            config.plugins.Boblight_grab.interpolation.setValue(True)
            config.plugins.Boblight_grab.standby.setValue(False)
            config.plugins.Boblight_grab.value.setValue(20.0)
            config.plugins.Boblight_grab.valuemin.setValue(0)
            config.plugins.Boblight_grab.valuemax.setValue(1)
            config.plugins.Boblight_grab.presets.setValue(0)
            config.plugins.Boblight_grab.hscanstart.setValue(0)
            config.plugins.Boblight_grab.vscanstart.setValue(0)
            config.plugins.Boblight_grab.hscanend.setValue(0)
            config.plugins.Boblight_grab.vscanend.setValue(0)
            config.plugins.Boblight_grab.mode.setValue(1)
            config.plugins.Boblight_grab.gamma.setValue(2)
            config.plugins.Boblight_grab.network_onoff.setValue(False)      
            config.plugins.Boblight_grab.threshold.setValue(0)

            self.save()
    
    def LinkFile(self, src, dst):
        if (os.access(dst, os.F_OK) or os.symlink(src, dst)):
            pass

    def DeleteLink(self, dst):
        if (os.access(dst, os.F_OK) and os.unlink(dst)):
            pass                             
                
    def DaemonStart(self):
        self.save()
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control start')
        if config.plugins.Boblight_grab.network_onoff.value is True:
            startMsg = "Networkmode: Start client for ip: "+str(config.plugins.Boblight_grab.address.value)
        else:
            startMsg = "Start boblight..."
        self.session.open(MessageBox, _(startMsg), MessageBox.TYPE_INFO, timeout=5)
        self.createConfigList()
                
    def ColorStart(self):
        self.save()
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control start_moodlamp')
        if config.plugins.Boblight_grab.network_onoff.value is True:
            startMsg = "Networkmode: Start moodlamp for ip: "+str(config.plugins.Boblight_grab.address.value)
        else:
            startMsg = "Start moodlamp..."
        self.session.open(MessageBox, _(startMsg), MessageBox.TYPE_INFO, timeout=5)        
        self.createConfigList()
                
    def ColorRestart(self):
        self.save()
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control restart_moodlamp')
        if config.plugins.Boblight_grab.network_onoff.value is True:
            startMsg = "Networkmode: Reload moodlamp for ip: "+str(config.plugins.Boblight_grab.address.value)
        else:
            startMsg = "Reload moodlamp..."
        self.session.open(MessageBox, _(startMsg), MessageBox.TYPE_INFO, timeout=2)
        self.createConfigList()
                
    def DaemonReload(self):
        self.save()
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control restart')
        if config.plugins.Boblight_grab.network_onoff.value is True:
            startMsg = "Networkmode: Reload client for ip: "+str(config.plugins.Boblight_grab.address.value)
        else:
            startMsg = "Reload client..."
        self.session.open(MessageBox, _(startMsg), MessageBox.TYPE_INFO, timeout=2) 
        self.createConfigList()
        
    def DaemonStop(self):
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control stop')
        self.session.open(MessageBox, _('Stop all clients...'), MessageBox.TYPE_INFO, timeout=3)
        self.createConfigList()
    
class Boblight():
    
    def __init__(self):
        self.session = None 
        self.dialog = None
        self.active = False
        config.misc.standbyCounter.addNotifier(self.enterStandby, initial_call = False)

    def enterStandby(self, configElement):
        Standby.inStandby.onClose.append(self.endStandby)
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control sleep')
        #self.session.open(MessageBox, _('[Boblight] Standby...'), MessageBox.TYPE_INFO, timeout=3)
          
    def endStandby(self):
        self.container = eConsoleAppContainer()
        self.container.execute('/etc/init.d/boblight-control wakeup')
        #self.session.open(MessageBox, _('[Boblight] Wake up....'), MessageBox.TYPE_INFO, timeout=5)
        
bob = Boblight()
