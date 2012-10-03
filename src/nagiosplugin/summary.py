class Summary:

    def ok(self, results, verbose=0):
        return str(results.first_significant())

    def problem(self, results, verbose=0):
        return str(results.first_significant())
