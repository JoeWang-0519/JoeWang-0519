# 1. Current Progress Outline
## Done:

- **ATO login model:**
   - v1.1: 16 features + xgbt
      - [https://yuque.antfin.com/docs/share/2ecda00a-aec1-48d1-a9d7-4b6b5a267973?#](https://yuque.antfin.com/docs/share/2ecda00a-aec1-48d1-a9d7-4b6b5a267973?#) 《ATO login v1.1》
   - v1.2: 21 featuers + xgbt (re-fine on features and not change samples)
      -  [https://yuque.antfin.com/docs/share/064687c0-ac83-40eb-a653-a5a343faefa3?#](https://yuque.antfin.com/docs/share/064687c0-ac83-40eb-a653-a5a343faefa3?#) 《ATO login v1.2》
      - The review performance (precision) is not good
   - **v2 (includes 2 experiments): features + RF （deployed)**
      - [https://yuque.antfin.com/docs/share/b471cb63-d91c-4ea6-91d8-c814dc8b53de?#](https://yuque.antfin.com/docs/share/b471cb63-d91c-4ea6-91d8-c814dc8b53de?#) 《ATO login v2》
      - Make 2 settings for **v2 **(modification on v1):
         - 1. focus on detecting Seller-Scam MO;
         - 2. model is triggered by "new umid" login;
      - Compared with Experiment 1, Experiment 2 makes the following changes:
         - 1. change the size of white samples;
         - 2. standardize the time-window for features;
         - 3. little re-fine on feature list;
      - **Precision: 83% on Review Data for experiment 2**
- **ATO order-create model:**
   - v1 (includes 2 experiments):
      - [https://yuque.antfin.com/docs/share/31050c00-388c-4aed-b1c1-e210cc982893?#](https://yuque.antfin.com/docs/share/31050c00-388c-4aed-b1c1-e210cc982893?#) 《ATO order-create v1》
      - Focus on: **Direct ATO** Case;
      - Time period: From closest login to pay render; 
      - Experiment 1: Click Path Embedding (512 dimension) + RF;
      - Experiment 2: Click Path Embedding (512 dim) + Statistical Features (14) + RF
      - **Conclusion**:  With 14 statistical features, model can perform better in the sense of performance metric. [Experiment 1&2 shares the same black and white samples]
## To-do:

- ATO login model:
   - ATO login v3, take the previous click path of the current umid into consideration;
- ATO order-create model:
   - ATO order-create v2.1, use some tricks including PCA to pre-process the click-path embedding;
   - ATO order-create v2.2, formulate the problem directly as Sequential Data Classification problem and use some architectures like RNN, Transformer to train the model;
# 2. Code Details
#### 2.1 SQL details
[https://yuque.antfin.com/docs/share/dd8c4b86-a50c-4a3b-bfad-cfc5a16d9fcb?#](https://yuque.antfin.com/docs/share/dd8c4b86-a50c-4a3b-bfad-cfc5a16d9fcb?#) 《SQL Details》
#### 2.2 Python Experiments

- Login Model (recent one)

[ato_v2_experiment3_0708.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659088431633-47baa474-1fa9-4ba0-ac64-1469019e763f.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659088431633-47baa474-1fa9-4ba0-ac64-1469019e763f.ipynb%22%2C%22name%22%3A%22ato_v2_experiment3_0708.ipynb%22%2C%22size%22%3A1176925%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22u1e0c5ded-29c1-4919-9b5a-a7af7914925%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u3fd8f6fa%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)

- Order-create Model

[ato_order_create_v1_experiment1.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659106600213-ce18c237-fb84-4068-8664-9692d17c5bdd.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659106600213-ce18c237-fb84-4068-8664-9692d17c5bdd.ipynb%22%2C%22name%22%3A%22ato_order_create_v1_experiment1.ipynb%22%2C%22size%22%3A5082995%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22u7428f0b2-4054-42e3-b449-8a1ca51e0a7%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u5c2315f2%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)
[ato_order_create_v1_experiment2.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659106582954-f2285b20-0513-4d63-9827-160373a4afcf.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659106582954-f2285b20-0513-4d63-9827-160373a4afcf.ipynb%22%2C%22name%22%3A%22ato_order_create_v1_experiment2.ipynb%22%2C%22size%22%3A498805%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22ua4cb5578-523f-430a-83d3-66765bfebf7%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u42599753%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)
