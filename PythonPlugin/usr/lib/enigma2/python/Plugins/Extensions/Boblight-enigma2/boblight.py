import sys
import time

from Components.config import config, configfile, getConfigListEntry, ConfigFloat, ConfigSubsection, ConfigEnableDisable, ConfigSelection, ConfigSlider, ConfigDirectory, ConfigOnOff, ConfigNothing, ConfigInteger, ConfigYesNo
from enigma import ePicLoad, eConsoleAppContainer, getDesktop

DESKTOP_WIDTH  = getDesktop(0).size().width()
DESKTOP_HEIGHT = getDesktop(0).size().height()

config.plugins.Boblight_grab = ConfigSubsection()

#Moodlamp 
config.plugins.Boblight_grab.mode                       = ConfigSelection(default = "1", choices = [("1", "Dynamic"), ("2", "Moodlamp")])
config.plugins.Boblight_grab.moodlamp_onoff_standby     = ConfigEnableDisable(default=False)
#config.plugins.Boblight_grab.moodlamp_static_color_r    = ConfigSlider(default=28, increment=1, limits=(0,255))
#config.plugins.Boblight_grab.moodlamp_static_color_g    = ConfigSlider(default=107, increment=1, limits=(0,255))
#config.plugins.Boblight_grab.moodlamp_static_color_b    = ConfigSlider(default=160, increment=1, limits=(0,255))
config.plugins.Boblight_grab.moodlamp_static_color_r    = ConfigInteger(0,(0, 255))
config.plugins.Boblight_grab.moodlamp_static_color_g    = ConfigInteger(0,(0, 255))
config.plugins.Boblight_grab.moodlamp_static_color_b    = ConfigInteger(0,(0, 255))
config.plugins.Boblight_grab.address                    = ConfigFloat(default = [127,0,0,0], limits = [(0,255),(0,255),(0,255),(0,255)])
config.plugins.Boblight_grab.port                       = ConfigInteger(default = 19333, limits=(1, 65535) )
config.plugins.Boblight_grab.network_onoff              = ConfigEnableDisable(default=False)
config.plugins.Boblight_grab.moodlamp_static_profile    = ConfigSelection(default = "0", choices = [("0", "Custom color"),("1", "Ladybug"), ("2", "Blue"), ("3", "Ocean blue")])
config.plugins.Boblight_grab.moodlamp_static            = ConfigEnableDisable(default=False)
config.plugins.Boblight_grab.moodlamp_mode              = ConfigSelection(default = "0", choices = [("0", "Static color"), ("1", "Fading color (coming soon)")])

config.plugins.Boblight_grab.standby            = ConfigEnableDisable(default=False)
config.plugins.Boblight_grab.blackbar           = ConfigEnableDisable(default=False)
config.plugins.Boblight_grab.threshold          = ConfigInteger(0,(0, 255))   
config.plugins.Boblight_grab.pixels             = ConfigSelection(default = "128", choices = [("32", "32"), ("64", "64"), ("128", "128")])
config.plugins.Boblight_grab.setup              = ConfigSelection(default = "0", choices = [("0", "0"), ("1", "1")])
config.plugins.Boblight_grab.chasemode          = ConfigEnableDisable(default=False)

config.plugins.Boblight_grab.vscanstart         = ConfigSlider(default=0, increment=5, limits=(0,100))
config.plugins.Boblight_grab.vscanend           = ConfigSlider(default=0, increment=5, limits=(0,100))
config.plugins.Boblight_grab.hscanstart         = ConfigSlider(default=0, increment=5, limits=(0,100))
config.plugins.Boblight_grab.hscanend           = ConfigSlider(default=0, increment=5, limits=(0,100))

config.plugins.Boblight_grab.autostart          = ConfigEnableDisable(default=False)
config.plugins.Boblight_grab.presets            = ConfigSelection(default = "1", choices = [("1", "Smooth"),("2", "Very Smooth"),("3", "Smooth/Action"), ("4", "Action"), ("5", "Boblight defaults"), ("0", "Custom")])

config.plugins.Boblight_grab.saturation         = ConfigSelection(default = "1.0", choices = [
("0.0", "0.0"), 
("0.1", "0.1"), 
("0.2", "0.2"), 
("0.3", "0.3"),
("0.4", "0.4"),
("0.5", "0.5"), 
("0.6", "0.6"), 
("0.7", "0.7"),
("0.8", "0.8"),
("0.9", "0.9"), 
("1.0", "1.0"), 
("1.1", "1.1"), 
("1.2", "1.2"), 
("1.3", "1.3"),
("1.4", "1.4"),
("1.5", "1.5"), 
("1.6", "1.6"), 
("1.7", "1.7"),
("1.8", "1.8"),
("1.9", "1.9"), 
("2.0", "2.0"), 
("2.1", "2.1"),
("2.2", "2.2"),
("2.3", "2.3"), 
("2.4", "2.4"), 
("2.5", "2.5"),
("2.6", "2.6"),
("2.7", "2.7"), 
("2.8", "2.8"),
("2.9", "2.9"),
("3.0", "3.0"),
("3.1", "3.1"),
("3.2", "3.2"),
("3.3", "3.3"), 
("3.4", "3.4"), 
("3.5", "3.5"),
("3.6", "3.6"),
("3.7", "3.7"), 
("3.8", "3.8"),
("3.9", "3.9"),
("4.0", "4.0"),
("4.1", "4.1"),
("4.2", "4.2"),
("4.3", "4.3"), 
("4.4", "4.4"), 
("4.5", "4.5"),
("4.6", "4.6"),
("4.7", "4.7"), 
("4.8", "4.8"),
("4.9", "4.9"),
("5.0", "5.0"),
("5.0", "5.0"), 
("5.1", "5.1"), 
("5.2", "5.2"), 
("5.3", "5.3"),
("5.4", "5.4"),
("5.5", "5.5"), 
("5.6", "5.6"), 
("5.7", "5.7"),
("5.8", "5.8"),
("5.9", "5.9"), 
("6.0", "6.0"), 
("6.1", "6.1"),
("6.2", "6.2"),
("6.3", "6.3"), 
("6.4", "6.4"), 
("6.5", "6.5"),
("6.6", "6.6"),
("6.7", "6.7"), 
("6.8", "6.8"),
("6.9", "6.9"),
("7.0", "7.0"),
("7.1", "7.1"),
("7.2", "7.2"),
("7.3", "7.3"), 
("7.4", "7.4"), 
("7.5", "7.5"),
("7.6", "7.6"),
("7.7", "7.7"), 
("7.8", "7.8"),
("7.9", "7.9"),
("8.0", "8.0"),
("8.1", "8.1"),
("8.2", "8.2"),
("8.3", "8.3"), 
("8.4", "8.4"), 
("8.5", "8.5"),
("8.6", "8.6"),
("8.7", "8.7"), 
("8.8", "8.8"),
("8.9", "8.9"),
("9.0", "9.0"),
("9.1", "9.1"),
("9.2", "9.2"),
("9.3", "9.3"), 
("9.4", "9.4"), 
("9.5", "9.5"),
("9.6", "9.6"),
("9.7", "9.7"), 
("9.8", "9.8"),
("9.9", "9.9"),
("10.0", "10.0"),
("10.1", "10.1"), 
("10.2", "10.2"), 
("10.3", "10.3"),
("10.4", "10.4"),
("10.5", "10.5"), 
("10.6", "10.6"), 
("10.7", "10.7"),
("10.8", "10.8"),
("10.9", "10.9"), 
("11.0", "11.0"), 
("11.1", "11.1"),
("11.2", "11.2"),
("11.3", "11.3"), 
("11.4", "11.4"), 
("11.5", "11.5"),
("11.6", "11.6"),
("11.7", "11.7"), 
("11.8", "11.8"),
("11.9", "11.9"),
("12.0", "12.0"),
("12.1", "12.1"),
("12.2", "12.2"),
("12.3", "12.3"), 
("12.4", "12.4"), 
("12.5", "12.5"),
("12.6", "12.6"),
("12.7", "12.7"), 
("12.8", "12.8"),
("12.9", "12.9"),
("13.0", "13.0"),
("13.1", "13.1"),
("13.2", "13.2"),
("13.3", "13.3"), 
("13.4", "13.4"), 
("13.5", "13.5"),
("13.6", "13.6"),
("13.7", "13.7"), 
("13.8", "13.8"),
("14.9", "13.9"),
("14.0", "14.0"),
("14.1", "14.1"),
("14.2", "14.2"),
("14.3", "14.3"), 
("14.4", "14.4"), 
("14.5", "14.5"),
("14.6", "14.6"),
("14.7", "14.7"), 
("14.8", "14.8"),
("14.9", "14.9"),
("15.0", "15.0"),
("15.1", "15.1"),
("15.2", "15.2"),
("15.3", "15.3"), 
("15.4", "15.4"), 
("15.5", "15.5"),
("15.6", "15.6"),
("15.7", "15.7"), 
("15.8", "15.8"),
("15.9", "15.9"),
("16.0", "16.0"),
("16.1", "16.1"),
("16.2", "16.2"),
("16.3", "16.3"), 
("16.4", "16.4"), 
("16.5", "16.5"),
("16.6", "16.6"),
("16.7", "16.7"), 
("16.8", "16.8"),
("16.9", "16.9"),
("17.0", "17.0"),
("17.1", "17.1"),
("17.2", "17.2"),
("17.3", "17.3"), 
("17.4", "17.4"), 
("17.5", "17.5"),
("17.6", "17.6"),
("17.7", "17.7"), 
("17.8", "17.8"),
("17.9", "17.9"),
("18.0", "18.0"),
("18.1", "18.1"),
("18.2", "18.2"),
("18.3", "18.3"), 
("18.4", "18.4"), 
("18.5", "18.5"),
("18.6", "18.6"),
("18.7", "18.7"), 
("18.8", "18.8"),
("18.9", "18.9"),
("19.0", "19.0"),
("19.1", "19.1"),
("19.2", "19.2"),
("19.3", "19.3"), 
("19.4", "19.4"), 
("19.5", "19.5"),
("19.6", "19.6"),
("19.7", "19.7"), 
("19.8", "19.8"),
("19.9", "19.9"),
("20.0", "20.0")])

config.plugins.Boblight_grab.valuemin = ConfigSelection(default = "0.0", choices = [
("0.0", "0.0"), 
("0.1", "0.1"), 
("0.2", "0.2"), 
("0.3", "0.3"),
("0.4", "0.4"),
("0.5", "0.5"), 
("0.6", "0.6"), 
("0.7", "0.7"),
("0.8", "0.8"),
("0.9", "0.9"), 
("1.0", "1.0")])

config.plugins.Boblight_grab.valuemax = ConfigSelection(default = "1.0", choices = [
("0.0", "0.0"), 
("0.1", "0.1"), 
("0.2", "0.2"), 
("0.3", "0.3"),
("0.4", "0.4"),
("0.5", "0.5"), 
("0.6", "0.6"), 
("0.7", "0.7"),
("0.8", "0.8"),
("0.9", "0.9"), 
("1.0", "1.0")])
 
config.plugins.Boblight_grab.saturation = ConfigSelection(default = "1.0", choices = [
("0.0", "0.0"), 
("0.1", "0.1"), 
("0.2", "0.2"), 
("0.3", "0.3"),
("0.4", "0.4"),
("0.5", "0.5"), 
("0.6", "0.6"), 
("0.7", "0.7"),
("0.8", "0.8"),
("0.9", "0.9"), 
("1.0", "1.0"), 
("1.1", "1.1"), 
("1.2", "1.2"), 
("1.3", "1.3"),
("1.4", "1.4"),
("1.5", "1.5"), 
("1.6", "1.6"), 
("1.7", "1.7"),
("1.8", "1.8"),
("1.9", "1.9"), 
("2.0", "2.0"), 
("2.1", "2.1"),
("2.2", "2.2"),
("2.3", "2.3"), 
("2.4", "2.4"), 
("2.5", "2.5"),
("2.6", "2.6"),
("2.7", "2.7"), 
("2.8", "2.8"),
("2.9", "2.9"),
("3.0", "3.0"),
("3.1", "3.1"),
("3.2", "3.2"),
("3.3", "3.3"), 
("3.4", "3.4"), 
("3.5", "3.5"),
("3.6", "3.6"),
("3.7", "3.7"), 
("3.8", "3.8"),
("3.9", "3.9"),
("4.0", "4.0"),
("4.1", "4.1"),
("4.2", "4.2"),
("4.3", "4.3"), 
("4.4", "4.4"), 
("4.5", "4.5"),
("4.6", "4.6"),
("4.7", "4.7"), 
("4.8", "4.8"),
("4.9", "4.9"),
("5.0", "5.0")
])

config.plugins.Boblight_grab.gamma = ConfigSelection(default = "2.2", choices = [
("1.0", "1.0"), 
("1.1", "1.1"), 
("1.2", "1.2"), 
("1.3", "1.3"),
("1.4", "1.4"),
("1.5", "1.5"), 
("1.6", "1.6"), 
("1.7", "1.7"),
("1.8", "1.8"),
("1.9", "1.9"), 
("2.0", "2.0"), 
("2.1", "2.1"),
("2.2", "2.2"),
("2.3", "2.3"), 
("2.4", "2.4"), 
("2.5", "2.5"),
("2.6", "2.6"),
("2.7", "2.7"), 
("2.8", "2.8"),
("2.9", "2.9"),
("3.0", "3.0"),
("3.1", "3.1"),
("3.2", "3.2"),
("3.3", "3.3"), 
("3.4", "3.4"), 
("3.5", "3.5"),
("3.6", "3.6"),
("3.7", "3.7"), 
("3.8", "3.8"),
("3.9", "3.9"),
("4.0", "4.0"),
("4.1", "4.1"),
("4.2", "4.2"),
("4.3", "4.3"), 
("4.4", "4.4"), 
("4.5", "4.5"),
("4.6", "4.6"),
("4.7", "4.7"), 
("4.8", "4.8"),
("4.9", "4.9"),
("5.0", "5.0"),
("5.0", "5.0"), 
("5.1", "5.1"), 
("5.2", "5.2"), 
("5.3", "5.3"),
("5.4", "5.4"),
("5.5", "5.5"), 
("5.6", "5.6"), 
("5.7", "5.7"),
("5.8", "5.8"),
("5.9", "5.9"), 
("6.0", "6.0"), 
("6.1", "6.1"),
("6.2", "6.2"),
("6.3", "6.3"), 
("6.4", "6.4"), 
("6.5", "6.5"),
("6.6", "6.6"),
("6.7", "6.7"), 
("6.8", "6.8"),
("6.9", "6.9"),
("7.0", "7.0"),
("7.1", "7.1"),
("7.2", "7.2"),
("7.3", "7.3"), 
("7.4", "7.4"), 
("7.5", "7.5"),
("7.6", "7.6"),
("7.7", "7.7"), 
("7.8", "7.8"),
("7.9", "7.9"),
("8.0", "8.0"),
("8.1", "8.1"),
("8.2", "8.2"),
("8.3", "8.3"), 
("8.4", "8.4"), 
("8.5", "8.5"),
("8.6", "8.6"),
("8.7", "8.7"), 
("8.8", "8.8"),
("8.9", "8.9"),
("9.0", "9.0"),
("9.1", "9.1"),
("9.2", "9.2"),
("9.3", "9.3"), 
("9.4", "9.4"), 
("9.5", "9.5"),
("9.6", "9.6"),
("9.7", "9.7"), 
("9.8", "9.8"),
("9.9", "9.9"),
("10.0", "10.0")
])


config.plugins.Boblight_grab.saturationmin = ConfigSelection(default = "0.0", choices = [
("0.0", "0.0"), 
("0.1", "0.1"), 
("0.2", "0.2"), 
("0.3", "0.3"),
("0.4", "0.4"),
("0.5", "0.5"), 
("0.6", "0.6"), 
("0.7", "0.7"),
("0.8", "0.8"),
("0.9", "0.9"), 
("1.0", "1.0")])

config.plugins.Boblight_grab.saturationmax = ConfigSelection(default = "1.0", choices = [
("0.0", "0.0"), 
("0.1", "0.1"), 
("0.2", "0.2"), 
("0.3", "0.3"),
("0.4", "0.4"),
("0.5", "0.5"), 
("0.6", "0.6"), 
("0.7", "0.7"),
("0.8", "0.8"),
("0.9", "0.9"), 
("1.0", "1.0")])

config.plugins.Boblight_grab.value = ConfigSlider(default=1, increment=1, limits=(0,20))
config.plugins.Boblight_grab.speed = ConfigSlider(default=100, increment=1, limits=(0,100))
config.plugins.Boblight_grab.chase_speed = ConfigSlider(default=60, increment=1, limits=(0,100))
config.plugins.Boblight_grab.autospeed = ConfigSlider(default=0, increment=1, limits=(0,100))
config.plugins.Boblight_grab.interpolation = ConfigSelection(default = "true", choices = [("true", "Enabled"), ("false", "Disabled")])

pluginversion = "Version: 0.5r7"

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
    PluginDescriptor(name='Boblight | Enable / Disable', description=_('Ambilight clone'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon='boblight.png', fnc=DaemonToggle),
    PluginDescriptor(name='Boblight Menu', description=_('Ambilight clone'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon='boblight.png', fnc=startSetup)]

def main(session, **kwargs):
    session.open(startSetup)

def startSetup(session, **kwargs):
    print "[Boblight] start configuration"
    session.open(BoblightConfig)
