### Lexicon
将搜狗词库 scel 文件转换为 macOS 词库的 plist 文件。

从 https://pinyin.sogou.com/dict/ 下载所需的词库，放入 dict 文件夹，运行 main.py 即可。

打开 偏好设置>键盘>文本，先做好备份，再将产生的 plist 文件拖入即可，此时系统会有比较高的 CPU 占用。

并且注意词库是会随着 iCloud 同步的。





解析 scel 的代码来自 https://github.com/CQiang27/Spark_Python

