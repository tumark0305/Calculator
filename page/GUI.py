from kivy.core.window import Window

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import os
lable_hight = 40
ADDICTIONAL_COL = 7
total_col = 4
Window.size = (450, lable_hight*(total_col+ADDICTIONAL_COL))
ALL_EXP = [("G",1e9),("M",1e6),("k",1e3),("Empty",1.0),("m",1e-3),("u",1e-6),("n",1e-9),("p",1e-12),("f",1e-15)]

class Cache_frame:
    default_location = f"{os.getcwd()}/Cache"
    def __init__(self , _popup_id , _proc_name):
        self.popup_id = _popup_id
        self.proc_name = _proc_name
        self.location = self.default_location+"/"+self.proc_name
        self.file_path = f"{self.location}/{self.proc_name}_log.txt"
        os.makedirs(self.location,exist_ok=True)
        if not os.path.isfile(self.file_path):
            _f = open(self.file_path,"a")
            _f.close()
    def load(self):
        _f = open(self.file_path,"r")
        _data = _f.read()
        _f.close()
        if _data=='':
            _split_data = None
        else:
            try:
                _split_data = [_x.split('*') for _x in _data.split('\n')]
            except Exception as e:
                _split_data = None
        return _split_data
    def save(self,_mapping):
        _current_map = _mapping[self.popup_id]
        _exp_reference = [_y for _name,_y in ALL_EXP]
        _split_data = [[str(_x) for _x in _current_map[0].update_order[self.popup_id]]]
        for _x in _current_map:
            _input = _x.data
            _exp = ALL_EXP[_exp_reference.index(_x.exp)][0]
            _split_data.append([_input,_exp])
        _data = "\n".join(["*".join(_x) for _x in _split_data])
        _f = open(self.file_path,"w")
        _f.write(_data)
        _f.close()
        return None
class param_frame:
    counter = [0]
    update_order =[[]]
    everything = [[]]
    
    def __init__(self,_popup_id,_name,_input,_exp,_unit,_func,_cache:Cache_frame):
        self.popup_id = _popup_id
        if self.popup_id + 1 > len(param_frame.counter):
            param_frame.counter.append(0)
        if self.popup_id + 1 > len(param_frame.everything):
            param_frame.everything.append([])
        if self.popup_id + 1 > len(param_frame.update_order):
            param_frame.update_order.append([])
        self.id = param_frame.counter[self.popup_id]
        param_frame.everything[self.popup_id].append(self)
        param_frame.counter[self.popup_id] += 1
        param_frame.update_order[self.popup_id] = list(range(param_frame.counter[self.popup_id]))
        self.row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=lable_hight  
        )
        self.cache = _cache
        self.func = _func
        self.data = _input
        self.exp = ALL_EXP[[_name for _name,_y in ALL_EXP].index(_exp)][1]
        self.error = False
        self.label = Label(text=_name, size_hint_x=0.3)
        self.input_box = LabelLikeInput(text=_input)
        self.input_box.bind(text=self.update)
        self.spinner = Spinner(
            text=_exp,                         # 預設顯示
            values=[_name for _name,_y in ALL_EXP],    # 選項
            size_hint_x=0.4,
            option_cls=lambda **kw: Button(size_hint_y=None, height=lable_hight, **kw)
        )
        self.spinner.bind(text=self.on_select)
        self.unit = Label(text=_unit, size_hint_x=0.3)
        self.row.add_widget(self.label)
        self.row.add_widget(self.input_box)
        self.row.add_widget(self.spinner)
        self.row.add_widget(self.unit)
        self._internal_set = False
        
    def on_select(self, instance, _selected_value):
        if getattr(self, "_internal_set", False):
            return
        _selected_id = [_name for _name,_y in ALL_EXP].index(_selected_value)
        self.exp = ALL_EXP[_selected_id][1]
        _result = self.convert_cal_input()
        self.error = param_frame.__test_output_error(_result)
        if not self.error:
            self.cache.save(param_frame.everything)
    def convert_cal_input(self):
        _update_id = param_frame.update_order[self.popup_id].index(param_frame.counter[self.popup_id] - 1)
        _unpack = []
        for _x in range(len(param_frame.update_order[self.popup_id])):
            if _x != _update_id:
                _unpack.append(param_frame.everything[self.popup_id][_x].value())
        _output = self.func(_unpack,param_frame.everything[self.popup_id][_update_id].exp)
        
        param_frame.everything[self.popup_id][_update_id]._internal_set = True
        param_frame.everything[self.popup_id][_update_id].input_box.text =_output
        param_frame.everything[self.popup_id][_update_id].data =_output
        param_frame.everything[self.popup_id][_update_id].input_box.reset_scroll()
        param_frame.everything[self.popup_id][_update_id]._internal_set = False
        return _output
    def __test_output_error(_result_input):
        _output = False
        try:
            float(_output)
        except:
            _output = True
        return _output
    def update(self , instance ,value):
        if getattr(self, "_internal_set", False):
            return
        param_frame.update_order[self.popup_id] = self.reordering()
        self.data = value
        _result = self.convert_cal_input()
        self.error = param_frame.__test_output_error(_result)
        if not self.error:
            self.cache.save(param_frame.everything)
    def reordering(self):
        _output = [_x + 1 for _x in param_frame.update_order[self.popup_id]]
        _output[self.id] = 0
        _adj = [9 for _x in _output]
        for _i in range(len(_output)):
            if _i in _output:
                _adj[_output.index(_i)] = 0
            else:
                for _x in range(len(_adj)):
                    if _adj[_x] == 9:
                        _adj[_x]=-1
                break
        for _i in range(len(_adj)):
            _output[_i] += _adj[_i]
        return _output
    def value(self):
        try:
            _output = self.exp * float(self.data)
        except Exception as e:
            _output = str(e)
        return _output
    def delete(self):
        self.id = "deleted"
        param_frame.everything[self.popup_id].remove(self)
        param_frame.counter[self.popup_id] -= 1
        param_frame.update_order[self.popup_id] = list(range(param_frame.counter[self.popup_id]))
        return None
class LabelLikeInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.background_normal = ""
        self.background_active = ""
        self.background_color = (1,1,1,0.3)
        self.foreground_color = (1,1,1,1)
        self.size_hint_y = None
        self.height = lable_hight
    def reset_scroll(self, *args):
        self.scroll_x = 0
class GUI_frame(BoxLayout):
    counter = 0
    everything = []
    class Cache(Cache_frame):
        def __init__(self,_popup_id,_proc_name):
            super().__init__(_popup_id,_proc_name)
    class param_manager(param_frame):
        def __init__(self,_popup_id,_name,_input,_exp,_unit,_func,_cache):
            super().__init__(_popup_id,_name,_input,_exp,_unit,_func,_cache)
    def __init__(self,_func_name,_var_names,_var_units,_functions,**kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.popup_id = GUI_frame.counter
        GUI_frame.everything.append(self)
        GUI_frame.counter += 1
        self.var_names = _var_names
        self.var_units = _var_units
        self.cache = self.Cache(self.popup_id,_func_name)
        self.functions = _functions
        self.display_label = Label(
            text=_func_name,
            size_hint_y=None,
            height=lable_hight
        )
        _close_btn = Button(text="Exit",
            size_hint_y=None,
            height=lable_hight)
        self.params = []
        _load_data = self.cache.load()
        if _load_data is None:
            for _x in range(len(self.var_names)):
                self.params.append(self.param_manager(self.popup_id,self.var_names[_x],"0","Empty",self.var_units[_x],self.functions[_x],self.cache))
        else:
            _lastime_value = _load_data[1:]
            _load_order = [int(_x) for _x in _load_data[0]]
            for _x in range(len(self.var_names)):
                _new = self.param_manager(self.popup_id,self.var_names[_x],_lastime_value[_x][0],_lastime_value[_x][1],self.var_units[_x],self.functions[_x],self.cache)
                self.params.append(_new)
                _new.update_order[self.popup_id] = _load_order
            _new.convert_cal_input()
        self.add_widget(self.display_label)
        [self.add_widget(_x.row) for _x in self.params]
        self.add_widget(self.playback_row())
        self.add_widget(_close_btn)
        self.close_btn = _close_btn
    def delete(self):
        [_x.delete() for _x in self.params]
        self.popup_id = "deleted"
        GUI_frame.everything.remove(self)
        return None
    def playback_row(self):
        _row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=lable_hight  
        )
        _left_btn = Button(text="<--",
            size_hint_y=None,
            height=lable_hight)
        _right_btn = Button(text="-->",
            size_hint_y=None,
            height=lable_hight)
        _row.add_widget(_left_btn)
        _row.add_widget(_right_btn)
        return _row
class test_model:
    def __init__(self):
        self.variables = ['Va','Vb','Vc','Vd','Ve']
        self.units = ['a','b','c','d','e']
        self.functions = self.func()
    def func(self):
        def add(_data_pack,_exp):#str in and out
            _data  = []
            for _x in _data_pack:
                try:
                    _data.append(float(_x))
                except Exception as e:
                    return e
            w,x,y,z = _data
            return str((w+x+y+z)/_exp)
        _output = []
        _output.append(add)
        _output.append(add)
        _output.append(add)
        _output.append(add)
        _output.append(add)
        return _output
class TestApp(App):
    
    def build(self):
        root = BoxLayout(padding=10)
        btn = Button(text="Open Param Window")
        btn.bind(on_press=self.open_param_window)
        root.add_widget(btn)
        self.model = test_model()
        return root
    def open_param_window(self, *_):
        self.panel = GUI_frame("Parameters",self.model.variables,self.model.units,self.model.functions)
        self.pop = Popup(
            title="Parameters",
            content=self.panel,
            size_hint=(None, None),
            size=(600, lable_hight*(len(self.model.variables)+ADDICTIONAL_COL)),
            auto_dismiss=False
        )
        self.panel.close_btn.bind(on_press=lambda *_: self.close_popup())
        self.pop.open()
    def close_popup(self, *_):
        self.pop.dismiss()
        self.panel.delete()
        



if __name__ == "__main__":
    TestApp().run()