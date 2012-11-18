#ifndef CTHREAD
#define CTHREAD

#include "../util/inclstdint.h"

#include <pthread.h>
#include <unistd.h>

class CThread
{
  public:
    CThread();
    ~CThread();
    void StartThread();
    void StopThread();
    void AsyncStopThread();
    void JoinThread();
    bool IsRunning();

  protected:
    pthread_t     m_thread;
    volatile bool m_stop;
    volatile bool m_running;

    static void* ThreadFunction_RgbToDevice(void* args);
    virtual void Process_RgbToDevice();
};

#endif //CTHREAD

