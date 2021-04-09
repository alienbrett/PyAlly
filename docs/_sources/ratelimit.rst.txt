Rate Limiting
==============

Ally imposes rate limits for each account, "designed to protect accounts from abuse and servers from load."

PyAlly has thread-safe systems in place to respect these limits, and provides information and flexibility when dealing with these limits.

Every function avaliable in the library has a ``block`` keyword that modifies the behavior of the function when the rate limit has been exceeded. When true, the function will block the calling thread until the API will accept the call, should the function encounter a rate limit exception. When false, the function will raise a ``ally.exceptions.RateLimitException``. The user can then build custom logic around rate limit failures.

Also, users can accesss the current state of the rate limits. Rate limit information is held on a module-level, and provides only a single set of limits shared across all ``ally.Ally()`` instances.

Rate limit information can be queried with the ``ally.RateLimit.snapshot()`` function:

.. autofunction:: ally.RateLimit.snapshot
