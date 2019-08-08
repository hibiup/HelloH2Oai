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

### H2O and Spark/HDFS

H2O 通过名为 Sparkling Water 的组件来将计算投送到 Spark 上去进行分布式运算。(http://docs.h2o.ai/sparkling-water/2.3/latest-stable/doc/index.html)

## 客户端

参考 tests 下的测试案例
