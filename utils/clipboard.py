from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboardTypeString

class Clipboard:
    def __init__(self):
        self.pasteboard = NSPasteboard.generalPasteboard()
        self.types = self.pasteboard.types()
    
    def get_png(self):
        if NSPasteboardTypePNG in self.types:
            data = self.pasteboard.dataForType_(NSPasteboardTypePNG)
            return data
        return None

    def get_tiff(self):
        if NSPasteboardTypeTIFF in self.types:
            data = self.pasteboard.dataForType_(NSPasteboardTypeTIFF)
            return data
        return None

    def get_string(self):
        if NSPasteboardTypeString in self.types:
            data = self.pasteboard.dataForType_(NSPasteboardTypeString)
            return data
        return None
    
    def clear(self):
        self.pasteboard.clearContents()

    def set_text(self, text):
        self.pasteboard.clearContents()
        self.pasteboard.setString_forType_(text, NSPasteboardTypeString)