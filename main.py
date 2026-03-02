from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from page import GUI_frame, ADDICTIONAL_COL, lable_hight, RC_filter_model,RLC_series_resnoate_model,RLC_highpass_model,RLC_lowpass_model


class TestApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.opened = {}   # kind -> Popup
        _all_calualotor = [RC_filter_model(),RLC_lowpass_model(),RLC_highpass_model()]

        [root.add_widget(self.new_button(_calualotor)) for _calualotor in _all_calualotor]
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
    def new_button(self,_model):
        _output = Button(text=_model.title)
        _output.bind(on_press=partial(self.new_window, _model))
        return _output
    def new_window(self, _model , *_):
        if _model in self.opened:
            return

        panel = GUI_frame(
            _model.title,
            _model.variables,
            _model.units,
            _model.functions
        )

        pop = Popup(
            title=_model.title,
            content=panel,
            size_hint=(None, None),
            size=(600, lable_hight * (len(_model.variables) + ADDICTIONAL_COL)),
            auto_dismiss=False
        )
        panel.close_btn.bind(on_press=partial(self.close_popup, _model, pop, panel))
        pop.bind(on_dismiss=partial(self._on_popup_dismissed, _model, pop, panel))
        self.opened[_model] = pop
        pop.open()
    def close_popup(self, _model, pop, panel, *_):
        pop.dismiss()
    def _on_popup_dismissed(self, _model, pop, panel, *_):
        try:
            panel.delete()
        except Exception:
            pass
        if self.opened.get(_model) is pop:
            del self.opened[_model]


if __name__ == "__main__":
    TestApp().run()