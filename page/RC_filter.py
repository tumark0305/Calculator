import math
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from PIL import Image as PILImage
from io import BytesIO
class RC_filter_model:
    def __init__(self,_do_gen_image:bool):
        self.do_gen_image = _do_gen_image
        self.title = "RC_filter"
        self.variables = ['R','C','freq']
        self.units = ['ohm','F','Hz']
        self.formula = r"$f(x)=\frac{\sin x}{1+x^2}$"
        self.functions = self.func()
        if self.do_gen_image:
            self.image, self.image_size = self.__gen_graph_rgba()
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
    def __gen_graph_rgba(self, target_h=80):
        # 先用較高 dpi 生成，裁切後再縮放到固定高度，品質更好
        fig = plt.figure(figsize=(6, 1.2), dpi=200)
        fig.text(0.01, 0.3, self.formula, fontsize=24, va="center", color="white")
        plt.axis("off")

        buf = BytesIO()
        fig.savefig(
            buf, format="png", transparent=True,
            bbox_inches="tight", pad_inches=0.05
        )
        plt.close(fig)

        buf.seek(0)
        img = PILImage.open(buf).convert("RGBA")
        buf.close()

        # 固定高度 target_h，寬度等比例
        w, h = img.size
        if h <= 0:
            raise ValueError("Rendered image height is 0")

        new_w = max(1, int(round(w * (target_h / h))))
        img = img.resize((new_w, target_h), resample=PILImage.LANCZOS)

        return img.tobytes(), img.size





