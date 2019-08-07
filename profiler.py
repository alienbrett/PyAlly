import pstats
stats = pstats.Stats("profiler.output")
stats.sort_stats("tottime")
stats.print_stats(10)
