class FilterModule(object):
    def filters(self):
        return {
            "custom_test": self.custom_test,
        }

    @staticmethod
    def custom_test(data1: str, data2: str) -> str:
        return data1 + 'TEST' + data2
