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
    def __init__(self,_name,_input,_exp):
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
        self.data = ""
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
        param_frame.everything[_update_id]._internal_set = True
        param_frame.everything[_update_id].input_box.text ="output"
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
        def __init__(self,_name="param0",_input="0",_exp="Empty"):
            super().__init__(_name,_input,_exp)
    def __init__(self,**kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.display_label = Label(
            text="update now",
            size_hint_y=None,
            height=lable_hight
        )

        close_btn = Button(text="Exit",
            size_hint_y=None,
            height=lable_hight)
        param0 = self.param_manager("param0","0","Empty")
        param1 = self.param_manager("param1","1","Empty")
        param2 = self.param_manager("param2","2","Empty")
        param3 = self.param_manager("param3","3","Empty")
        self.add_widget(self.display_label)
        self.add_widget(param0.row)
        self.add_widget(param1.row)
        self.add_widget(param2.row)
        self.add_widget(param3.row)
        self.add_widget(close_btn)
        self.close_btn = close_btn


class TestApp(App):
    def build(self):
        root = BoxLayout(padding=10)
        btn = Button(text="Open Param Window")
        btn.bind(on_press=self.open_param_window)
        root.add_widget(btn)
        return root
    def open_param_window(self, *_):
        panel = GUI_frame()
        pop = Popup(
            title="Parameters",
            content=panel,
            size_hint=(None, None),
            size=(400, lable_hight*(total_col+ADDICTIONAL_COL)),
            auto_dismiss=False
        )
        panel.close_btn.bind(on_press=lambda *_: pop.dismiss())
        pop.open()

    open_param_window = open_param_window

if __name__ == "__main__":
    TestApp().run()