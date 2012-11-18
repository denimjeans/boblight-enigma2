dnl Process this file with autoconf to produce a configure script.

AC_INIT(boblight, 2.0)

AM_INIT_AUTOMAKE(AC_PACKAGE_NAME, AC_PACKAGE_VERSION)
AC_CONFIG_HEADERS([config.h])
AM_MAINTAINER_MODE

AC_ISC_POSIX
AC_PROG_CXX
AM_PROG_CC_STDC
AC_HEADER_STDC

AM_PROG_LIBTOOL

dnl all use this
AC_CHECK_LIB(pthread,[main])
AC_CHECK_LIB(rt,[main])
AC_CHECK_LIB(m,[main])
AC_CHECK_LIB(dl,[main])
AC_CHECK_LIB(stdc++,[main])
AC_CHECK_LIB(usb-1.0,[main])

AC_CHECK_DECL([clock_gettime], AC_DEFINE([HAVE_CLOCK_GETTIME], [1], [ ]), [], [[#include <time.h>]])


dnl boblightd
AC_CHECK_HEADERS([pthread.h])

dnl boblight-enigma2

AC_OUTPUT([
Makefile
src/Makefile
])
