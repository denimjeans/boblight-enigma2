/*
 * boblight
 * Copyright (C) Bob  2009 
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

#define BOBLIGHT_DLOPEN
#include "lib/boblight.h"
#include <malloc.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <vector>
#include <signal.h>
#include <unistd.h>

#include "config.h"
#include "util/misc.h"
#include "flagmanager-chase.h"

#define MIN(a, b) ((a) < (b)) ? (a) : (b)

int ** colours;
using namespace std;

int  Run();
void SignalHandler(int signum);

volatile bool stop = false;
CFlagManagerChase g_flagmanager;
int black[3] = {0, 0 ,0};


int main(int argc, char *argv[])
{
  //load the boblight lib, if it fails we get a char* from dlerror()
  char* boblight_error = boblight_loadlibrary(NULL);
  if (boblight_error)
  {
    PrintError(boblight_error);
    return 1;
  }

  //try to parse the flags and bitch to stderr if there's an error
  try
  {
    g_flagmanager.ParseFlags(argc, argv);
  }
  catch (string error)
  {
    PrintError(error);
    g_flagmanager.PrintHelpMessage();
    return 1;
  }
  
  if (g_flagmanager.m_printhelp) //print help message
  {
    g_flagmanager.PrintHelpMessage();
    return 1;
  }

  if (g_flagmanager.m_printboblightoptions) //print boblight options (-o [light:]option=value)
  {
    g_flagmanager.PrintBoblightOptions();
    return 1;
  }

  if (g_flagmanager.m_fork)
  {
    if (fork())
      return 0;
  }

  //set up signal handlers
  signal(SIGTERM, SignalHandler);
  signal(SIGINT, SignalHandler);

  //keep running until we want to quit
  return Run();
}

int Run()
{
   while(!stop)
  {
    //init boblight
    int mode = 0;
    
    void* boblight = boblight_init();

    cout << "Connecting to boblightd\n";
    
    //try to connect, if we can't then bitch to stderr and destroy boblight
    if (!boblight_connect(boblight, g_flagmanager.m_address, g_flagmanager.m_port, 5000000) ||
        !boblight_setpriority(boblight, g_flagmanager.m_priority))
    {
      PrintError(boblight_geterror(boblight));
      cout << "Waiting 10 seconds before trying again\n";
      boblight_destroy(boblight);
      sleep(10);
      continue;
    }

    cout << "Connection to boblightd opened\n";

    //try to parse the boblight flags and bitch to stderr if we can't
    try
    {
      g_flagmanager.ParseBoblightOptions(boblight);
    }
    catch (string error)
    {
      PrintError(error);
      return 1;
    }

	
    //load the color into int array
//    int rgb[3] = {(g_flagmanager.m_color >> 16) & 0xFF, (g_flagmanager.m_color >> 8) & 0xFF, g_flagmanager.m_color & 0xFF};
    
    mode = g_flagmanager.m_mode;
    printf("param: %d\n", g_flagmanager.m_color);
   /* Chase */
    if(mode == 0)
    {
        printf("Mode: Chase %i\n",g_flagmanager.m_mode);
        int rgb[3] = {0, 0 ,0};
        int numPix = boblight_getnrlights(boblight);
        int i = 0;
        int starting =  1;
        int curPix = 0;
        colours = (int **) calloc(numPix + 4, sizeof(int *));
        for(i = 0 ; i < numPix + 4; i++)
        {
            colours[i] = (int *) calloc(3, sizeof(int));
        }   
	srand ( time(NULL) );   
       
        boblight_addpixel(boblight, -1, rgb);
        while(!stop)
        {
	     int  newIndex = (starting + numPix + 3) % (numPix + 4);
             int desiredBrightness = g_flagmanager.m_color;

	     float actualBrightness;
	     float factor;
             colours[newIndex][0] = rand() % 0xFF;
             colours[newIndex][1] = rand() % 0xFF;
             colours[newIndex][2] = rand() % 0xFF;
	     actualBrightness = sqrt(colours[newIndex][0] * colours[newIndex][0] * 0.299 + colours[newIndex][1] * colours[newIndex][1] * 0.578 + colours[newIndex][2] * colours[newIndex][2] * 0.114);
	     factor = desiredBrightness / actualBrightness;

	     colours[newIndex][0] *= factor;
             colours[newIndex][1] *= factor;
	     colours[newIndex][2] *= factor;

             starting--;
	     if (starting < 0)
	         starting += numPix + 4;

            for(i = 0; i < numPix; i++)
            {
                int j = 0;
                //set all lights to the color we want and send it
                //for(j = 0; j < 4; j++)
		{
			int bitPattern = (starting - 1) & 0x3;
			int colourIndex = numPix + starting + 63 +  4 - i;
			colourIndex |= 0x3;
	//		colourIndex -= 4;
			//colourIndex |= 0x1;
			colourIndex %= (numPix + 4);
			boblight_addpixel(boblight, i, colours[colourIndex]);
		}
		//i+= 3;
		
             }	

		
             if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
             {
                 PrintError(boblight_geterror(boblight));
                 boblight_destroy(boblight);
                 continue;
             }
             usleep(50 * 1000);
	}
    } else if(mode == 1) {
       /* Pulse */
        printf("Mode: Chase %i\n",g_flagmanager.m_mode);
	int i;
	int desiredBrightness = g_flagmanager.m_color;
	int rgb[3] = {desiredBrightness, desiredBrightness, desiredBrightness};
	int newRGB[3] = {desiredBrightness, desiredBrightness, desiredBrightness};

	float factor = 0.0;
	float actualBrightness;

	cout << "Desired Brightness " << desiredBrightness << endl;
	while(!stop)
	{

		while((!stop) && (rgb[0] != newRGB[0] || rgb[1] != newRGB[1] || rgb[2] != newRGB[2]))
		{

			for(i =0; i < 3; i++)
			{
				if(rgb[i] < newRGB[i])
				{
					rgb[i]++;
				} else if(rgb[i] > newRGB[i])
				{
					rgb[i]--;
				}
			}		

			boblight_addpixel(boblight, -1, rgb);
			
			if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
      	      		{
        			PrintError(boblight_geterror(boblight));
        			boblight_destroy(boblight);
        			continue;
      			}
			usleep(20 * 1000);

		}
		newRGB[0] = rand() % 0xFF;       
		newRGB[1] = rand() % 0xFF;       
		newRGB[2] = rand() % 0xFF;       

		actualBrightness = sqrt(newRGB[0] * newRGB[0] * 0.299 + newRGB[1] * newRGB[1] * 0.578 + newRGB[2] * newRGB[2] * 0.114);
		factor = desiredBrightness / actualBrightness;
		newRGB[0] *= factor;
		newRGB[1] *= factor;
		newRGB[2] *= factor;	

		newRGB[0] =  MIN(0xFF, newRGB[0]);
		newRGB[1] =  MIN(0xFF, newRGB[1]);
		newRGB[2] =  MIN(0xFF, newRGB[2]);

	  }
    } else if(mode == 2){
/* Rainbow */	
        printf("Mode: Rainbow\n");
	int rgb[7][3] = {{0xFF, 0, 0}, {0xFF, 0x80, 0}, {0xFF, 0xFF,  0}, {0, 0xFF, 0}, {0, 0, 0xFF}, {0x4B, 0, 0x82}, {0xEE, 0x82, 0xEE}};
        int numPix = boblight_getnrlights(boblight);
	int  finalRGB[numPix][3];
	int i, j;

	for(i = 0; i < numPix; i++)
	{
		finalRGB[i][0] = rgb[7 * i/numPix][0];
		finalRGB[i][1] = rgb[7 * i/numPix][1];
		finalRGB[i][2] = rgb[7 * i/numPix][2];
	}

	for(i = 0; i < numPix; i++)
	{
			boblight_addpixel(boblight, i, finalRGB[numPix - i]);
	}
	
	if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
      	{
        	PrintError(boblight_geterror(boblight));
        	boblight_destroy(boblight);
        	continue;
      	}

	
    } else if(mode == 3){
/* Pulse Rainbow */
        printf("Mode: Pule Rainbow\n");
	int counter=  0;
        int numPix = boblight_getnrlights(boblight);
	int * bitFields;
	int i = 0, j = 0;
	int mode = 0;
	int rgb[7][3] = {{0xFF, 0, 0}, {0xFF, 0x80, 0}, {0xFF, 0xFF,  0}, {0, 0xFF, 0}, {0, 0, 0xFF}, {0x4B, 0, 0x82}, {0xEE, 0x82, 0xEE}};
	int m, n;
	bitFields = (int *) calloc(numPix / 32, sizeof(int));
	

	while(!stop)
	{
		switch(mode)
		{
			case 0:
				bitFields[i >> 5] |= (1 << (i % 32));
				break;
			case 1:
				bitFields[i >> 5] ^= (1 << (i % 32));
				break;
	
			case 2:
				{
					int k = numPix - i - 1;
					bitFields[k >> 5] |= (1 << (k % 32));
					break;
				}			
			case 3:
				{
					int k = numPix - i - 1;
					bitFields[k >> 5] ^= (1 << (k % 32));
					break;
				}
		}





		for(j = 0; j < numPix; j++)
		{
//				printf("add %d\n", j);
				for(m = 6; m >= 0; m--)
				{
					for(n = 0; n < 9; n++)
					{	
						if(bitFields[(10*m + n) >> 5] & (1 << ((10 * m + n) % 32)))
						{

							boblight_addpixel(boblight,  9*m + n + m, rgb[6-m]);
						}  else  {

							boblight_addpixel(boblight,  9*m + n + m, black);
						}
							
					}


				//ooboblight_addpixel(boblight,  j, rgb);
				}
		}
		
		if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
      		{
        		PrintError(boblight_geterror(boblight));
        		boblight_destroy(boblight);
        		continue;
      		}

		usleep(40 * 1000);
		i++;
		if(i == numPix)
		{
			i = 0;
			mode++;
			mode %= 4;
		}
        }
    } else if (mode == 4) {
/*  Rainbow 3 */
        printf("Mode: Rainbow 3\n");
	int counter=  0;
        int numPix = boblight_getnrlights(boblight);
	int * bitFields;
	int i = 0, j = 0, k =0;
	int m, n;

	int rgb[7][3] = {{0xFF, 0, 0}, {0xFF, 0x80, 0}, {0xFF, 0xFF,  0}, {0, 0xFF, 0}, {0, 0, 0xFF}, {0x4B, 0, 0x82}, {0xEE, 0x82, 0xEE}};
	int  finalRGB[numPix][3];

	for(i = 0; i < numPix; i++)
	{
		finalRGB[i][0] = rgb[7 * i/numPix][0];
		finalRGB[i][1] = rgb[7 * i/numPix][1];
		finalRGB[i][2] = rgb[7 * i/numPix][2];
	}


	bitFields = (int *) calloc(numPix / 32, sizeof(int));
	

	while(!stop)
	{

	        boblight_addpixel(boblight, -1, black);
	        
		if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
  		{
    			PrintError(boblight_geterror(boblight));
        		boblight_destroy(boblight);
        		continue;
      		}


		for( i = 0 ; i < numPix; i++) // Turning each LED on
		{
			for(j = numPix; j >= i; j--) // Ticking for each LED turned on
			{
				
				for(k = 0; k < numPix; k++) // draw each pixel in tick
				{				
					if(k < i)
					{
						boblight_addpixel(boblight, k, finalRGB[numPix - k]);
					}
				
					if(k == j)
					{
						boblight_addpixel(boblight, k, finalRGB[numPix - i]);
					}						
				}
				
				if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
  				{
    					PrintError(boblight_geterror(boblight));
        				boblight_destroy(boblight);
        				continue;
      				}
	
				usleep(10 * 1000);
				
			}
			


		}
		sleep(2);			
    	}

    } else if (mode == 5) {
         
        printf("Mode: Static Color:%x\n",g_flagmanager.m_color);
        while(!stop)
        {
                int rgb[3];// = {(g_flagmanager.m_color >> 0) & 0xFF, (g_flagmanager.m_color >> 8) & 0xFF, (g_flagmanager.m_color >> 16) & 0xFF};
                
                rgb[0] = (g_flagmanager.m_color >> 16) & 0xFF;
		        rgb[1] = (g_flagmanager.m_color >> 8) & 0xFF;
		        rgb[2] = (g_flagmanager.m_color >> 0) & 0xFF;
		        
                //set all lights to the color we want and send it
                boblight_addpixel(boblight, -1, rgb);
                
                if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
                {
                        PrintError(boblight_geterror(boblight));
                        boblight_destroy(boblight);
                        continue;
                }
                
                usleep(200  * 1000);
        }

    }else {
	int  flashCol[3] = { 0x80, 0x80, 0x80 };
	int  curFlash[3];
	int i,j;
	boblight_addpixel(boblight, -1, black);
	
	if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
      	{
        	PrintError(boblight_geterror(boblight));
        	boblight_destroy(boblight);
        	continue;
      	}
	usleep(200 * 1000);


	for(i = 0; i < 5; i++)
	{
		curFlash[0] =  flashCol[0]; curFlash[1] = flashCol[1]; curFlash[2] = flashCol[2];

		for(j = 0; j <  25; j++)
		{
			boblight_addpixel(boblight, -1, curFlash);
			
			if (!boblight_sendrgb(boblight, 1, NULL)) //some error happened, probably connection broken, so bitch and try again
      			{
        			PrintError(boblight_geterror(boblight));
        			boblight_destroy(boblight);
        			continue;
      			}

			curFlash[0] -= flashCol[0] / 25;
			curFlash[1] -= flashCol[1] / 25;
			curFlash[2] -= flashCol[2] / 25;
			usleep(20 * 1000);
			
		}

		usleep(500 * 1000);
	}

	return(0);
	

	


    }
    //keep checking the connection to boblightd every 10 seconds, if it breaks we try to connect again
    while(!stop)
    {
      if (!boblight_ping(boblight, NULL))
      {
        PrintError(boblight_geterror(boblight));
        break;
      }
      sleep(10);
    }

    boblight_destroy(boblight);
  }

  cout << "Exiting\n";
  
  return 0;
}

void SignalHandler(int signum)
{
  if (signum == SIGTERM)
  {
    cout << "caught SIGTERM\n";
    stop = true;
  }
  else if (signum == SIGINT)
  {
    cout << "caught SIGINT\n";
    stop = true;
  }
}
