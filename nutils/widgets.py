from django import forms

class ReadOnlyWidget(forms.Widget):

    def __init__(self, original_value, display_value=None):
        self.original_value = original_value
        self.display_value = display_value or self.original_value
        super(ReadOnlyWidget, self).__init__()
        
    def _has_changed(self, initial, data):
        return False
        
    def render(self, name, value, attrs=None):
        return unicode(self.display_value)

    def value_from_datadict(self, data, files, name):
        return self.original_value            