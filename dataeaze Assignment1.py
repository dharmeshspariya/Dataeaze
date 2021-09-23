#source d1.1/bin/activate
#pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
import pyspark.sql.functions as f
spark = SparkSession.builder.appName("MyFirstCSVLoad").getOrCreate()
df1 = spark.read.csv(path="startup.csv",sep=",",header=True,quote='"',inferSchema=True,)
df2 = spark.read.load("consumerInternet.parquet")
# Assignment 1
df11 = df1.union(df2)
df11.registerTempTable("emp1")
df11=spark.sql("select count(*) from emp1 where city ='Pune'")
df11.write.option("header","true").csv("/home/ubuntu/Desktop/Dataeaze/output/output1")

# Assignment 2
df12 = df1.union(df2)
df12.registerTempTable("emp2")
df12=spark.sql("select count(*) from employees where InvestmentnType ='Seed/ Angel Funding'")
df12.write.option("header","true").csv("/home/ubuntu/Desktop/Dataeaze/output/output2")

# Assignment 3
df3 = df1.union(df2)
df3.registerTempTable("emp3")
df3=spark.sql("select sum(regexp_replace(regexp_replace(Amount_in_USD,'N/A','0'),',','')) as Amount from emp3 where City='Pune'")
df3.write.option("header","true").csv("/home/ubuntu/Desktop/Dataeaze/output/output3")

# Assignment 4
df4 = df1.union(df2)
df4.registerTempTable("emp4")
df4=spark.sql("select Sr_No,replace(Industry_Vertical,('\\\\\'),'') Industry_Vertical from emp4")
df4.registerTempTable("emp4")
df4=spark.sql("select Sr_No,replace(replace(replace(Industry_Vertical,'xe2x80x93',''),'xe2x80x99',''),'xc2xa0','') Industry_Vertical from emp4")
df4.registerTempTable("emp4")
df4=spark.sql("select Industry_Vertical, count(Industry_Vertical) as total from emp4 GROUP BY Industry_Vertical ORDER BY total DESC LIMIT 5 ")
df4.write.option("header","true").csv("/home/ubuntu/Desktop/Dataeaze/output/output4")

# Assignment 5
df5 = df1.union(df2)
df5.registerTempTable("emp5")
df5=spark.sql("select Sr_No,replace(Date,('\\\\\'),'') as Date,replace(Investors_Name,('\\\\\'),'') as Investors_Name,replace(Amount_in_USD,('\\\\\'),'') as Amount from emp5")
df5.registerTempTable("emp5")
df5=spark.sql("select Sr_No,replace(replace(replace(Date,'xe2x80x93',''),'xe2x80x99',''),'xc2xa0','') as Date,replace(replace(replace(Investors_Name,'xe2x80x93',''),'xe2x80x99',''),'xc2xa0','') as Investors_Name,replace(replace(replace(Amount,'xe2x80x93',''),'xe2x80x99',''),'xc2xa0','') as Amount from emp5")
df5.registerTempTable("emp5")
df5=spark.sql("select Sr_No,Date,Investors_Name, regexp_replace(Amount, '[^0-9]+', '') as Amount from emp5")
df5.registerTempTable("emp5")
df6 = df5.withColumn('years',f.year(f.to_timestamp('date', 'dd/MM/yyyy')))
df6.registerTempTable("emp6")
df6=spark.sql("select Sr_No,Investors_Name,Amount,years from emp6")
df6.registerTempTable("emp6")
from pyspark.sql.types import IntegerType
df7 = df6.withColumn("Amount", df6["Amount"].cast(IntegerType()))
df7.registerTempTable("emp7")
spark.sql("select Investors_Name, years, Amount from "+" (select *, row_number() OVER (PARTITION BY years ORDER BY Amount DESC) as rn "+" FROM emp7) tmp where rn = 1").show()
#spark.sql("SELECT Investors_Name,years, MAX(Amount) FROM emp7 GROUP BY years").show()


