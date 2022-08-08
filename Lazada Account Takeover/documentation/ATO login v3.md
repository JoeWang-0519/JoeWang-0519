# Idea:
In this version (v3), we take the click path into consideration. The logic to combine click-path with login model is: 

- In the data perspective, we observe that there exists cluster behavior. Therefore, in the previous version, we take 'no_acct_same_umid' into consideration;
- The disadvantage is, this will increase FP ideally. That is to say, the feature is too rough, s.t it covers more than ATO;
- To avoid this, we can do things as follow:
   - for each login, check the previous order record with the same login umid (if exists);
   - use the closest login time (with one order record) and find the click path;
   - find the click embedding (even other click-related features).
- This can be viewed as another fine way to make full use of 'cluster behavior'.
