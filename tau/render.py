from tau.vdom import VDOMNode

# from gi.repository import GObject


def render_naive(node: VDOMNode):
    widget = node.widget()

    for key in node.props:
        widget.set_property(key, node.props[key])

    for key in node.signals:
        widget.connect(key, node.signals[key])

    if len(node.children) == 0:
        pass
    elif len(node.children) == 1:
        if hasattr(widget, "append"):
            widget.append(render_naive(node.children[0]))
        else:
            widget.set_child(render_naive(node.children[0]))
    else:
        for child in node.children:
            widget.append(render_naive(child))

    return widget


def render_diff(widget: any, old_node: VDOMNode, node: VDOMNode):
    if old_node.widget != node.widget:
        widget = node.widget()

    # Props
    for key in node.widget.list_properties():
        name = key.name
        if name in node.props and node.props[name] != widget.get_property(name):
            widget.set_property(name, node.props[name])
        elif (
            name not in node.props
            and old_node.widget == node.widget
            and name in old_node.props
        ):
            value = node.widget.get_default_value(name)
            widget.set_property(name, value.dup_object())

    # # Signals
    # for key in GObject.signal_list_names(node.widget):
    #     if key in node.signals and node.props[key] != widget.get_property(key):
    #         # TODO Clear signals
    #         # widget.disconnect(key + "")
    #         widget.connect(key, node.signals[key])
    #     elif (
    #         key not in node.props
    #         and old_node.widget == node.widget
    #         and key in old_node.props
    #     ):
    #         value = node.widget.get_default_value(key)
    #         widget.set_property(key, value.dup_object())

    # Add and update signals
    # for key in node.signals:
    #     if key in old_node.signals:
    #         if node.signals[key] != old_node.signals[key]:
    #             widget.disconnect_by_func(old_node.signals[key])
    #             widget.connect(key, node.signals[key])
    #     else:
    #         widget.connect(key, node.signals[key])

    # Remove signals
    # for key in old_node.signals:
    #     if key not in node.signals:
    #         widget.disconnect_by_func(old_node.signals[key])

    # TODO: Mount and unmount children
    # Add and update children

    # if len(node.children) == 0:
    #     if len(old_node.children) != 0:
    #         widget.set_child(None)
    # elif len(node.children) == 1:
    #     if old_node.children[0] != node.children[0]:
    #         if hasattr(widget, "append"):
    #             widget.append(render_naive(node.children[0]))
    #         else:
    #             widget.set_child(render_naive(node.children[0]))
    # else:
    #     # TODO: Smart diff array
    #     if old_node.children != node.children:
    #         for child in widget.get_children():
    #             widget.remove(child)
    #         for child in node.children:
    #             widget.append(render_diff(child))

    # for i in old_node.children:
    #     while a := widget.get_first_child():
    #         widget.remove(a)

    #     for i in node.children:
    #         widget.append(render_naive(i))
    # render_diff(widget.get_children()[i], old_node.children[i], node.children[i])

    return widget
