/*
 * Boblight
 * Copyright (C) Bob Loosen  2009 
 * Copyright (C) Martijn Vos and Carsten presser 2012
 *
 * boblight is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * boblight is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along
 * with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <iostream>

#include "flagmanager-enigma2.h"
#include "util/misc.h"
#include "config.h"

using namespace std;

CFlagManagerEnigma2::CFlagManagerEnigma2()
{
  //extend the base getopt flags
  //i = interval, u = pixels, d = debug
  m_flags += "i:u:t:d::b::g::";

  m_blackbar= false;	 // Blackbar detection, default disabled
  m_interval= 0.1;   	 // default interval is 100 milliseconds
  m_pixels 	= 128;   	 // Set pixel default to 128.
  m_debug 	= false; 	 // no debugging by default
  m_picdump = false;  	 // Picture dump, default false
  m_sync 	= true;      // sync mode, enabled by default
  m_timeshift = 0;
}

void CFlagManagerEnigma2::ParseFlagsExtended(int& argc, char**& argv, int& c, char*& optarg)
{
  if (c == 'i') //interval
  {
    if (!StrToFloat(optarg, m_interval) || m_interval <= 0.0)
    {
      throw string("Wrong value " + string(optarg) + " for interval");
    }
  }
  else if (c == 'u') //nr of pixels to use
  {
    if (!StrToInt(optarg, m_pixels) || m_pixels <= 0)
    {
      throw string("Wrong value " + string(optarg) + " for pixels");
    }
  }
  else if (c == 't') //beta timeshift test
  {
    if (!StrToInt(optarg, m_timeshift) || m_timeshift <= 0)
    {
      throw string("Wrong value " + string(optarg) + " for timeshift");
    }
  }
  else if (c == 'd') //turn on debug mode
  {
    m_debug = true;
  }
  else if (c == 'b') //turn on blackbar mode
  {
    m_blackbar = true;
  }
  else if (c == 'g') //turn on picdump mode
  {
    m_picdump = true;
  }
}

void CFlagManagerEnigma2::PrintHelpMessage()
{
  cout << "Usage: boblight-enigma2 [OPTION]\n";
  cout << "\n";
  cout << "  options:\n";
  cout << "\n";
  cout << "  -p  priority, from 0 to 255, default is 128\n";
  cout << "  -s  address:[port], set the address and optional port to connect to\n";
  cout << "  -o  add libboblight option, syntax: [light:]option=value\n";
  cout << "  -l  list libboblight options\n";
  cout << "  -i  set the interval in mseconds, default is 0.1 (100 milliseconds)\n";
  cout << "  -u  maximum size for the intermediate image (default 128)\n";
  cout << "  -d  enable debug mode. \n";
  cout << "  -b  enable blackbar mode (only top/bottom for now). \n";
  cout << "  -g  enable picture dump mode. Be carefull! this stores a lot of image data to /tmp! \n";
  cout << "  -f  fork\n";
  cout << "\n";
}
