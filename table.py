class Table:
    def __init__(self, fields=None):
        self.fields = ''
        self.count_of_rows = 0
        if fields:
            self.fields = fields

    def get_fields(self):
        return self.fields

    def get_count_of_rows(self):
        return self.count_of_rows

    def increase_count_of_rows(self, n=1):
        self.count_of_rows += n

    def decrease_count_of_rows(self, n=1):
        self.count_of_rows -= n

    def set_count_of_rows(self, n):
        self.count_of_rows = n

    def get_fields_to_string(self):
        fields_string = ""
        for field in self.fields:
            if field == "id":
                continue
            fields_string = fields_string + field + ', '
        return fields_string[:-2]
