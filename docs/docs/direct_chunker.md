<div style="background:rgba(0,0,0,0.1); border-left:4px solid #0366d6; padding:1em; border-radius:4px;">

Imagine three extractors (A, B, C) with differing dataset sizes and chunk sizes:

| Extractor | Total Rows | Chunk Size | # Chunks | Coordinates              |
|:---------:|:----------:|:----------:|:--------:|:-------------------------|
| **X**     |     100    |     50     |    2     | (0,16), (16,16)<br/>(32,16), (48,16)<br/>(64,16), (80,16)|
| **Y**     |     60     |     20     |    3     | (0,10), (10,10)<br/>(20,10), (30,10)<br/>(40,10), (50,10)|
| **Z**     |     30     |     30     |    1     | (0,5), (5,5)<br/>(10,5), (15,5)<br/>(20,5), (25,5)       |

The total # of executions = #Chunks X * #Chunks Y * #Chunks Z = 2 × 3 × 1 = 6.

Now to calculate the chunk coordinates we distribute the total rows across all 6 executions.

Extractor X: 100/6 = 16 Remainder 4

Extractor Y: 60/6 = 10 

Extractor Z: 30/6 = 5

Therefore, the `Pipeline` will execute 6 seperate times:

| Execution |       X       |       Y       |       Z       |
|:---------:|:-------------:|:-------------:|:-------------:|
| 1         | (0,16)        | (0,10)        | (0,5)         |
| 2         | (16,16)       | (10,10)       | (5,5)         |
| 3         | (32,16)       | (20,10)       | (10,5)        |
| 4         | (48,16)       | (30,10)       | (15,5)        |
| 5         | (64,16)       | (40,10)       | (20,5)        |
| 6         | (80,16)       | (50,10)       | (25,5)        |

The last execution will include the final chunk as well as any remaining rows of data.

</div>