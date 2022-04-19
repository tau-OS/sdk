from ctypes import Union
from dataclasses import dataclass
from pyclbr import Function
from typing import Any
from gi.repository import GObject
import re
from deepdiff import DeepDiff


def clean_identifier(varStr):
    return re.sub(r"\W+|^(?=\d)", "_", varStr)


class VDOMNode:
    def __init__(self, tag, attrs, children):
        self.tag = tag
        self.attrs = attrs
        self.children = children


@dataclass
class VDOMNode:
    widget: Any
    props: dict[str, Any]
    signals: dict[str, Function]
    children: list[VDOMNode]


def to_vdom_constructor(gtk_widget):
    props = dict(
        map(
            lambda x: (clean_identifier(x.name), x.name),
            gtk_widget.list_properties(),
        )
    )

    signals = dict(
        map(
            lambda x: ("on_" + clean_identifier(x), x),
            GObject.signal_list_names(gtk_widget),
        )
    )

    def constructor(*args, **kargs):
        mapped_props = dict(
            map(
                lambda x: (props[x[0]], x[1]),
                filter(lambda x: x[0] in props, kargs.items()),
            )
        )

        mapped_signals = dict(
            map(
                lambda x: (signals[x[0]], x[1]),
                filter(lambda x: x[0] in signals, kargs.items()),
            )
        )

        return VDOMNode(
            widget=gtk_widget,
            props=mapped_props,
            signals=mapped_signals,
            children=list(args),
        )

    return constructor
