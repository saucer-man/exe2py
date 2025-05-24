# exe2py

对于pyinstaller打包成的可执行文件，可以一键反编译成py文件

```buildoutcfg
python exe2py.py index.exe
```

其中

- exe -> pyc 来自 [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor)
- pyc -> py 来自 [uncompyle6](https://github.com/rocky/python-uncompyle6)

备注：
python版本和exe对应的python版本版本要对应

# exe2py_v2

使用大模型来实现`pyc -> py`，兼容性更好
