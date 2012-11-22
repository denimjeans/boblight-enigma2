#!/bin/bash

 # boblight
 # Copyright (C) Bob Loosen 2009 
 #
 # makeboblight.sh created by Adam Boeglin <adamrb@gmail.com>, modded by Martijn Vos (Speedy1985)
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
echo -n "Default[4]"
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

echo -n "What is the depth that the hscan and vscan should look into the screen? Default[20] "
read depth

echo -n "How many lights on the Left side? Default[0] "
read left

echo -n "How many lights on the Top? Default[0] "
read top

echo -n "How many lights on the Right side? Default[0] "
read right

echo -n "How many lights on the Bottom? Default[0] "
read bottom

# Calculate total
total=$(expr $left + $top + $right + $bottom)
channels=$(expr $total + $total + $total)

# Set the defaults
left=${left:-0}
top=${top:-0}
right=${right:-0}
bottom=${bottom:-0}
devicename=${devicename:-ambilight1}
depth=${depth:-20}

output=${output:-/dev/ttyUSB0}
prefix=${prefix:-}
postfix=${postfix:-}

echo ""
echo "Create boblight.conf file..."
rm boblight.conf 2> /dev/null
echo "[global]"  >> boblight.conf
echo "#interface    10.0.0.2" >> boblight.conf
echo "#port         19333" >> boblight.conf
echo >> boblight.conf

## Karatelight ##
if [ ${device} == 4 ]; then
	
	echo "[device]" >> boblight.conf
	echo "name      $devicename" >> boblight.conf
	echo "output    $output" >> boblight.conf
	echo "channels  $channels" >> boblight.conf
	echo "type		karate" >> boblight.conf
	echo "interval	16000" >> boblight.conf
	echo "prefix	FF" >> boblight.conf
	echo "rate		38400" >> boblight.conf
fi

## Sedu ##
if [ ${device} == 2 ]; then
	
	echo "[device]" >> boblight.conf
	echo "name		$devicename" >> boblight.conf
	echo "output    $output" >> boblight.conf
	echo "channels	$channels" >> boblight.conf
	echo "type		sedu" >> boblight.conf
	echo "interval	10000" >> boblight.conf
	echo "rate		500000" >> boblight.conf
fi

## Momo ##
if [ ${device} == 1 ]; then
	
	echo "[device]" >> boblight.conf
	echo "name		$devicename" >> boblight.conf
	echo "output    $output" >> boblight.conf
	echo "channels	$channels" >> boblight.conf
	echo "type		momo" >> boblight.conf
	echo "interval	16000" >> boblight.conf
	if [ $prefix ]; then
		echo "prefix	$prefix" >> boblight.conf
	fi
	if [ $postfix ]; then
		echo "postfix	$postfix" >> boblight.conf
	fi
	echo "rate		115200" >> boblight.conf
fi

## Oktolight ##
if [ ${device} == 5 ]; then
	
	echo "[device]" >> boblight.conf
	echo "name		$devicename" >> boblight.conf
	echo "output    $output" >> boblight.conf
	echo "channels	$channels" >> boblight.conf
	echo "type		karate" >> boblight.conf
	echo "interval	16000" >> boblight.conf
	echo "rate		115200" >> boblight.conf
    echo "prefix    FF" >> boblight.conf
fi

## Atmolight ##
if [ ${device} == 3 ]; then
	
	echo "[device]" >> boblight.conf
	echo "name		$devicename" >> boblight.conf
	echo "output    $output" >> boblight.conf
	echo "channels	$channels" >> boblight.conf
	echo "type		atmo" >> boblight.conf >> boblight.conf
	echo "interval	16000" >> boblight.conf
	echo "rate      38400" >> boblight.conf
	echo "prefix    FF" >> boblight.conf
fi

#create colors
echo >> boblight.conf
echo >> boblight.conf
echo "[color]" >> boblight.conf
echo "name		red" >> boblight.conf
echo "rgb		FF0000" >> boblight.conf
echo >> boblight.conf
echo "[color]" >> boblight.conf
echo "name		green" >> boblight.conf
echo "rgb		00FF00" >> boblight.conf
echo >> boblight.conf
echo "[color]" >> boblight.conf
echo "name		blue" >> boblight.conf
echo "rgb		0000FF" >> boblight.conf


#create lights section
current=1

#Channels
colorcount=1


if [ $bottom -ne 0 ]; then
	bcount=1
	brange=$(echo "scale=2; 100 / $bottom" | bc)
	bcurrent=50

	while [ $bcount -le $(expr $bottom / 2 2>/dev/null) ]; do
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
	bcurrent=100

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
