color_dict = {'~O': '\033[93m', '~F': '\033[96m', '~R': '\033[92m', '~E': '\033[0m'}

def fixColor(text):
    for i, j in color_dict.items():
        text = text.replace(i, j)
    return text