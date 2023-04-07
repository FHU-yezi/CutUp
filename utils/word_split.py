from jieba import enable_parallel
from sspeedup.word_split.jieba import (
    JiebaPossegSplitter,
    JiebaSearchSplitter,
    JiebaSplitter,
)

enable_parallel(2)

jieba_spliter = JiebaSplitter(
    stopwords_file="word_split_assets/stopwords.txt",
    hotwords_file="word_split_assets/hotwords.txt",
)
jieba_search_spliter = JiebaSearchSplitter(
    stopwords_file="word_split_assets/stopwords.txt",
    hotwords_file="word_split_assets/hotwords.txt",
)
jieba_posseg_spliter = JiebaPossegSplitter(
    stopwords_file="word_split_assets/stopwords.txt",
    hotwords_file="word_split_assets/hotwords.txt",
)
