# 1. Review 1 (black prediction is achieved by threshold 0.85)
0621:
('410403081127','1590887','400114485127','400205907540','400215606377','400313742582','400325922966','779680')
0622:
('400025974429', '400041573305', '400150155337', '400660458471', '400688631010')
0623:
('400029218850', '400023270667', '400191294495')
0624:
('32330000', '400130166144', '400135527502', '400163868278', '400394001854', '400692138592', '400692795688', '410401053917')
0625:
('11415590', '400163868278', '400385793232', '400033504401', '400218252999', '400375350199', '400247988635')
0626:
('400019440153', '400097976103', '400113501448', '400172994123', '400273209562', '400336824041', '400378602578', '410434335755', '11167527', '400325454905', '410476107903', '8000833', '400069686152', '400197453128')
0627:
()
0628:
('400314390195', '11167527', '400336824041')

#### Detail:
##### 0621 (Precision: 7/8)
###### 1. buyer_id = '779680' (FP non-ATO)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657677540051-f6275ac8-607a-44f9-b5a0-251c8b6df355.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=168&id=u4e12faf7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=336&originWidth=2582&originalType=binary&ratio=1&rotation=0&showTitle=false&size=246028&status=done&style=none&taskId=u7e7abc5f-bcc9-43e7-8374-50a3609ad93&title=&width=1291)
**Non-ato**, browser 

- trigger model (different ip/umid over past 3mon)
###### 2. buyer_id = '1590887'
a) changing address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657679240333-7fb544db-03f0-4e54-a257-534e24a316d2.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=122&id=u0c3d3480&margin=%5Bobject%20Object%5D&name=image.png&originHeight=244&originWidth=1444&originalType=binary&ratio=1&rotation=0&showTitle=false&size=53438&status=done&style=none&taskId=ua228d301-e2a0-4f9b-b67a-3d9de9266fa&title=&width=722)
b) not frequent umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657679283930-a3a47b99-0c96-445a-86ee-e57add806912.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=180&id=u83926bb7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=360&originWidth=2544&originalType=binary&ratio=1&rotation=0&showTitle=false&size=234748&status=done&style=none&taskId=u7a67f9f8-4ebb-4fe2-9605-b27443b6d4b&title=&width=1272)
c) suspicious order afterwards (cancel OTC + paylater)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657679342239-54b97722-484d-4757-9662-250f79fd0cb1.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=57&id=u15ee7d47&margin=%5Bobject%20Object%5D&name=image.png&originHeight=114&originWidth=2402&originalType=binary&ratio=1&rotation=0&showTitle=false&size=73551&status=done&style=none&taskId=u6bde696e-c693-4b62-bc83-c9d6ee5a49d&title=&width=1201)
**ATO**
###### 3. buyer_id = '400114485127'
a) changing address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657679672647-28fb3430-7c33-4505-b84f-003f414d136d.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=168&id=u06e4bbe3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=336&originWidth=1476&originalType=binary&ratio=1&rotation=0&showTitle=false&size=96377&status=done&style=none&taskId=u41d69971-cce9-45da-800a-06a78155dff&title=&width=738)
b) suspicous goods (digital wallet cash)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657679751433-0cff2316-613e-4504-8c2e-c08e2977bd8d.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=61&id=u399eb313&margin=%5Bobject%20Object%5D&name=image.png&originHeight=122&originWidth=2286&originalType=binary&ratio=1&rotation=0&showTitle=false&size=71235&status=done&style=none&taskId=u6e0341ee-6461-4b1f-890b-6e1547072a1&title=&width=1143)c) not frequent umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657679988298-a9189a69-e6dc-457b-bc1d-5a3cdd3bc0d9.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=101&id=u5a35b901&margin=%5Bobject%20Object%5D&name=image.png&originHeight=202&originWidth=2448&originalType=binary&ratio=1&rotation=0&showTitle=false&size=140125&status=done&style=none&taskId=u0ef684be-6c88-4240-9b40-e4470174189&title=&width=1224)
d) change info
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657680005992-1156cb3c-91fa-4d28-bb74-969e5813b9a4.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=150&id=u6b8f5518&margin=%5Bobject%20Object%5D&name=image.png&originHeight=370&originWidth=492&originalType=binary&ratio=1&rotation=0&showTitle=false&size=36436&status=done&style=none&taskId=u426407ea-aeca-4ed8-8de0-bf6c3f70f7f&title=&width=200)
**ATO**
###### 4. buyer_id = '400205907540'
a) changing address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657680213139-eb6e0157-2537-40bf-80e4-9c188471abfc.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=244&id=u23e2120a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=488&originWidth=1730&originalType=binary&ratio=1&rotation=0&showTitle=false&size=176541&status=done&style=none&taskId=u8f96f7d7-2063-40d5-8a6c-13009fab8f3&title=&width=865)
b) pay_later payment method 
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657680240494-4283bfed-53c6-47d7-bc42-efd984059434.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=133&id=ub94a057e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=266&originWidth=944&originalType=binary&ratio=1&rotation=0&showTitle=false&size=65021&status=done&style=none&taskId=uea712524-3bbb-40e1-8282-aba1c413722&title=&width=472)
3) abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657680750676-c3311a1e-59af-4260-84d2-1c275de3f3dc.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=115&id=u4fb22d4c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=230&originWidth=2390&originalType=binary&ratio=1&rotation=0&showTitle=false&size=162326&status=done&style=none&taskId=u1b52e9b8-9288-4fd6-8edc-cf74a386b94&title=&width=1195)
**ATO**
###### 5. buyer_id = '400215606377'
a) abnormal login, both for ip and umid (device) information
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657681080236-91b4bbde-28ba-472c-af2a-e3751f05df22.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=95&id=u83d0bea1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=190&originWidth=2608&originalType=binary&ratio=1&rotation=0&showTitle=false&size=144453&status=done&style=none&taskId=ufa95aaf1-85f7-479f-b8e3-2bb7eddfae4&title=&width=1304)
b) no suspicious trade
c) info-change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657682052657-47c72259-12e1-467e-8919-a322bdd5c882.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=50&id=ucf460224&margin=%5Bobject%20Object%5D&name=image.png&originHeight=100&originWidth=1038&originalType=binary&ratio=1&rotation=0&showTitle=false&size=27148&status=done&style=none&taskId=u0d0f3b7b-5f64-4291-80f6-cacae8e5cc7&title=&width=519)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657682043203-1c770b4b-94ba-4afa-be41-f533086f56ce.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=98&id=u154de9c6&margin=%5Bobject%20Object%5D&name=image.png&originHeight=196&originWidth=474&originalType=binary&ratio=1&rotation=0&showTitle=false&size=16867&status=done&style=none&taskId=uc4d14637-f4f6-4466-b64e-bd51827aed5&title=&width=237)
~~cannot determine whether ATO or not~~ (**ATO**!)
###### 6. buyer_id = '400313742582'
a) very suspicous login record
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657681307836-5e9ee0d8-6f6f-4202-90ff-86f2bed291d0.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=156&id=udd954810&margin=%5Bobject%20Object%5D&name=image.png&originHeight=312&originWidth=2604&originalType=binary&ratio=1&rotation=0&showTitle=false&size=222955&status=done&style=none&taskId=u7729ff36-cae8-44b7-81be-4d5fb5c801e&title=&width=1302)
b) info-change (reset password)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657681837742-b0b1546e-e696-488f-8274-e5facba52a14.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=91&id=ubc371896&margin=%5Bobject%20Object%5D&name=image.png&originHeight=182&originWidth=1502&originalType=binary&ratio=1&rotation=0&showTitle=false&size=52151&status=done&style=none&taskId=u26bbec63-84c3-4838-bd06-7cbe0144556&title=&width=751)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657681885564-f671a181-2959-4ce8-8a64-34879bdcc9dd.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=99&id=ub50a1bce&margin=%5Bobject%20Object%5D&name=image.png&originHeight=198&originWidth=1228&originalType=binary&ratio=1&rotation=0&showTitle=false&size=39272&status=done&style=none&taskId=u1cf590d9-01dc-4613-a9d6-579e67e4fe9&title=&width=614)
c) no suspicious trade records
**ATO**
###### 7. buyer_id = '400325922966'
a) suspicous trade records (cancel by seller on 0821)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657682138035-bc167725-2352-493c-8b16-8ee2804742d9.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=156&id=u55effc76&margin=%5Bobject%20Object%5D&name=image.png&originHeight=312&originWidth=2604&originalType=binary&ratio=1&rotation=0&showTitle=false&size=137777&status=done&style=none&taskId=u45ec4f46-a521-4eb8-a781-37088dccea1&title=&width=1302)
b) abnormal login records
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657682215032-838a9e92-714d-4253-9b5f-6cfb5f0dbe91.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=83&id=u18f49fff&margin=%5Bobject%20Object%5D&name=image.png&originHeight=166&originWidth=2638&originalType=binary&ratio=1&rotation=0&showTitle=false&size=125988&status=done&style=none&taskId=u03cd41da-aa58-46a7-81a2-0795ade9eac&title=&width=1319)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657682242112-17c33a24-9b91-4297-99a7-fe6f9c91384c.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=218&id=ua0ff2db2&margin=%5Bobject%20Object%5D&name=image.png&originHeight=436&originWidth=262&originalType=binary&ratio=1&rotation=0&showTitle=false&size=24974&status=done&style=none&taskId=u3ded4ade-29b9-497c-b570-a7baf5ef71d&title=&width=131)
c) info-change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657682642433-bc337ff8-e6d9-4378-b994-bcfe6a6b667c.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=136&id=u6fb32582&margin=%5Bobject%20Object%5D&name=image.png&originHeight=272&originWidth=1960&originalType=binary&ratio=1&rotation=0&showTitle=false&size=72572&status=done&style=none&taskId=u3244993d-35a6-4b8f-bcc3-e75c95d25ea&title=&width=980)
first 3 records come from scammer, the last one comes from user himeself;
**ATO**
###### 8. buyer_id = '410403081127
a) suspicious trade records (cancel VA + account payment)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657683648818-dd1350f2-1eda-4db1-ab5e-ed71efdfc58f.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=75&id=ucc52f04e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=192&originWidth=688&originalType=binary&ratio=1&rotation=0&showTitle=false&size=36050&status=done&style=none&taskId=uc91e564f-4d13-4f6c-a0e2-4531437ee9a&title=&width=270)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657683663053-7ce2d015-3705-451b-b564-8f9b600784c6.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=77&id=u0a2099ba&margin=%5Bobject%20Object%5D&name=image.png&originHeight=204&originWidth=826&originalType=binary&ratio=1&rotation=0&showTitle=false&size=26732&status=done&style=none&taskId=uff71ada5-b875-4fde-8dca-6b1234d19aa&title=&width=312)
b) change shipping address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657683721522-2126076a-57df-4cdb-bb21-49782fdf89e4.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=110&id=u458f0b56&margin=%5Bobject%20Object%5D&name=image.png&originHeight=220&originWidth=1470&originalType=binary&ratio=1&rotation=0&showTitle=false&size=55945&status=done&style=none&taskId=u6dc88e35-3d51-4c6d-844c-23c063a92c6&title=&width=735)
c) abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657683765341-5e05b886-3cab-43b6-bc3a-633427e67ccd.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=104&id=ue85849f9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=208&originWidth=2378&originalType=binary&ratio=1&rotation=0&showTitle=false&size=134432&status=done&style=none&taskId=u2d777959-9d01-4840-9444-c4a5b1633d5&title=&width=1189)
**ATO**
##### 0622 (Precision: 4/5)
###### buyer_id = '400025974429'
a) abnormal login umid + abnormal login ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657766797318-d9f272cd-27ab-47e9-9b8f-4630b746bf87.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=207&id=u5075b467&margin=%5Bobject%20Object%5D&name=image.png&originHeight=414&originWidth=2014&originalType=binary&ratio=1&rotation=0&showTitle=false&size=218708&status=done&style=none&taskId=ua103b16b-35de-4969-9528-6e9f917fa40&title=&width=1007)
b) cancel VA order (cancel by seller) + place digital order
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657766905964-737f3662-96af-4c2e-8799-bafcb4be1f38.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=101&id=u76db4ec4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=202&originWidth=1044&originalType=binary&ratio=1&rotation=0&showTitle=false&size=50380&status=done&style=none&taskId=u50a8f23f-a490-43b2-9e52-a945a293fa0&title=&width=522)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657766923712-e5901c4d-4d7b-4454-bf0c-5260b59b5b97.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=110&id=ud4cd28a1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=220&originWidth=1440&originalType=binary&ratio=1&rotation=0&showTitle=false&size=56265&status=done&style=none&taskId=uca24b137-e0c0-419e-b03e-699a692a0e3&title=&width=720)
c) shipping info change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657766945878-f22addea-d66a-4a01-b26c-fc184c4926e1.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=103&id=u29c6073b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=206&originWidth=1444&originalType=binary&ratio=1&rotation=0&showTitle=false&size=55179&status=done&style=none&taskId=u20345cfc-3609-438d-827c-91ac4c8fb13&title=&width=722)
**ATO**
###### buyer_id = '400041573305'
a) abnormal login umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657767149286-eb1fd2e4-47d3-41eb-baff-61ac4dc42fe9.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=209&id=u027a79a7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=418&originWidth=2028&originalType=binary&ratio=1&rotation=0&showTitle=false&size=242829&status=done&style=none&taskId=ufe6dbc07-9ace-4292-9c83-9c7d14c48c8&title=&width=1014)
In addition, this abnormal umid tries to login 1 day later:
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657767214506-d503d82a-190d-41fd-a7a7-e21fdfdf9967.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=184&id=u05551430&margin=%5Bobject%20Object%5D&name=image.png&originHeight=368&originWidth=2048&originalType=binary&ratio=1&rotation=0&showTitle=false&size=197071&status=done&style=none&taskId=uce1cc61d-c07d-432e-8bb0-25d9d8c06ed&title=&width=1024)
This account seems to be frozen after 0624 (all the login records are 'otherdate_issuc' = False)
b) cancel time agrees with the abnormal login time
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657767708871-4099eb7b-a712-4fc6-8ebd-956756a2f7bf.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=42&id=u9eeba5fd&margin=%5Bobject%20Object%5D&name=image.png&originHeight=84&originWidth=2018&originalType=binary&ratio=1&rotation=0&showTitle=false&size=40857&status=done&style=none&taskId=uabf2c998-e901-42a0-8f68-653c3be9d7c&title=&width=1009)
payment method is credit card:
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657767825645-92c7f11d-66e1-4690-a345-131b3d9b009f.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=85&id=u4cdceb3b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=170&originWidth=1254&originalType=binary&ratio=1&rotation=0&showTitle=false&size=54331&status=done&style=none&taskId=u6183ab10-73f0-42d3-b452-5eee867e329&title=&width=627)
c) use paylater, change shipping address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657767857610-cf1d8066-ba7b-429e-b1bd-51fbe6051912.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=171&id=uf431456b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=342&originWidth=1416&originalType=binary&ratio=1&rotation=0&showTitle=false&size=100829&status=done&style=none&taskId=ub4a1fc97-e48e-4eed-b46e-6745f448651&title=&width=708)
d) very suspicious info-change records
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657768981804-9824f409-3825-4e59-a142-cea63561d9a4.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=91&id=ubc81f0cb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=362&originWidth=1924&originalType=binary&ratio=1&rotation=0&showTitle=false&size=84576&status=done&style=none&taskId=ubfa53885-3456-4c6b-91be-0f2f9fbc08c&title=&width=485)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657769002135-1751e5af-1a6f-4a36-afc4-001e51ac38dc.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=95&id=ua18c8c64&margin=%5Bobject%20Object%5D&name=image.png&originHeight=334&originWidth=260&originalType=binary&ratio=1&rotation=0&showTitle=false&size=24226&status=done&style=none&taskId=udc40217a-a6c5-4fbe-98ce-ec9e62d2b48&title=&width=74)
**e) strange points (subtle)**

1. no profit point (only paylater)
1. the order pattern dramatically changed since the abnormal login happened

BEFORE
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657769315704-2b7282a9-3d19-4634-b38e-ae33d3ea1b26.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=354&id=ud2932560&margin=%5Bobject%20Object%5D&name=image.png&originHeight=708&originWidth=1812&originalType=binary&ratio=1&rotation=0&showTitle=false&size=265204&status=done&style=none&taskId=u08bd122f-a886-4e79-a7e4-f56bb2c64b3&title=&width=906)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657769331525-7e50868b-00be-47f4-a1e0-20250615958e.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=379&id=u569d1992&margin=%5Bobject%20Object%5D&name=image.png&originHeight=758&originWidth=934&originalType=binary&ratio=1&rotation=0&showTitle=false&size=141949&status=done&style=none&taskId=u689a4282-37f4-4897-a97b-a5c3fdbb1e8&title=&width=467)
relatively normal
AFTER
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657769377635-891397b5-e25a-4ebe-b4ca-f75fe0c26fdb.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=419&id=u585d6190&margin=%5Bobject%20Object%5D&name=image.png&originHeight=838&originWidth=1484&originalType=binary&ratio=1&rotation=0&showTitle=false&size=277014&status=done&style=none&taskId=ud0f9e846-4a9a-4311-9a49-4f5c8ad84d9&title=&width=742)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657769398217-c92e6c86-852a-4d37-a64d-c371e0b409b3.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=419&id=u86cf7256&margin=%5Bobject%20Object%5D&name=image.png&originHeight=838&originWidth=1116&originalType=binary&ratio=1&rotation=0&showTitle=false&size=242832&status=done&style=none&taskId=u829ab09f-5915-472b-9c8b-38b713cc20e&title=&width=558)
dupilicate order + cancel (never successful make payment)
**ATO**
###### buyer_id = '400150155337'
a) new umid but likely to be the same device (pc)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657769581946-e1991f20-16e5-4f8f-9f51-49d973b166fc.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=164&id=u9789355b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=328&originWidth=1930&originalType=binary&ratio=1&rotation=0&showTitle=false&size=198588&status=done&style=none&taskId=ub96482ca-f0a5-4aff-89ee-7b7c0463f92&title=&width=965)
**non-ATO**
###### buyer_id = '400660458471'
a) abnormal login umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657770497612-4780c4ff-814f-4d26-9403-993afa5b8c57.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=95&id=uafab72cb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=189&originWidth=1018&originalType=binary&ratio=1&rotation=0&showTitle=false&size=94888&status=done&style=none&taskId=ufa72f436-8bb2-482a-af67-82c289b8627&title=&width=509)
b) cancel VA + digital payment with payment account
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657770555077-6ce763ab-0df2-4677-b068-c84bfb07d25e.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=102&id=u072f48cd&margin=%5Bobject%20Object%5D&name=image.png&originHeight=204&originWidth=521&originalType=binary&ratio=1&rotation=0&showTitle=false&size=32450&status=done&style=none&taskId=u0795f219-79c5-4b82-86bc-9433b062b6f&title=&width=260.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657770597664-79122f05-3030-42b8-a7cd-968a321a348b.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=100&id=ub2b573ad&margin=%5Bobject%20Object%5D&name=image.png&originHeight=200&originWidth=730&originalType=binary&ratio=1&rotation=0&showTitle=false&size=50297&status=done&style=none&taskId=ud2e77e42-bd62-4938-b40d-43a88800bf8&title=&width=365)
**ATO**
###### buyer_id = '400688631010'
a) abnormal login umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776088778-256539aa-5973-4ac1-8999-33657970d160.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=100&id=u65f88b17&margin=%5Bobject%20Object%5D&name=image.png&originHeight=200&originWidth=1015&originalType=binary&ratio=1&rotation=0&showTitle=false&size=97258&status=done&style=none&taskId=u330acebf-f405-4ba7-a647-9c7ede4a456&title=&width=507.5)
b) VA cancel + digital payment with payment account
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776160583-2eff22a3-30bd-4c61-8f85-07a2d648480d.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=52&id=ue95b1e07&margin=%5Bobject%20Object%5D&name=image.png&originHeight=104&originWidth=605&originalType=binary&ratio=1&rotation=0&showTitle=false&size=30142&status=done&style=none&taskId=uc231a84d-479e-4895-a6bc-c07da1c2761&title=&width=302.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776185413-4d34df4d-1698-4add-9cd6-ced7017b6dcf.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=50&id=u70f18e43&margin=%5Bobject%20Object%5D&name=image.png&originHeight=100&originWidth=815&originalType=binary&ratio=1&rotation=0&showTitle=false&size=23010&status=done&style=none&taskId=uedb9d2dc-cdf1-486d-a382-10a421f066b&title=&width=408.5)
c) changing shipping address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776238135-895e8ca1-1606-4ce4-8ad9-eb1fc64ae08b.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=99&id=ude576627&margin=%5Bobject%20Object%5D&name=image.png&originHeight=198&originWidth=605&originalType=binary&ratio=1&rotation=0&showTitle=false&size=49142&status=done&style=none&taskId=udf6dcc90-6027-408a-be2e-23247337098&title=&width=302.5)
**ATO**
###### Discovery:
Rumah fauzi occurs in two different ATO cases (shipping customer change to Rumah fauzi)
##### 0623 (Precision: 2/3)
###### buyer_id = '400023270667'
a) VA cancel (cancel by seller side) + digital payment with payment account
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776605305-c9719cb3-b804-46b6-8705-478dd0e67379.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=79&id=ue8806537&margin=%5Bobject%20Object%5D&name=image.png&originHeight=176&originWidth=833&originalType=binary&ratio=1&rotation=0&showTitle=false&size=50244&status=done&style=none&taskId=ue52d5e55-f4ce-402c-8280-c1f91757e15&title=&width=375.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776686337-fc49aa0c-980f-42cd-b0bb-1350c97df20f.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=80&id=u6e546e06&margin=%5Bobject%20Object%5D&name=image.png&originHeight=159&originWidth=715&originalType=binary&ratio=1&rotation=0&showTitle=false&size=40176&status=done&style=none&taskId=ud1fab791-0f24-48fb-91a6-3410fa942b8&title=&width=357.5)
b) changing address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776664250-685cbcb9-47a3-409f-8ef3-80eae0462392.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=80&id=u4eafb70c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=159&originWidth=721&originalType=binary&ratio=1&rotation=0&showTitle=false&size=41676&status=done&style=none&taskId=u5aca42f4-73f2-4368-8cb6-650c9080f7e&title=&width=360.5)
c) abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657776831436-9a4799db-bbd1-46ab-8084-46fb489a86f3.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=81&id=ud52623f0&margin=%5Bobject%20Object%5D&name=image.png&originHeight=162&originWidth=1014&originalType=binary&ratio=1&rotation=0&showTitle=false&size=77630&status=done&style=none&taskId=u8edc548f-2756-41ca-aaa6-372f65d45ed&title=&width=507)
**ATO**
###### buyer_id = '400029218850'
a) no info change
b) no successful payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657777820461-2d94e385-b556-4e01-a4d8-eccd9e89a666.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=236&id=uf2992812&margin=%5Bobject%20Object%5D&name=image.png&originHeight=472&originWidth=492&originalType=binary&ratio=1&rotation=0&showTitle=false&size=49486&status=done&style=none&taskId=ud52543c7-5521-4fd5-8a1b-05aee686b36&title=&width=246)
c) duplicate order
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657777850237-6d189ca5-d2f5-48d6-936a-c37384318b05.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=232&id=u8fa4c70b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=464&originWidth=960&originalType=binary&ratio=1&rotation=0&showTitle=false&size=166616&status=done&style=none&taskId=ua79e2a7d-d7f8-474f-a13b-ce93e508f6e&title=&width=480)
d) only 6 login records from 0301 to 0714 (2 different devices)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657777914673-8c97ffd9-968c-4ed3-b7dd-e57fddfa873e.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=84&id=u2ddac355&margin=%5Bobject%20Object%5D&name=image.png&originHeight=168&originWidth=1009&originalType=binary&ratio=1&rotation=0&showTitle=false&size=64848&status=done&style=none&taskId=uc84c5242-92e1-470d-98e6-6baa6041b0b&title=&width=504.5)
**difficult to determine whether ATO, but tends to be non-ATO (May need to be further checked)**
###### buyer_id = '400191294495'
a) abnormal login, device (frequent device is APPLE but abnormal one is XIAOMI) and ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657778192554-48f0cf17-33f5-4cf7-9dde-ffe776801200.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=91&id=u97465e08&margin=%5Bobject%20Object%5D&name=image.png&originHeight=181&originWidth=1016&originalType=binary&ratio=1&rotation=0&showTitle=false&size=86918&status=done&style=none&taskId=u01e41333-441d-44f5-a7e1-cbf5cd72020&title=&width=508)
b) reset password
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657778347376-6ac4bce4-2607-4358-80dc-dcfebf2b130d.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=46&id=u72a0bb28&margin=%5Bobject%20Object%5D&name=image.png&originHeight=91&originWidth=652&originalType=binary&ratio=1&rotation=0&showTitle=false&size=21848&status=done&style=none&taskId=u92da2a79-1326-424b-a116-21fb9accd1e&title=&width=326)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657778360345-b2cfa25c-71fe-4f92-9534-36c5458e426f.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=45&id=uc46759fa&margin=%5Bobject%20Object%5D&name=image.png&originHeight=79&originWidth=367&originalType=binary&ratio=1&rotation=0&showTitle=false&size=12650&status=done&style=none&taskId=uc48e47f9-2fc1-4892-a162-d5a5318748b&title=&width=208.5)
c) suspicious click path (many many info-change click and bank-add click and cancel-order click)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657778970955-093c13bb-89eb-47ca-8cfd-bc00b1b551c6.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=211&id=uaa343a83&margin=%5Bobject%20Object%5D&name=image.png&originHeight=422&originWidth=818&originalType=binary&ratio=1&rotation=0&showTitle=false&size=148665&status=done&style=none&taskId=u45c8302b-9ef4-46fa-b61d-e81fa4751ad&title=&width=409)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657778983218-4e6185be-5651-4dcb-9883-8b87876e877a.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=204&id=u697d3093&margin=%5Bobject%20Object%5D&name=image.png&originHeight=407&originWidth=908&originalType=binary&ratio=1&rotation=0&showTitle=false&size=171433&status=done&style=none&taskId=ua8053452-7cb1-448d-a14c-bd79026a2b7&title=&width=454)
d) VA cancel record (cancel by seller)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657779064739-c72c5674-753d-42bd-97b5-1d699d029054.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=32&id=uf6940415&margin=%5Bobject%20Object%5D&name=image.png&originHeight=64&originWidth=725&originalType=binary&ratio=1&rotation=0&showTitle=false&size=16388&status=done&style=none&taskId=uac0240f3-10e0-4ba9-b53d-40b0b1ff6ca&title=&width=362.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657779075469-82d43201-b743-4003-9490-3f343bbc1a72.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=30&id=u7790332b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=60&originWidth=726&originalType=binary&ratio=1&rotation=0&showTitle=false&size=16176&status=done&style=none&taskId=ufcf0601e-5d4c-4eef-a4e7-1bd954641e9&title=&width=363)
**ATO**
##### 0624 (Precision: 6/8)
###### buyer_id = '32330000'
a) not abnormal umid (pc login with similar ip address)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657779760839-a1e60563-e389-4634-a84f-95f9d6174877.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=66&id=u30a458d3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=132&originWidth=1000&originalType=binary&ratio=1&rotation=0&showTitle=false&size=70672&status=done&style=none&taskId=uf35d8dcc-2693-49dc-96fb-118b262aeaa&title=&width=500)
**non-ATO**
###### buyer_id = '400130166144'
a) VA cancel + account payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657779884399-c38841ec-be1a-4d3a-91ec-21eb3bde443a.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=73&id=u54303f0b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=145&originWidth=484&originalType=binary&ratio=1&rotation=0&showTitle=false&size=21893&status=done&style=none&taskId=u02ab901c-daaf-4a0d-b851-5408c9548ff&title=&width=242)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657779926582-48aa6670-9167-49e6-9ad4-bad7b84f7af5.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=70&id=ub98192e7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=140&originWidth=486&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18717&status=done&style=none&taskId=u9fe56f2e-9201-41f4-9c02-c1f0d174848&title=&width=243)
b) abnormal login umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657780109304-b299b3c7-2e24-4299-82e4-090b047fcea6.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=88&id=uefe524f5&margin=%5Bobject%20Object%5D&name=image.png&originHeight=176&originWidth=1016&originalType=binary&ratio=1&rotation=0&showTitle=false&size=93820&status=done&style=none&taskId=u822a16fc-ffa2-4b88-8f17-db1a5211131&title=&width=508) 
c) shipping address change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657780220834-20d7cdd4-9ac2-4e34-9e0d-a525fb23effe.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=140&id=u0147a6ca&margin=%5Bobject%20Object%5D&name=image.png&originHeight=279&originWidth=500&originalType=binary&ratio=1&rotation=0&showTitle=false&size=32490&status=done&style=none&taskId=u8f90a651-ffe4-4335-899c-792716c530d&title=&width=250)
**ATO**
###### buyer_id = '400135527502'
a) paylater cancel (seller cancel) + digital goods paylater
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657780381831-4461b4b9-8df8-42b0-8059-9c409e4959e3.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=59&id=ua1b818fb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=142&originWidth=729&originalType=binary&ratio=1&rotation=0&showTitle=false&size=49498&status=done&style=none&taskId=uc8c6e47e-c16e-4b28-8498-f973e51406c&title=&width=304.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657780444905-a0be36bb-dad1-4ea1-bdc2-8bfc181ae699.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=59&id=uba4d5aca&margin=%5Bobject%20Object%5D&name=image.png&originHeight=118&originWidth=826&originalType=binary&ratio=1&rotation=0&showTitle=false&size=37877&status=done&style=none&taskId=u11dbc5f1-c92d-43f6-a9d4-e53fe313561&title=&width=413)
Another point is: Once cancel, start to make payment
b) change address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657780521235-9289eaa0-66e2-4a83-9216-3d2d05cbbe35.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=117&id=ue0af82ce&margin=%5Bobject%20Object%5D&name=image.png&originHeight=233&originWidth=969&originalType=binary&ratio=1&rotation=0&showTitle=false&size=89991&status=done&style=none&taskId=ufd4bd11b-188e-4795-8ec5-a9df997c525&title=&width=484.5)
c)abnormal umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657780569929-8a563146-7c81-413c-89db-8d377087f627.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=99&id=uf17e1ae4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=198&originWidth=983&originalType=binary&ratio=1&rotation=0&showTitle=false&size=92675&status=done&style=none&taskId=u134003f5-e3bd-4a0c-8418-a35e57e91f7&title=&width=491.5)
**ATO**
###### buyer_id = '400163868278'
a) 229 login records from 0601 to 0714, using more than 5 different devices
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781047196-4bdd803c-cfab-47fe-864f-bd2c18945a86.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=72&id=u84eeb748&margin=%5Bobject%20Object%5D&name=image.png&originHeight=144&originWidth=181&originalType=binary&ratio=1&rotation=0&showTitle=false&size=15123&status=done&style=none&taskId=ub06b36d2-5d13-48ce-8914-4a75d5d75db&title=&width=90.5)
b) multiple shipping address, including some ATO address (Rumah Fauzi)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781093612-aad4e19f-cb6c-4e70-91a0-adc92f5b93b9.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=73&id=ua3c45c62&margin=%5Bobject%20Object%5D&name=image.png&originHeight=145&originWidth=185&originalType=binary&ratio=1&rotation=0&showTitle=false&size=11048&status=done&style=none&taskId=uae10cbb5-42bc-40d1-82ed-5707e52f8e9&title=&width=92.5)
c) no successful payment (1000+ cancel records from 0601 to 0714)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781271597-82c27a01-11e4-4370-b974-ae208a80eb4a.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=261&id=u3e04e70d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=522&originWidth=1015&originalType=binary&ratio=1&rotation=0&showTitle=false&size=167264&status=done&style=none&taskId=ub27de598-9637-4532-8c5f-0f974c70fb8&title=&width=507.5)
**non-ATO, but is a suspicious case**
###### buyer_id = '400394001854'
a) cancel OTC and use payment account
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781433025-412c1da5-ca17-447b-81fa-b8d367497bd9.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=110&id=u90658e02&margin=%5Bobject%20Object%5D&name=image.png&originHeight=287&originWidth=962&originalType=binary&ratio=1&rotation=0&showTitle=false&size=102435&status=done&style=none&taskId=ufa2e275f-47f7-4d22-a11a-6dbaabc9633&title=&width=370)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781452560-72e02913-554c-4044-8fa7-97daeb53f756.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=110&id=u97de337a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=286&originWidth=607&originalType=binary&ratio=1&rotation=0&showTitle=false&size=58362&status=done&style=none&taskId=u9313a292-a4f3-4016-bfda-1baec47df88&title=&width=233.5)
b) change address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781495255-a43db9be-dfbb-45c2-8ccd-7954a9f6bb88.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=148&id=u3cde05e1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=295&originWidth=797&originalType=binary&ratio=1&rotation=0&showTitle=false&size=83118&status=done&style=none&taskId=u32a99d34-1c71-4399-93cd-907be2f384c&title=&width=398.5)
c) abnormal umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657781530525-cd7b4ee7-585a-4165-a75b-c462a610e594.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=96&id=u6930fc78&margin=%5Bobject%20Object%5D&name=image.png&originHeight=192&originWidth=1019&originalType=binary&ratio=1&rotation=0&showTitle=false&size=92571&status=done&style=none&taskId=uf61f5b5a-4fd4-48d8-9bbc-08bfc545a5c&title=&width=509.5)
**ATO**
###### buyer_id = '400692138592'
a) info-change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782298547-204a4c0a-b6cb-40b4-8785-f861eb1decf7.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=72&id=ue7683d1d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=144&originWidth=666&originalType=binary&ratio=1&rotation=0&showTitle=false&size=26623&status=done&style=none&taskId=ucd0bcac5-8ea0-4807-83c0-b6590266f8c&title=&width=333)
b) abnormal login umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782344857-83c53cc1-e1b9-4efa-a26b-0842eba66d67.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=99&id=u96fb76d4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=197&originWidth=1004&originalType=binary&ratio=1&rotation=0&showTitle=false&size=89142&status=done&style=none&taskId=ua7a836c6-0b6d-4f84-b527-2a16ed845ac&title=&width=502)
c) VA cancel but no further payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782392525-8f1fc95b-3c57-419e-a62b-948eca5710da.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=42&id=u7e46133d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=83&originWidth=597&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18821&status=done&style=none&taskId=uf5ad016d-4fec-4fe3-87c9-49e064b8187&title=&width=298.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782382303-e884a036-9152-4bf4-9d3a-ae974298acad.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=44&id=u59e0d488&margin=%5Bobject%20Object%5D&name=image.png&originHeight=89&originWidth=823&originalType=binary&ratio=1&rotation=0&showTitle=false&size=23372&status=done&style=none&taskId=u046ec21e-70c6-4a93-a043-baf84817374&title=&width=403.5)
d) click path (info-change, social accounts, bank-add)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782527580-60114d03-e44c-4904-85c0-f31d25859f33.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=96&id=uc50ebe58&margin=%5Bobject%20Object%5D&name=image.png&originHeight=191&originWidth=487&originalType=binary&ratio=1&rotation=0&showTitle=false&size=21676&status=done&style=none&taskId=u95ea5246-07f2-4890-9214-9d71a0750e6&title=&width=243.5)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782540429-2899fddf-768c-40fd-b56b-e1ad07d3e206.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=73&id=uf4e85c18&margin=%5Bobject%20Object%5D&name=image.png&originHeight=146&originWidth=471&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18031&status=done&style=none&taskId=u59eb8015-e509-4d4f-a170-0d0b7ed4d78&title=&width=235.5)
**ATO**
###### buyer_id = '400692795688'
a) abnormal umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782698671-f0040856-b45c-470f-a2d3-67c20cbec304.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=91&id=u07d1b307&margin=%5Bobject%20Object%5D&name=image.png&originHeight=182&originWidth=976&originalType=binary&ratio=1&rotation=0&showTitle=false&size=78905&status=done&style=none&taskId=u4a74c56a-3b57-41f6-9733-e16cc91f47f&title=&width=488)
b) VA cancel + account payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782738772-9c47ebc3-84e9-47af-8fc6-a033e53ad211.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=122&id=uccabdbfd&margin=%5Bobject%20Object%5D&name=image.png&originHeight=244&originWidth=610&originalType=binary&ratio=1&rotation=0&showTitle=false&size=69829&status=done&style=none&taskId=u3e75830d-5da7-43f4-b587-cbff8780f9e&title=&width=305)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782752175-3e7e8f58-a5c5-438d-b48f-ca0f281220da.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=121&id=u838c8f1b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=240&originWidth=834&originalType=binary&ratio=1&rotation=0&showTitle=false&size=51849&status=done&style=none&taskId=uda948181-79f0-4ce9-9911-d812622603b&title=&width=419)
c) change shipping address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657782778591-dfde6fae-5572-4f57-8576-97340c48966d.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=121&id=u0b6e6683&margin=%5Bobject%20Object%5D&name=image.png&originHeight=241&originWidth=829&originalType=binary&ratio=1&rotation=0&showTitle=false&size=71553&status=done&style=none&taskId=u4b20f50f-b8cd-4b4e-bf1f-61939ff7789&title=&width=414.5)
**ATO**
###### buyer_id = '410401053917'
a) abnormal umid + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783039361-04a8b8e6-24ed-4a77-aa6f-ef73963fc49f.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=91&id=uade61722&margin=%5Bobject%20Object%5D&name=image.png&originHeight=182&originWidth=1002&originalType=binary&ratio=1&rotation=0&showTitle=false&size=86328&status=done&style=none&taskId=uabbe0d16-23f5-4fb1-9372-f145f4c63ce&title=&width=501)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783053995-fd6fa674-7072-4567-97e7-a797ccc6c8d8.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=82&id=u7fd25944&margin=%5Bobject%20Object%5D&name=image.png&originHeight=164&originWidth=1001&originalType=binary&ratio=1&rotation=0&showTitle=false&size=91521&status=done&style=none&taskId=ueaa25617-cc56-4d4d-9d95-3a92d84cbe3&title=&width=500.5)
b) info-change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783224950-b802aed2-29f3-4bdd-b039-e011b8067874.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=73&id=uad230cf5&margin=%5Bobject%20Object%5D&name=image.png&originHeight=145&originWidth=368&originalType=binary&ratio=1&rotation=0&showTitle=false&size=15164&status=done&style=none&taskId=u26882e12-55f0-4e55-9392-72acec4d2d1&title=&width=184)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783237906-888e500c-478f-406f-9201-e4fd8c850e15.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=72&id=u7515c3fa&margin=%5Bobject%20Object%5D&name=image.png&originHeight=139&originWidth=486&originalType=binary&ratio=1&rotation=0&showTitle=false&size=14699&status=done&style=none&taskId=ua3d05c92-e206-4352-966d-7bc0a83ab7b&title=&width=251)
c) cancel VA + payment account
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783477008-949e0030-4278-4e6d-aee8-1e5616453f6e.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=114&id=ucca1934c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=227&originWidth=605&originalType=binary&ratio=1&rotation=0&showTitle=false&size=59483&status=done&style=none&taskId=uecf659bf-58b5-49d4-94fb-37e6396db4f&title=&width=302.5)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783497177-81537c47-4acd-4d02-b538-c166491da17c.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=115&id=ucde6bbde&margin=%5Bobject%20Object%5D&name=image.png&originHeight=237&originWidth=603&originalType=binary&ratio=1&rotation=0&showTitle=false&size=57100&status=done&style=none&taskId=u408ef8f8-6249-4fe5-aec7-ff555669ddd&title=&width=291.5)
d) shipping address
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657783518675-5c002c3b-9dcf-4acf-a206-d5bb0dcda555.png#clientId=u29438747-349c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=127&id=u990dd711&margin=%5Bobject%20Object%5D&name=image.png&originHeight=254&originWidth=727&originalType=binary&ratio=1&rotation=0&showTitle=false&size=67847&status=done&style=none&taskId=ue550529b-6331-4f4e-a083-17e8f92b4b6&title=&width=363.5)
**ATO**
##### 0625-0628 (Precision: 20/24) [Review by Will's team]
[ATO model review_v2.xlsx](https://yuque.antfin.com/attachments/lark/0/2022/xlsx/59656497/1658302351511-b7a1adcb-3a2f-4e7a-9e2c-7aa7d50c3f2e.xlsx?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fxlsx%2F59656497%2F1658302351511-b7a1adcb-3a2f-4e7a-9e2c-7aa7d50c3f2e.xlsx%22%2C%22name%22%3A%22ATO+model+review_v2.xlsx%22%2C%22size%22%3A8173%2C%22type%22%3A%22application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet%22%2C%22ext%22%3A%22xlsx%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Afalse%2C%22taskId%22%3A%22u91905b97-aaaa-4887-8f26-a6aa91185cc%22%2C%22taskType%22%3A%22transfer%22%2C%22id%22%3A%22uee98549c%22%2C%22card%22%3A%22file%22%7D)
# 2. Review 2 (those samples whose scores are between 0.8 and 0.85)
0621:
('18107980', '19768915', '400042542453', '400325922966')
0622:
('400285545897', '400382316704', '410413752724', '525826')
0623:
('400326261530', '400082889556')
0624:
('400299867297',  '400394001854',  '400354830130',  '400356168998',  '410445921893',  '410446017115',  '410446431534',  '400131558494')
0625:
('400169220724')
0626:
('1781100', '400000914513', '400097976103', '400069686152')
0627:
()
0628:
('400211625512', '400692138592')
#### Detail:
##### 0621 (Precision: 3/4)
###### buyer_id = '18107980'
a) reverse reason
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658304325884-1aa1afed-a542-424d-a846-49e0ebe4ede3.png#clientId=ud38d0c3b-c2f9-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=157&id=u5084749b&margin=%5Bobject%20Object%5D&name=image.png&originHeight=314&originWidth=1776&originalType=binary&ratio=1&rotation=0&showTitle=false&size=84848&status=done&style=none&taskId=u14dde725-799c-47de-a753-42162d28f65&title=&width=888)
b) paylater payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658304348714-33f3b6e8-9398-4a93-8c75-30b46c45ed47.png#clientId=ud38d0c3b-c2f9-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=153&id=u8bd0b853&margin=%5Bobject%20Object%5D&name=image.png&originHeight=306&originWidth=728&originalType=binary&ratio=1&rotation=0&showTitle=false&size=50463&status=done&style=none&taskId=u1eb7aae0-bcb7-4239-aa57-d770570200d&title=&width=364)
c) abnormal umid + app version + ip
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658304438519-689c57fe-3962-429b-ad52-25dc6aab76da.png#clientId=ud38d0c3b-c2f9-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=95&id=u7f9e1fb6&margin=%5Bobject%20Object%5D&name=image.png&originHeight=190&originWidth=1930&originalType=binary&ratio=1&rotation=0&showTitle=false&size=87868&status=done&style=none&taskId=u21e0fde9-a40e-4975-97f1-5cbf9518ad4&title=&width=965)
**ATO**
###### buyer_id = '19768915'
a) different umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317697458-08f33c2c-da3f-491d-8596-15f98ca7a532.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=177&id=udb58bdbb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=354&originWidth=2050&originalType=binary&ratio=1&rotation=0&showTitle=false&size=195156&status=done&style=none&taskId=u82328ce3-e5de-4f86-8f84-d82057ebf1a&title=&width=1025)
)b) no profit point and no successful payment (might not be ATO but other fraud)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317878325-d1426335-77d9-49f0-939a-806176085960.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=250&id=uacca9acc&margin=%5Bobject%20Object%5D&name=image.png&originHeight=500&originWidth=1634&originalType=binary&ratio=1&rotation=0&showTitle=false&size=184546&status=done&style=none&taskId=u3372e556-746b-4745-9543-8daccb0621e&title=&width=817)
**DIFFICULT TO SAY**
###### buyer_id = '400042542453'
a) suspicious order
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658316931856-57cbb856-cc8b-4ad2-9b6e-57709f895058.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=70&id=u19b158e9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=242&originWidth=966&originalType=binary&ratio=1&rotation=0&showTitle=false&size=57268&status=done&style=none&taskId=u71834836-985b-4847-b7fb-b5099546785&title=&width=280)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658316946138-2c225a67-26a6-491e-8ed0-bcae75903fa4.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=68&id=uf6086427&margin=%5Bobject%20Object%5D&name=image.png&originHeight=232&originWidth=1462&originalType=binary&ratio=1&rotation=0&showTitle=false&size=60828&status=done&style=none&taskId=u0265a62a-b526-4477-9d67-c4d2055e8a5&title=&width=429)
b) suspicious login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658316996073-aad026bb-4246-4fc2-b7f3-a21f8e4ea662.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=177&id=u3eea4fa7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=354&originWidth=2006&originalType=binary&ratio=1&rotation=0&showTitle=false&size=198237&status=done&style=none&taskId=u3b408634-f9e9-40c1-b3ac-62b6094b3ca&title=&width=1003)
c) info-change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317430675-f5bea72d-e3f3-4a7d-adad-61001effe8a4.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=163&id=u1a131083&margin=%5Bobject%20Object%5D&name=image.png&originHeight=326&originWidth=2020&originalType=binary&ratio=1&rotation=0&showTitle=false&size=132116&status=done&style=none&taskId=u354da6da-fcbb-4b71-9da4-d27852757e6&title=&width=1010)
**ATO**
###### buyer_id = '400325922966'
a) order cancelled by seller
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317277837-3a79a0d8-d6bb-40d8-9a05-9a9b809898ec.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=137&id=u13fa2daa&margin=%5Bobject%20Object%5D&name=image.png&originHeight=274&originWidth=1576&originalType=binary&ratio=1&rotation=0&showTitle=false&size=77369&status=done&style=none&taskId=ue1099c91-5f31-412d-b963-ccea2042501&title=&width=788)
b) abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317384833-729a1a4f-e04a-445a-b70c-34478fdebf9e.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=198&id=gjQLo&margin=%5Bobject%20Object%5D&name=image.png&originHeight=396&originWidth=2048&originalType=binary&ratio=1&rotation=0&showTitle=false&size=209972&status=done&style=none&taskId=ua9423752-b0fb-4784-b277-f7ccc729237&title=&width=1024)
**ATO**
###### Another Discovery:
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317361211-889a8d42-e103-4856-8940-111df6afd2ea.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=39&id=u868226cf&margin=%5Bobject%20Object%5D&name=image.png&originHeight=78&originWidth=2036&originalType=binary&ratio=1&rotation=0&showTitle=false&size=41152&status=done&style=none&taskId=u9ee9da35-ae94-490a-9bb8-9986dbf9f9f&title=&width=1018)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658317384833-729a1a4f-e04a-445a-b70c-34478fdebf9e.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=198&id=uee578cd8&margin=%5Bobject%20Object%5D&name=image.png&originHeight=396&originWidth=2048&originalType=binary&ratio=1&rotation=0&showTitle=false&size=209972&status=done&style=none&taskId=ua9423752-b0fb-4784-b277-f7ccc729237&title=&width=1024)
same device + same umid
##### 0622 (Precision: 1/4)
###### buyer_id = '525826'
a) seems not abnormal umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658329907797-3e098b5c-ce8c-4bc6-9f2c-d98340af6b6b.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=184&id=ua072d5a4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=368&originWidth=1986&originalType=binary&ratio=1&rotation=0&showTitle=false&size=183559&status=done&style=none&taskId=u904708f1-6aa2-48eb-89c6-6cdcf24c4d3&title=&width=993)
b) no suspicious trade
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658329933980-6f1f9110-7fce-46dd-acaa-31cfcd870750.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=273&id=u083d0f04&margin=%5Bobject%20Object%5D&name=image.png&originHeight=546&originWidth=2054&originalType=binary&ratio=1&rotation=0&showTitle=false&size=241534&status=done&style=none&taskId=u85f2ef3b-945d-4a7a-9089-aa88bd720e1&title=&width=1027)
**non-ATO**
###### buyer_id = '400285545897'
a) VA order cancelled 
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658330025467-c6cbb27a-eef8-4112-971f-a5ba9848e079.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=69&id=u1032bf93&margin=%5Bobject%20Object%5D&name=image.png&originHeight=380&originWidth=1902&originalType=binary&ratio=1&rotation=0&showTitle=false&size=146036&status=done&style=none&taskId=udb5be9c9-647d-4912-9491-0054a5a61a7&title=&width=345)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658330047176-4a54379d-67b4-4edc-a22a-53b764499fbc.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=71&id=u20ecedeb&margin=%5Bobject%20Object%5D&name=image.png&originHeight=368&originWidth=1672&originalType=binary&ratio=1&rotation=0&showTitle=false&size=113369&status=done&style=none&taskId=uf4496fd4-f203-4f29-943a-8950535df53&title=&width=321)
b) abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658330144525-280372b1-98e8-400f-ae80-6a071ed887b6.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=190&id=u2751aea9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=380&originWidth=1984&originalType=binary&ratio=1&rotation=0&showTitle=false&size=190091&status=done&style=none&taskId=ue1d93a8d-41db-400a-b2e3-ff13c0cf925&title=&width=992)
**ATO**
###### buyer_id = '400382316704'
a) PC login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658330831654-45b691a5-4b47-4d3a-b6d5-cd988ad793b5.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=177&id=u20f5a3a3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=354&originWidth=2042&originalType=binary&ratio=1&rotation=0&showTitle=false&size=207924&status=done&style=none&taskId=u2be51d49-c841-4861-bdb8-b1942945a8d&title=&width=1021)
tend to be **non-ATO**
###### buyer_ id = '410413752724'
a) all login umids are different, might be other kind of fraud
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658330455115-ba3236d7-2182-40da-9b39-52a4c6b0d49d.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=225&id=uf1f887f7&margin=%5Bobject%20Object%5D&name=image.png&originHeight=450&originWidth=2078&originalType=binary&ratio=1&rotation=0&showTitle=false&size=218593&status=done&style=none&taskId=ud226032d-a741-494c-accb-1cf95e859e2&title=&width=1039)
**non-ATO**
##### 0624 (Precision: 1/8)
###### buyer_id = '400131558494'
a) order cancel (VA)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658331033184-a91b9103-fbd8-436f-affd-8899bf753381.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=47&id=ufca429ed&margin=%5Bobject%20Object%5D&name=image.png&originHeight=166&originWidth=968&originalType=binary&ratio=1&rotation=0&showTitle=false&size=37444&status=done&style=none&taskId=u4402b6cf-d7da-4df5-9de4-17cc2eeadaf&title=&width=274)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658331043264-6968dbb9-49cc-436b-aaf0-0c357720c4e7.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=49&id=u710e5a03&margin=%5Bobject%20Object%5D&name=image.png&originHeight=158&originWidth=1470&originalType=binary&ratio=1&rotation=0&showTitle=false&size=48404&status=done&style=none&taskId=ud4c4612f-c984-4ca6-9053-d1ef03cc043&title=&width=455)
b) seems not abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332048166-4e844fae-205a-434c-a130-22f784a22b4f.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=204&id=u57938d86&margin=%5Bobject%20Object%5D&name=image.png&originHeight=408&originWidth=2030&originalType=binary&ratio=1&rotation=0&showTitle=false&size=230583&status=done&style=none&taskId=uea7e8e95-d5ad-4998-9908-07a7d131aaa&title=&width=1015)
**non-ATO**
###### buyer_id = '400299867297'
a) 0623 created orders are cancelled at 0624
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658331200188-cca4b84c-a204-44cb-a527-855512d7e5ae.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=265&id=u0b4b4d42&margin=%5Bobject%20Object%5D&name=image.png&originHeight=530&originWidth=1696&originalType=binary&ratio=1&rotation=0&showTitle=false&size=218279&status=done&style=none&taskId=u773fd3c2-0589-486c-a5e5-aa698489114&title=&width=848)
b) VA payments are on 0613
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658331244469-190ae332-ca07-4f26-a3ca-83c728539c1f.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=200&id=u6bfafa6c&margin=%5Bobject%20Object%5D&name=image.png&originHeight=400&originWidth=718&originalType=binary&ratio=1&rotation=0&showTitle=false&size=73993&status=done&style=none&taskId=u16890f19-de53-4b73-843f-81f8794f0ec&title=&width=359)![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658331257939-831e4715-c500-4810-8de0-511e30fa2a0c.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=199&id=u2b68a2d5&margin=%5Bobject%20Object%5D&name=image.png&originHeight=398&originWidth=720&originalType=binary&ratio=1&rotation=0&showTitle=false&size=90090&status=done&style=none&taskId=ufc05c852-b7f9-48a7-a31e-2014b966def&title=&width=360)
c) all orders are cancelled
d) similar useragent but totally different umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332158706-0939ace5-3195-4d3b-85a7-589ee589f047.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=212&id=uaf0e5fe0&margin=%5Bobject%20Object%5D&name=image.png&originHeight=424&originWidth=1958&originalType=binary&ratio=1&rotation=0&showTitle=false&size=236993&status=done&style=none&taskId=u03fe124e-29b8-49e6-9fd4-2484f067d7d&title=&width=979)
seems other fraud,  **non-ATO**
###### buyer_id = '400354830130'
a) similar useragent but totally different umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332426462-67ffa852-237a-4cd1-a0d4-9252c6478f9a.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=218&id=ucd171ffa&margin=%5Bobject%20Object%5D&name=image.png&originHeight=436&originWidth=1968&originalType=binary&ratio=1&rotation=0&showTitle=false&size=233254&status=done&style=none&taskId=uc188caa5-55ee-411b-bb8b-90bedc0f7aa&title=&width=984)b) all cancelled order
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332491844-020c481d-4b80-4f40-b23d-a0e56813fbf9.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=225&id=u127e27e6&margin=%5Bobject%20Object%5D&name=image.png&originHeight=450&originWidth=2064&originalType=binary&ratio=1&rotation=0&showTitle=false&size=211184&status=done&style=none&taskId=uca85b1f9-aa16-4020-8713-3190545cb1f&title=&width=1032)
**THIS CASE IS ALMOST THE SAME AS PREVIOUS ONE!!!!!!**
**non-ATO**
###### buyer_id = '400356168998'
**Totally the same as preivous two case**
**non-ATO**
###### buyer_id = '400394001854'
a) OTC cancelled
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332811787-8f26cf67-17cd-476d-bcae-afd05ca4358e.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=98&id=udf0a17db&margin=%5Bobject%20Object%5D&name=image.png&originHeight=196&originWidth=2040&originalType=binary&ratio=1&rotation=0&showTitle=false&size=82517&status=done&style=none&taskId=u26a7332a-1a6d-41b1-9f27-00a263e0241&title=&width=1020)
b) shipping address change
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332825357-74dffb02-6726-43d8-94d1-cedd8611a3fb.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=169&id=uead5e041&margin=%5Bobject%20Object%5D&name=image.png&originHeight=338&originWidth=1680&originalType=binary&ratio=1&rotation=0&showTitle=false&size=131590&status=done&style=none&taskId=u72ec8cd3-5c2b-412b-a159-2dee975f608&title=&width=840)
c) abnormal login
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658332877697-fdfbf12f-4c0c-4293-93e3-9b6e178baa7f.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=187&id=u3a18a962&margin=%5Bobject%20Object%5D&name=image.png&originHeight=374&originWidth=2006&originalType=binary&ratio=1&rotation=0&showTitle=false&size=205974&status=done&style=none&taskId=u5a5783eb-31bf-4bee-8a4b-51b02037a66&title=&width=1003)
**ATO**
###### buyer_id = '410445921893'
a) umid is all different
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658367829602-c46b364d-3240-4e68-a785-e8363af3bd28.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=198&id=u264acebf&margin=%5Bobject%20Object%5D&name=image.png&originHeight=396&originWidth=2008&originalType=binary&ratio=1&rotation=0&showTitle=false&size=221315&status=done&style=none&taskId=u7f9194c3-5c02-4792-a242-a1cb327a2a5&title=&width=1004)
b) no successful payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658367964418-65fa9d92-5e94-4d68-839f-38200fd329c2.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=260&id=ud96a6fa1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=520&originWidth=1954&originalType=binary&ratio=1&rotation=0&showTitle=false&size=244353&status=done&style=none&taskId=ubaad2afe-2d9f-49a3-9e80-fc73ecd6f9c&title=&width=977)
**non-ATO**
###### buyer_id = '410446017115'
a) umid is nearly all different
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658368100019-ea42b826-d3f0-4e3c-86d5-611e098b24aa.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=189&id=ub38a41bd&margin=%5Bobject%20Object%5D&name=image.png&originHeight=378&originWidth=2022&originalType=binary&ratio=1&rotation=0&showTitle=false&size=222591&status=done&style=none&taskId=u25a57012-af1f-4250-9fda-d891d762c54&title=&width=1011)
b) no successful payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658368151671-2b6a48f8-5bcd-4e7b-82ee-99ce70415dda.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=285&id=u08236dca&margin=%5Bobject%20Object%5D&name=image.png&originHeight=570&originWidth=1938&originalType=binary&ratio=1&rotation=0&showTitle=false&size=253192&status=done&style=none&taskId=u09b0dc32-a870-4b93-a1de-280819f24cb&title=&width=969)
**non-ATO**
###### buyer_id = '410446431534'
a) different umid
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658368388109-5bbee376-5495-4704-8db8-8b953f1d1ed0.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=192&id=ue80ccb44&margin=%5Bobject%20Object%5D&name=image.png&originHeight=384&originWidth=2036&originalType=binary&ratio=1&rotation=0&showTitle=false&size=220502&status=done&style=none&taskId=u65bbea08-8025-4fb8-9bb8-2fe32c03af1&title=&width=1018)
b) no successful payment
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658368244799-38279d76-3038-44df-bc8f-77bd904a5eff.png#clientId=uf7d869c3-1216-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=280&id=u5a81f601&margin=%5Bobject%20Object%5D&name=image.png&originHeight=560&originWidth=1968&originalType=binary&ratio=1&rotation=0&showTitle=false&size=248140&status=done&style=none&taskId=u32fea9e6-2e73-4a96-a69f-52e67a435ea&title=&width=984)
**non-ATO**
##### Strange Pattern:
On 0624, buyer_id = ('410446431534', '410446017115', '410445921893', '400356168998', '400354830130', '400299867297') [**6 cases**] **share the same pattern**: 

1. As for login records, almost all the umids are different;
1. As for trade records, there are 2 payment methods:
   1. COD, no successful payment (all cancel);
   1. VA, successful payment
3. As for trade records, the products and shops are similar with each other

On 0623, buyer_id = ('410413752724') also **shares the same pattern**.
###### Login and Trade records:
[suspicous account.xlsx](https://yuque.antfin.com/attachments/lark/0/2022/xlsx/59656497/1658371613784-a68ab9c2-1897-4f4f-86da-6dc74ecfa4b1.xlsx?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fxlsx%2F59656497%2F1658371613784-a68ab9c2-1897-4f4f-86da-6dc74ecfa4b1.xlsx%22%2C%22name%22%3A%22suspicous+account.xlsx%22%2C%22size%22%3A124338%2C%22type%22%3A%22application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet%22%2C%22ext%22%3A%22xlsx%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22ua3214752-fcb3-4ccd-8960-6cde48a9fb2%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u89fb1bdc%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)
