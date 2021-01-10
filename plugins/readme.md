# PuzzleAPI plugins

Plugins go in this directory.  Plugins can either be a single .py file, or a directory with an __init__.py file.

After importing the following 2 variables should be accessible - they can be empty if not required:

```python
requests: List[Tuple[str, tornado.web.RequestHandler]]
# This is a list of tuples consisting of a web address, and a class that inherits from the tornado RequestHandler base which handles the URI.
```

```python
indexItems: List[str]
# This is a list of strings containing HTML chunks for displaying some form of input, or informing a user how to use the tool
```
