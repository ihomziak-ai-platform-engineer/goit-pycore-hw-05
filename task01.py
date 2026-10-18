"""Command-line log analyzer for the homework task 1."""

def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        print(f"START fibonacci({n})")

        if n <= 0:
            return 0

        if n == 1:
            return 1

        if n in cache:
            print(f"CACHE HIT: {n} = {cache[n]}")
            return cache[n]

        print(f"CALCULATING fibonacci({n})")

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)

        print(f"SAVED cache[{n}] = {cache[n]}")

        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()
    print(f"RESULT: {fib(4)}")