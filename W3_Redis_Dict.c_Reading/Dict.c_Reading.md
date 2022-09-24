<h1><center>Redis中dict.c文件的源码解析</center></h1>
<h3><center>姓名:江英翔 学号:1120212709 班级:2107</center></h3>
<!-- TOC -->

- [前言](#%E5%89%8D%E8%A8%80)
- [字典的定义](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%AE%9A%E4%B9%89)
- [字典的初始化操作](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%88%9D%E5%A7%8B%E5%8C%96%E6%93%8D%E4%BD%9C)
    - [字典的创建](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%88%9B%E5%BB%BA)
    - [初始化字典](#%E5%88%9D%E5%A7%8B%E5%8C%96%E5%AD%97%E5%85%B8)
    - [重置字典](#%E9%87%8D%E7%BD%AE%E5%AD%97%E5%85%B8)
    - [字典的大小](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%A4%A7%E5%B0%8F)
- [字典的增删改查](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%A2%9E%E5%88%A0%E6%94%B9%E6%9F%A5)
    - [字典的增加](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%A2%9E%E5%8A%A0)
    - [字典的删除](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%88%A0%E9%99%A4)
    - [字典的修改](#%E5%AD%97%E5%85%B8%E7%9A%84%E4%BF%AE%E6%94%B9)
    - [字典的查找](#%E5%AD%97%E5%85%B8%E7%9A%84%E6%9F%A5%E6%89%BE)
- [字典的扩容](#%E5%AD%97%E5%85%B8%E7%9A%84%E6%89%A9%E5%AE%B9)
- [字典的迭代器](#%E5%AD%97%E5%85%B8%E7%9A%84%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [初始化字典迭代器](#%E5%88%9D%E5%A7%8B%E5%8C%96%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [安全地初始化字典迭代器](#%E5%AE%89%E5%85%A8%E5%9C%B0%E5%88%9D%E5%A7%8B%E5%8C%96%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [释放字典迭代器](#%E9%87%8A%E6%94%BE%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [重置字典迭代器](#%E9%87%8D%E7%BD%AE%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [返回字典迭代器的当前节点](#%E8%BF%94%E5%9B%9E%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8%E7%9A%84%E5%BD%93%E5%89%8D%E8%8A%82%E7%82%B9)
    - [获取安全的字典迭代器](#%E8%8E%B7%E5%8F%96%E5%AE%89%E5%85%A8%E7%9A%84%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [释放字典迭代器](#%E9%87%8A%E6%94%BE%E5%AD%97%E5%85%B8%E8%BF%AD%E4%BB%A3%E5%99%A8)
    - [获得迭代器](#%E8%8E%B7%E5%BE%97%E8%BF%AD%E4%BB%A3%E5%99%A8)
- [哈希相关](#%E5%93%88%E5%B8%8C%E7%9B%B8%E5%85%B3)
    - [哈希函数](#%E5%93%88%E5%B8%8C%E5%87%BD%E6%95%B0)
    - [rehash函数](#rehash%E5%87%BD%E6%95%B0)
    - [哈希函数种子设置与获取](#%E5%93%88%E5%B8%8C%E5%87%BD%E6%95%B0%E7%A7%8D%E5%AD%90%E8%AE%BE%E7%BD%AE%E4%B8%8E%E8%8E%B7%E5%8F%96)
    - [哈希函数](#%E5%93%88%E5%B8%8C%E5%87%BD%E6%95%B0)
- [字典的其他操作](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%85%B6%E4%BB%96%E6%93%8D%E4%BD%9C)
    - [字典的重构](#%E5%AD%97%E5%85%B8%E7%9A%84%E9%87%8D%E6%9E%84)
    - [字典试图扩展](#%E5%AD%97%E5%85%B8%E8%AF%95%E5%9B%BE%E6%89%A9%E5%B1%95)
    - [rehash移动指定毫秒时间](#rehash%E7%A7%BB%E5%8A%A8%E6%8C%87%E5%AE%9A%E6%AF%AB%E7%A7%92%E6%97%B6%E9%97%B4)
    - [rehash移动指定数量](#rehash%E7%A7%BB%E5%8A%A8%E6%8C%87%E5%AE%9A%E6%95%B0%E9%87%8F)
- [字典的释放及内存回收](#%E5%AD%97%E5%85%B8%E7%9A%84%E9%87%8A%E6%94%BE%E5%8F%8A%E5%86%85%E5%AD%98%E5%9B%9E%E6%94%B6)
    - [清除字典](#%E6%B8%85%E9%99%A4%E5%AD%97%E5%85%B8)
    - [释放字典](#%E9%87%8A%E6%94%BE%E5%AD%97%E5%85%B8)
    - [字典的指纹](#%E5%AD%97%E5%85%B8%E7%9A%84%E6%8C%87%E7%BA%B9)
        - [字典的指纹定义](#%E5%AD%97%E5%85%B8%E7%9A%84%E6%8C%87%E7%BA%B9%E5%AE%9A%E4%B9%89)
        - [字典的指纹计算](#%E5%AD%97%E5%85%B8%E7%9A%84%E6%8C%87%E7%BA%B9%E8%AE%A1%E7%AE%97)
    - [字典的随机条目](#%E5%AD%97%E5%85%B8%E7%9A%84%E9%9A%8F%E6%9C%BA%E6%9D%A1%E7%9B%AE)
    - [释放未连接的条目](#%E9%87%8A%E6%94%BE%E6%9C%AA%E8%BF%9E%E6%8E%A5%E7%9A%84%E6%9D%A1%E7%9B%AE)
- [随机返回几个字典的键](#%E9%9A%8F%E6%9C%BA%E8%BF%94%E5%9B%9E%E5%87%A0%E4%B8%AA%E5%AD%97%E5%85%B8%E7%9A%84%E9%94%AE)
- [字典的迭代](#%E5%AD%97%E5%85%B8%E7%9A%84%E8%BF%AD%E4%BB%A3)
- [字典使用指针查找dictEntry引用](#%E5%AD%97%E5%85%B8%E4%BD%BF%E7%94%A8%E6%8C%87%E9%92%88%E6%9F%A5%E6%89%BEdictentry%E5%BC%95%E7%94%A8)
- [调试](#%E8%B0%83%E8%AF%95)
    - [字典信息获取](#%E5%AD%97%E5%85%B8%E4%BF%A1%E6%81%AF%E8%8E%B7%E5%8F%96)
- [字典的基准](#%E5%AD%97%E5%85%B8%E7%9A%84%E5%9F%BA%E5%87%86)
    - [基准测试](#%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95)
    - [基准测试基础](#%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95%E5%9F%BA%E7%A1%80)
- [结语](#%E7%BB%93%E8%AF%AD)

<!-- /TOC -->
# 1.前言
``Redis``是一个使用``ANSI C``编写的开源、支持网络、基于内存、分布式、可选持久性的键值对存储数据库。
``Redis``的数据结构采用多种多样的数据结构，其中最常用的就是哈希表，``Redis``中的哈希表是通过字典来实现的。
本文将对``Redis``中的``dict.c``进行源码解析。
# 2.字典的定义
Redis中的字典是一个哈希表，它的定义如下：
```c
typedef struct dict {
    dictType *type;
    void *privdata;
    dictht ht[2];
    long rehashidx; /* rehashing not in progress if rehashidx == -1 */
    int iterators; /* number of iterators currently running */
} dict;
```
代码位于``dict.h``第79行  
字典的定义中包含了三个哈希表，一个是``ht[0]``，一个是``ht[1]``，还有一个是``rehashidx``。
``ht[0]``和``ht[1]``是两个哈希表，``rehashidx``是一个索引，用于标识当前正在进行rehash操作的哈希表。
字典中的``type``和``privdata``是一个指向``dictType``结构的指针，用于指定字典的类型，``privdata``是一个指向任意类型的指针，用于保存字典的私有数据。
``iterators``是一个整数，用于记录当前正在运行的迭代器的数量。
<h1> dict.c源码解析</h1>

# 字典的初始化操作
## 字典的创建
```c
dict *dictCreate(dictType *type)
{
    dict *d = zmalloc(sizeof(*d));

    _dictInit(d,type);
    return d;
}
```
代码位于``dict.c``第105行  
``dictCreate``函数用于创建一个字典，
它首先使用``zmalloc``函数分配一个字典的大小的内存，
然后调用``_dictInit``函数对字典进行初始化。
##  初始化字典
```c
int _dictInit(dict *d, dictType *type)
{
    _dictReset(d, 0);
    _dictReset(d, 1);
    d->type = type;
    d->rehashidx = -1;
    d->pauserehash = 0;
    return DICT_OK;
}
```
代码位于``dict.c``第114行  
``_dictInit``函数首先调用``_dictReset``函数对字典进行初始化，
然后将``type``赋值给字典的``type``，
将``rehashidx``赋值为-1， 表示当前没有进行rehash操作，
最后将``pauserehash``赋值为0，表示当前没有暂停rehash操作。
## 重置字典
```c
static void _dictReset(dict *d, int htidx)
{
    d->ht_table[htidx] = NULL;
    d->ht_size_exp[htidx] = -1;
    d->ht_used[htidx] = 0;
}
```
代码位于``dict.c``第97行  
``_dictReset``函数用于对字典进行初始化，
它将字典的``ht_table``赋值为空，代表当前哈希表为空，
将字典的``ht_size_exp``赋值为-1，代表当前哈希表的大小为0，
将字典的``ht_used``赋值为0，代表当前哈希表的已使用节点数为0。

## 字典的大小
```c
static signed char _dictNextExp(unsigned long size)
{
    unsigned char e = DICT_HT_INITIAL_EXP;

    if (size >= LONG_MAX) return (8*sizeof(long)-1);
    while(1) {
        if (((unsigned long)1<<e) >= size)
            return e;
        e++;
    }
}
```
代码位于``dict.c``文件第1030行，
该函数用于计算字典的大小，
``size``是字典的大小，
该函数返回值是字典的大小。
首先将``e``赋值为``DICT_HT_INITIAL_EXP``，
然后判断``size``是否大于等于``LONG_MAX``，
如果大于等于，
则返回``8*sizeof(long)-1``，
否则进入循环，
然后判断``(unsigned long)1<<e``是否大于等于``size``，
如果大于等于，
则返回``e``，
否则将``e``加1，
然后进入下一次循环。

# 字典的增删改查
## 字典的增加
```c
int dictAdd(dict *d, void *key, void *val)
{
    dictEntry *entry = dictAddRaw(d,key);

    if (!entry) return DICT_ERR;
    dictSetVal(d, entry, val);
    return DICT_OK;
}
```
代码位于``dict.c``第295行  
``dictAdd``函数用于向字典中添加一个键值对，
它首先调用``dictAddRaw``函数向字典中添加一个键值对，
如果添加失败，那么返回的是``DICT_ERR``，
如果添加成功，那么调用``dictSetVal``函数将值赋值给新添加的节点，
最后返回DICT_OK。
```c
dictEntry *dictAddRaw(dict *d, void *key, dictEntry **existing)
{
    long index;
    dictEntry *entry;
    int htidx;

    if (dictIsRehashing(d)) _dictRehashStep(d);

    /* Get the index of the new element, or -1 if
     * the element already exists. */
    if ((index = _dictKeyIndex(d, key, dictHashKey(d,key), existing)) == -1)
        return NULL;
    htidx = dictIsRehashing(d) ? 1 : 0;
    size_t metasize = dictMetadataSize(d);
    entry = zmalloc(sizeof(*entry) + metasize);
    if (metasize > 0) {
        memset(dictMetadata(entry), 0, metasize);
    }
    entry->next = d->ht_table[htidx][index];
    d->ht_table[htidx][index] = entry;
    d->ht_used[htidx]++;

    /* Set the hash entry fields. */
    dictSetKey(d, entry, key);
    return entry;
}
```
代码位于``dict.c``第322行  
``dictAddRaw``函数用于向字典中添加一个键值对，
它首先判断字典是否正在进行rehash操作，
如果正在进行rehash操作，那么调用``_dictRehashStep``函数进行一步rehash操作，
然后调用``_dictKeyIndex``函数获取键值对的索引，
如果索引为-1，那么表示键值对已经存在，
如果索引不为-1，那么表示键值对不存在，
那么调用``zmalloc``函数分配一个节点的内存，
然后将节点插入到哈希表中，
最后返回新添加的节点。
## 字典的删除
```c
int dictDelete(dict *ht, const void *key) {
    return dictGenericDelete(ht,key,0) ? DICT_OK : DICT_ERR;
}
```
代码位于``dict.c``第355行  
``dictDelete``函数用于从字典中删除一个键值对，
它首先调用``dictGenericDelete``函数从字典中删除一个键值对，
如果删除成功，那么返回DICT_OK，
如果删除失败，那么返回DICT_ERR。
```c
static dictEntry *dictGenericDelete(dict *d, const void *key, int nofree) {
    uint64_t h, idx;
    dictEntry *he, *prevHe;
    int table;

    if (dictSize(d) == 0) return NULL;

    if (dictIsRehashing(d)) _dictRehashStep(d);
    h = dictHashKey(d, key);

    for (table = 0; table <= 1; table++) {
        idx = h & DICTHT_SIZE_MASK(d->ht_size_exp[table]);
        he = d->ht_table[table][idx];
        prevHe = NULL;
        while(he) {
            if (key==he->key || dictCompareKeys(d, key, he->key)) {
                if (prevHe)
                    prevHe->next = he->next;
                else
                    d->ht_table[table][idx] = he->next;
                if (!nofree) {
                    dictFreeUnlinkedEntry(d, he);
                }
                d->ht_used[table]--;
                return he;
            }
            prevHe = he;
            he = he->next;
        }
        if (!dictIsRehashing(d)) break;
    }
    return NULL; /* not found */
}
```
代码位于``dict.c``第398行  
``dictGenericDelete``函数用于从字典中删除一个键值对，
他首先判断字典是否为空，
如果字典为空，那么返回NULL，
如果字典不为空，那么判断字典是否正在进行rehash操作，
如果正在进行rehash操作，那么调用``_dictRehashStep``函数进行一步rehash操作，
然后调用``dictHashKey``函数计算键的哈希值，
然后遍历字典中的两个哈希表，
如果键值对存在，那么调用``dictFreeUnlinkedEntry``函数释放节点，
最后返回被删除的节点。
## 字典的修改
```c
int dictReplace(dict *d, void *key, void *val)
{
    dictEntry *entry, *existing, auxentry;

    entry = dictAddRaw(d,key,&existing);
    if (entry) {
        dictSetVal(d, entry, val);
        return 1;
    }
    auxentry = *existing;
    dictSetVal(d, existing, val);
    dictFreeVal(d, &auxentry);
    return 0;
}
```
代码位于``dict.c``第359行  
``dictReplace``函数用于向字典中添加一个键值对，
如果键值对已经存在，那么修改键值对的值，
如果键值对不存在，那么添加键值对。
## 字典的查找
```c
dictEntry *dictFind(dict *d, const void *key)
{
    dictEntry *he;
    uint64_t h, idx, table;

    if (dictSize(d) == 0) return NULL; /* dict is empty */
    if (dictIsRehashing(d)) _dictRehashStep(d);
    h = dictHashKey(d, key);
    for (table = 0; table <= 1; table++) {
        idx = h & DICTHT_SIZE_MASK(d->ht_size_exp[table]);
        he = d->ht_table[table][idx];
        while(he) {
            if (key==he->key || dictCompareKeys(d, key, he->key))
                return he;
            he = he->next;
        }
        if (!dictIsRehashing(d)) return NULL;
    }
    return NULL;
}
```
代码位于``dict.c``第509行  
``dictFind``函数用于从字典中查找一个键值对，
如果找到，那么返回该键值对，
如果没有找到，那么返回NULL。
```c
static long _dictKeyIndex(dict *d, const void *key, uint64_t hash, dictEntry **existing)
{
    unsigned long idx, table;
    dictEntry *he;
    if (existing) *existing = NULL;

    /* Expand the hash table if needed */
    if (_dictExpandIfNeeded(d) == DICT_ERR)
        return -1;
    for (table = 0; table <= 1; table++) {
        idx = hash & DICTHT_SIZE_MASK(d->ht_size_exp[table]);
        /* Search if this slot does not already contain the given key */
        he = d->ht_table[table][idx];
        while(he) {
            if (key==he->key || dictCompareKeys(d, key, he->key)) {
                if (existing) *existing = he;
                return -1;
            }
            he = he->next;
        }
        if (!dictIsRehashing(d)) break;
    }
    return idx;
}
```
代码位于``dict.c``文件第1049行，
该函数用于获取键的索引，
首先判断``existing``是否为空，
如果不为空，
则将``*existing``赋值为``NULL``，
然后调用``_dictExpandIfNeeded``函数，
如果返回值为``DICT_ERR``，
则返回-1，
然后将``table``赋值为0，
然后判断``table``是否小于等于1，
如果小于等于1，
则将``idx``赋值为``hash & DICTHT_SIZE_MASK(d->ht_size_exp[table])``，
然后将``he``赋值为``d->ht_table[table][idx]``，
然后判断``he``是否为空，
如果不为空，
则判断``key``是否等于``he->key``或者调用``dictCompareKeys``函数返回值为真，
如果是，
则判断``existing``是否为空，
如果不为空，
则将``*existing``赋值为``he``，
然后返回-1，
否则将``he``赋值为``he->next``，
然后判断``!dictIsRehashing(d)``是否为真，
如果为真，
则跳出循环，
否则将``table``加1，
最后返回``idx``。
```c
void *dictFetchValue(dict *d, const void *key)
{
    dictEntry *he;

    he = dictFind(d,key);
    return he ? dictGetVal(he) : NULL;
}
```
代码位于``dict.c``第525行  
``dictFetchValue``函数用于从字典中查找一个键值对，
如果找到，那么返回该键值对的值，
如果没有找到，那么返回NULL。

# 字典的扩容
```c
static int dictTypeExpandAllowed(dict *d) {
    if (d->type->expandAllowed == NULL) return 1;
    return d->type->expandAllowed(
                    DICTHT_SIZE(_dictNextExp(d->ht_used[0] + 1)) * sizeof(dictEntry*),
                    (double)d->ht_used[0] / DICTHT_SIZE(d->ht_size_exp[0]));
}
```
代码位于``dict.c``第998行  
``dictTypeExpandAllowed``函数用于判断字典是否允许扩容，
如果字典的类型没有实现``expandAllowed``函数，那么返回1，
如果字典的类型实现了``expandAllowed``函数，那么调用该函数判断是否允许扩容。
```c
static int _dictExpandIfNeeded(dict *d)
{
    if (dictIsRehashing(d)) return DICT_OK;

    if (DICTHT_SIZE(d->ht_size_exp[0]) == 0) return dictExpand(d, DICT_HT_INITIAL_SIZE);

    if (d->ht_used[0] >= DICTHT_SIZE(d->ht_size_exp[0]) &&
        (dict_can_resize ||
         d->ht_used[0]/ DICTHT_SIZE(d->ht_size_exp[0]) > dict_force_resize_ratio) &&
        dictTypeExpandAllowed(d))
    {
        return dictExpand(d, d->ht_used[0] + 1);
    }
    return DICT_OK;
}
```
代码位于``dict.c``第1006行  
``_dictExpandIfNeeded``函数用于判断字典是否需要扩容，
它首先判断字典是否正在进行rehash操作，
如果正在进行rehash操作，那么返回DICT_OK，
如果没有进行rehash操作，那么判断字典的哈希表是否为空，
如果哈希表为空，那么调用``dictExpand``函数扩容字典，
如果哈希表不为空，那么判断字典的使用节点数是否大于等于哈希表的大小，
如果大于等于，那么判断是否允许扩容，
如果允许扩容，那么调用``dictExpand``函数扩容字典，
如果不允许扩容，那么返回DICT_OK。
```c
int dictExpand(dict *d, unsigned long size) {
    return _dictExpand(d, size, NULL);
}
int _dictExpand(dict *d, unsigned long size, int* malloc_failed)
{
    if (malloc_failed) *malloc_failed = 0;

    if (dictIsRehashing(d) || d->ht_used[0] > size)
        return DICT_ERR;

    dictEntry **new_ht_table;
    unsigned long new_ht_used;
    signed char new_ht_size_exp = _dictNextExp(size);

    size_t newsize = 1ul<<new_ht_size_exp;
    if (newsize < size || newsize * sizeof(dictEntry*) < newsize)
        return DICT_ERR;

    if (new_ht_size_exp == d->ht_size_exp[0]) return DICT_ERR;

    if (malloc_failed) {
        new_ht_table = ztrycalloc(newsize*sizeof(dictEntry*));
        *malloc_failed = new_ht_table == NULL;
        if (*malloc_failed)
            return DICT_ERR;
    } else
        new_ht_table = zcalloc(newsize*sizeof(dictEntry*));

    new_ht_used = 0;

    if (d->ht_table[0] == NULL) {
        d->ht_size_exp[0] = new_ht_size_exp;
        d->ht_used[0] = new_ht_used;
        d->ht_table[0] = new_ht_table;
        return DICT_OK;
    }

    /* Prepare a second hash table for incremental rehashing */
    d->ht_size_exp[1] = new_ht_size_exp;
    d->ht_used[1] = new_ht_used;
    d->ht_table[1] = new_ht_table;
    d->rehashidx = 0;
    return DICT_OK;
}
```
代码位于``dict.c``第140行与191行  
``dictExpand``与``_dictExpand``函数用于扩容字典，
它们首先判断字典是否正在进行rehash操作，
如果正在进行rehash操作，那么返回DICT_ERR，
如果没有进行rehash操作，那么判断字典的使用节点数是否大于等于size，
如果大于等于，那么返回DICT_ERR，
如果小于，那么判断字典的哈希表是否为空，
如果哈希表为空，那么调用``_dictExpand``函数扩容字典，
如果哈希表不为空，那么判断字典的哈希表的大小是否等于size，
如果等于，那么返回DICT_ERR，
如果不等于，那么调用``_dictExpand``函数扩容字典。

# 字典的迭代器
## 初始化字典迭代器
```c
void dictInitIterator(dictIterator *iter, dict *d)
{
    iter->d = d;
    iter->table = 0;
    iter->index = -1;
    iter->safe = 0;
    iter->entry = NULL;
    iter->nextEntry = NULL;
}
```
代码位于``dict.c``第575行  
``dictInitIterator``函数用于初始化字典的迭代器，
它首先将字典的地址赋值给迭代器的字典指针，代表迭代器正在迭代的字典，
然后将迭代器的哈希表索引赋值为-1，代表迭代器正在迭代的哈希表索引，
之后将迭代器的安全标志赋值为0，代表迭代器不是安全的，
最后将迭代器的当前节点指针与下一个节点指针赋值为NULL，代表迭代器当前没有节点。

## 安全地初始化字典迭代器
```c
void dictSafeIterator(dictIterator *iter, dict *d)
{
    dictInitIterator(iter, d);
    iter->safe = 1;
}
```
代码位于``dict.c``第585行  
``dictSafeIterator``函数用于安全地初始化字典的迭代器，
它首先调用``dictInitIterator``函数初始化字典的迭代器，
然后将迭代器的安全标志赋值为1，代表迭代器是安全的。

## 释放字典迭代器
```c
void  (dictIterator *iter)
{
    dictResetIterator(iter);
    zfree(iter);
}
```
代码位于``dict.c``第648行  
``dictReleaseIterator``函数用于释放字典的迭代器，
它首先调用``dictResetIterator``函数重置字典的迭代器，
然后释放迭代器的内存。

## 重置字典迭代器
```c
void dictResetIterator(dictIterator *iter)
{
    if (!(iter->index == -1 && iter->table == 0)) {
        if (iter->safe)
            dictResumeRehashing(iter->d);
        else
            assert(iter->fingerprint == dictFingerprint(iter->d));
    }
}
```
代码位于``dict.c``第596行  
``dictResetIterator``函数用于重置字典的迭代器，
它首先判断迭代器的哈希表索引是否等于-1，且迭代器的哈希表索引是否等于0，
如果不等于，那么判断迭代器是否是安全的，
如果是安全的，那么调用``dictResumeRehashing``函数恢复字典的rehash操作，
如果不是安全的，那么判断迭代器的指纹是否等于字典的指纹，
如果不等于，那么程序出错。

## 返回字典迭代器的当前节点
```c
dictEntry *dictNext(dictIterator *iter)
{
    while (1) {
        if (iter->entry == NULL) {
            if (iter->index == -1 && iter->table == 0) {
                if (iter->safe)
                    dictPauseRehashing(iter->d);
                else
                    iter->fingerprint = dictFingerprint(iter->d);
            }
            iter->index++;
            if (iter->index >= (long) DICTHT_SIZE(iter->d->ht_size_exp[iter->table])) {
                if (dictIsRehashing(iter->d) && iter->table == 0) {
                    iter->table++;
                    iter->index = 0;
                } else {
                    break;
                }
            }
            iter->entry = iter->d->ht_table[iter->table][iter->index];
        } else {
            iter->entry = iter->nextEntry;
        }
        if (iter->entry) {
            /* We need to save the 'next' here, the iterator user
             * may delete the entry we are returning. */
            iter->nextEntry = iter->entry->next;
            return iter->entry;
        }
    }
    return NULL;
}
```
代码位于``dict.c``第615行  
``dictNext``函数用于返回字典迭代器的当前节点，
它首先进入一个死循环，
然后判断迭代器的当前节点是否为空，
如果为空，那么判断迭代器的哈希表索引是否等于-1，且迭代器的哈希表索引是否等于0，
如果等于，那么判断迭代器是否是安全的，
如果是安全的，那么调用``dictPauseRehashing``函数暂停字典的rehash操作，
如果不是安全的，那么将迭代器的指纹赋值为字典的指纹，
然后将迭代器的哈希表索引加1，
如果迭代器的哈希表索引大于等于字典的哈希表大小，
那么判断字典是否正在rehash，且迭代器的哈希表索引是否等于0，
如果是，那么将迭代器的哈希表索引赋值为1，代表正在迭代第二个哈希表，
然后将迭代器的哈希表索引赋值为0，
如果不是，那么跳出循环，
然后将迭代器的当前节点赋值为字典的哈希表的当前节点，
如果迭代器的当前节点不为空，
那么将迭代器的下一个节点赋值为当前节点的下一个节点，
然后返回当前节点。

## 获取安全的字典迭代器
```c
dictIterator *dictGetSafeIterator(dict *d) {
    dictIterator *i = dictGetIterator(d);

    i->safe = 1;
    return i;
}
```
代码位于``dict.c``第608行  
``dictGetSafeIterator``函数用于获取安全的字典迭代器，
它首先调用``dictGetIterator``函数获取一个字典迭代器，
然后将迭代器的安全标识赋值为1，
最后返回迭代器。

## 释放字典迭代器
```c
void dictReleaseIterator(dictIterator *iter)
{
    dictResetIterator(iter);
    zfree(iter);
}
```
代码位于``dict.c``第648行  
``dictReleaseIterator``函数用于释放字典迭代器，
它首先调用``dictResetIterator``函数重置字典迭代器，
然后释放迭代器。

## 获得迭代器
```c
dictIterator *dictGetIterator(dict *d)
{
    dictIterator *iter = zmalloc(sizeof(*iter));
    dictInitIterator(iter, d);
    return iter;
}
```
代码位于``dict.c``第601行  
``dictGetIterator``函数用于获取字典迭代器，
它首先为字典迭代器分配内存，
然后调用``dictInitIterator``函数初始化字典迭代器，
最后返回字典迭代器。

# 哈希相关
## 哈希函数
```c
uint64_t dictGenHashFunction(const void *key, size_t len) {
    return siphash(key,len,dict_hash_function_seed);
}
```
代码位于``dict.c``第86行  
``dictGenHashFunction``函数用于生成哈希值，
它首先调用``siphash``函数生成哈希值，
然后返回哈希值。

## ``rehash``函数
```c
int dictRehash(dict *d, int n) {
    int empty_visits = n*10; 
    if (!dictIsRehashing(d)) return 0;

    while(n-- && d->ht_used[0] != 0) {
        dictEntry *de, *nextde;

        assert(DICTHT_SIZE(d->ht_size_exp[0]) > (unsigned long)d->rehashidx);
        while(d->ht_table[0][d->rehashidx] == NULL) {
            d->rehashidx++;
            if (--empty_visits == 0) return 1;
        }
        de = d->ht_table[0][d->rehashidx];
        while(de) {
            uint64_t h;

            nextde = de->next;
            h = dictHashKey(d, de->key) & DICTHT_SIZE_MASK(d->ht_size_exp[1]);
            de->next = d->ht_table[1][h];
            d->ht_table[1][h] = de;
            d->ht_used[0]--;
            d->ht_used[1]++;
            de = nextde;
        }
        d->ht_table[0][d->rehashidx] = NULL;
        d->rehashidx++;
    }

    /* Check if we already rehashed the whole table... */
    if (d->ht_used[0] == 0) {
        zfree(d->ht_table[0]);
        /* Copy the new ht onto the old one */
        d->ht_table[0] = d->ht_table[1];
        d->ht_used[0] = d->ht_used[1];
        d->ht_size_exp[0] = d->ht_size_exp[1];
        _dictReset(d, 1);
        d->rehashidx = -1;
        return 0;
    }

    /* More to rehash... */
    return 1;
}
```
代码位于``dict.c``第211行  
``dictRehash``函数用于rehash操作，
它首先判断字典是否正在rehash，
如果不是，那么返回0，
如果是，那么首先初始化空的哈希表索引的访问次数，
然后判断字典的哈希表索引是否小于哈希表的大小，
如果不小于，那么判断空的哈希表索引的访问次数是否等于0，
如果等于，那么返回1，
如果不等于，那么判断哈希表的索引是否为空，
如果为空，那么将哈希表的索引加1，
如果不为空，那么将哈希表的索引的元素赋值给``de``
然后判断``de``是否为空，
如果为空，那么将哈希表的索引加1，
如果不为空，那么将哈希表的索引的元素赋值给``nextde``，
然后调用``dictHashKey``函数生成哈希值，
然后将哈希值与哈希表的大小取与，
然后将哈希表的索引的元素的下一个元素赋值给哈希表的索引的元素，
然后将哈希表的索引的元素赋值给哈希表的索引的元素的下一个元素，
然后将哈希表的索引的元素赋值给``de``，
然后将哈希表的索引的元素赋值为``NULL``，
然后将哈希表的索引加1，
然后判断哈希表的使用量是否等于0，
如果等于，那么释放哈希表的索引，
然后将哈希表的索引赋值给哈希表的索引的下一个元素，
然后将哈希表的使用量赋值给哈希表的使用量的下一个元素，
然后将哈希表的大小赋值给哈希表的大小的下一个元素，
然后调用``_dictReset``函数重置字典，
然后将哈希表的索引赋值为-1，
如果不等于，那么返回1。

## 哈希函数种子设置与获取
```c
static uint8_t dict_hash_function_seed[16];

void dictSetHashFunctionSeed(uint8_t *seed) {
    memcpy(dict_hash_function_seed,seed,sizeof(dict_hash_function_seed));
}

uint8_t *dictGetHashFunctionSeed(void) {
    return dict_hash_function_seed;
}
```
代码位于``dict.c``第70行  
``dictSetHashFunctionSeed``函数用于设置哈希函数种子，
它首先调用``memcpy``函数将哈希函数种子的值赋值给``dict_hash_function_seed``，
然后返回``dict_hash_function_seed``，
``dictGetHashFunctionSeed``函数用于获取哈希函数种子，
它直接返回``dict_hash_function_seed``。

## 哈希函数
```c
uint64_t siphash(const uint8_t *in, const size_t inlen, const uint8_t *k);
uint64_t siphash_nocase(const uint8_t *in, const size_t inlen, const uint8_t *k);

uint64_t dictGenCaseHashFunction(const unsigned char *buf, size_t len) {
    return siphash_nocase(buf,len,dict_hash_function_seed);
}
```
代码位于``dict.c``第83行  
``dictGenCaseHashFunction``函数用于生成哈希值，
它首先调用``siphash_nocase``函数生成哈希值，
然后返回哈希值。

# 字典的其他操作
## 字典的重构
```c
int dictResize(dict *d)
{
    unsigned long minimal;

    if (!dict_can_resize || dictIsRehashing(d)) return DICT_ERR;
    minimal = d->ht_used[0];
    if (minimal < DICT_HT_INITIAL_SIZE)
        minimal = DICT_HT_INITIAL_SIZE;
    return dictExpand(d, minimal);
}
```
代码位于``dict.c``第126行  
``dictResize``函数用于字典的重构，
它首先判断字典是否可以重构或者字典是否正在重构，
如果可以，那么将哈希表的使用量赋值给``minimal``，
如果哈希表的使用量小于哈希表的初始大小，
那么将哈希表的初始大小赋值给``minimal``，
然后调用``dictExpand``函数扩展字典，
否则返回``DICT_ERR``。

## 字典试图扩展
```c
int dictTryExpand(dict *d, unsigned long size) {
    int malloc_failed;
    _dictExpand(d, size, &malloc_failed);
    return malloc_failed? DICT_ERR : DICT_OK;
}
```
代码位于``dict.c``第196行  
``dictTryExpand``函数用于字典试图扩展，也就是在内存分配失败时不会报错，
它首先调用``_dictExpand``函数扩展字典，
然后判断内存分配是否失败，
如果失败，那么返回``DICT_ERR``，
否则返回``DICT_OK``。

## rehash移动指定毫秒时间
```c
int dictRehashMilliseconds(dict *d, int ms) {
    if (d->pauserehash > 0) return 0;

    long long start = timeInMilliseconds();
    int rehashes = 0;

    while(dictRehash(d,100)) {
        rehashes += 100;
        if (timeInMilliseconds()-start > ms) break;
    }
    return rehashes;
}
```
代码位于``dict.c``第269行  
``dictRehashMilliseconds``函数用于rehash移动指定毫秒时间，
它首先获取当前时间，
然后初始化``rehashes``为0，
接着循环调用``dictRehash``函数，
每次循环``rehashes``加100，
如果当前时间减去开始时间大于指定毫秒时间，
那么跳出循环，
最后返回``rehashes``。

## rehash移动指定数量
```c
static void _dictRehashStep(dict *d) {
    if (d->pauserehash == 0) dictRehash(d,1);
}
```
代码位于``dict.c``第290行  
``_dictRehashStep``函数用于rehash移动指定数量，
它首先判断字典是否暂停rehash，
如果没有，那么调用``dictRehash``函数，
否则不做任何操作。

# 字典的释放及内存回收
## 清除字典
```c
int _dictClear(dict *d, int htidx, void(callback)(dict*)) {
    unsigned long i;

    /* Free all the elements */
    for (i = 0; i < DICTHT_SIZE(d->ht_size_exp[htidx]) && d->ht_used[htidx] > 0; i++) {
        dictEntry *he, *nextHe;

        if (callback && (i & 65535) == 0) callback(d);

        if ((he = d->ht_table[htidx][i]) == NULL) continue;
        while(he) {
            nextHe = he->next;
            dictFreeKey(d, he);
            dictFreeVal(d, he);
            zfree(he);
            d->ht_used[htidx]--;
            he = nextHe;
        }
    }
    /* Free the table and the allocated cache structure */
    zfree(d->ht_table[htidx]);
    /* Re-initialize the table */
    _dictReset(d, htidx);
    return DICT_OK; /* never fails */
}
```
代码位于``dict.c``第475行  
``_dictClear``函数用于清除字典，
它首先初始化``i``为0，
然后循环遍历哈希表，
如果哈希表的使用量大于0，
那么调用``callback``函数，
然后判断哈希表的第``i``个桶是否为空，
如果不为空，那么循环遍历哈希表的第``i``个桶，
首先获取下一个哈希表节点，
然后释放哈希表节点的键和值，
最后释放哈希表节点，
最后将哈希表的使用量减1，
最后释放哈希表，
然后重置哈希表，
最后返回``DICT_OK``。

## 释放字典
```c
void dictRelease(dict *d)
{
    _dictClear(d,0,NULL);
    _dictClear(d,1,NULL);
    zfree(d);
}
```
代码位于``dict.c``第502行  
``dictRelease``函数用于释放字典，
它首先调用``_dictClear``函数清除哈希表0，
然后调用``_dictClear``函数清除哈希表1，
最后释放字典。

## 字典的指纹
### 字典的指纹定义
> * A fingerprint is a 64 bit number that represents the state of the dictionary at a given time, it's just a few dict properties xored together. When an unsafe iterator is initialized, we get the dict fingerprint, and check the fingerprint again when the iterator is released.If the two fingerprints are different it means that the user of the iterator performed forbidden operations against the dictionary while iterating. 

### 字典的指纹计算
```c
unsigned long long dictFingerprint(dict *d) {
    unsigned long long integers[6], hash = 0;
    int j;

    integers[0] = (long) d->ht_table[0];
    integers[1] = d->ht_size_exp[0];
    integers[2] = d->ht_used[0];
    integers[3] = (long) d->ht_table[1];
    integers[4] = d->ht_size_exp[1];
    integers[5] = d->ht_used[1];

    /* We hash N integers by summing every successive integer with the integer
     * hashing of the previous sum. Basically:
     *
     * Result = hash(hash(hash(int1)+int2)+int3) ...
     *
     * This way the same set of integers in a different order will (likely) hash
     * to a different number. */
    for (j = 0; j < 6; j++) {
        hash += integers[j];
        /* For the hashing step we use Tomas Wang's 64 bit integer hash. */
        hash = (~hash) + (hash << 21); // hash = (hash << 21) - hash - 1;
        hash = hash ^ (hash >> 24);
        hash = (hash + (hash << 3)) + (hash << 8); // hash * 265
        hash = hash ^ (hash >> 14);
        hash = (hash + (hash << 2)) + (hash << 4); // hash * 21
        hash = hash ^ (hash >> 28);
        hash = hash + (hash << 31);
    }
    return hash;
}
```
代码位于``dict.c``第543行  
``dictFingerprint``函数用于计算字典的指纹，
它首先初始化``integers``数组，
然后将哈希表0的表指针、哈希表0的大小指数、哈希表0的使用量、哈希表1的表指针、哈希表1的大小指数、哈希表1的使用量分别赋值给``integers``数组，
然后初始化``hash``为0，
然后循环遍历``integers``数组，
首先将``hash``加上``integers``数组的第``j``个元素，
然后将``hash``进行哈希运算，
最后返回``hash``。

## 字典的随机条目
```c
dictEntry *dictGetRandomKey(dict *d)
{
    dictEntry *he, *orighe;
    unsigned long h;
    int listlen, listele;

    if (dictSize(d) == 0) return NULL;
    if (dictIsRehashing(d)) _dictRehashStep(d);
    if (dictIsRehashing(d)) {
        unsigned long s0 = DICTHT_SIZE(d->ht_size_exp[0]);
        do {
            /* We are sure there are no elements in indexes from 0
             * to rehashidx-1 */
            h = d->rehashidx + (randomULong() % (dictSlots(d) - d->rehashidx));
            he = (h >= s0) ? d->ht_table[1][h - s0] : d->ht_table[0][h];
        } while(he == NULL);
    } else {
        unsigned long m = DICTHT_SIZE_MASK(d->ht_size_exp[0]);
        do {
            h = randomULong() & m;
            he = d->ht_table[0][h];
        } while(he == NULL);
    }

    /* Now we found a non empty bucket, but it is a linked
     * list and we need to get a random element from the list.
     * The only sane way to do so is counting the elements and
     * select a random index. */
    listlen = 0;
    orighe = he;
    while(he) {
        he = he->next;
        listlen++;
    }
    listele = random() % listlen;
    he = orighe;
    while(listele--) he = he->next;
    return he;
}
```
代码位于``dict.c``第656行  
``dictGetRandomKey``函数用于获取字典的随机条目，
它首先判断字典的大小是否为0，
如果为0，则返回NULL，
否则判断字典是否正在进行rehash，
如果正在进行rehash，则调用``_dictRehashStep``函数进行rehash，
然后判断字典是否正在进行rehash，
如果正在进行rehash，
则首先初始化``s0``为哈希表0的大小，
然后循环遍历哈希表0和哈希表1的所有槽，
首先初始化``h``为rehash索引加上随机数对``dictSlots``减去rehash索引的余数，
然后判断``h``是否大于等于``s0``，
如果大于等于``s0``，
则将哈希表1的第``h``减去``s0``个槽赋值给``he``，
否则将哈希表0的第``h``个槽赋值给``he``，
然后判断``he``是否为NULL，
如果为NULL，
则继续循环遍历哈希表0和哈希表1的所有槽，
否则跳出循环，
如果字典不是正在进行rehash，
则首先初始化``m``为哈希表0的大小掩码，
然后循环遍历哈希表0的所有槽，
首先初始化``h``为随机数与``m``的与运算结果，
然后将哈希表0的第``h``个槽赋值给``he``，
然后判断``he``是否为NULL，
如果为NULL，
则继续循环遍历哈希表0的所有槽，
否则跳出循环，
然后初始化``listlen``为0，
初始化``orighe``为``he``，
然后循环遍历``he``，
首先将``he``的下一个元素赋值给``he``，
然后将``listlen``加1，
然后初始化``listele``为随机数对``listlen``的余数，
然后将``orighe``赋值给``he``，
然后循环遍历``listele``，
首先将``he``的下一个元素赋值给``he``，
然后返回``he``。

## 释放未连接的条目
```c
void dictFreeUnlinkedEntry(dict *d, dictEntry *he) {
    if (he == NULL) return;
    dictFreeKey(d, he);
    dictFreeVal(d, he);
    zfree(he);
}
```
代码位于``dict.c``第467行  
``dictFreeUnlinkedEntry``函数用于释放未连接的条目，


# 随机返回几个字典的键
```c
unsigned int dictGetSomeKeys(dict *d, dictEntry **des, unsigned int count) {
    unsigned long j; /* internal hash table id, 0 or 1. */
    unsigned long tables; /* 1 or 2 tables? */
    unsigned long stored = 0, maxsizemask;
    unsigned long maxsteps;

    if (dictSize(d) < count) count = dictSize(d);
    maxsteps = count*10;

    /* Try to do a rehashing work proportional to 'count'. */
    for (j = 0; j < count; j++) {
        if (dictIsRehashing(d))
            _dictRehashStep(d);
        else
            break;
    }

    tables = dictIsRehashing(d) ? 2 : 1;
    maxsizemask = DICTHT_SIZE_MASK(d->ht_size_exp[0]);
    if (tables > 1 && maxsizemask < DICTHT_SIZE_MASK(d->ht_size_exp[1]))
        maxsizemask = DICTHT_SIZE_MASK(d->ht_size_exp[1]);

    /* Pick a random point inside the larger table. */
    unsigned long i = randomULong() & maxsizemask;
    unsigned long emptylen = 0; /* Continuous empty entries so far. */
    while(stored < count && maxsteps--) {
        for (j = 0; j < tables; j++) {
            /* Invariant of the dict.c rehashing: up to the indexes already
             * visited in ht[0] during the rehashing, there are no populated
             * buckets, so we can skip ht[0] for indexes between 0 and idx-1. */
            if (tables == 2 && j == 0 && i < (unsigned long) d->rehashidx) {
                /* Moreover, if we are currently out of range in the second
                 * table, there will be no elements in both tables up to
                 * the current rehashing index, so we jump if possible.
                 * (this happens when going from big to small table). */
                if (i >= DICTHT_SIZE(d->ht_size_exp[1]))
                    i = d->rehashidx;
                else
                    continue;
            }
            if (i >= DICTHT_SIZE(d->ht_size_exp[j])) continue; /* Out of range for this table. */
            dictEntry *he = d->ht_table[j][i];

            /* Count contiguous empty buckets, and jump to other
             * locations if they reach 'count' (with a minimum of 5). */
            if (he == NULL) {
                emptylen++;
                if (emptylen >= 5 && emptylen > count) {
                    i = randomULong() & maxsizemask;
                    emptylen = 0;
                }
            } else {
                emptylen = 0;
                while (he) {
                    /* Collect all the elements of the buckets found non
                     * empty while iterating. */
                    *des = he;
                    des++;
                    he = he->next;
                    stored++;
                    if (stored == count) return stored;
                }
            }
        }
        i = (i+1) & maxsizemask;
    }
    return stored;
}
```
代码位于``dict.c``文件第718行，
该函数用于随机返回几个字典的键，
该函数的参数``d``为字典，
参数``des``为字典的键数组，
参数``count``为随机返回的键的个数，
首先判断字典的大小是否小于``count``，
如果小于``count``，
则将字典的大小赋值给``count``，
然后初始化``maxsteps``为``count*10``，
然后循环遍历``count``，
首先判断字典是否正在进行rehash，
如果正在进行rehash，
则调用``_dictRehashStep``函数，
否则跳出循环，
然后初始化``tables``为1，
如果字典正在进行rehash，
则将``tables``赋值为2，
然后初始化``maxsizemask``为哈希表0的大小掩码，
然后判断``tables``是否大于1，
如果大于1，
并且``maxsizemask``小于哈希表1的大小掩码，
则将``maxsizemask``赋值为哈希表1的大小掩码，
然后随机生成一个数，
并将该数与``maxsizemask``进行与运算，
然后将结果赋值给``i``，
然后初始化``emptylen``为0，
然后循环遍历``count``和``maxsteps``，
首先循环遍历``tables``，
然后判断``tables``是否等于2，
如果等于2，
并且``j``等于0，
并且``i``小于``rehashidx``，
则判断``i``是否大于等于哈希表1的大小，
如果大于等于哈希表1的大小，
则将``rehashidx``赋值给``i``，
否则跳过该次循环，
然后判断``i``是否大于等于哈希表的大小，
如果大于等于哈希表的大小，
则跳过该次循环，
然后将哈希表``j``的第``i``个元素赋值给``he``，
然后判断``he``是否为空，
如果为空，
则将``emptylen``加1，
然后判断``emptylen``是否大于等于5，
并且``emptylen``大于``count``，
如果满足条件，
则随机生成一个数，
并将该数与``maxsizemask``进行与运算，
然后将结果赋值给``i``，
然后将``emptylen``赋值为0，
否则将``emptylen``赋值为0，
然后判断``he``是否为空，
如果不为空，
则循环遍历``he``，
首先将``he``的值赋值给``des``，
然后将``des``指向下一个元素，
然后将``he``指向下一个元素，
然后将``stored``加1，
然后判断``stored``是否等于``count``，
如果等于``count``，
则返回``stored``，
否则跳过该次循环，
然后将``i``加1与``maxsizemask``进行与运算，
返回``stored``。

# 字典的迭代
```c
unsigned long dictScan(dict *d,
                       unsigned long v,
                       dictScanFunction *fn,
                       dictScanBucketFunction* bucketfn,
                       void *privdata)
{
    int htidx0, htidx1;
    const dictEntry *de, *next;
    unsigned long m0, m1;

    if (dictSize(d) == 0) return 0;

    /* This is needed in case the scan callback tries to do dictFind or alike. */
    dictPauseRehashing(d);

    if (!dictIsRehashing(d)) {
        htidx0 = 0;
        m0 = DICTHT_SIZE_MASK(d->ht_size_exp[htidx0]);

        /* Emit entries at cursor */
        if (bucketfn) bucketfn(d, &d->ht_table[htidx0][v & m0]);
        de = d->ht_table[htidx0][v & m0];
        while (de) {
            next = de->next;
            fn(privdata, de);
            de = next;
        }

        /* Set unmasked bits so incrementing the reversed cursor
         * operates on the masked bits */
        v |= ~m0;

        /* Increment the reverse cursor */
        v = rev(v);
        v++;
        v = rev(v);

    } else {
        htidx0 = 0;
        htidx1 = 1;

        /* Make sure t0 is the smaller and t1 is the bigger table */
        if (DICTHT_SIZE(d->ht_size_exp[htidx0]) > DICTHT_SIZE(d->ht_size_exp[htidx1])) {
            htidx0 = 1;
            htidx1 = 0;
        }

        m0 = DICTHT_SIZE_MASK(d->ht_size_exp[htidx0]);
        m1 = DICTHT_SIZE_MASK(d->ht_size_exp[htidx1]);

        /* Emit entries at cursor */
        if (bucketfn) bucketfn(d, &d->ht_table[htidx0][v & m0]);
        de = d->ht_table[htidx0][v & m0];
        while (de) {
            next = de->next;
            fn(privdata, de);
            de = next;
        }

        /* Iterate over indices in larger table that are the expansion
         * of the index pointed to by the cursor in the smaller table */
        do {
            /* Emit entries at cursor */
            if (bucketfn) bucketfn(d, &d->ht_table[htidx1][v & m1]);
            de = d->ht_table[htidx1][v & m1];
            while (de) {
                next = de->next;
                fn(privdata, de);
                de = next;
            }

            /* Increment the reverse cursor not covered by the smaller mask.*/
            v |= ~m1;
            v = rev(v);
            v++;
            v = rev(v);

            /* Continue while bits covered by mask difference is non-zero */
        } while (v & (m0 ^ m1));
    }

    dictResumeRehashing(d);

    return v;
}
```
代码位于``dict.c``文件第907行，
该函数用于迭代字典，
该函数接收5个参数，
``d``是字典，
``v``是游标，
``fn``是回调函数，
``bucketfn``是桶回调函数，
``privdata``是私有数据，
该函数返回值是``v``。
首先判断字典的大小是否为0，
如果为0，
则返回0，
否则跳过该次循环，
然后调用``dictPauseRehashing``函数暂停字典的rehash，
然后判断字典是否正在rehash，
如果不是，
则将``htidx0``赋值为0，代表``ht_table[0]``，
然后将``m0``赋值为``DICTHT_SIZE_MASK(d->ht_size_exp[htidx0])``，
然后判断``bucketfn``是否为空，
如果不为空，
则调用``bucketfn``函数，
然后将``de``赋值为``d->ht_table[htidx0][v & m0]``，
然后判断``de``是否为空，
如果不为空，
则将``next``赋值为``de->next``，
然后调用``fn``函数，
然后将``de``赋值为``next``，
然后将``v``与``~m0``进行或运算，
然后将``v``赋值为``rev(v)``，
然后将``v``加1，
然后将``v``赋值为``rev(v)``，
如果字典正在rehash，
则将``htidx0``赋值为0，代表``ht_table[0]``，
然后将``htidx1``赋值为1，代表``ht_table[1]``，
然后判断``DICTHT_SIZE(d->ht_size_exp[htidx0])``是否大于``DICTHT_SIZE(d->ht_size_exp[htidx1])``，
如果大于，
则将``htidx0``赋值为1，代表``t0``是较小的表，
然后将``htidx1``赋值为0，代表``t1``是较大的表，
然后将``m0``赋值为``DICTHT_SIZE_MASK(d->ht_size_exp[htidx0])``，
然后将``m1``赋值为``DICTHT_SIZE_MASK(d->ht_size_exp[htidx1])``，
然后判断``bucketfn``是否为空，
如果不为空，
则调用``bucketfn``函数，
然后将``de``赋值为``d->ht_table[htidx0][v & m0]``，
然后判断``de``是否为空，
如果不为空，
则将``next``赋值为``de->next``，
然后调用``fn``函数，
然后将``de``赋值为``next``，
然后将``v``与``~m1``进行或运算，
然后将``v``赋值为``rev(v)``，
然后将``v``加1，
然后将``v``赋值为``rev(v)``，
然后判断``v``与``(m0 ^ m1)``进行与运算的结果是否为0，
如果不为0，
则跳过该次循环，
否则跳出循环，
然后调用``dictResumeRehashing``函数恢复字典的rehash，
最后返回``v``。

# 字典使用指针查找dictEntry引用
```c
dictEntry **dictFindEntryRefByPtrAndHash(dict *d, const void *oldptr, uint64_t hash) {
    dictEntry *he, **heref;
    unsigned long idx, table;

    if (dictSize(d) == 0) return NULL; /* dict is empty */
    for (table = 0; table <= 1; table++) {
        idx = hash & DICTHT_SIZE_MASK(d->ht_size_exp[table]);
        heref = &d->ht_table[table][idx];
        he = *heref;
        while(he) {
            if (oldptr==he->key)
                return heref;
            heref = &he->next;
            he = *heref;
        }
        if (!dictIsRehashing(d)) return NULL;
    }
    return NULL;
}
```
代码位于``dict.c``文件第1098行，
该函数用于查找指针``oldptr``对应的``dictEntry``的引用，
首先判断字典的大小是否为0，
如果为0，
则返回NULL，
否则进入循环，
首先将``idx``赋值为``hash``与``DICTHT_SIZE_MASK(d->ht_size_exp[table])``进行与运算的结果，
然后将``heref``赋值为``d->ht_table[table][idx]``，
然后将``he``赋值为``*heref``，
然后判断``he``是否为空，
如果不为空，
则判断``oldptr``是否等于``he->key``，
如果等于，
则返回``heref``，
否则将``heref``赋值为``he->next``，
然后将``he``赋值为``*heref``，
然后判断``he``是否为空，
如果不为空，
则跳过该次循环，
否则判断字典是否正在rehash，
如果不是，
则返回NULL，
否则将``table``加1，
然后判断``table``是否大于1，
如果大于1，
则返回NULL，
否则跳过该次循环，
最后返回NULL。

# 调试
## 字典信息获取
```c
size_t _dictGetStatsHt(char *buf, size_t bufsize, dict *d, int htidx) {
    unsigned long i, slots = 0, chainlen, maxchainlen = 0;
    unsigned long totchainlen = 0;
    unsigned long clvector[DICT_STATS_VECTLEN];
    size_t l = 0;

    if (d->ht_used[htidx] == 0) {
        return snprintf(buf,bufsize,
            "No stats available for empty dictionaries\n");
    }

    /* Compute stats. */
    for (i = 0; i < DICT_STATS_VECTLEN; i++) clvector[i] = 0;
    for (i = 0; i < DICTHT_SIZE(d->ht_size_exp[htidx]); i++) {
        dictEntry *he;

        if (d->ht_table[htidx][i] == NULL) {
            clvector[0]++;
            continue;
        }
        slots++;
        /* For each hash entry on this slot... */
        chainlen = 0;
        he = d->ht_table[htidx][i];
        while(he) {
            chainlen++;
            he = he->next;
        }
        clvector[(chainlen < DICT_STATS_VECTLEN) ? chainlen : (DICT_STATS_VECTLEN-1)]++;
        if (chainlen > maxchainlen) maxchainlen = chainlen;
        totchainlen += chainlen;
    }

    /* Generate human readable stats. */
    l += snprintf(buf+l,bufsize-l,
        "Hash table %d stats (%s):\n"
        " table size: %lu\n"
        " number of elements: %lu\n"
        " different slots: %lu\n"
        " max chain length: %lu\n"
        " avg chain length (counted): %.02f\n"
        " avg chain length (computed): %.02f\n"
        " Chain length distribution:\n",
        htidx, (htidx == 0) ? "main hash table" : "rehashing target",
        DICTHT_SIZE(d->ht_size_exp[htidx]), d->ht_used[htidx], slots, maxchainlen,
        (float)totchainlen/slots, (float)d->ht_used[htidx]/slots);

    for (i = 0; i < DICT_STATS_VECTLEN-1; i++) {
        if (clvector[i] == 0) continue;
        if (l >= bufsize) break;
        l += snprintf(buf+l,bufsize-l,
            "   %ld: %ld (%.02f%%)\n",
            i, clvector[i], ((float)clvector[i]/DICTHT_SIZE(d->ht_size_exp[htidx]))*100);
    }

    /* Unlike snprintf(), return the number of characters actually written. */
    if (bufsize) buf[bufsize-1] = '\0';
    return strlen(buf);
}
```
代码位于``dict.c``文件第1121行，
该函数用于获取字典的统计信息，
输出到``buf``中，
统计信息含有：
- ``table size``：字典的大小
- ``number of elements``：字典中的元素数量
- ``different slots``：字典中不同的槽的数量
- ``max chain length``：字典中链表的最大长度
- ``avg chain length (counted)``：字典中链表的平均长度（计算得到）
- ``avg chain length (computed)``：字典中链表的平均长度（统计得到）
- ``Chain length distribution``：字典中链表的长度分布  
同时存在
```c
void dictGetStats(char *buf, size_t bufsize, dict *d) {
    size_t l;
    char *orig_buf = buf;
    size_t orig_bufsize = bufsize;

    l = _dictGetStatsHt(buf,bufsize,d,0);
    buf += l;
    bufsize -= l;
    if (dictIsRehashing(d) && bufsize > 0) {
        _dictGetStatsHt(buf,bufsize,d,1);
    }
    /* Make sure there is a NULL term at the end. */
    if (orig_bufsize) orig_buf[orig_bufsize-1] = '\0';
}
```
代码位于``dict.c``文件第1181行，
也是为了获取字典的统计信息，
但是该函数会判断字典是否正在rehash，
如果正在rehash，
则会获取rehash的字典的统计信息。

# 字典的基准
## 基准测试
```c
int dictTest(int argc, char **argv, int flags) {
    long j;
    long long start, elapsed;
    dict *dict = dictCreate(&BenchmarkDictType);
    long count = 0;
    int accurate = (flags & REDIS_TEST_ACCURATE);

    if (argc == 4) {
        if (accurate) {
            count = 5000000;
        } else {
            count = strtol(argv[3],NULL,10);
        }
    } else {
        count = 5000;
    }

    start_benchmark();
    for (j = 0; j < count; j++) {
        int retval = dictAdd(dict,stringFromLongLong(j),(void*)j);
        assert(retval == DICT_OK);
    }
    end_benchmark("Inserting");
    assert((long)dictSize(dict) == count);

    /* Wait for rehashing. */
    while (dictIsRehashing(dict)) {
        dictRehashMilliseconds(dict,100);
    }

    start_benchmark();
    for (j = 0; j < count; j++) {
        char *key = stringFromLongLong(j);
        dictEntry *de = dictFind(dict,key);
        assert(de != NULL);
        zfree(key);
    }
    end_benchmark("Linear access of existing elements");

    start_benchmark();
    for (j = 0; j < count; j++) {
        char *key = stringFromLongLong(j);
        dictEntry *de = dictFind(dict,key);
        assert(de != NULL);
        zfree(key);
    }
    end_benchmark("Linear access of existing elements (2nd round)");

    start_benchmark();
    for (j = 0; j < count; j++) {
        char *key = stringFromLongLong(rand() % count);
        dictEntry *de = dictFind(dict,key);
        assert(de != NULL);
        zfree(key);
    }
    end_benchmark("Random access of existing elements");

    start_benchmark();
    for (j = 0; j < count; j++) {
        dictEntry *de = dictGetRandomKey(dict);
        assert(de != NULL);
    }
    end_benchmark("Accessing random keys");

    start_benchmark();
    for (j = 0; j < count; j++) {
        char *key = stringFromLongLong(rand() % count);
        key[0] = 'X';
        dictEntry *de = dictFind(dict,key);
        assert(de == NULL);
        zfree(key);
    }
    end_benchmark("Accessing missing");

    start_benchmark();
    for (j = 0; j < count; j++) {
        char *key = stringFromLongLong(j);
        int retval = dictDelete(dict,key);
        assert(retval == DICT_OK);
        key[0] += 17; /* Change first number to letter. */
        retval = dictAdd(dict,key,(void*)j);
        assert(retval == DICT_OK);
    }
    end_benchmark("Removing and adding");
    dictRelease(dict);
    return 0;
}
```
代码位于``dict.c``文件第1252行，
该函数用于测试字典的性能，
测试的内容有：
- 现有元素的线性访问
- 随机访问现有元素
- 访问随机密钥
- 删除和添加

## 基准测试基础
```c
void start_benchmark(void) {
    start = ustime();
}
void end_benchmark(char *title) {
    elapsed = ustime()-start;
    printf("%s: %lld microseconds\n", title, elapsed);
}
uint64_t hashCallback(const void *key) {
    return dictGenHashFunction((unsigned char*)key, strlen((char*)key));
}

int compareCallback(dict *d, const void *key1, const void *key2) {
    int l1,l2;
    UNUSED(d);

    l1 = strlen((char*)key1);
    l2 = strlen((char*)key2);
    if (l1 != l2) return 0;
    return memcmp(key1, key2, l1) == 0;
}

void freeCallback(dict *d, void *val) {
    UNUSED(d);

    zfree(val);
}

char *stringFromLongLong(long long value) {
    char buf[32];
    int len;
    char *s;

    len = snprintf(buf,sizeof(buf),"%lld",value);
    s = zmalloc(len+1);
    memcpy(s, buf, len);
    s[len] = '\0';
    return s;
}

dictType BenchmarkDictType = {
    hashCallback,
    NULL,
    NULL,
    compareCallback,
    freeCallback,
    NULL,
    NULL
}
```
代码位于``dict.c``文件第1203行，
该函数为基准测试提供了一些基础函数，
包括：
- ``start_benchmark``函数用于记录开始时间
- ``end_benchmark``函数用于记录结束时间并打印时间差
- ``hashCallback``函数用于计算哈希值
- ``compareCallback``函数用于比较两个键是否相等
- ``freeCallback``函数用于释放键值对
- ``stringFromLongLong``函数用于将整数转换为字符串
- ``BenchmarkDictType``结构体用于初始化字典

# 结语  
本文介绍了``Redis``的字典实现，其中很多操作都是基于哈希表的。想要读懂``Redis``中``dict.c``的源码，必须要对哈希表有一定的了解。``dict.c``让c语言的指针变得更加灵活，让c语言的结构体变得更加强大。实现了其它语言中内置的字典功能，让c语言也可以实现类似的功能。  
本文中的代码都是基于``Redis 7.0.5``版本的，如果有错误，欢迎指正。


---
你可以在通过如下方式联系我：
- [邮箱](apexleapsean@gmail.com):apexleapsean@gmail.com
- [QQ](592841725):592841725
---
  



























