class FieldType(object):
    """
    FieldTypes are used to automatically generate input boxes in the GUI,
    so that when adding new furrow events, one needs modify only
    the back-end by specifying the furrow event's parameter's with FieldTypes.
    """
    def __init__(self, value):
        self.value = value

    def validate(self, new_val):
        """
        If new_val is a valid value for the field type,
        set it as the current value and return True. Otherwise,
        leave the value unchanged and return False.
        """
        self.value = new_val
        return True


class IntegerFieldType(FieldType):
    """
    A Field Type for integer inputs.
    """
    def __init__(self, value):
        super(IntegerFieldType, self).__init__(value)

    def validate(self, new_val):
        try:
            i = int(new_val)
            self.value = i
            return True
        except:
            return False
