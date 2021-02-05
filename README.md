Timeout After (X Seconds)
===========================
A signal free, multi-threading safe, method of setting A mid-function Timeout
---------------------------------------------------------------------------

In an effort to find a non-blocking, minimally intrusive, replacement for the [signal method](https://www.jujens.eu/posts/en/2018/Jun/02/python-timeout-function/) of making a mid-function timeout, I stumbled upon this "Nasty hack" posted by [liuw on GitHub](https://gist.github.com/liuw/2407154), which allowed me to actual do what I originally though was impossible.

As LIU points out, this is a NASTY hack and is only possible by breaking the C level interpreter to allow this to happen. This can be a point of concern and my be fixed in the future, but as for now it seems safe to use with the current version of python 3 (Tested on 3.6.5 - 3.8.0)

And if I haven’t stressed this enough, I (we) take no responsibility for the use of this exploit, use at your own risk.


References
----------
  - https://gist.github.com/liuw/2407154 (Nasty Hack)
  - https://www.jujens.eu/posts/en/2018/Jun/02/python-timeout-function/ (Code Style Inspiration)


Example Usage
-------------

```python
import timeout_after

def test_me():
	try:
		with TimeoutAfter(timeout=3, exception=TimeoutError):
			for x in range(0, 6):
				print('Tick {}'.format(x + 1))
				time.sleep(1)
		print("I don't say anything...")
	except TimeoutError:
		print('Looks like we ran out of ticks...')

thread = threading.Thread(target = test_me)
thread.start()
thread.join()
```
