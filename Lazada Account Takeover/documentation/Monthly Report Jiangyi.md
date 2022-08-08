# 202207
## Done:
### ATO login model (v2):

- Finish ATO login v2, which focuses on detecting Seller-Scam ATO;
   - Send 0621-0628 prediction result to Will's team for manual review, and the precision rate is 81.25%;
   - Divide users into 10 ranks based on the prediction probability (0~0.1 corresponds to rank 0, so on so forth). Give the distribution of each rank and the highest rank's (rank 9) precision rate is up to 92.31%
- Finish building offline indicators table and ready to deploy model;
### ATO order-create model (v1):

- Finish 2 experiments, which focus on detecting direct ATO;
   - For experiment 1, only use click-path embedding features;
      - 0.99 precision; 0.88 recall
   - For experiment 2, make the feature list, combining with the click-path embedding;
      - 0.99 precision; 0.90 recall
- Use PCA to visualise the result of click-path embedding;
   - First 10 components of PCA for click-path embedding are quite separable;
### Hand-over:

- Prepare documentations for hand-over and share with Guo Yang;
## To-do:

- For hand-over, still need to write notes for SQL codes;
- Deploy the ATO login v2 model;
- Prepare the report for ATO models;
## Self-learning:

- Undersatnd the basic algorithm of CNN. Based on that, read some famous paper of modified CNN architecture, including AlexNet and ResNet;
- Understand the procedure of Graph Neural Network (GNN) and some variants model;
# 202206
## Done:

- Keep diving into the ATO scenarios to find useful features from different aspects. Based on the further understanding of problem, give the standard for selecting black and white samples and feature list;
- build the model for ATO login step with respect to the feature list and experiment samples;
   - 1155 black samples, 31718 white samples;
   - estimated precision 0.97, estimated recall 0.97;
- Send 0611 prediction to Will's team for review. Complete bad case analysis for the review result. FIgure out the modification which can be made to our model based on the analysis result;
   - We should re-select the white samples based on the case analysis and re-fine the features' time window;
- Figure out the ways to save xgboost model (through PAI). Train the ATO login model v1 on PAI platform;
- Go back to the problem and determine next we should build seperate models for direct ATO and seller-scam ATO respectively;
## To-do:

- Make the next version ATO login model (ATO login v2);
   - update the white samples;
   - move away some features and do modification on the time window;
- Understand the model for order-create scenario and then make it;
## Self-learning:

- Understand some basic algorithms in NLP (word2vec, glove etc.);
- Understand recurrent neural network (RNN), with respect to the basic model, some variants (especially LSTM), some interesting mechanism (encoder-decoder mode, attention) and some limitation (long-term dependency and gradient vanish, which is actually equivalent);
- Understand transformer model;
# 202205
## Onboarding (0509-0513)

1. Equipment setup and onboarding sessions;
1. Get acquainted with the DS tools and daily softwares: Yuque,  ODPS, Datastudio, etc;
1. Get familiar with database;
1. Gain more details about ATO process.
## 0516-0531
### Reflection:
Keep on diving deeper into data to totally understand every detail of ATO process. Talk with business team (Kira) to gain more insights about ATO cases and then back to data for validation. Try to stand at the scammers' perspective, how to make money? Use data to check our thoughts and recover the whole ATO process, which must be the first step before giving the solution.
#### 

### Progress:
#### ATO project
**Done**

- Our ultimate aim for doing ATO detection:
   - Prevent costumers from losing their money
      - Focus on non-COD cases
- Agreed on building the detect model in login step first (version 1) and purchase step later:
   - In login step, we will focus on: Environemnt information (umid, useragent, ipparse_ipisp etc.); Seller information (based on checking previous order records, characterize the suspicious sellers by features); Buyer information (checking previous order records, focus on payment methods, IM if existed). All should be based on EDA of better black samples (already recieve from Kira).
   - In later steps, more information can be considered, including click data (page stay time, url records etc), order cancellation behavior etc.
- Comprehensive check and recovery on several samples to explore MOs in ATO cases. Actually there exists much noise in black cases, which may not have specific behaviours of ATO (making money) but abnormal login occurs.
   - Generally, get across the whole process of ATO from the database
   - This step is still complusory for the update of our model in the future to figure out the updated MOs of ATO in the sense of data.

**To-do:**

- Make the 1-st feature list and make features and do EDA to check the reasonability of features
- Build up RF model (baseline model) in login step and do bad-case analysis to iterate our model

