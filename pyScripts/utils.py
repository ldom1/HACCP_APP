from kivy import utils


def format_text(text):
    new_text = text.strip()
    new_text = new_text.replace('[u]', '')
    new_text = new_text.replace('[/u]', '')
    return new_text


def clean_widget(app, screen_id, widget_id):
    widget = app.root.ids[screen_id].ids[widget_id]
    for banner in widget.children:
        for float_layout in banner.children:
            for elt in float_layout.children:
                elt.color = utils.get_color_from_hex("#ffffff")
