#!/bin/bash

 # boblight
 # Copyright (C) Bob Loosen 2009 
 #
 # makeboblight.sh created by Adam Boeglin <adamrb@gmail.com>
 #                                       modded by 
 #                                Martijn Vos (Speedy1985) 
 #                                          and 
 #                            Oktay Oeztueter (info@oktay.com)
 # 
 # boblight is free software: you can redistribute it and/or modify it
 # under the terms of the GNU General Public License as published by the
 # Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 # 
 # boblight is distributed in the hope that it will be useful, but
 # WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 # See the GNU General Public License for more details.
 # 
 # You should have received a copy of the GNU General Public License along
 # with this program.  If not, see <http://www.gnu.org/licenses/>.


# Usage
#
# This script makes quite a few assumptions of your light system
#
# 1. You have your lights evenly spaced on each side they are on
# 2. You only have one device configured
# 3. Each color light is on the same device
# 4. >>>Lights are arranged clockwise around monitor starting at the bottom center<<<
# 5. Probably some other things I'm missing
#
# How to run:
# This should work on any *nix system with bash and 'bc' installed.
#
# Make the script executable (chmod +x makeboblight.sh), and run it with ./makeboblight.sh

clear

# Set the defaults
dleft=4
dtop=4
dright=4
dbottom=4
ddevicename="karatelight"
ddepth=20
doutput="/dev/ttyUSB0"
dprefix=""
dpostfix=""
dblacklevel="0.1"

oktolight="oktolight"
karatelight="karatelight"
momolight="momolight"
sedulight="sedulight"
atmolight="atmolight"

echo "*** Boblight Configuration Generator ***"
echo "Please answer the following questions.  Press [enter] for defaults."
echo
echo "Choose your setup:"
echo "1. MOMO: Adalight etc....."
echo "2. Sedulight"
echo "3. Atmolight"
echo "4. Karatelight"
echo "5. Oktolight"
echo ""
echo -n "Default[4] "
read device

#Set default
device=${device:-4}

echo -n "Where is your device? Default[/dev/ttyUSB0] "
read output

if [ ${device} == 1 ]; then
	echo -n "Does this device need a prefix? type the prefix. Default[] "
	read prefix

	echo -n "Does this device need a postfix? type the postfix. Default[] "
	read postfix
fi

echo -n "What is the depth that the hscan and vscan should look into the screen? Default[$ddepth] "
read depth

echo -n "How many lights on the Left side? Default[$dleft] "
read left

echo -n "How many lights on the Top? Default[$dtop] "
read top

echo -n "How many lights on the Right side? Default[$dright] "
read right

echo -n "How many lights on the Bottom? Default[$dbottom] "
read bottom

echo -n "Enter the blacklevel you like. Default[$dblacklevel] "
read blacklevel

# Set the defaults, if they were accepted.
left=${left:-$dleft}
top=${top:-$dtop}
right=${right:-$dright}
bottom=${bottom:-$dbottom}
depth=${depth:-$ddepth}

blacklevel=${blacklevel:-$dblacklevel}

output=${output:-$doutput}
prefix=${prefix:-$dprefix}
postfix=${postfix:-$dpostfix}


# Calculate total
total=$((left + top + right + bottom))
channels=$((total + total + total))

echo ""
echo "Create boblight.conf file..."
rm boblight.conf 2> /dev/null
echo "[global]"  >> boblight.conf
echo "#interface    	10.0.0.2" >> boblight.conf
echo "#port         	19333" >> boblight.conf
echo >> boblight.conf

## Momo ##
if [ ${device} == 1 ]; then
	devicename=$momolight
	echo "[device]" >> boblight.conf
	echo "name		$momolight" >> boblight.conf
	echo "output   	 	$output" >> boblight.conf
	echo "channels		$channels" >> boblight.conf
	echo "type		momo" >> boblight.conf
	echo "interval		16000" >> boblight.conf
	if [ $prefix ]; then
		echo "prefix		$prefix" >> boblight.conf
	fi
	if [ $postfix ]; then
		echo "postfix		$postfix" >> boblight.conf
	fi
	echo "rate	115200" >> boblight.conf
fi

## Sedu ##
if [ ${device} == 2 ]; then
	devicename=$sedulight
	echo "[device]" >> boblight.conf
	echo "name		$sedulight" >> boblight.conf
	echo "output    	$output" >> boblight.conf
	echo "channels		$channels" >> boblight.conf
	echo "type		sedu" >> boblight.conf
	echo "interval		10000" >> boblight.conf
	echo "rate		500000" >> boblight.conf
fi

## Atmolight ##
if [ ${device} == 3 ]; then
	devicename=$atmolight
	echo "[device]" >> boblight.conf
	echo "name		$atmolight" >> boblight.conf
	echo "output    	$output" >> boblight.conf
	echo "channels		$channels" >> boblight.conf
	echo "type		atmo" >> boblight.conf >> boblight.conf
	echo "interval		16000" >> boblight.conf
	echo "rate      	38400" >> boblight.conf
	echo "prefix    	FF" >> boblight.conf
fi

## Karatelight ##
if [ ${device} == 4 ]; then
	devicename=$karatelight	
	echo "[device]" >> boblight.conf
	echo "name      	$karatelight" >> boblight.conf
	echo "output    	$output" >> boblight.conf
	echo "channels  	$channels" >> boblight.conf
	echo "type		karate" >> boblight.conf
	echo "interval		16000" >> boblight.conf
	echo "rate		38400" >> boblight.conf
fi

## Oktolight ##
if [ ${device} == 5 ]; then
	devicename=$oktolight
	echo "[device]" >> boblight.conf
	echo "name		$okotlight" >> boblight.conf
	echo "output    	$output" >> boblight.conf
	echo "channels		$channels" >> boblight.conf
	echo "type		karate" >> boblight.conf
	echo "interval		16000" >> boblight.conf
	echo "rate		115200" >> boblight.conf
fi

#create colors
echo >> boblight.conf
echo >> boblight.conf

if [ $devicename == $oktolight ]; then
	rrgb="00FF00"
	grgb="0000FF"
	brgb="FF0000"
else
        rrgb="FF0000"
        grgb="00FF00"
        brgb="0000FF"
fi

echo "[color]" >> boblight.conf
echo "name              red" >> boblight.conf
echo "rgb               $rrgb" >> boblight.conf
echo "blacklevel        $blacklevel" >> boblight.conf
echo >> boblight.conf
echo "[color]" >> boblight.conf
echo "name              green" >> boblight.conf
echo "rgb               $grgb" >> boblight.conf
echo "blacklevel        $blacklevel" >> boblight.conf
echo >> boblight.conf
echo "[color]" >> boblight.conf
echo "name              blue" >> boblight.conf
echo "rgb               $brgb" >> boblight.conf
echo "blacklevel        $blacklevel" >> boblight.conf

#create lights section
current=1

#Channels
colorcount=1


if [ $left -ne 0 ]; then
	lcount=1
	lrange=$(echo "scale=2; 100 / $left" | bc)
	lcurrent=100

	while [ $lcount -le $left ]; do
		ltop=$(echo "scale=2; $lcurrent - $lrange" | bc)
		
		echo >> boblight.conf
		echo "[light]" >> boblight.conf
		echo "name            left$lcount" >> boblight.conf
		
		echo "color           red     $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           green   $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           blue    $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "hscan           0 $depth" >> boblight.conf
		echo "vscan           $ltop $lcurrent" >> boblight.conf

		lcurrent=$ltop

		((lcount++))
		((current++))
	done
fi


if [ $top -ne 0 ]; then
	tcount=1
	trange=$(echo "scale=2; 100 / $top" | bc)
	tcurrent=0

	while [ $tcount -le $top ]; do
		ttop=$(echo "scale=2; $tcurrent + $trange" | bc)

		echo >> boblight.conf
		echo "[light]" >> boblight.conf
		echo "name            top$tcount" >> boblight.conf

		echo "color           red     $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           green   $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           blue    $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "hscan           $tcurrent $ttop" >> boblight.conf
		echo "vscan           0 $depth" >> boblight.conf


		tcurrent=$ttop

		((tcount++))
		((current++))
	done
fi


if [ $right -ne 0 ]; then
	rcount=1
	rrange=$(echo "scale=2; 100 / $right" | bc)
	rcurrent=0

	while [ $rcount -le $right ]; do
		rtop=$(echo "scale=2; $rcurrent + $rrange" | bc)

		echo >> boblight.conf
		echo "[light]" >> boblight.conf
		echo "name            right$rcount" >> boblight.conf

		echo "color           red     $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           green   $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           blue    $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "hscan           $(echo "scale=2; 100 - $depth" | bc) 100" >> boblight.conf
		echo "vscan           $rcurrent $rtop" >> boblight.conf

		rcurrent=$rtop

		((rcount++))
		((current++))
	done
fi


if [ $bottom -ne 0 ]; then
	bcount=1

	bcurrent=100
	 brange=$(echo "scale=2; 100 / $bottom" | bc)

	while [ $bcount -le $bottom ]; do
		btop=$(echo "scale=2; $bcurrent - $brange" | bc)

		echo >> boblight.conf
		echo "[light]" >> boblight.conf
		echo "name            bottom$bcount" >> boblight.conf

		echo "color           red     $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           green   $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "color           blue    $devicename $colorcount" >> boblight.conf
		((colorcount++))

		echo "hscan           $btop $bcurrent" >> boblight.conf
		echo "vscan           $(echo "scale=2; 100 - $depth" | bc) 100" >> boblight.conf


		bcurrent=$btop

		((bcount++))
		((current++))
	done
fi

echo -n "Do you want to save the file boblight.conf to /etc ? [y]"
read question
question=${question:-y}

if [ ${question} == "y" ]; then
    mv boblight.conf /etc/boblight.conf 2>/dev/null
    echo "File 'boblight.conf' saved to /etc"
else
    mv boblight.conf /home/boblight.conf 2>/dev/null
    echo "File 'boblight.conf saved to /home"
fi