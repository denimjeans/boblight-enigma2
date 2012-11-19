/*
 * grabber-enigma2
 * Copyright (C) Martijn Vos and c@presser 2012
 *
 * parts of this code were taken from
 * - aiograb		(http://schwerkraft.elitedvb.net/projects/aio-grab/)
 * - boblight-X11	
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

#ifndef GRABBER
#define GRABBER

#include <string>

#include "config.h"
#include "util/timer.h"
#include "util/mutex.h"

#define CLAMP(x)    ((x < 0) ? 0 : ((x > 255) ? 255 : x))
#define SWAP(x,y)	{ x ^= y; y ^= x; x ^= y; }
#define CLIP(x)     ((x < 0) ? 1 : ((x > 250) ? 250 : x))

#define RED565(x)    ((((x) >> (11 )) & 0x1f) << 3)
#define GREEN565(x)  ((((x) >> (5 )) & 0x3f) << 2)
#define BLUE565(x)   ((((x) >> (0)) & 0x1f) << 3)

#define YFB(x)    ((((x) >> (10)) & 0x3f) << 2)
#define CBFB(x)  ((((x) >> (6)) & 0xf) << 4)
#define CRFB(x)   ((((x) >> (2)) & 0xf) << 4)
#define BFFB(x)   ((((x) >> (0)) & 0x3) << 6)

// dont change SPARE_RAM and DMA_BLOCKSIZE until you really know what you are doing !!!
#define SPARE_RAM 252*1024*1024 // the last 4 MB is enough...
#define DMA_BLOCKSIZE 0x3FF000 // should be big enough to hold a complete YUV 1920x1080 HD picture, otherwise it will not work properly on DM8000

// STB-Types
#define UNKNOWN     0
#define PALLAS      0
#define VULCAN      0
#define XILLEON     0
#define BRCM7401    1
#define BRCM7400    2
#define BRCM7405    3
#define BRCM7335    4
#define BRCM7358    5
#define BRCM7356    6
#define BRCM7325    7

// for writing BMP files
#define PUT32(x) hdr[i++] = ((x)&0xFF); hdr[i++] = (((x)>>8)&0xFF); hdr[i++] = (((x)>>16)&0xFF); hdr[i++] = (((x)>>24)&0xFF);
#define PUT16(x) hdr[i++] = ((x)&0xFF); hdr[i++] = (((x)>>8)&0xFF);
#define PUT8(x) hdr[i++] = ((x)&0xFF);

class CGrabber
{
  public:
    CGrabber(void* boblight, volatile bool& stop, bool sync);
    ~CGrabber();

    std::string& GetError()           { return m_error; }        //retrieves the latest error
    
    void SetInterval(double interval) { m_interval = interval; } //sets interval, negative means vblanks
    void SetSize(int size)            { m_size = size; }         //sets how many pixels we want to grab maximum
    void SetDebug(bool debug)         { m_debug = debug; }       //sets debug mode
    void SetPicdump(bool picdump)     { m_picdump = picdump; }   //sets picdump mode
    void SetBlackbar(bool blackbar)   { m_blackbar = blackbar; } //sets blackbar mode to enabled
    void SetTimeshift(int timeshifts)   { m_timeshift = timeshifts; } // For testing
    
    bool Setup();                                                //base setup function
    bool Run();                       				             //main run function
    
  protected:
    
        
    //
    // Buffer
    //
    unsigned long** create_2D_char_array( int numrows, int numcols);
    void             DeletePixelData();
    void             ResetPixelData();
    int              numCols;
    int              numRows;
    unsigned long** rgbBuffer;
    unsigned char   pointer;
    unsigned char   timeshift;
    int cycle_save;
    int cycles;
    int delay;
    int cyclecount;
    
    //
    // helper functions. taken from aiograb
    //
    const char 	*file_getline(const char *filename);
    int 		    file_scanf_line(const char *filename, const char *fmt, ...);
    int 		    file_scanf_lines(const char *filename, const char *fmt, ...);

    //
    // detect the Type of the Box
    //
    bool            detectSTB();
    int             stb_type;

    //
    // the actual grabber
    //
    bool            grabVideo();
    
    int             mem_fd;			        // handle to the memory
    bool            blank;			        // blank signal bool 
    int             blank_count;
    int             chr_luma_stride;
    int             xres_orig, yres_orig;	// original resolution
    int             xres, yres;		        // final resolution
    int             xres_old, yres_old;	    // stored to detect resolution changes
    int             skiplines;		        // downscale-factor (power of two)
    unsigned char  *luma, *chroma;         // buffer for chroma and luma data  
    unsigned char  *video;			        // buffer for RGB-Data
    
    //fps
    long double     m_lastupdate;
    long double     m_lastmeasurement;
    long double     m_measurements;
    int              m_nrmeasurements;
    long double     m_fps;
    
    //
    // Blackbar detecttion
    //
    void        CalcBeamTop();
    int         y_,v_,v__,x_,sb_old,blackbars_y,sb_end,yres_new,beamcount,top_lines,bottom_lines,save_bottom,save_top,save_total;
    
    //
    // convert the video from YUV to RGB
    //
    bool        convertVideo();
    int         getPixel(int xpos, int ypos);
    int         filename_count;
    bool        sb_toggle;
    int         m_skipper_h;
    
    // save grabbed image as PNG
    bool        SaveBMP();
    int         filename_counter;
    
    // Timer
    double           	m_interval;                                //interval in seconds, or negative for vblanks
    CTimer            	m_timer;                                   //our timer

    volatile bool& 	m_stop;

    std::string       	m_error;                                   //latest error
    
    void*             	m_boblight;                                //our handle from libboblight
    
    int               	m_size;                                    //nr of pixels on lines to grab

    bool              	m_debug;                                   //if we have debug mode on
    bool              	m_picdump;                                 //if we have picdump mode on
    bool                m_blackbar;                                //blackbar mde
    int                 m_timeshift;
    
    void              	UpdateDebugFps();                          
    int64_t 		    fps_now, fps_lastupdate;
    int		            fps_framecount;
    
    bool              	m_sync;                                    //sync mode for libboblight
};

#endif //GRABBER
