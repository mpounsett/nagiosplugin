class Summary:

    def brief(self, results):
        try:
            return str(results.worst_category[0])
        except IndexError:
            return ''

    def verbose(self, results):
        return self.brief(results)
