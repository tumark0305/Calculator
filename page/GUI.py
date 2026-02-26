from kivy.core.window import Window

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
lable_hight = 40
total_col = 4
ADDICTIONAL_COL = 6
Window.size = (400, lable_hight*(total_col+ADDICTIONAL_COL))

class param_frame:
    counter = 0
    update_order =[]
    everything = []
    ALL_EXP = [("G",1e9),("M",1e6),("k",1e3),("Empty",1.0),("m",1e-3),("u",1e-6),("n",1e-9),("p",1e-12),("f",1e-15)]
    def __init__(self,_name,_input,_exp,_func):
        self.id = param_frame.counter
        param_frame.everything.append(self)
        param_frame.counter += 1
        param_frame.update_order = list(range(param_frame.counter))
        self.row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=lable_hight  
        )
        self.func = _func
        self.data = _input
        self.exp = 0
        self.label = Label(text=_name, size_hint_x=0.3)
        self.input_box = LabelLikeInput(text=_input)
        self.input_box.bind(text=self.update)
        self.spinner = Spinner(
            text=_exp,                         # 預設顯示
            values=[_name for _name,_y in self.ALL_EXP],    # 選項
            size_hint_x=0.4,
            option_cls=lambda **kw: Button(size_hint_y=None, height=lable_hight, **kw)
        )
        self.spinner.bind(text=self.on_select)
        self.row.add_widget(self.label)
        self.row.add_widget(self.input_box)
        self.row.add_widget(self.spinner)
        self._internal_set = False
    def on_select(self, instance, _selected_value):
        _selected_id = [_name for _name,_y in self.ALL_EXP].index(_selected_value)
        self.exp = self.ALL_EXP[_selected_id]
    def update(self , instance ,value):
        if getattr(self, "_internal_set", False):
            return
        param_frame.update_order = self.reordering()
        self.data = value
        _update_id = param_frame.update_order.index(param_frame.counter - 1)
        _unpack = []
        for _x in range(len(param_frame.update_order)):
            if _x != _update_id:
                _unpack.append(param_frame.everything[_x].data)
        _output = str(self.func(_unpack))
        param_frame.everything[_update_id]._internal_set = True
        param_frame.everything[_update_id].input_box.text =_output
        param_frame.everything[_update_id]._internal_set = False

    def reordering(self):
        _output = [_x + 1 for _x in param_frame.update_order]
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


class GUI_frame(BoxLayout):
    class param_manager(param_frame):
        def __init__(self,_name,_input,_exp,_func):
            super().__init__(_name,_input,_exp,_func)
    def __init__(self,_functions,**kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.functions = _functions
        self.display_label = Label(
            text="update now",
            size_hint_y=None,
            height=lable_hight
        )

        close_btn = Button(text="Exit",
            size_hint_y=None,
            height=lable_hight)
        params = []
        params.append(self.param_manager("param0","0","Empty",self.functions[0]))
        params.append(self.param_manager("param1","1","Empty",self.functions[1]))
        params.append(self.param_manager("param2","2","Empty",self.functions[2]))
        params.append(self.param_manager("param3","3","Empty",self.functions[3]))
        if len(params) != total_col:
            raise BufferError("params != total_col !")
        self.add_widget(self.display_label)
        [self.add_widget(_x.row) for _x in params]
        self.add_widget(close_btn)
        self.close_btn = close_btn

def test_calculator():
    def add(_data_pack):#str in and out
        _data  = []
        for _x in _data_pack:
            try:
                _data.append(float(_x))
            except Exception as e:
                return e
        x,y,z = _data
        return str(x+y+z)
    _output = []
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
        return root
    def open_param_window(self, *_):
        panel = GUI_frame(test_calculator())
        pop = Popup(
            title="Parameters",
            content=panel,
            size_hint=(None, None),
            size=(400, lable_hight*(total_col+ADDICTIONAL_COL)),
            auto_dismiss=False
        )
        panel.close_btn.bind(on_press=lambda *_: pop.dismiss())
        pop.open()


if __name__ == "__main__":
    TestApp().run()