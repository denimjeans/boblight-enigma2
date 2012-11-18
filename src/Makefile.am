## Process this file with automake to produce Makefile.in

AM_CFLAGS =\
	 -Wall

bin_PROGRAMS = \
    boblight-chase \
	boblight-enigma2 \
	boblightd \
	boblight-constant

boblight_chase_SOURCES = \
    clients/boblight-chase/boblight-chase.cpp \
	clients/flagmanager.cpp \
	clients/boblight-chase/flagmanager-chase.cpp \
	util/misc.cpp

boblight_constant_SOURCES = \
	clients/boblight-constant/boblight-constant.cpp \
	clients/flagmanager.cpp \
	clients/boblight-constant/flagmanager-constant.cpp \
	util/misc.cpp

boblightd_SOURCES = \
	util/condition.cpp \
	util/log.cpp \
	util/misc.cpp \
	util/mutex.cpp \
	util/thread.cpp \
	util/timer.cpp \
	util/serialport.cpp \
    util/timeutils.cpp \
	main.cpp \
	util/tcpsocket.cpp \
	util/messagequeue.cpp \
	client.cpp \
	light.cpp \
	configuration.cpp \
	device/device.cpp \
	device/devicepopen.cpp \
	device/devicers232.cpp \
	device/deviceltbl.cpp \
	device/devicedioder.cpp \
	device/deviceibelight.cpp \
    util/signaltimer.cpp 

boblightd_LDFLAGS = -lusb-1.0
        
boblightd_LDADD = 

boblight_enigma2_SOURCES = \
	clients/boblight-enigma2/boblight-enigma2.cpp \
	util/timer.cpp \
	util/condition.cpp \
	util/mutex.cpp \
	util/misc.cpp \
    util/timeutils.cpp \
	clients/flagmanager.cpp \
	clients/boblight-enigma2/grabber-enigma2.cpp \
	clients/boblight-enigma2/flagmanager-enigma2.cpp 
	
boblight_enigma2_LDFLAGS = 

lib_LTLIBRARIES = \
	libboblight.la

libboblight_la_SOURCES = \
	lib/boblight_client.cpp \
	lib/boblight.cpp \
	util/messagequeue.cpp \
	util/misc.cpp \
	util/tcpsocket.cpp
	
libboblight_la_CPPFLAGS = $(AM_CPPFLAGS)
