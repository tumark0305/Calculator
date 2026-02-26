
from page.GUI import GUI_frame,ADDICTIONAL_COL,lable_hight

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class test_model:
    def __init__(self):
        self.variables = ['R','C','freq']
        self.units = ['ohm','F','Hz']
        self.functions = self.func()
    def func(self):
        def add(_data_pack):#str in and out
            _data  = []
            for _x in _data_pack:
                try:
                    _data.append(float(_x))
                except Exception as e:
                    return e
            w,x = _data
            return str(w+x)
        _output = []
        _output.append(add)
        _output.append(add)
        _output.append(add)
        return _output
class TestApp(App):
    
    def build(self):
        root = BoxLayout(padding=10)
        btn = Button(text="RC_filter")
        btn.bind(on_press=self.open_param_window)
        root.add_widget(btn)
        self.model = test_model()
        return root
    def open_param_window(self, *_):
        panel = GUI_frame("RC_filter",self.model.variables,self.model.units,self.model.functions)
        pop = Popup(
            title="RC_filter",
            content=panel,
            size_hint=(None, None),
            size=(500, lable_hight*(len(self.model.variables)+ADDICTIONAL_COL)),
            auto_dismiss=False
        )
        panel.close_btn.bind(on_press=lambda *_: pop.dismiss())
        pop.open()


if __name__ == "__main__":
    TestApp().run()




