"""Verify that it's on test PyPI.
```bash
uv run generator/verify.py --script --no-project --index-url https://test.pypi.org/simple/ spotify-async
```

Expect:
```python
<class 'spotipython.client.Client'>
```
"""

from spotipython import Client

print(Client)
