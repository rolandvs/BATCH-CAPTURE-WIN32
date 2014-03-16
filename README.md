BATCH-CAPTURE-WIN32
===================

BATCH CAPTURE FOR WINDOWS


The Windows Version of the Batch-Capture program is written using C++ Visual Studio Express 2010.

The process is the same as the original Batch-Capture with the exception that there is no shell command to provide the configuration. A text file is used to configure the cycle (batch) capture.

The serial capture is still using Python with PYSERIAL. The version posted here does not forward the serial to a tcp socket.

The PCL6.exe binary must be used for printing to pdf. There is a binary version available for download from this site:

http://dl.dropbox.com/u/271144/GhostPCL-W32-Binaries.zip

The PCL6.exe can be saved in the same folder as the compiled Batch-Capture application.

No installation is needed for any executables. All the applications have successfully run on Win XP (Serv. Pack 3) and up.
