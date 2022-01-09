from flask import Flask, request
import json
from classes import AutoCompleteIndex, IncrementalAutoCompleteSearch

app = Flask(__name__)

options = [('aaa', 3), ('aa', 10), ('azz', 4)]
auto_complete_index = AutoCompleteIndex(options)
auto_complete_search = IncrementalAutoCompleteSearch(
    auto_complete_index, 2, 'query.txt')


@app.route('/')
def get_suggestions():
    try:
        auto_complete_index.add_options()
        auto_complete_index.create_cache()
        q = request.args.get("q")
        res = auto_complete_search.type_character(q)

        return json.dumps(res)
    except Exception as e:
        return e


@app.route('/delete')
def delete():
    try:
        auto_complete_search.delete_character()
        return 'deleted successfully'
    except Exception as e:
        print(e)
        return 'deletion failed'


@app.route('/add-options', methods=['POST'])
def add_options():
    try:
        data = request.json
        auto_complete_index.add_options(data)
        auto_complete_index.create_cache()
        return 'success'
    except Exception as e:
        print('problem with add options')
        print(e)
        return 'adding options failed'


if __name__ == '__main__':
    app.run()
