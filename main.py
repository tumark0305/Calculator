from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from page import GUI_frame, ADDICTIONAL_COL, lable_hight, RC_filter_model


class TestApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.opened = {}   # kind -> Popup
        btn1 = Button(text="Option A")
        btn2 = Button(text="Option B")
        btn3 = Button(text="Option C")

        btn1.bind(on_press=partial(self.open_window, "A"))
        btn2.bind(on_press=partial(self.open_window, "B"))
        btn3.bind(on_press=partial(self.open_window, "C"))

        root.add_widget(btn1)
        root.add_widget(btn2)
        root.add_widget(btn3)

        self.model = RC_filter_model()
        return root
    def open_window(self, kind, *_):
        if kind in self.opened:
            return

        panel = GUI_frame(
            f"RC_filter-{kind}",
            self.model.variables,
            self.model.units,
            self.model.functions
        )

        pop = Popup(
            title=f"RC_filter ({kind})",
            content=panel,
            size_hint=(None, None),
            size=(600, lable_hight * (len(self.model.variables) + ADDICTIONAL_COL)),
            auto_dismiss=False
        )
        panel.close_btn.bind(on_press=partial(self.close_popup, kind, pop, panel))
        pop.bind(on_dismiss=partial(self._on_popup_dismissed, kind, pop, panel))
        self.opened[kind] = pop
        pop.open()

    def close_popup(self, kind, pop, panel, *_):
        pop.dismiss()

    def _on_popup_dismissed(self, kind, pop, panel, *_):
        try:
            panel.delete()
        except Exception:
            pass
        if self.opened.get(kind) is pop:
            del self.opened[kind]


if __name__ == "__main__":
    TestApp().run()