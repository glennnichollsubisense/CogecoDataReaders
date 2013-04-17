

class InequalityInFields(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)


class ClassNotManaged(Exception):
    
    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)


class InvalidDSType(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)

    
class InvalidJoin(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)

    

class SheetIsCoax(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)


class FieldNotMapped(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)

class PriorityZero(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)

class TrailingSpaceInFieldName(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)

class TrailingSpaceInClassName(Exception):

    def __init__(self, value):
        self.value=value

    def __str__(self):
        return repr(self.value)
