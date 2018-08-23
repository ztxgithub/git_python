# python 正则表达式
 
## pyhton 正则表达式使用

```shell

    知识点：
        (1) 默认情况下正则表达式是匹配全文的一行
            如果要匹配范围为全文,则增加传入的参数 re.DOTALL
            match_obj = re.match('.*name="_xsrf" value="(.*?)"', 
                                 response_text,
                                 re.DOTALL)

    1.Python提供re模块，包含所有正则表达式的功能
    2.强烈建议使用Python的r前缀，就不用考虑字符串转义问题:
        s = r'ABC\-001' # Python的字符串
        # 对应的正则表达式字符串不变：
        # 'ABC\-001'
        
    3.判断正则表达式是否匹配
      match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None。常见的判断方法就是
      
      test = '用户输入的字符串'
      if re.match(r'正则表达式', test):
          print('ok')
      else:
          print('failed')
          
      例如:
        >>> import re
        >>> re.match(r'^\d{3}-\d{3,8}$', '010-12345')
        <_sre.SRE_Match object; span=(0, 9), match='010-12345'>
        >>> re.match(r'^\d{3}-\d{3,8}$', '010 12345')
        >>>
        
    4.用正则表达式切分字符串
        (1) 切分多个连续空格
            >>> re.split(r'\s+', 'a b   c')
            ['a', 'b', 'c']
            
        (2) >>> re.split(r'[\s,;]+', 'a,b;; c  d')  
            ['a', 'b', 'c', 'd']
            
    5.分组
        提取子串的强大功能。用()表示的就是要提取的分组（Group）
        group(0)永远是原始字符串，group(1)、group(2)……表示第1、2、……个子串。
        
        >>> m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
        >>> m
        <_sre.SRE_Match object; span=(0, 9), match='010-12345'>
        >>> m.group(0)
        '010-12345'
        >>> m.group(1)
        '010'
        >>> m.group(2)
        '12345'
        
        嵌套分组由父循环到子循环
            import re
            line = "boobby123"
            regex_str = "((boby|boobby)123)"
            match_obj = re.match(regex_str,line)
            if match_obj:
                print("group1:%s" % match_obj.group(1))
                print("group2:%s" % match_obj.group(2))
                
           结果:
                group1:boobby123
                group2:boobby
        
    6.贪婪匹配
        (1) 正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符。（可以从字符串的由后往前进行匹配）
                举例如下，由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了
                >>> re.match(r'^(\d+)(0*)$', '102300').groups()
                ('102300', '')
                
                line = "booooobb123"
                regex_str = ".*(b.*b).*"    //贪婪匹配
                match_obj = re.match(regex_str,line)
                if match_obj:
                    print(match_obj.group(1)) 
                结果:
                    bb
                
        (2) \d+采用非贪婪匹配（也就是尽可能少匹配）, 加上 ? (相当与从前面开始匹配)
                line = "booooobb123"
                regex_str = ".*?(b.*?b).*" // ? 非贪婪匹配
                match_obj = re.match(regex_str,line)
                if match_obj:
                    print(match_obj.group(1)) 
                结果:
                    booooob
                
        
    7.编译
      当我们在Python中使用正则表达式时，re模块内部会干两件事情：
      
          A.编译正则表达式，如果正则表达式的字符串本身不合法，会报错；
          B.用编译后的正则表达式去匹配字符串。
          
    如果一个正则表达式要重复使用几千次，出于效率的考虑，我们可以预编译该正则表达式，
    接下来重复使用时就不需要编译这个步骤了，直接匹配：
    
        >>> import re
        # 编译:
        >>> re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
        # 使用：
        >>> re_telephone.match('010-12345').groups()
        ('010', '12345')
        >>> re_telephone.match('010-8086').groups()
        ('010', '8086')
```
