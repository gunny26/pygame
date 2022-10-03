#!/usr/bin/python


for start in range(3, 100):
    print(start)
    counter = 0
    last = start  # difference between the lst and actual number
    while start != 1:
        if start & 0x1:
            start *= 3
            start += 1
        else:
            start = start // 2
        diff = start - last
        print(f"{start} difference {diff}")
        counter += 1
        last = start
    print(f"finished in {counter} steps")
