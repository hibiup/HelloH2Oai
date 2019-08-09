import unittest, os
import h2o

from pyspark import SparkContext
from operator import add

"""
下载 `winutils.exe` (https://github.com/cdarlint/winutils) 到 SPARK_HOME/bin 目录下。
并设置以下环境变量指向 `Spark_with_hadoop`.
"""


os.environ["SPARK_HOME"] = """C:/DevApps/Spark/spark-2.4.3-bin-hadoop2.7"""
os.environ["HADOOP_HOME"] = """C:/DevApps/Spark/spark-2.4.3-bin-hadoop2.7"""


class PySparklingTest(unittest.TestCase):
    def test_PySpark(self):
        """
         以下测试将以 local 模式运行在本地 Spark 中。
        """
        sc = SparkContext()
        data = sc.parallelize(list("Hello World"))
        counts = data.map(lambda x: (x, 1)).reduceByKey(add).sortBy(lambda x: x[1], ascending=False).collect()
        for (word, count) in counts:
            print("{}: {}".format(word, count))
        sc.stop()


if __name__ == '__main__':
    unittest.main()
