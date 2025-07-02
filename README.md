# libls

library containing functions for the lizardscanner project


## helper

some helpful functions

### get_logger()
logger with custom format

arguments
- name: name to be displayed
- debug: show debug messages
- time: show timestamps

```
>>> from libls.logger import getLogger
>>> l = getLogger(name="someName", debug=True, time=False)
>>> l.info("some info")
[  someName:I:       <module>] some info
```

