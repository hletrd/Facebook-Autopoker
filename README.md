# PyPoker
* The only multithreaded Facebook autopoker
* Fully multithreaded, speed is not affected by number of person being poked concurrently.
 * Multithreading is not supported by PHP(poker.php)

## Running (by Python, recommended)
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

## Running (by PHP)
* Open poker.php by any text editor, and type rerquired informations in.
```php
define("COOKIE_c_user", 'Your Facebook cookie: c_user');
define("COOKIE_xs", 'Your Facebook cookie xs');
```

*run
```
$ php poker.php
```
