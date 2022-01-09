from utils import delete_from_file, read_json_file, sort_dict, create_cache,\
    does_file_exist, read_from_file, write_to_file, write_to_json_file

class AutoCompleteIndex:

    def __init__(self, options):
        self.options = options
        self.sorted_dict = {}

    def add_options(self, options=None):
        try:
            if options:
                data = read_json_file('data.json')

                for _, key in enumerate(options):
                    data[key] = options[key]
                data = sort_dict(data)
                write_to_json_file('data.json', data)
            else:
                d = read_json_file('data.json')
                self.sorted_dict = sort_dict(d)
        except Exception as e:
            print('error with add options')
            print(e)

    def create_cache(self):
        data = read_json_file('data.json')
        write_to_json_file('cache.json', create_cache(data))


class IncrementalAutoCompleteSearch(object):

    def __init__(self, auto_complete_index, num_recommendations, file_name):
        self.auto_complete_index = auto_complete_index
        self.num_recommendations = num_recommendations
        self.file_name = file_name

    def get_final_query(self, query=None):
        if not query:
            final_query = read_from_file(self.file_name)
            return final_query
        if does_file_exist(self.file_name) == True:
            pre_query = read_from_file(self.file_name)
            final_query = pre_query + query
            write_to_file(self.file_name, query)
            return final_query
        else:
            write_to_file(self.file_name, query)
            return query

    def suggest(self, query):
        cache = read_json_file('cache.json')
        if query in cache:
            suggestions = []
            num_of_iterations = min(
                self.num_recommendations, len(cache[query]))
            for num in range(num_of_iterations):
                if cache[query][num]:
                    suggestions.append(cache[query][num])
                else:
                    return []
            return suggestions
        else:
            return []

    def type_character(self, query):
        q = self.get_final_query(query)
        return self.suggest(q)

    def delete_character(self):
        delete_from_file(self.file_name)
        q = self.get_final_query()
        return self.suggest(q)