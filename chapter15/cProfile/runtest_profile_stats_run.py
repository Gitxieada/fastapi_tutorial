import pstats
p = pstats.Stats("runtest_profile.stats")
p.sort_stats("cumulative")  # 和显示明细一样
# p.print_stats()
p.print_callers()  # 可以显示函数被哪些函数调用
