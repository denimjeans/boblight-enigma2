#include "thread.h"

CThread::CThread()
{
  m_thread = NULL;
  m_running = false;
}

CThread::~CThread()
{
  StopThread();
}

void CThread::StartThread()
{
  m_stop = false;
  m_running = true;
  pthread_create(&m_thread, 0, ThreadFunction_RgbToDevice, reinterpret_cast<void*>(this));
}

void* CThread::ThreadFunction_RgbToDevice(void* args)
{
  CThread* thread = reinterpret_cast<CThread*>(args);
  thread->Process_RgbToDevice();
  thread->m_running = false;
}

void CThread::Process_RgbToDevice()
{
}

void CThread::StopThread()
{
  AsyncStopThread();
  JoinThread();
}

void CThread::AsyncStopThread()
{
  m_stop = true;
}

void CThread::JoinThread()
{
  if (m_thread)
  {
    pthread_join(m_thread, 0);
    m_thread = 0;
  }
}

bool CThread::IsRunning()
{
  return m_running;
}

