import struct
import os
import plistlib
 
# 拼音表偏移，
startPy = 0x1540
 
# 汉语词组表偏移
startChinese = 0x2628

# 空字符
chrEmpty = chr(0)
 
# 全局拼音表
GPy_Table = {}
 
# 解析结果
# 元组(词频,拼音,中文词组)的列表
GTable = []

# 将字节转化为小端
def littleEndian(data):
    return struct.unpack('H', data)[0]
 
# 原始字节码转为字符串
def byte2str(data):
    pos = 0
    str = ''
    while pos < len(data):
        c = chr(littleEndian(data[pos:pos+2]))
        if c != chrEmpty:
            str += c
        pos += 2
    return str
 
# 获取拼音表
def getPyTable(data):
    data = data[4:]
    pos = 0
    while pos < len(data):
        index = littleEndian(data[pos:pos+2])
        pos += 2
        lenPy = littleEndian(data[pos:pos+2])
        pos += 2
        py = byte2str(data[pos:pos+lenPy])
        GPy_Table[index] = py
        pos += lenPy
 
# 获取一个词组的拼音
def getWordPy(data):
    pos = 0
    ret = ''
    while pos < len(data):
        index = littleEndian(data[pos:pos+2])
        ret += GPy_Table[index]
        pos += 2
    return ret
 
# 读取中文表
def getChinese(data):
    pos = 0
    while pos < len(data):
        # 同音词数量
        same = littleEndian(data[pos:pos+2])
 
        # 拼音索引表长度
        pos += 2
        py_table_len = littleEndian(data[pos:pos+2])
 
        # 拼音索引表
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len])
 
        # 中文词组
        pos += py_table_len
        for i in range(same):
            # 中文词组长度
            c_len = littleEndian(data[pos:pos+2])
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = littleEndian(data[pos:pos+2])
            # 词频
            pos += 2
            count = littleEndian(data[pos:pos+2])
 
            # 保存
            GTable.append((count, py, word))
 
            # 到下个词的偏移位置
            pos += ext_len
 
 
def scel2txt(file_name):
    # 分隔符
    print('-' * 60)
    # 读取文件
    with open(file_name, 'rb') as f:
        data = f.read()
 
    print("词库名：", byte2str(data[0x130:0x338])) # .encode('GB18030')
    print("词库类型：", byte2str(data[0x338:0x540]))
    print("描述信息：", byte2str(data[0x540:0xd40]))
    print("词库示例：", byte2str(data[0xd40:startPy]))
 
    getPyTable(data[startPy:startChinese])
    getChinese(data[startChinese:])

def genPlist(file_name):
    pairs = []
    for count, py, word in GTable:
        pairs.append({"phrase": word, "shortcut": py})
    with open(file_name, 'wb') as f:
        plistlib.dump(pairs, f)

if __name__ == '__main__':
 
    # scel所在文件夹路径
    in_path = "dict"
 
    fin = [fname for fname in os.listdir(in_path) if fname[-5:] == ".scel"]
    for f in fin:
        f = os.path.join(in_path, f)
        scel2txt(f)

    genPlist("output.plist")        
    # f = open('./coal_dict.txt', 'w')
    # for count, py, word in GTable:
    #     f.write(str(count)+ '\t\t\t' + py + '\t\t\t' + word + '\n')
    # f.close()