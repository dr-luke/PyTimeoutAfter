#!/usr/bin/env python3
import threading, time, ctypes

'''
-----------------------------------------------------------------------
Copyright (c) 2021 Levi M. Luke, LIU Wei, Brett Husar, and others
-----------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

class TimeoutAfter():
	def __init__(self, timeout=(10), exception=TimeoutError):
		self._exception = exception
		self._caller_thread = threading.current_thread()
		self._timeout = timeout
		self._timer = threading.Timer(self._timeout, self.raise_caller)
		self._timer.daemon = True
		self._timer.start()

	def __enter__(self):
		try:
			yield
		finally:
			self._timer.cancel()
		return self

	def __exit__(self, type, value, traceback):
		self._timer.cancel()
		
	def raise_caller(self):
		ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._caller_thread._ident), ctypes.py_object(self._exception))
		if ret == 0:
			raise ValueError("Invalid thread ID")
		elif ret > 1:
			ctypes.pythonapi.PyThreadState_SetAsyncExc(self._caller_thread._ident, NULL)
			raise SystemError("PyThreadState_SetAsyncExc failed")
