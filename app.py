# Create another file for the dictionary itself. All operations work on the file itself
# the add options will work becaue it works on a persistent data store, a file


from flask import Flask, request
import json
from utils import delete_from_file, read_json_file, sort_dict, create_cache,\
    does_file_exist, read_from_file, write_to_file, write_to_json_file

app = Flask(__name__)


@app.route('/')
def get_suggestions():
    try:

        options = [('aaa', 3), ('aa', 10), ('azz', 4)]
        auto_complete_index = AutoCompleteIndex(options)
        auto_complete_index.add_options()
        auto_complete_index.create_cache()
        auto_complete_search = IncrementalAutoCompleteSearch(
            auto_complete_index, 2, 'query.txt')

        is_delete = request.args.get("delete")
        if is_delete:
            auto_complete_search.delete_character()

        q = request.args.get("q")
        res = auto_complete_search.type_character(q)

        return json.dumps(res)
    except Exception as e:
        return e


@app.route('/add-options', methods=['POST'])
def add_options():
    try:
        options = [('aaa', 3), ('aa', 10), ('azz', 4)]
        data = request.json
        auto_complete_index = AutoCompleteIndex(options)
        auto_complete_index.add_options(data)
        auto_complete_index.create_cache()
        return 'success'
    except Exception as e:
        print('problem with add options')
        print(e)
        return 'adding options failed'


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


if __name__ == '__main__':
    app.run()
