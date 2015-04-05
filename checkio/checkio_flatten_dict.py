'''
============================================================
http://www.checkio.org/mission/flatten-dict/solve/

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def flatten(dictionary):
    stack = [((), dictionary)]
    result = {}
    while stack:
        path, current = stack.pop()
        for k, v in current.items():
            if isinstance(v, dict) and v: stack.append((path + (k,), v))
            else: result["/".join((path + (k,)))] = "" if isinstance(v, dict) and not v else v
    return result

if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert flatten({"empty": {}}) == {"empty": ""}, "Empty value"
    assert flatten({"key": "value"}) == {"key": "value"}, "Simple"
    assert flatten(
        {"key": {"deeper": {"more": {"enough": "value"}}}}
    ) == {"key/deeper/more/enough": "value"}, "Nested"
    assert flatten({"name": {
                        "first": "One",
                        "last": "Drone"},
                    "job": "scout",
                    "recent": {},
                    "additional": {
                        "place": {
                            "zone": "1",
                            "cell": "2"}}}
    ) == {"name/first": "One",
          "name/last": "Drone",
          "job": "scout",
          "recent": "",
          "additional/place/zone": "1",
          "additional/place/cell": "2"}
