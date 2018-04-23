# python 接口函数
 
- range()函数

```shell

    可以生成一个整数序列,range(5)生成的序列是从0开始小于5的整数(0,1,2,3,4)
    >>> list(range(5))
        [0, 1, 2, 3, 4]

```

- 数据类型转换

```shell

   (1) >>> int('123')
        123
        
   (2) >>> int(12.34)
        12
   (3) >>> float('12.34')
        12.34
   (4) >>> str(1.23)
        '1.23'
   (5) >>> str(100)
        '100'
   (6) >>> bool(1)
        True
   (7) >>> bool('')
        False

```

- isinstance() : 数据类型检查

```shell

   def my_abs(x):
       if not isinstance(x, (int, float)):
           raise TypeError('bad operand type')
       if x >= 0:
           return x
       else:
           return -x

```

- list(Iterator) 函数

```shell

    通过list()函数让它把惰性序列序列(Iterator )都计算出来并返回一个list

```