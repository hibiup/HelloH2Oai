## 服务器

H2O 以C/S模式运行，首先需要启动一个服务端：

```bash
cd ~/Downloads
unzip h2o-3.24.0.3.zip
cd h2o-3.24.0.3
java -jar h2o.jar
```
缺省将启动一个服务在 http://localhost:54321

### 认证

缺省的 H2O 服务允许匿名访问, 设置访问认证参考该地址: http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html#authentication-options 

### Cluster

多个 H2O 实例可以组成 Cluster。以下在本地启动一个名为 `MyH2OCluster` 的 Cluster(同一个 cluster 名称必须相同)，每个节点分配 2G 内存:
```bash
$ java -Xmx2g -jar h2o.jar -name MyH2OCluster -port 54321
$ java -Xmx2g -jar h2o.jar -name MyH2OCluster -port 54322
$ java -Xmx2g -jar h2o.jar -name MyH2OCluster -port 54323
```

可以不指定端口，h2o会自动从 54322 开始寻找空闲端口。如果各实例启动在不同主机上， H2O Cluster 支持通过广播（multicast based）或 Flatfile based 两种模式找到其他节点。

* Multicast: 通过参数 `-network <ip_address>/<mask>` 来启动 h2o.jar。例如：`-network 178.0.0.0/8`
* Flatfile: 将主机IP地址罗列在一个文本文件中，然后通过 `-flatfile <file_name>` 传递个 h2o.jar

Flatfile 格式如下：
```
192.168.1.163:54321
192.168.1.164:54321
```

参考地址：
* http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html#h2o-options
* http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html#clouding-up-cluster-creation

### H2O on Spark/HDFS

H2O 通过名为 Sparkling Water 的组件来将计算投送到 Spark 去进行分布式运算。Sparkling Water 以 Spark 的客户端代理的方式运行在本地。
下载地址：https://s3.amazonaws.com/h2o-release/sparkling-water/spark-2.4/3.26.2-2.4/index.html

#### Sparkling Water for Spark（local模式）

Sparkling Water for Spark local，适合本地开发时使用。(非 Windows)

设置 Spark 环境变量：

~~~bash
$ export SPARK_HOME="/path/to/spark/installation" 
$ export MASTER="local[*]" 
~~~

启动 local 模式下的 Sparkling Water 命令行环境来代替 Spark-shell：
~~~bash
$ cd sparkling-water-3.26.2-2.3
$ bin/sparkling-shell --conf "spark.executor.memory=1g"
~~~

#### Sparkling Water for Spark(Standalone)

设置 Spark 环境变量：

~~~bash
$ export SPARK_HOME="/path/to/spark/installation" 
$ export MASTER="spark://localhost:7077"
~~~

启动 Sparkling Water 命令行环境来代替 Spark-shell：
~~~bash
$ cd sparkling-water-3.26.2-2.3
$ bin/sparkling-shell
~~~

#### Sparkling Water for HDFS/YARN (集群计算模式)

Sparkling Water for HDFS/YARN 可以使用 YARN Cluster 的计算能力。

设置 HADOOP 环境变量：

~~~bash
$ export SPARK_HOME='/path/to/spark/installation'
$ export HADOOP_CONF_DIR=/etc/hadoop/conf
$ export MASTER="yarn"                    # yarn cluster
或
$ export MASTER="yarn-client"             # yarn client
~~~

启动 yarn cluster 模式下的 Sparkling Water 的命令行环境来代替 Spark-shell

~~~bash
$ cd sparkling-water-3.26.2-2.3/
$ bin/sparkling-shell --num-executors 3 --executor-memory 2g --master yarn --deploy-mode client
~~~

#### Sparkling Water as Spark package

以上模式中 Sparkling Water 都运行在本地，Sparkling Water as Spark package 允许将 Sparkling Water 以包的形式运行在 Spark cluster 内：

设置 Spark 环境变量：

~~~bash
$ export SPARK_HOME="/path/to/spark/installation" 
$ export MASTER="spark://localhost:7077"  # standalone
或
$ export MASTER="yarn"                    # yarn cluster
或
$ export MASTER="yarn-client"             # yarn client
~~~

在 Spark-cluster 中启动 Sparkling Water:
~~~bash
$ SPARK_HOME/bin/spark-shell --packages ai.h2o:sparkling-water-package_2.11:3.26.2-2.3
~~~ 

以上配置参考：
* http://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/install/install_and_start.html
* https://www.h2o.ai/blog/sparkling-water-on-yarn-example/

其他参考地址：
* ttp://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/index.html
* http://docs.h2o.ai/h2o/latest-stable/h2o-docs/welcome.html#getting-started-with-sparkling-water

## 客户端

参考 tests 下的测试案例
