=========
Changelog
=========

0.5
~~~
* Added hook for performing a synchronous refresh of stale items
* Updated docs for invalidation

0.4
~~~
* Handle some error cases
* Add invalidate method

0.3
---
* Fixed nasty bug where caching could find it's way into a limbo state (#5)
* Remove bug where it was assumed that cached items would be iterable (#4)
* Added handling of uncacheable types

0.2
---
* Docs? Docs!
* Added method for determining whether to "fetch on miss"

0.1
---
Minimal viable product
