def toAbstract(srtUrl):
    a = 1
    b = 2
    c = 3
    state = a
    text = ''
    with open(srtUrl, 'r', encoding='utf-8') as f:  # 打开srt字幕文件，并去掉文件开头的\ufeff
        for line in f.readlines():  # 遍历srt字幕文件
            if state == a:  # 跳过第一行
                state = b
            elif state == b:  # 跳过第二行
                state = c
            elif state == c:  # 读取第三行字幕文本
                if len(line.strip()) != 0:
                    text += ' ' + line.strip()  # 将同一时间段的字幕文本拼接
                    state = c
                elif len(line.strip()) == 0:
                    with open('test1.txt', 'a', encoding='utf8') as fa:  # 写入txt文本文件中
                        text2 = text.replace(
                            'Conversion failed', '')
                        text2 = text2.replace(
                            '<font color=#FF0000>', '')
                        fa.write(text2.replace('\n', ''))
                        text = '\n'
                        state = a
                        fa.close()
    import codecs
    from textrank4zh import TextRank4Keyword, TextRank4Sentence
    # 读取文件
    text = codecs.open('test1.txt', 'r', encoding='utf8').read()
    # 关键词和关键短语
    tr4w = TextRank4Keyword()
    tr4w.analyze(text)

    print('关键词：')
    for item in tr4w.get_keywords(num=5, word_min_len=2):  # 提取5个关键词，关键词最少为2个字
        print(item.word, '权重:', item.weight)
    print()

    print('关键短语：')
    # 从20个关键词中选出出现次数至少为2的关键短语
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        print(phrase)
    print()

    # 摘要
    tr4s = TextRank4Sentence()
    tr4s.analyze(text)
    print('摘要：')
    for item in tr4s.get_key_sentences(num=3):
        # index是语句在文本中位置，weight是权重
        print(item.index, item.weight, '\n  ', item.sentence, '\n')

        # -*- encoding:utf-8 -*-

        import codecs
        from textrank4zh import TextRank4Keyword, TextRank4Sentence

        text = codecs.open('./text/01.txt', 'r', 'utf-8').read()
        tr4w = TextRank4Keyword(stop_words_file='./stopword.data')  # 导入停止词

        # 使用词性过滤，文本小写，窗口为2
        tr4w.train(text=text, speech_tag_filter=True, lower=True, window=2)