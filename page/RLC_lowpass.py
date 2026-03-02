import math

class RLC_lowpass_model:
    def __init__(self):
        self.title = "RLC_lowpass"
        self.variables = ['R','C','freq']
        self.units = ['ohm','F','Hz']
        self.functions = self.func()
    def func(self):
        def add(_data_pack,_exp):#str in and out
            _data  = []
            for _x in _data_pack:
                try:
                    _data.append(float(_x))
                except Exception as e:
                    return str(e)
            try:
                x,y = _data
                outcome = 1/(2*math.pi*x*y)
                return str((outcome)/_exp)
            except Exception as e:
                return str(e)
        _output = []
        _output.append(add)
        _output.append(add)
        _output.append(add)
        return _output