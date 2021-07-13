public: yes
tags: [mysql, paradigm, note]
summary: |
  Learning mysql paradigm

mysql paradigm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| 1. 保证表中每列数据的原子性，及每列数据都是不可拆分的
| 2. 保证一个表只描述一件事情，否则这张表就是需要拆分为多个的
| 3. 保证表中的数据都依赖于主键，不能出现传递依赖的关系，即 A -> B -> C -> 主键

以上为个人理解的 **MYSQL** 三范式。
