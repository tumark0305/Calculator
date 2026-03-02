import math

class RLC_series_resnoate_model:
    def __init__(self):
        self.title = "RLC_series_resnoate"
        self.variables = ['R','L','C','freq','Q','damping']
        self.units = ['ohm','H','F','Hz','','']
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
    def R_eq(_data_pack,_exp):
        _data  = []
        for _x in _data_pack:
            try:
                _data.append(float(_x))
            except Exception as e:
                return str(e)
        try:
            L,C,f,Q,d = _data
            outcome = 1/Q * math.sqrt(L/C)
            return str((outcome)/_exp)
        except Exception as e:
            return str(e)