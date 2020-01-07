from typing import Union

from IPython.display import Markdown, display
from pyomeca import Analogs3d, Markers3d


def print_md(string: str):
    display(Markdown(string))


def color_md(string: str, color: str = None):
    return f"<span style='color:{color}'>{string}</span>"


def describe_data(data: Union[Markers3d, Analogs3d]):
    default_color = "firebrick"

    def section_str(s: str):
        return f"__{color_md(s.title(), default_color)}__"

    print_md(f"{section_str('shape')}: {data.shape}")
    print_md(f"{section_str('rate')}: {data.get_rate}")
    print_md(f"{section_str('labels')}:")
    print(data.get_labels)

    print_md(f"{section_str('time frames')}:")
    print(data.get_time_frames)

    print_md(f"{section_str('first frame')}:")
    print(data[..., 0])
