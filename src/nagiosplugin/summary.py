class Summary:

    def ok(self, results):
        return str(results.first_significant())

    def problem(self, results):
        return str(results.first_significant())

    def verbose(self, results):
        pass
