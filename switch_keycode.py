class switch_keycode:
    def __init__(self,Key_Code):
        self.Key_Code = Key_Code
    def switch_content(self):
        global value
        if self.Key_Code == 65:
            value = 'A'
        elif self.Key_Code == 66:
            value = 'B'
        elif self.Key_Code == 67:
            value = 'C'
        elif self.Key_Code == 68:
            value = 'D'
        elif self.Key_Code == 69:
            value = 'E'
        elif self.Key_Code == 70:
            value = 'F'
        elif self.Key_Code == 71:
            value = 'G'
        elif self.Key_Code == 72:
            value = 'H'
        elif self.Key_Code == 73:
            value = 'I'
        elif self.Key_Code == 74:
            value = 'J'
        elif self.Key_Code == 75:
            value = 'K'
        elif self.Key_Code == 76:
            value = 'L'
        elif self.Key_Code == 77:
            value = 'M'
        elif self.Key_Code == 78:
            value = 'N'
        elif self.Key_Code == 79:
            value = 'O'
        elif self.Key_Code == 80:
            value = 'P'
        elif self.Key_Code == 81:
            value = 'Q'
        elif self.Key_Code == 82:
            value = 'R'
        elif self.Key_Code == 83:
            value = 'S'
        elif self.Key_Code == 84:
            value = 'T'
        elif self.Key_Code == 85:
            value = 'U'
        elif self.Key_Code == 86:
            value = 'V'
        elif self.Key_Code == 87:
            value = 'W'
        elif self.Key_Code == 88:
            value = 'X'
        elif self.Key_Code == 89:
            value = 'Y'
        elif self.Key_Code == 90:
            value = 'Z'
        elif self.Key_Code == 48:
            value = '0'
        elif self.Key_Code == 49:
            value = '1'
        elif self.Key_Code == 50:
            value = '2'
        elif self.Key_Code == 51:
            value = '3'
        elif self.Key_Code == 52:
            value = '4'
        elif self.Key_Code == 53:
            value = '5'
        elif self.Key_Code == 54:
            value = '6'
        elif self.Key_Code == 55:
            value = '7'
        elif self.Key_Code == 56:
            value = '8'
        elif self.Key_Code == 57:
            value = '9'

        return value