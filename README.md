## 服务器

H2O 以C/S模式运行，首先需要启动一个服务端：

```bash
cd ~/Downloads
unzip h2o-3.24.0.3.zip
cd h2o-3.24.0.3
java -jar h2o.jar
```
缺省将启动一个服务在 <http://localhost:54321>

### 认证

缺省的 H2O 服务允许匿名访问, 设置访问认证参考该地址: <http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html#authentication-options> 

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
* <http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html#h2o-options>
* <http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html#clouding-up-cluster-creation>

### H2O on Spark/HDFS

H2O 通过名为 Sparkling Water 的组件来将计算投送到 Spark 去进行分布式运算。Sparkling Water 
可以以多种方式集成并管理 H2O. 它以 Spark 应用程序（Spark driver）的方式来运行。

缺省模式下，Sparkling Water 自动管理 H2O Server, 用户只需和 Sparkling Water 打交道即可。
Sparkling Water 通过两种方式与 Spark Cluster 集成并在 Spark Cluster 内启动 H2O Server：

`Internal backend` 模式下的 Sparkling Water 启动后会在每一个 Spark executor 中启动 H2O 
Service, 然后通过 H2OContext 来保持 driver 与 H2O cluster 和 Spark 三方之间的通讯。

External backend 模式下的 Sparkling Water 会保持 H2O service 和 Spark 分开以避免相互干扰。

也可以将 H2O service 和 Sparkling Water 分开，手动实现两者的连接. 手动方式下 H2O Server 
只能以 External backend 的方式管理。

参考《SparklingWaterBooklet》文档第16页开始的说明，《SparklingWaterBooklet》下载地址：

* <http://h2o-release.s3.amazonaws.com/h2o/rel-yau/2/docs-website/h2o-docs/booklets/SparklingWaterBooklet.pdf>

Sparkling Water 下载地址：<https://s3.amazonaws.com/h2o-release/sparkling-water/spark-2.4/3.26.2-2.4/index.html>

`External backend` 模式不能直接使用下载的 h2o.jar, 需要使用 Sparkling Water/bin 目录下的 `get-extendend-h2o.sh`
并指定 CDH 发行版本号或 `standalone` 作为参数下载相应的 jar 文件，然后以此 jar 作为连接外部 h2o cluster
的可执行文件。

为简单起见，以下仅以 `Internal backend` 为例简单介绍如何使用 Sparkling Water:

#### Sparkling Water for Spark（local模式）

Sparkling Water for Spark local，适合本地开发时使用。(非 Windows)

设置 Spark 环境变量：
~~~bash
$ export MASTER="local[*]"
$ export SPARK_HOME="/path/to/spark/installation"
~~~

如果在 windows 上使用 spark_with_hadoop 做本地开发环境，还需要设置：
~~~bash
$ export HADOOP_HOME="/path/to/spark/installation"
~~~

然后启动 local 模式下的 Sparkling Water 命令行环境来代替 Spark-shell：
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

#### Sparkling Water for Spark over YARN

Sparkling Water for Spark over YARN 可以使用 YARN Cluster 的计算能力。

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
* <http://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/install/install_and_start.html>
* <https://www.h2o.ai/blog/sparkling-water-on-yarn-example/>

其他参考地址：
* <ttp://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/index.html>
* <http://docs.h2o.ai/h2o/latest-stable/h2o-docs/welcome.html#getting-started-with-sparkling-water>

#### pysparkling

sparkling-shell 打开的是 Sbt 环境，默认使用 Scala 作为开发语言，如果希望使用 Python 作为开发语言，
可以使用 `pysparkling` 命令，所有环境配置都和 `sparkling-shell` 一样，只是进入后的 shell 换成 Python。

使用参考：
http://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/pysparkling.html#pysparkling-and-spark-version

## 客户端

参考 tests 下的测试案例
