from kivy.core.window import Window

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
lable_hight = 40
total_col = 7
Window.size = (300, lable_hight*total_col)

class param_frame:
    counter = 0
    data = []
    update_order =[]
    everything = []
    def __init__(self,_name):
        self.id = param_frame.counter
        param_frame.everything.append(self)
        param_frame.counter += 1
        param_frame.data = list(range(param_frame.counter))
        param_frame.update_order = list(range(param_frame.counter))
        self.row = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=lable_hight  
        )
        self.label = Label(text=_name, size_hint_x=0.3)
        self.input_box = LabelLikeInput(text="input here")
        self.input_box.bind(text=self.update)
        self.row.add_widget(self.label)
        self.row.add_widget(self.input_box)
    def update(self , instance ,value):
        param_frame.update_order = [_x + 1 for _x in param_frame.update_order]
        param_frame.update_order[self.id] = 0
        param_frame.data[self.id] = value
        print(f"id={self.id}")

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


class DemoApp(App):
    class param_manager(param_frame):
        def __init__(self,_name="param0"):
            super().__init__(_name)
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.display_label = Label(
            text="update now",
            size_hint_y=None,
            height=lable_hight
        )

        btn = Button(text="Exit",
            size_hint_y=None,
            height=lable_hight)
        btn.bind(on_press=self.close_app)
        param0 = self.param_manager("param0")
        param1 = self.param_manager("param1")
        param2 = self.param_manager("param2")
        param3 = self.param_manager("param3")
        root.add_widget(self.display_label)
        root.add_widget(param0.row)
        root.add_widget(param1.row)
        root.add_widget(param2.row)
        root.add_widget(param3.row)
        root.add_widget(btn)
        return root

    
    def close_app(self, _):
        self.stop()   # ⭐ 關閉整個程式


if __name__ == "__main__":
    DemoApp().run()