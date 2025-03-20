

```python
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(...)
engine = create_engine(connection_url, ...)
```

```python
from pyodbc 

engine = pyodbc.connect(...)
```