# Facebook Autopoker
* Implemented for 2 languages (Python 2.7/3, PHP)
* The only multithreaded Facebook autopoker (PyPoker only)
* Fully multithreaded, speed is not affected by number of person being poked concurrently. (PyPoker only)
* Supports Python 2.7, Python 3 (PyPoker only)
* Supports SQLite logging (PyPoker only)

## Running PyPoker (Recommended)
* Open poker.py by any text editor, and type rerquired informations in.
```python
c_user = 'Your Facebook cookie: c_user'
xs = 'Your Facebook cookie: xs'
db = 'filename that log will be stored'
```
* run
```
$ python poker.py
```

### Running monitor for PyPoker (Optional)
* Open poker.py by any text editor, and type rerquired informations in.
 * db have to be the same with PyPoker to monitor the poking activity correctly.
```python
db = 'filename of the SQLite DB'
```
* run
```
$ python monitor.py
```

## Running PHPPoker
* Open poker.php by any text editor, and type rerquired informations in.
```php
define("COOKIE_c_user", 'Your Facebook cookie: c_user');
define("COOKIE_xs", 'Your Facebook cookie xs');
```

* run
```
$ php poker.php
```
