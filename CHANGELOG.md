# Changelog

## 0.0.1b
### Added:
  - Utility classes for Snowflake and Cache.
  - A simple rate limiter for a future Gateway implementation.
  - Better documentation straight away from the beginning.
  
### Changed:
  - The library will no be use trio instead of gevent and with that, it requires an async/await syntax.
  - Some further code changes and cleanups for simplifying it.
  
### Removed:
  - The pre-existing Gateway implementation as it probably will be best to just rewrite it.