from kivy import utils


def format_text(text):
    new_text = text.strip()
    new_text = new_text.replace('[u]', '')
    new_text = new_text.replace('[/u]', '')
    return new_text


def clean_widget(widget):
    for banner in widget.children:
        for float_layout in banner.children:
            for elt in float_layout.children:
                elt.color = utils.get_color_from_hex("#ffffff")
