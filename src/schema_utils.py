import os
import re
import sys
from functools import reduce
from typing import List


def read_files(directory, ext_whitelist: List[str] = None):
    files = os.listdir(directory)

    if ext_whitelist is not None:
        rgx = re.compile(r"\.(" + "|".join(ext_whitelist) + ")$", re.IGNORECASE)
        files = filter(lambda x: rgx.search(x), files)

    return files


# https://bitbucket.org/ericvsmith/toposort/src/default/toposort.py
def toposort(data):
    """Dependencies are expressed as a dictionary whose keys are items
    and whose values are a set of dependent items. Output is a list of
    sets in topological order. The first set consists of items with no
    dependences, each subsequent set consists of items that depend upon
    items in the preceeding sets."""

    # Special case empty input.
    if len(data) == 0:
        return

    # Copy the input so as to leave it unmodified.
    data = data.copy()
    # print(data.items())

    # Ignore (remove) self dependencies.
    for k, v in data.items():
        v.discard(k)

    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    if len(extra_items_in_deps):
        raise Exception("Some dependencies not found! " + str(extra_items_in_deps))

    # Add empty dependences where needed.
    # data.update({item: set() for item in extra_items_in_deps})

    while True:
        ordered = set(item for item, dep in data.items() if len(dep) == 0)
        if not ordered:
            break
        yield ordered
        data = {
            item: (dep - ordered) for item, dep in data.items() if item not in ordered
        }

    if len(data) != 0:
        raise Exception("Circular dependency in " + str(data))


# https://bitbucket.org/ericvsmith/toposort/src/default/toposort.py
def toposort_flatten(data, sort=True):
    """Returns a single list of dependencies. For any set returned by
    toposort(), those items are sorted and appended to the result (just to
    make the results deterministic)."""
    result = []
    for d in toposort(data):
        result.extend((sorted if sort else list)(d))
    return result


def get_schema(schema_dir: str, tbl_prefix: str = ""):
    # collect files with extension whitelist
    filenames = read_files(schema_dir, ["sql"])

    # read content and save dependecies (via magic sql comment "-- require <filename>")
    req_rgx = re.compile(r"--\s*##\s*require ([\S]+)", re.IGNORECASE)

    def _require_reducer(memo, name):
        with open(os.path.join(schema_dir, name), "r") as f:
            sql = f.read()

        deps = set()
        for _name in req_rgx.findall(sql):
            if _name[-4:].lower() != ".sql":
                _name += ".sql"
            deps.add(_name)

        memo[name] = deps
        return memo

    deps_graph = reduce(_require_reducer, filenames, {})

    # resolve depencies from above
    try:
        resolved = list(toposort_flatten(deps_graph))
    except Exception as e:
        print("Dependency error: " + str(e))
        sys.exit(2)

    # collect final sql
    sql = ""
    for name in resolved:
        with open(os.path.join(schema_dir, name), "r") as f:
            sql += f.read()

    return sql.replace("TBLPREFIX____", tbl_prefix)
