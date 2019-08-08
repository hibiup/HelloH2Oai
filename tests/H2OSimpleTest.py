import unittest
import h2o


class H2OSimpleTest(unittest.TestCase):
    """
    参考：http://docs.h2o.ai/h2o/latest-stable/h2o-docs/starting-h2o.html
    """
    def test_h2o_init(self):
        """
        init方法首先尝试连接服务端，如果没有可连接的服务器就会在本地启动一个。

        返回信息如下：

        Checking whether there is an H2O instance running at http://localhost:54323 . connected.
        --------------------------  ------------------------------------------
        。。。
        H2O cluster name:           MyH2OCluster
        H2O cluster total nodes:    3
        H2O cluster free memory:    6 Gb
        ...
        H2O connection url:         http://localhost:54323
        ...
        --------------------------  ------------------------------------------
        """
        h2o.init(ip='localhost', port='54323',
                 name='MyH2OCluster'  # Cluster name, 可选. 如果指定了该名称客户端会检查是否与登录的 Cluster 匹配。
        )

        """
        航班信息分析案例：
        
        allyears2k_headers.zip 是一个测试数据集，包含各年份航班信息，内容如下：
        
        Year,Month,DayofMonth,DayOfWeek,DepTime,CRSDepTime,ArrTime,CRSArrTime,UniqueCarrier,FlightNum,TailNum,ActualElapsedTime,CRSElapsedTime,AirTime,ArrDelay,DepDelay,Origin,Dest,Distance,TaxiIn,TaxiOut,Cancelled,CancellationCode,Diverted,CarrierDelay,WeatherDelay,NASDelay,SecurityDelay,LateAircraftDelay,IsArrDelayed,IsDepDelayed
        1987,10,14,3,741,730,912,849,PS,1451,NA,91,79,NA,23,11,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,YES,YES
        1987,10,15,4,729,730,903,849,PS,1451,NA,94,79,NA,14,-1,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,YES,NO
        1987,10,17,6,741,730,918,849,PS,1451,NA,97,79,NA,29,11,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,YES,YES
        1987,10,18,7,729,730,847,849,PS,1451,NA,78,79,NA,-2,-1,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,NO,NO
        1987,10,19,1,749,730,922,849,PS,1451,NA,93,79,NA,33,19,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA,YES,YES
        ...
        
        1.  载入数据
        
        import_file() 函数以服务器当地为参照地址载入数据文件。支持 HTTP 或 HDFS url
        upload_file() 以客户点本地为参照上载数据文件。
        
        数据集处理的基本API可参考：http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-munging.html
        """
        # airlines = h2o.import_file("allyears2k_headers.zip")
        airlines = h2o.upload_file("allyears2k_headers.zip")

        """
        2. 指定＂因子(factor)＂字段．关于 factor 的解释参考：https://www.zhihu.com/question/48472404
        
        H2O支持的算法参考：http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science.html
        """
        airlines['Year'] = airlines['Year'].asfactor()
        airlines['Month'] = airlines['Month'].asfactor()
        airlines['DayOfWeek'] = airlines['DayOfWeek'].asfactor()
        airlines['Cancelled'] = airlines['Cancelled'].asfactor()
        airlines['FlightNum'] = airlines['FlightNum'].asfactor()

        """
        3. 设置要预测的字段和 response 字段
        """
        predictors = ['Origin', 'Dest', 'Year', 'UniqueCarrier', 'DayOfWeek', 'Month', 'Distance', 'FlightNum']
        response = 'IsDepDelayed'

        """
        4. 分割数据集
        """
        train, valid = airlines.split_frame(ratios=[0.8], seed=1234)

        """
        5. ...
        """
        bin_num = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
        label = ['8', '16', '32', '64', '128', '256', '512', '1024', '2048', '4096']

        from h2o.estimators import H2OGradientBoostingEstimator
        for key, num in enumerate(bin_num):
            airlines_gbm = H2OGradientBoostingEstimator(nbins_cats=num, seed=1234)
            airlines_gbm.train(x=predictors, y=response, training_frame=train, validation_frame=valid)

        print(label[key], 'training score', airlines_gbm.auc(train=True))
        print(label[key], 'validation score', airlines_gbm.auc(valid=True))
