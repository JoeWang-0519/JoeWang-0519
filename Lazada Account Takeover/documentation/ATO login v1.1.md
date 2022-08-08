#  1. White Samples (Done)
For white samples, building piplines as follows (criterion):

- select (wallet/bank-card/info-change) = 0 (click data) from 0201 to 0601
- Try to sample w.r.t histogram to keep the distribution of umid #

(reason is, we want our choice of white samples changes the distribution of features)

## Pipline:
Build piplines as follow (Consider **_the customers from 0201 to 0601_** in click table):

- Choose (wallet/bank-add/bank-list/info-change) = 0;
   - **_Totally 31728574/56935800 records. _**There are 56935800 distinct user_id within 4 months, 31728573 of which have 0 abnormal records.
- Match with 'lzd_secods.odl_event_async_lazada_login_success' table, find the **_latest login record_** and the previous 14 days login records (number of distinct umid);
   - We can only store those active account to achieve meaningful information, e.g., over the past 4 months, login_count >=100 and the difference between first login time and last login time >= 2 months;
      - **_288323/31728574 records_**
- Check the **_distribution of distinct umid #_** and do sampling to a reasonable number;
   - **_131/288323_**: # of distinct umid = **_0_** (they may use 3rd pc to login within past 14 days 数据问题？);
   - **_281682/288323_**: # of distinct umid =**_ 1_** (majority part);
   - **_6070/288323_**: # of distinct umid = **_2_**
   - **_314/288323_**: # of distinct umid = **_3_**
   - **_62/288323_**: # of distinct umid = **_4_**
   - **_15/288323_**: # of distinct umid = **_5_**
   - **_10/288323_**: # of distinct umid = **_6_**
   - **_10/288323_**: # of distinct umid = **_7_**
   - **_7/288323_**: # of distinct umid = **_8_**
   - **_1/288323_**: # of distinct umid = **_9_**
   - **_21/288323_**: # of distinct umid >= **_10 (kick out)_**
      - further check on useragent (required later, in the first version, we kick out)
- For the aim of **robustness**, in the **first version**, we try to **s**_**ample around 30000 white samples**_, which constitutes:
   - **_28168 samples_** that distinct umid # = **_1_**;
   - **_3000 samples_** that disticnt umid # = **_2_**;
   - **_550 others_** are full-sampling;
   - **_totally 31718 white samples_**;
```

-- add-bank/change-info/wallet records = 0
SET odps.instance.priority = 0;

drop table if exists lazada_biz_sec_dev.white_acct_list;
create table if not exists lazada_biz_sec_dev.white_acct_list LIFECYCLE 60 as

select *
from
    (
        SELECT 
            a.user_id,
            sum(a.indicator_ATO) as cnt_suspicious
        from 
            (
                select   
                    user_id,
                    case when (url like '%wallet%') or (url like '%bank-add%') or (url like '%bank-list%') or (url like '%info-change%') then '1'
                        else '0'
                    end as indicator_ATO -- 1 represents suspicious, 0 represents non-suspicious
                from alilog.dwd_lzd_log_ut_pv_di
                where ds >= '20220221' and ds <= '20220601'
                and venture = 'ID'
                and user_id >0
                and url_type = 'other'
            ) a
        group by a.user_id
    )
;

drop table if exists lazada_biz_sec_dev.white_acct_list_cnt0;
create table if not exists lazada_biz_sec_dev.white_acct_list_cnt0 LIFECYCLE 60 as
select * from lazada_biz_sec_dev.white_acct_list where cnt_suspicious = 0 and user_id > 0;

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- For those white samples, check # of distinct umids in past 14 days
-- Firstly, prepare the full corresponding login table

set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base LIFECYCLE 60 as

select 
    a.user_id as user_id,
    b.umid,
    b.receive_time,
    b.envdata_useragent,
    b.logindata_logintype,
    b.ipparse_ipisp
from 
    (
        select 
            user_id
        from lazada_biz_sec_dev.white_acct_list
        where cnt_suspicious = 0
        and user_id > 0
    )   a
left join
    (
        select acctdata_userid,
            from_unixtime(receive_time/1000) as receive_time,
            umid,
            envdata_useragent,
            logindata_logintype,
            ipparse_ipisp
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220201' and substr(ds,1,8) <= '20220601'
        and acsdata_cntry = 'id'
        and otherdata_issucc = 'true'
        and acctdata_bizrole = 'byr'
    )   b
on a.user_id = b.acctdata_userid
;


-- Secondly, construct the number of login number per user_id
set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base2;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base2 LIFECYCLE 60 as

select 
    user_id,
    login_cnt,
    latest_login_date
from
    (
        select 
            user_id,
            count(distinct receive_time) as login_cnt,
            datediff(max(receive_time), min(receive_time), 'mm') as last_mon,
            max(receive_time) as latest_login_date
        from lazada_biz_sec_dev.white_acct_logrec_base 
        group by user_id
    )
where login_cnt > 100
and last_mon >= 2
;


-- Thirdly, check the distinct umid # over past 14 days distribution for these data

set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base3;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base3 LIFECYCLE 60 as

SELECT 
    user_id,
    count(distinct umid) as distinct_umid_cnt_14d,
    count(distinct receive_time) as distinct_login_cnt_14d,
    count(distinct ipparse_ipisp) as distinct_ipisp_cnt_14d
from
    (
        SELECT 
            b.user_id,
            b.receive_time,
            a.latest_login_date,
            b.umid,
            b.envdata_useragent,
            b.logindata_logintype,
            b.ipparse_ipisp

        FROM 
            (
                select 
                    *
                from lazada_biz_sec_dev.white_acct_logrec_base2
            )   a
        left JOIN 
            (
                select 
                    *
                from lazada_biz_sec_dev.white_acct_logrec_base
            )   b
        on a.user_id = b.user_id and datediff(a.latest_login_date, b.receive_time, 'dd') <= 14
    )
group by user_id
;

-----------------------------------------------------------------------------------------------------------------------------
-- Lastly, sampling
-- 分层采样

set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base3_1;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base3_1 LIFECYCLE 60 as

select * from lazada_biz_sec_dev.white_acct_logrec_base3 where distinct_umid_cnt_14d = 1;

drop table if exists lazada_biz_sec_dev.white_acct_logrec_base3_2;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base3_2 LIFECYCLE 60 as

select * from lazada_biz_sec_dev.white_acct_logrec_base3 where distinct_umid_cnt_14d = 2;

drop table if exists lazada_biz_sec_dev.white_acct_logrec_base3_3;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base3_3 LIFECYCLE 60 as

select * from lazada_biz_sec_dev.white_acct_logrec_base3 where distinct_umid_cnt_14d = 0 or distinct_umid_cnt_14d >= 3;


-- white samples:
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base4;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base4 LIFECYCLE 60 as

select 
    *
from lazada_biz_sec_dev.white_acct_logrec_base3_3
where distinct_umid_cnt_14d < 10

union all 
    (
        select
            *
        from lazada_biz_sec_dev.white_acct_logrec_base3_2
        order by RAND()
        limit 3000
    )

union all
    (
        select
            *
        from lazada_biz_sec_dev.white_acct_logrec_base3_1
        order by RAND()
        limit 28168
    )
;

-- the final white samples and their corresponding login record
drop table if exists lazada_biz_sec_dev.white_ato_login_sample;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample LIFECYCLE 60 as

select
    a.user_id,
    c.umid, -- normal umid
    b.latest_login_date,
    c.ip,
    c.useragent,
    c.acsdata_entrance,
    c.app_version,
    c.ipparse_ipisp,
    c.ipparse_ipcntryname,
    c.ipparse_ipprovname,
    c.logindata_logintype,
    a.distinct_umid_cnt_14d,
    a.distinct_login_cnt_14d,
    a.distinct_ipisp_cnt_14d

from
    (
        select 
            * 
        from lazada_biz_sec_dev.white_acct_logrec_base4 
    )   a

left join 
    (
        select 
            *
        from lazada_biz_sec_dev.white_acct_logrec_base2
    )   b 
on a.user_id = b.user_id

left JOIN 
    (
        select 
            acctdata_userid,
            umid,
            FROM_UNIXTIME(receive_time/1000) as receive_time,
            envdata_ip as ip,
            envdata_useragent as useragent,
            acsdata_entrance,
            appdata_appver as app_version,
            ipparse_ipisp,
            ipparse_ipcntryname,
            ipparse_ipprovname,
            logindata_logintype

        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220201' and substr(ds,1,8) <= '20220601'
        and acsdata_cntry = 'id'
        and otherdata_issucc = 'true'
        and acctdata_bizrole = 'byr'
    )   c
on b.user_id = c.acctdata_userid and b.latest_login_date = c.receive_time
;

drop table if exists lazada_biz_sec_dev.white_ato_login_sample_v1;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_v1 LIFECYCLE 1 as

-- 去重复(login_table同一时间可能有多次登陆,ip等信息会有微小不同)
SELECT 
    user_id,
    max(umid) as umid, -- normal umid
    max(latest_login_date) as latest_login_date,
    max(ip) as ip,
    max(useragent) as useragent,
    max(acsdata_entrance) as acsdata_entrance,
    max(app_version) as app_version,
    max(ipparse_ipisp) as ipparse_ipisp,
    max(ipparse_ipcntryname) as ipparse_ipcntryname,
    max(ipparse_ipprovname) as ipparse_ipprovname,
    max(logindata_logintype) as logindata_logintype,
    max(distinct_umid_cnt_14d) as distinct_umid_cnt_14d,
    max(distinct_login_cnt_14d) as distinct_login_cnt_14d,
    max(distinct_ipisp_cnt_14d) as distinct_ipisp_cnt_14d
FROM
    lazada_biz_sec_dev.white_ato_login_sample
group by user_id
;
```

# 2. Black Samples (Done)
The key-point is to determine the abnormal login time for each ATO case. 
Our intuition is, we focus on the order_create_time, and select the 2 nearest suspicous login records. We collect these 2 abnormal umids (corresponding to the earlier and later one) and treat the earliest one as the first abnormal login record. 

   - **_逆向打款 -> refund -> 确定逆向订单 (__Next Version can give more precise ATO MO__)_**
- Abnormal umids definition: we wil use the most frequent umid as customer's umid, those umids which are different from that one is the abnormal umids;
- There are three scenorios:
   - one is 'null', then we just use the other one;
   - both same, use the same one;
   - different, further check

## Pipline:
Thus, for black samples, building piplines as follows:

- select the **_earliest ATO record with corresponding order_id_** for each buyer from 'byr_ato_case_sample';
   - 1711 samples (include 5 _'null' buyer_id_, so kick out)
      - 1706 samples
- match with 'lazada_cdm.dwd_lzd_trd_core_create_di' table **for the corresponding **_**buyer_id and order_create_time**;_
   - 43/1706: cannot find the corresponding order records;
   - 200/1706: in the order records, the buyer_id is different from the buyer_id that creates ATO cases;
      - This case, the customer may use other accounts to create cases. Thus we focus on the order_buyer_id;
   - Therefore, we kick out those 43 samples for which we cannot match order records
      - 1706 - 43 = 1663 samples
      - Here, there exists **_17/1663 cases that different users make the same ATO case._**
         - To conclude, there are **_1646 different ATO orders (distinct order_id)_**. And here, there exists **_9/1646 cases that order_id corresponds to the same user_**.
         - There are **_1637 users' distinct ATO orders _**(9 users have multiple ATO orders).
         - Here, for the same user, we choose the earliest ATO order (**_totally 1637_**)
   - To conclude, we choose 
      - For different created ATO case with one order, we choose the latest one (**ATO create time**)since we assume that after this time point, the account is more likely to be safe.
      - For different ATO orders with one user, we choose the earliest one (**Order create time**)
      - Based on these 2 choice manner,  we collect **_1637_** data
- match with 'lzd_secods.odl_event_async_lazada_login_success' table for all umids from 0201 to 0601 to find the frequent umid; (double check)
   - **218/1637: only 1 used umid (there must be no abnormal login for these cases);**
   - 1419/1637: >= 2 used umids (potential ATO)
      - 7/1419: have >= 10 different umids (**_too many different umids seem to be suspicious account_**)
      - 1412/1419:  2 <= different umids < 10 
         - **Define frequqent umid: **
            - max(login times) >=4 and the corresponding umid	(_can modify_)
            - Next generation: explode cleverer ways for determine frequent umids
               - One idea: use percentage of all login number, select some thresholds, then we may have multiple frequent umids (if use max, we can just have one).
               - One compensation: s
         - 42/1412 : max(login times) <= 3, inactive customers, kick out
         - 1370/1412:  max(login times) >= 4, our interest
            - 9/1370: multiple maximum, kick out
            - 1361/1370: one max login times record, treat as frequent umid! (**_totally 1361_**)
- match with 'lzd_secods.odl_event_async_lazada_login_success' table, **find the login records that, 1. not frequent umid; 2. logintype != 'auto'; 3. the nearest two (before and after). Moreover, we require that, cnt_umid_login <= 10;**
   - **_totally 1361 records_**
      - **_before: 340_**
      - **_after:  1092_**
- choose the record that satisfies **_either of these 3 scenarios:_** 
   - 1. umid_before = '\N' but umid_after exists; 
   - 2. umid_before exists but umid_after = '\N'; 
   - 3. umid_before and umid_after both exists and umid_before = umid_after;
   - **totally 1155 records (which is our black samples)**

With this procedure, there are **1155** black samples;
```
--odps sql 
--********************************************************************--
--author:WANG, JIANGYI
--create time:2022-06-08 17:36:51
--********************************************************************--
----------------------------------------------------------------------------------------------------------------------------------
--Black sample Extraction
-- 对于多个报案记录，取最早的报案记录

SET odps.instance.priority = 0;

drop table if exists lazada_biz_sec_dev.black_acct_order_create;
create table if not exists lazada_biz_sec_dev.black_acct_order_create LIFECYCLE 600 as

SELECT 
    tab.*
from 
    (
        select 
            a1.ATO_create_date,   -- singapore time
            dateadd(a2.order_create_date, 1, 'hour') as order_create_date, -- transfer to singapore time
            a1.buyer_id as create_buyer_id,
            a2.buyer_id as order_buyer_id,
            a1.buyer_id - a2.buyer_id as diff_id,
            a1.order_number,
            a1.hit_tag
        from
            (
                SELECT a.created_date as ATO_create_date,
                    a.buyer_id as buyer_id,
                    a.hit_tag,
                    b.order_number
                
                FROM 
                    (
                        SELECT 
                            created_date,
                            buyer_id,
                            order_tag,
                            case
                                when ARRAY_CONTAINS(COLLECT_LIST(hit_tag), 'R_4336701') then 'R_4336701'
                                else 'NULL'
                            end as hit_tag
                        from 
                            (
                                select min(created_date) as created_date, -- want find the earliest case
                                    buyer_id,
                                    order_tag,
                                    hit_tag,
                                    venture
                                from 
                                    (
                                        select *
                                        from lzd_secapp_dev.byr_ato_case_sample
                                        where venture = 'ID'
                                        and order_tag = 1
                                    )
                                --and hit_tag <> 'NULL'             -- Cancel the requirement on hit_tag
                                                                    -- We allow some that not trigger the second verification
                                group by buyer_id, order_tag, venture, hit_tag
                            )
                            group by created_date, buyer_id, order_tag
                    )   a

                left join
                    (
                        SELECT created_date,
                            buyer_id,
                            order_number,
                            hit_tag
                        from lzd_secapp_dev.byr_ato_case_sample 
                        where order_tag = 1
                        and venture = 'ID'
                    ) b
                on a.created_date = b.created_date and a.buyer_id = b.buyer_id and a.hit_tag = b.hit_tag
                where a.buyer_id <> '\N'
            )   a1

        left join 
            (
                select distinct
                    sales_order_id,
                    order_create_date,       --local time
                    buyer_id
                from lazada_cdm.dwd_lzd_trd_core_create_di
                where ds >= '20220201'
                and venture = 'ID'
            ) a2
        on a1.order_number = a2.sales_order_id
    )   tab
where tab.order_create_date >= '2022-02-01 00:00:00'  -- kick out those '\N' 
;

---------------------------------------------------------------------------------------------------------------------------------------
-- Find the Abnormal Login Time
-- 1. find the frequent devices
-- base1 have
    -- ATO_create_date, order_create_date, order_buyer_id, order_number, id_flag, hit_flag

drop table if exists lazada_biz_sec_dev.black_acct_order_create_base1;
create table if not exists lazada_biz_sec_dev.black_acct_order_create_base1 LIFECYCLE 600 as

select 
    ato_create_date,
    order_create_date,
    order_buyer_id,
    order_number,
    case 
        when diff_id = 0 then '0'
        ELSE '1'
    end as id_flag, -- 0表示create_buyer_id和order_buyer_id一致
    CASE 
        when hit_tag = 'R_4336701' then '1'
        else '0'
    end as hit_flag -- 1表示触发二次验证
from lazada_biz_sec_dev.black_acct_order_create;


-----------------------------------------------------------------------------------------------------------
--1637 total cases
-- base2 only have
    -- order_create_date, order_buyer_id, order_number

drop table if exists lazada_biz_sec_dev.black_acct_order_create_base2;
create table if not exists lazada_biz_sec_dev.black_acct_order_create_base2 LIFECYCLE 6000 as
select
    a.order_create_date,
    a.order_buyer_id,
    b.order_number
from 
    (
        select 
            --ato_create_date,
            min(order_create_date) as order_create_date,
            order_buyer_id
        from lazada_biz_sec_dev.black_acct_order_create_base1 
        group by order_buyer_id 
    )   a
left join
    (
        select distinct
            order_create_date,
            order_buyer_id,
            order_number
        from  lazada_biz_sec_dev.black_acct_order_create_base1 
    )   b
on a.order_create_date = b.order_create_date and a.order_buyer_id = b.order_buyer_id
;

drop table if exists lazada_biz_sec_dev.black_acct_order_create_base25;
create table if not exists lazada_biz_sec_dev.black_acct_order_create_base25 LIFECYCLE 6000 as
SELECT 
    max(ato_create_date) as ato_create_date, -- idea is, for the latest ato_create_date, the case is more likely to be solved,
    order_create_date,
    order_buyer_id,
    order_number
FROM 
    (
            SELECT 
            b.ato_create_date,
            a.*
        from lazada_biz_sec_dev.black_acct_order_create_base2   a
        left JOIN 
        (
            SELECT 
                order_number,
                order_buyer_id,
                ato_create_date
            from lazada_biz_sec_dev.black_acct_order_create_base1 
        )   b
        on a.order_buyer_id = b.order_buyer_id and a.order_number = b.order_number
    )
group by order_create_date, order_buyer_id, order_number
;
        

-----------------------------------------------------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.black_acct_freq_umid;
create table if not exists lazada_biz_sec_dev.black_acct_freq_umid LIFECYCLE 6000 as

select 
    tab.order_buyer_id,
    tab.umid,
    count(1) as cnt_umid_login
from
    (
        SELECT a.order_buyer_id,
            b.umid
        FROM lazada_biz_sec_dev.black_acct_order_create_base2   a
        left join 
            (
                SELECT umid,
                    acctdata_userid
                FROM lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20220201' and SUBSTR(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr' 
            )   b
        on a.order_buyer_id = b.acctdata_userid
    )   tab
group by tab.order_buyer_id, tab.umid
;


------------------------------------------------------------------------------------------------------------
-- construct the table that, 
-- 1. different umid in [2,9]
-- 2. max login umid times >= 4
drop table if exists lazada_biz_sec_dev.black_acct_order_create_base3;
create table if not exists lazada_biz_sec_dev.black_acct_order_create_base3 LIFECYCLE 6000 as

select
    a1.order_buyer_id,
    a2.umid,
    a1.freq_cnt_umid
from
    (
        SELECT 
        *
        FROM 
            (
                SELECT 
                    a.order_buyer_id,
                    max(b.cnt_umid_login) as freq_cnt_umid
                FROM 
                    (
                        SELECT 
                            order_buyer_id
                        from
                            (
                                select order_buyer_id,
                                    count(order_buyer_id) as umid_cnt
                                from lazada_biz_sec_dev.black_acct_freq_umid 
                                group by order_buyer_id
                            )
                        where umid_cnt >= 2 and umid_cnt < 10
                    )   a

                left join
                    lazada_biz_sec_dev.black_acct_freq_umid b

                on  a.order_buyer_id = b.order_buyer_id
                group by a.order_buyer_id
            )
        where freq_cnt_umid >=4
    )   a1

left JOIN 
    (
        select *
        from lazada_biz_sec_dev.black_acct_freq_umid
    )   a2
on a1.freq_cnt_umid = a2.cnt_umid_login and a1.order_buyer_id = a2.order_buyer_id
;
------------------------------------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.black_freq_umid;
create table if not exists lazada_biz_sec_dev.black_freq_umid LIFECYCLE 6000 as

select
    a2.ato_create_date,
    a2.order_create_date,
    a1.order_buyer_id,
    a2.order_number,
    a1.freq_umid
FROM 
    (
        SELECT 
            a.order_buyer_id,
            b.umid as freq_umid
        FROM 
            (
                select *
                FROM 
                    (
                        select order_buyer_id,
                            count(freq_cnt_umid) as flag
                        from lazada_biz_sec_dev.black_acct_order_create_base3
                        group by order_buyer_id
                    )
                where flag = 1
            )   a

        left JOIN 
            (
                SELECT order_buyer_id,
                    umid
                from lazada_biz_sec_dev.black_acct_order_create_base3
            )   b
        on a.order_buyer_id = b.order_buyer_id
    )   a1
left JOIN 
    (
        select  
        order_create_date,
        order_buyer_id,
        order_number,
        ato_create_date
        from lazada_biz_sec_dev.black_acct_order_create_base25
    )   a2

on a1.order_buyer_id = a2.order_buyer_id
;


-----------------------------------------------------------------------------------------------------------------
-- 2. Find out the first abnormal login
drop table if exists lazada_biz_sec_dev.black_all_umid;
create table if not exists lazada_biz_sec_dev.black_all_umid LIFECYCLE 6000 as

select 
    a.ato_create_date,
    a.order_create_date,
    a.order_buyer_id,
    a.order_number,
    a.freq_umid,
    b.login_date,
    b.umid,
    b.otherdata_issucc,
    b.envdata_useragent,
    b.logindata_logintype
from 
    (
        select 
            ato_create_date,
            order_create_date,
            order_buyer_id,
            order_number,
            freq_umid
        from lazada_biz_sec_dev.black_freq_umid
    )   a
left JOIN 
    (
        select 
            umid,
            from_unixtime(receive_time/1000) as login_date,
            acctdata_userid,
            otherdata_issucc,
            envdata_useragent,
            logindata_logintype
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220201' and substr(ds,1,8) <= '20220601'
        and acsdata_cntry = 'id'
        --and otherdata_issucc = 'true'
        and acctdata_bizrole = 'byr' 
    )   b
on a.order_buyer_id = b.acctdata_userid
;




drop table if exists lazada_biz_sec_dev.black_all_umid_distinct;
create table if not exists lazada_biz_sec_dev.black_all_umid_distinct LIFECYCLE 365 as

select distinct *,
    datediff(login_date, order_create_date,'mi') as date_diff
from lazada_biz_sec_dev.black_all_umid;


----------------------------------------------------------------------------------------------------------------------------------------------------

drop table if exists lazada_biz_sec_dev.black_before_tmp;
create table if not exists lazada_biz_sec_dev.black_before_tmp LIFECYCLE 365 as


SELECT 
    a.ato_create_date,
    a.order_create_date,
    a.order_buyer_id,
    a.order_number,
    a.freq_umid,
    b.login_date,
    b.umid,
    b.otherdata_issucc,
    b.envdata_useragent,
    b.logindata_logintype,
    a.abnormal_date_diff
FROM 
    (
        select
            tmp.ato_create_date,
            tmp.order_create_date,
            tmp.order_buyer_id,
            tmp.order_number,
            tmp.freq_umid,
            max(date_diff) as abnormal_date_diff
        from
            (
                -- select non-freq_umid login
                select *
                from lazada_biz_sec_dev.black_all_umid_distinct
                where date_diff < 0
                and umid <> freq_umid
                and logindata_logintype <> 'auto'
                and otherdata_issucc = 'true'
            )   tmp
        group by tmp.ato_create_date, tmp.order_create_date, tmp.order_buyer_id, tmp.order_number, tmp.freq_umid
    )   a
left JOIN 
    (
        SELECT 
            *
        from lazada_biz_sec_dev.black_all_umid_distinct
        where otherdata_issucc = 'true'
        and logindata_logintype <> 'auto'
    )   b
on a.order_number = b.order_number and a.abnormal_date_diff = b.date_diff
;

--------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.black_before;
create table if not exists lazada_biz_sec_dev.black_before LIFECYCLE 365 as


select
    b.*,
    c.cnt_umid_login
FROM   
    (
        select order_number,
            min(login_date) as login_date
        from lazada_biz_sec_dev.black_before_tmp
        group by order_number
    )   a
left join 
    (
        select * 
        from lazada_biz_sec_dev.black_before_tmp
    )   b
on a.order_number = b.order_number and a.login_date = b.login_date
left join lazada_biz_sec_dev.black_acct_freq_umid   c
on b.order_buyer_id = c.order_buyer_id and b.umid = c.umid
;

----------------------------------------------------------------------------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.black_after_tmp;
create table if not exists lazada_biz_sec_dev.black_after_tmp LIFECYCLE 365 as

SELECT 
    a.ato_create_date,
    a.order_create_date,
    a.order_buyer_id,
    a.order_number,
    a.freq_umid,
    b.login_date,
    b.umid,
    b.otherdata_issucc,
    b.envdata_useragent,
    b.logindata_logintype,
    a.abnormal_date_diff
FROM 
    (
        select
            tmp.ato_create_date,
            tmp.order_create_date,
            tmp.order_buyer_id,
            tmp.order_number,
            tmp.freq_umid,
            min(date_diff) as abnormal_date_diff
        from
            (
                -- select non-freq_umid login
                select *
                from lazada_biz_sec_dev.black_all_umid_distinct
                where date_diff >= 0
                and umid <> freq_umid
                and logindata_logintype <> 'auto'
                and otherdata_issucc = 'true'
            )   tmp
        group by tmp.ato_create_date, tmp.order_create_date, tmp.order_buyer_id, tmp.order_number, tmp.freq_umid
    )   a
left JOIN 
    (
        SELECT 
            *
        from lazada_biz_sec_dev.black_all_umid_distinct
        where otherdata_issucc = 'true'
        and logindata_logintype <> 'auto'
    )   b
on a.order_number = b.order_number and a.abnormal_date_diff = b.date_diff
;

--------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.black_after;
create table if not exists lazada_biz_sec_dev.black_after LIFECYCLE 365 as

select
    b.*,
    c.cnt_umid_login
FROM   
    (
        select order_number,
            min(login_date) as login_date
        from lazada_biz_sec_dev.black_after_tmp
        group by order_number
    )   a
left join 
    (
        select * 
        from lazada_biz_sec_dev.black_after_tmp
    )   b
on a.order_number = b.order_number and a.login_date = b.login_date
left join lazada_biz_sec_dev.black_acct_freq_umid   c
on b.order_buyer_id = c.order_buyer_id and b.umid = c.umid
;



------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.black_before_after;
create table if not exists lazada_biz_sec_dev.black_before_after LIFECYCLE 365 as
       
select *       
from
    (
        select
            a.ato_create_date,
            a.order_create_date,
            a.order_buyer_id,
            a.order_number,
            a.freq_umid,
            b.login_date as login_date_before,
            b.umid as umid_before,
            b.otherdata_issucc as issucc_before,
            b.envdata_useragent as useragent_before,
            b.logindata_logintype as logintype_before,
            b.abnormal_date_diff as diff_before,
            b.cnt_umid_login as cnt_umid_login_before,
            c.login_date as login_date_after,
            c.umid as umid_after,
            c.otherdata_issucc as issucc_after,
            c.envdata_useragent as useragent_after,
            c.logindata_logintype as logintype_after,
            c.abnormal_date_diff as diff_after,
            c.cnt_umid_login as cnt_umid_login_after

        FROM lazada_biz_sec_dev.black_freq_umid a
        left join
            (
                select * 
                FROM lazada_biz_sec_dev.black_before
                where cnt_umid_login <= 10
            )   b
        on a.order_number = b.order_number
        left JOIN 
            (
                select * 
                from lazada_biz_sec_dev.black_after
                where cnt_umid_login <= 10
            )   c
        on a.order_number = c.order_number
    )
where (cnt_umid_login_before is Null and cnt_umid_login_after is not Null)
    or (cnt_umid_login_before is not Null and cnt_umid_login_after is Null)
    or (cnt_umid_login_before is not Null and cnt_umid_login_after is not Null and umid_before = umid_after)
;

------------------------------------------------------------------------------------------------------
-- Find the abnormal login umid and corresponding first records

drop table if exists lazada_biz_sec_dev.black_abnormal_umid;
create table if not exists lazada_biz_sec_dev.black_abnormal_umid LIFECYCLE 365 as
select 
    ato_create_date,
    order_create_date,
    order_buyer_id,
    order_number,
    freq_umid,
    CASE 
        when umid_before is Null then umid_after
        when umid_after is Null then umid_before
        else umid_after
    end as abnormal_umid
from lazada_biz_sec_dev.black_before_after
;


drop table if exists lazada_biz_sec_dev.black_abnormal_umid_total_login;
create table if not exists lazada_biz_sec_dev.black_abnormal_umid_total_login LIFECYCLE 365 as

select a.ato_create_date,
    a.order_create_date,
    a.order_number,
    a.order_buyer_id,
    a.freq_umid,
    a.abnormal_umid,
    b.login_date,
    b.ip,
    b.useragent,
    b.acsdata_entrance,
    b.app_version,
    b.ipparse_ipisp,
    b.ipparse_ipcntryname,
    b.logindata_logintype

from lazada_biz_sec_dev.black_abnormal_umid a
left join
    (
        select umid,
            from_unixtime(receive_time/1000) as login_date,
            envdata_ip as ip,
            envdata_useragent as useragent,
            acctdata_userid,
            acsdata_entrance,
            appdata_appver as app_version,
            ipparse_ipisp,
            ipparse_ipcntryname,
            logindata_logintype
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220201' and substr(ds,1,8) <= '20220601'
        and acsdata_cntry = 'id'
        and otherdata_issucc = 'true'
        and acctdata_bizrole = 'byr' 
    )   b
on a.order_buyer_id = b.acctdata_userid and a.abnormal_umid = b.umid
;


drop table if exists lazada_biz_sec_dev.black_ato_login_sample;
create table if not exists lazada_biz_sec_dev.black_ato_login_sample LIFECYCLE 365 as
SELECT 
    b.ato_create_date,
    b.order_create_date,
    b.order_number,
    a.order_buyer_id,
    b.freq_umid,
    b.abnormal_umid,
    a.earliest_abnormal_login,
    b.ip,
    b.useragent,
    b.acsdata_entrance,
    b.app_version,
    b.ipparse_ipisp,
    b.ipparse_ipcntryname,
    b.logindata_logintype
FROM 
    (
        select 
            order_buyer_id,
            min(login_date) as earliest_abnormal_login
        from lazada_biz_sec_dev.black_abnormal_umid_total_login
        group by order_buyer_id
    )   a
LEFT  JOIN 
    lazada_biz_sec_dev.black_abnormal_umid_total_login  b
on a.order_buyer_id = b.order_buyer_id and a.earliest_abnormal_login = b.login_date
;

```
## Black samples analysis:
### 1. MO (Scenarios)

- **_64/1155_**: order_create_date >= earliest_abnormal_login_date, which can be **_direct scam case;_**
- **_1091/1155_**: order_create_date < earliest_abnormal_login_Date, which must be **_reverse scam case_**.
### 2. One umid, multiple ATO login records
There are totally **_1155 different buyers_** who are suffered from ATO. However, for the abnormal_umid that login their accounts in the first time, there are only **_430_** different umids.
For example, umid = 'WV10z625580203ac453db00060c0208e6' login 47 different accounts.


# 3. Features (Done)
## Analysis:
In the login step, we can have features as follows:

1. Previous order abnormal behaviour:
   1. seller ATO (reverse scame)
      1. will have abnormal order info (assume those sellers will use some dicounted products or something to attract more customers and sellers need to customers' payments to achieve their information)
   2. non-seller ATO (direct scam)
      1. will not have abnormal order info (in this part, sellers can achieve customers information directly from other parties)
2. Abnormal login environment difference:
   - For both 2 cases, this feature is similar and obvious, but not so powerful.
3. Login cluster behaviours:
   - From data analysis, we find there exists patterns for **_Similar Scammers Do Mulitiple ATO Cases_**.
4. Device indicators:
   - Assume that some of the devices that do scam are more likely to be rooted or something.

We combine these all as our features.
## Feature list:
Abnormal environment difference: 

| index | feature | remark |
| --- | --- | --- |
|  | buyer_id |  |
|  | login_date |  |
|  | labels (black/white) |  |
| 1 | no_unique_umid_14d |  |
| 2 | no_unique_ip2_14d |  |
| 3 | no_unique_ipisp_14d |  |
| 4 | id_new_umid_14d | indicator of new umid (14d) |
| 5 | id_new_ip2_14d |  |
| 6 | id_new_ipisp_14d |  |
| * | is_auto | logintype (**_next version_**) |

Order info features: ~~(时间点拉长)~~ (**_next version focus on sellers' side_**)

| index | feature | remark |
| --- | --- | --- |
| 7 | id_umid_same_seller_14d | indicator of same device with some ordered sellers |
| 8 | id_ip2_same_seller_14d |  |
| 9 | avg_price_per_order_14d |  |
| 10 | std_price_per_order_14d |  |
| 11 | avg_discount_per_order_14d |  |
| 12 | std_discount_per_order_14d |  |
| 13 | avg_shpfee_per_order_14d |  |
| 14 | std_shpfee_per_order_14d |  |
| * | id_susp_paymethod_14d | indicator of suspicious payment method over past 14 days (**_next version_**) |

Login cluster features:

| index | feature | remark |
| --- | --- | --- |
| 15 | no_acct_umid_14d | number of different accounts for the same umid (14d) |
| 16 | ipprovname |  |

Sellers' side features:

| index | feature | remark |
| --- | --- | --- |
| * | max_cancel_rate_14d | maximum of cancel rate for sellers over past 14d |
| * | discount/shipfee/price | **_similar to order features, will replace those order info in next version_** |

Device indicators (from Chloe): 

| index | feature | remark |
| --- | --- | --- |
| * | is_root, is_shell etc. | **_next version_** |



## Pipline:
Thus, for black samples, building piplines as follows:

- In our selection of white/black samples, we have:
   - order_buyer_id;
   - login_time;

Our aim is to make features based on these 2 information.

- Environment Features: 'lzd_secods.odl_event_async_lazada_login_success' table
- Order Info Features: 'lazada_cdm.dwd_lzd_trd_core_create_di' table and 'lzd_secods.odl_event_async_lazada_login_success' table (**_based on sellers info_**)
```
--odps sql 
--********************************************************************--
--author:WANG, JIANGYI
--create time:2022-06-18 10:06:07
--********************************************************************--

-- Basic information
-- buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info;
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info LIFECYCLE 30 as

select 
    order_buyer_id as buyer_id,
    earliest_abnormal_login as current_login_time,
    abnormal_umid as current_umid,
    concat(split_part(ip,'.',1), split_part(ip,'.',2)) as current_ip2, --可以调整成ip1字段和ip2字段
    ipparse_ipisp as current_ipisp,
    ipparse_ipprovname as current_ipprovname
from lazada_biz_sec_dev.black_ato_login_sample
;


---------------------------------------------------------------------------------------------------------------------------

-- Combine with previsou 14 days login records
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full; -- basic_info_full_login
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full LIFECYCLE 60 as

select 
    a.*,
    b.previous_login_time,
    b.previous_umid,
    b.previous_ip2,
    b.previous_ipisp,
    b.previous_ipprovname
from lazada_biz_sec_dev.black_ato_login_sample_basic_info   a
left join
    (
        select
            acctdata_userid,
            FROM_UNIXTIME(receive_time/1000) as previous_login_time,
            umid as previous_umid,
            concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2)) as previous_ip2,
            ipparse_ipisp as previous_ipisp,
            ipparse_ipprovname as previous_ipprovname
        from lzd_secods.odl_event_async_lazada_login_success
        where SUBSTR(ds,1,8) >= '20220201' and SUBSTR(ds,1,8) <= '20220601'
        and acsdata_cntry = 'id'
        and otherdata_issucc = 'true'
        and acctdata_bizrole = 'byr'  
    )   b
on a.buyer_id = b.acctdata_userid and a.current_login_time > previous_login_time and DATEDIFF(a.current_login_time, b.previous_login_time, 'dd') <= 14
;

--------------------------------------------------------------------------------------------------------------------------

-- environment features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_env;
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_env LIFECYCLE 60 as

SELECT 
    buyer_id,
    current_login_time,
    current_umid,
    current_ip2,
    current_ipisp,
    current_ipprovname,
    no_unique_umid_14d,
    no_unique_ip2_14d,
    no_unique_ipisp_14d,
    CASE 
        when ARRAY_CONTAINS(list_previous_umid_14d, current_umid) then '0' else '1'
    end as id_new_umid_14d,
    CASE 
        when ARRAY_CONTAINS(list_previous_ip2_14d, current_ip2) then '0' else '1'
    end as id_new_ip2_14d,
    CASE 
        when ARRAY_CONTAINS(list_previous_ipisp_14d, current_ipisp) then '0' else '1'
    end as id_new_ipisp_14d

FROM 
    (
        select 
            buyer_id, 
            current_login_time, 
            current_umid, current_ip2, 
            current_ipisp, 
            current_ipprovname,
            count(distinct previous_umid) as no_unique_umid_14d,
            count(distinct previous_ip2) as no_unique_ip2_14d,
            count(distinct previous_ipisp) as no_unique_ipisp_14d,
            COLLECT_LIST(distinct previous_umid) as list_previous_umid_14d,
            COLLECT_LIST(distinct previous_ip2) as list_previous_ip2_14d,
            COLLECT_LIST(distinct previous_ipisp) as list_previous_ipisp_14d

        from lazada_biz_sec_dev.black_ato_login_sample_basic_info_full
        group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname
    )
;


--------------------------------------------------------------------------------------------------------------------------

-- basic_info_full_order
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order; -- basic_info_full_order
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order LIFECYCLE 60 as


SELECT 
    a.buyer_id,
    a.current_login_time,
    a.current_umid,
    a.current_ip2,
    a.current_ipisp,
    a.current_ipprovname,
    b.seller_id,
    b.sales_order_id,
    b.order_create_date,
    b.list_price,
    b.unit_price,
    b.paid_price,
    b.shipping_amount_total,
    b.payment_method

FROM 
    (
        select 
            buyer_id,
            current_login_time,
            current_umid,
            current_ip2,
            current_ipisp,
            current_ipprovname
        from lazada_biz_sec_dev.black_ato_login_sample_basic_info
    )   a

left JOIN
    (
        SELECT 
            seller_id,
            buyer_id,
            sales_order_id,
            list_price,
            unit_price,
            paid_price,
            shipping_amount_total,
            payment_method,
            dateadd(order_create_date, 1, 'hour') as order_create_date -- Convert to Singapore Time
        FROM lazada_cdm.dwd_lzd_trd_core_create_di
        WHERE ds >= '20220110' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.buyer_id = b.buyer_id 
    and DATEDIFF(a.current_login_time, b.order_create_date, 'dd') <= 14 and a.current_login_time > b.order_create_date
;


--------------------------------------------------------------------------------------------------------------------------

-- From the perspective of each order (combine multiple sub-orders together)
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_order; -- basic_info_full_order_group
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_order LIFECYCLE 60 as

SELECT 
    buyer_id,
    current_login_time,
    current_umid,
    current_ip2,
    current_ipisp,
    current_ipprovname,
    collect_list(seller_id) as list_seller_id,
    sales_order_id,
    sum(list_price) as list_price_order,
    sum(unit_price) as unit_price_order,
    sum(paid_price) as paid_price_order,
    max(shipping_amount_total) as shipping_fee_order,
    payment_method
FROM lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order
group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname, sales_order_id, order_create_date, payment_method
;

-- Aim to find the seller (14d) list for each user_id
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_order_seller_list; 
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_order_seller_list LIFECYCLE 60 as

SELECT 
    buyer_id,
    current_login_time,
    current_umid,
    current_ip2,
    current_ipisp,
    current_ipprovname,
    COLLECT_LIST(distinct to_char(seller_id)) as list_seller_id --seller id is BIGINT
FROM lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order
group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname
;


-------------------------------------------------------------------------------------------------------------------

-- Method 2, to achieve id_umid_same_seller_14d, id_ip2_same_seller_14d
-- Starting from 'black_ato_login_sample_basic_info_full_order' table

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_order_seller_list; -- feature_order_full
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_order_seller_list LIFECYCLE 60 as

select 
    buyer_id,
    current_login_time,
    current_umid,
    current_ip2,
    current_ipisp,
    current_ipprovname,
    COLLECT_LIST(distinct to_char(seller_id)) as list_seller_id,
    COLLECT_LIST(distinct seller_umid) as list_seller_umid,
    COLLECT_LIST(distinct seller_ip2) as list_seller_ip2

FROM 
    (
        SELECT 
            a.*,
            b.umid as seller_umid,
            b.ip2 as seller_ip2

        FROM 
            (
                select 
                    buyer_id,
                    current_login_time,
                    current_umid,
                    current_ip2,
                    current_ipisp,
                    current_ipprovname,
                    seller_id
                from lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order 
            )   a 
        left join 
            (
                SELECT
                    acctdata_userid,
                    FROM_UNIXTIME(receive_time/1000) as receive_time,
                    umid,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2)) as ip2
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds, 1, 8) >= '20220201' and substr(ds, 1, 8) <= '20220601'
                and acctdata_bizrole <> 'byr'
                and otherdata_issucc = 'true'
            )   b
        on a.seller_id = b.acctdata_userid and a.current_login_time >= b.receive_time
    )
group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname
;


--------------------------------------------------------------------------------------------------------------------------

-- Order info features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_order; -- feature_order
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_order LIFECYCLE 60 as

select 
    a.*,
    b.list_seller_id,
    CASE 
        when ARRAY_CONTAINS(b.list_seller_umid, a.current_umid) then '1' else '0'
    end as id_umid_same_seller_14d,
    CASE 
        when ARRAY_CONTAINS(b.list_seller_ip2, a.current_ip2) then '1'  else '0'
    end as id_ip2_same_seller_14d

from
    (
        SELECT 
            buyer_id,
            current_login_time,
            current_umid,
            current_ip2,
            current_ipisp,
            current_ipprovname,
            COLLECT_LIST(sales_order_id) as list_sales_order_id_14d,
            avg(paid_price_order) as avg_price_per_order_14d,
            stddev(paid_price_order) as std_price_per_order_14d,
            avg(list_price_order - paid_price_order) as avg_discount_per_order_14d,
            stddev(list_price_order - paid_price_order) as std_discount_per_order_14d,
            avg(shipping_fee_order) as avg_shpfee_per_order_14d,
            stddev(shipping_fee_order) as std_shpfee_per_order_14d,
            COLLECT_LIST(distinct payment_method) as list_payment_method
        FROM lazada_biz_sec_dev.black_ato_login_sample_basic_info_order
        group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname
    )   a

left JOIN 
    (
        SELECT 
            *
        from lazada_biz_sec_dev.black_ato_login_sample_order_seller_list
    )   b
on a.buyer_id = b.buyer_id
;

-------------------------------------------------------------------------------------------------------------------
-- login cluster
-- number of different accounts for the same umid

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_cluster; 
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_cluster LIFECYCLE 60 as

SELECT 
    buyer_id,
    current_login_time,
    current_umid,
    current_ip2,
    current_ipisp,
    current_ipprovname,
    count(distinct login_id) as no_acct_umid_14d
FROM 
    (
        SELECT 
            a.*,
            b.login_id,
            b.login_time
        FROM 
            (
                select
                    buyer_id,
                    current_login_time,
                    current_umid,
                    current_ip2,
                    current_ipisp,
                    current_ipprovname
                from lazada_biz_sec_dev.black_ato_login_sample_order_seller_list
            )   a

        left join
            (
                select
                    acctdata_userid as login_id,
                    umid,
                    FROM_UNIXTIME(receive_time/1000) as login_time
                from lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20220201' and SUBSTR(ds,1,8) <= '20220601'
                and otherdata_issucc = 'true'
            )   b
        on a.current_umid = b.umid and DATEDIFF(a.current_login_time, b.login_time, 'dd') <= 14 and a.current_login_time >= b.login_time
    )
group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname
;

-------------------------------------------------------------------------------------------------------------------
-- Final features


SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature; 
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature LIFECYCLE 60 as

SELECT 
    1 as label, -- black sample
    a.no_unique_umid_14d,
    a.no_unique_ip2_14d,
    a.no_unique_ipisp_14d,
    a.id_new_umid_14d,
    a.id_new_ip2_14d,
    a.id_new_ipisp_14d,
    b.id_umid_same_seller_14d,
    b.id_ip2_same_seller_14d,
    b.avg_price_per_order_14d,
    b.std_price_per_order_14d,
    b.avg_discount_per_order_14d,
    b.std_discount_per_order_14d,
    b.avg_shpfee_per_order_14d,
    b.std_shpfee_per_order_14d,
    c.no_acct_umid_14d

FROM 
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_env
    )   a

left join
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_order 
    )   b
on a.buyer_id = b.buyer_id

left join 
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_cluster 
    )   c
on a.buyer_id = c.buyer_id
;

select * from lazada_biz_sec_dev.black_ato_login_sample_feature;

```

# 4. Model (Done)
For both methods, we split the whole dataset into training set (80%) and testing set (20%). To determine the parameters, we use 5-folds CV. 
To conclude, there are 32873 records in total, and 1155 of them are black samples.
**_-Random Forest Model_**

- The best parameter is:
   -  best estimator: { bootstrap : True class_weight : balanced criterion : gini max_depth : 8 n_estimators : 256 oob_score : True random_state : 0 }
- Performance metric:

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655813968268-8e027f2f-91e1-46ca-9192-8e01f166c089.png#clientId=u00db55b0-abd1-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=249&id=u2a52c002&margin=%5Bobject%20Object%5D&name=image.png&originHeight=498&originWidth=688&originalType=binary&ratio=1&rotation=0&showTitle=false&size=123982&status=done&style=none&taskId=ue708a34e-9445-447a-847d-863a4db812d&title=&width=344)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655814104893-a31d5ff5-fe1e-4ce0-9dc1-bf26e51705d3.png#clientId=u00db55b0-abd1-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=245&id=u1af433c2&margin=%5Bobject%20Object%5D&name=image.png&originHeight=490&originWidth=692&originalType=binary&ratio=1&rotation=0&showTitle=false&size=126846&status=done&style=none&taskId=u89482ff6-638b-49a5-b9c5-d5de10bb060&title=&width=346)

**_-XGBoost_**

- The best parameter is：
   - best estimator:  { colsample_bytree : 0.6 gamma : 1.5 max_depth : 3 min_child_weight : 1 random_state : 0 subsample : 1.0 use_label_encoder : False verbosity : 0 }
- Performance Metric

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655818164672-e43594ad-41ad-4f59-a912-926b89c10a2e.png#clientId=u00db55b0-abd1-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=249&id=uf2c58733&margin=%5Bobject%20Object%5D&name=image.png&originHeight=498&originWidth=656&originalType=binary&ratio=1&rotation=0&showTitle=false&size=127379&status=done&style=none&taskId=ua355353a-7dc8-4266-ade8-938e29d3f6d&title=&width=328)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655818184208-ad06de8a-4d5e-4330-b88d-ea735a5fb5fc.png#clientId=u00db55b0-abd1-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=244&id=u5b896e1f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=488&originWidth=636&originalType=binary&ratio=1&rotation=0&showTitle=false&size=124867&status=done&style=none&taskId=u99d3772d-325b-467d-ace7-334a0a6ba7a&title=&width=318)

# 5. Notation
Temp tables for building features (take white samples as example): 

1. white_ato_login_sample: selected white samples based on manual criteria, along with login_date, login environment etc;
1. white_ato_login_sample_basic_info: abnormal/normal login information tablel;
1. white_ato_login_sample_basic_info_full: previous 14d full login information table;
1. white_ato_login_sample_feature_env: environemnt features;
1. white_ato_login_sample_basic_info_full_order: previous 14d full order information table (product-level);
1. white_ato_login_sample_basic_info_order: combine different products into one order (order-level previous 14d order information table);
1. white_ato_login_sample_order_seller_list: sellers information (umid, ip, id) with respect to each buyer;
1. white_ato_login_sample_feature_order: order features;
1. white_ato_login_sample_feature_cluster: cluster features;
1. white_ato_login_sample_feature: total features;

# 

