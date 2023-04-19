import urwid

class ChoiceWidget(urwid.Text):

    def __init__(self, choices):
        self.choices = choices
        items = []
        for k, v in choices.items():
            items += ['(', k, '):', v]
        items += [' ']
        urwid.Text.__init__(self, items)
