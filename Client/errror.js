Exception in thread Thread-2:
Traceback (most recent call last):
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/threading.py", line 916, in _bootstrap_inner
self.run()
File "./server2.py", line 66, in run
data = json.loads(data)
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/json/__init__.py", line 354, in loads
return _default_decoder.decode(s)
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/json/decoder.py", line 339, in decode
obj, end = self.raw_decode(s, idx=_w(s, 0).end())
File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/json/decoder.py", line 357, in raw_decode
raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
