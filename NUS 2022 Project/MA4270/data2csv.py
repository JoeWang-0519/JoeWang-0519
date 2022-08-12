import pandas as pd
import numpy as np
'''
data1=pd.io.stata.read_stata('/Users/wangjiangyi/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/a5fbb78a4ca6d25f20f82111c22fdefd/Message/MessageTemp/d438e0a5c0459328eb7479e8f2056980/OpenData/131133/25ad3ba4c863382d48c5053a14b4df88/primedata/cfps2014adult_201906.dta', convert_categoricals=False)
data1.to_csv('/Users/wangjiangyi/Desktop/adult.csv')
data2=pd.io.stata.read_stata('/Users/wangjiangyi/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/a5fbb78a4ca6d25f20f82111c22fdefd/Message/MessageTemp/d438e0a5c0459328eb7479e8f2056980/OpenData/131133/25ad3ba4c863382d48c5053a14b4df88/primedata/cfps2018famconf_202008.dta', convert_categoricals=False)
data2.to_csv('/Users/wangjiangyi/Desktop/familly.csv')
data3=pd.io.stata.read_stata('/Users/wangjiangyi/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/a5fbb78a4ca6d25f20f82111c22fdefd/Message/MessageTemp/d438e0a5c0459328eb7479e8f2056980/OpenData/131133/25ad3ba4c863382d48c5053a14b4df88/primedata/cfps2018person_202012.dta', convert_categoricals=False)
data3.to_csv('/Users/wangjiangyi/Desktop/person.csv')
'''
data4=pd.io.stata.read_stata('/Users/wangjiangyi/Downloads/小珠桃子/处理数据/14_18.dta', convert_categoricals=False)

#data4['real_fincome14']=np.exp(data4['fincome14'])-1
#data4['real_fincome18']=np.exp(data4['fincome18'])-1
#data4['increment']=data4['real_fincome18']-data4['real_fincome14']
#data4['log_increment']=np.log(data4['increment'])
#std=(data4.increment-data4.increment.min())/(data4.increment.max()-data4.increment.min())
#data4['std_increment']=std
data4.to_csv('/Users/wangjiangyi/Desktop/1418_01.csv')