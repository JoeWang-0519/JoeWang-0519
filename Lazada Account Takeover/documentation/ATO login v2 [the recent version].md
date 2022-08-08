# 1. Experiment1
Main points: 

- re-select white samples based on modifying the trigger point of our model;
   - we only trigger models for those 4-month new umid;
   - our white samples are:
      - 1. from white samples definition, which guarantee this account hasn't been taken over;
      - 2. select those first login ones (in 4-month time window)
- re-fine feature list (kick out some subtle ones) and modify the time window;
## 1.1 White samples
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1656864356728-903325f5-d234-4b14-8549-c61b432977cc.png#clientId=udd83d7ac-58d7-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=577&id=u5c8936f4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1154&originWidth=1360&originalType=binary&ratio=1&rotation=0&showTitle=false&size=99244&status=done&style=none&taskId=uc4e696d3-f7c8-4bbb-a71f-fdbce55455b&title=&width=680)

- For white samples, the criterion is modified as follows to find cleaner white samples: 
   - no change mob\email\password;
   - unique shipping address\phone;
- Select for the first occured umid over the past 4 months;
   - one account may correspond to several login records, unless it is new over past 4 months
- At last, randomly pick 1500 login records for experiment.
### Code:
临时查询 - Jiangyi - feature_white_v2
```sql

SET odps.instance.priority = 0;

drop table if exists lazada_biz_sec_dev.white_acct_list_v2;
create table if not exists lazada_biz_sec_dev.white_acct_list_v2 LIFECYCLE 60 as

SELECT 
    a.user_id,
    a.cnt_suspicious_pay,
    b.cnt_distinct_cust,
    b.cnt_distinct_shpadd
from
    (
        SELECT 
            a.user_id,
            sum(a.indicator_ATO) as cnt_suspicious_pay
        from 
            (
                select   
                    user_id,
                    case when (url like '%wallet%') or (url like '%bank-add%') or (url like '%bank-list%') or (url like '%info-change%') then '1'
                    else '0'
                    end as indicator_ATO -- 1 represents suspicious, 0 represents non-suspicious
                from alilog.dwd_lzd_log_ut_pv_di
                where ds >= '20220301' and ds <= '20220601'
                and venture = 'ID'
                and user_id > 0
                and url_type = 'other'
            ) a
        group by a.user_id
    )   a
left JOIN 
    (
        SELECT 
            buyer_id,
            count(distinct shipping_address) as cnt_distinct_shpadd,
            count(distinct shipping_customer_name) as cnt_distinct_cust
        from lazada_cdm.dwd_lzd_trd_core_create_di
        where ds >= '20220301' and ds <= '20220601'
        and venture = 'ID'
        group by buyer_id
    )   b
on a.user_id = b.buyer_id
; 

---------------------------------------------------------------------------------
select count(1) from lazada_biz_sec_dev.white_acct_list_v2
where cnt_suspicious_pay = 0
and cnt_distinct_cust = 1
and cnt_distinct_shpadd = 1
;

---------------------------------------------------------------------------------
set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base_v2;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base_v2 LIFECYCLE 60 as

select 
    a.user_id as user_id,
    b.umid,
    b.receive_time,
    b.envdata_useragent,
    b.envdata_ip,
    b.acsdata_entrance,
    b.logindata_logintype,
    b.ipparse_ipisp,
    b.previous_umid_list
from 
    (
        select 
            user_id
        from lazada_biz_sec_dev.white_acct_list_v2
        where cnt_suspicious_pay = 0
        and cnt_distinct_cust = 1
        and cnt_distinct_shpadd = 1
    )   a
left join
    (   
        SELECT 
            a1.*,
            collect_list(distinct a2.umid) as previous_umid_list
        FROM 
            (
                select 
                    acctdata_userid,
                    from_unixtime(receive_time/1000) as receive_time,
                    umid,
                    envdata_useragent,
                    logindata_logintype,
                    ipparse_ipisp,
                    envdata_ip,
                    acsdata_entrance
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds,1,8) >= '20220301' and substr(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'
            )   a1
        left join 
            (
                SELECT
                    acctdata_userid,
                    from_unixtime(receive_time/1000) as receive_time,
                    umid
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds,1,8) >= '20211201' and substr(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'
            )   a2
        on DATEDIFF(a1.receive_time, a2.receive_time, 'mm') <= 4 and a1.receive_time > a2.receive_time
            and a1.acctdata_userid = a2.acctdata_userid 
        group by a1.acctdata_userid, a1.receive_time, a1.umid, a1.envdata_useragent, a1.logindata_logintype, a1.ipparse_ipisp, a1.envdata_ip, a1.acsdata_entrance
    )   b
on a.user_id = b.acctdata_userid
;

---------------------------------------------------------------------------------
set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base2_v2;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base2_v2 LIFECYCLE 60 as

SELECT 
    user_id,
    umid,
    receive_time,
    envdata_useragent,
    logindata_logintype,
    ipparse_ipisp,
    envdata_ip,
    acsdata_entrance,
    previous_umid_list
FROM 
    (
        select 
            user_id,
            umid,
            receive_time,
            envdata_useragent,
            logindata_logintype,
            ipparse_ipisp,
            envdata_ip,
            acsdata_entrance,
            case when ARRAY_CONTAINS(previous_umid_list, umid) then 0
            else 1 end as new_umid_flag,
            previous_umid_list
        from lazada_biz_sec_dev.white_acct_logrec_base_v2
        where size(previous_umid_list) <> 0
        and previous_umid_list is not Null
    )
where new_umid_flag = 1
;
---------------------------------------------------------------------------------
select * from lazada_biz_sec_dev.white_acct_logrec_base2_v2;
---------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_v2;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_v2 LIFECYCLE 30 as

select 
    user_id,
    umid, -- normal umid
    receive_time as login_date,
    envdata_ip as ip,
    envdata_useragent as useragent,
    acsdata_entrance,
    logindata_logintype
from lazada_biz_sec_dev.white_acct_logrec_base2_v2
where logindata_logintype <> 'auto'
order by RAND()
limit 1500
;

select * from lazada_biz_sec_dev.white_ato_login_sample_v2;

```
## 1.2 Black samples
We use two different black samples to make experiments:

- seller-scam ATO  records (524);
- all ATO records (1155);
### Code:

- seller-scam ATO
   - 临时查询 - Jiangyi - black_sampe_v2
```sql

drop table if exists lazada_biz_sec_dev.black_ato_scam_seller_v2;
create table if not exists lazada_biz_sec_dev.black_ato_scam_seller_v2 LIFECYCLE 60 as

SELECT 
    created_date,
    buyer_id,
    seller_id,
    order_number
FROM  lazada_ads.ads_lzd_xspace_cases_df 
WHERE ds = MAX_PT('lazada_ads.ads_lzd_xspace_cases_df')
AND substr(created_date,1,10)>='2022-02-21' AND substr(created_date,1,10)<='2022-06-01'
AND case_type = 'Child'    ---子订单
AND service_type='CSC'      ---买家
and (TOLOWER(final_contact_reason) LIKE '%account take%'    ---账号被盗ATO
OR TOLOWER(final_contact_reason) LIKE '%suspicious transaction on lazada%')  ---ATO & ST 
and (length(order_number)=15 OR length(order_number)=14) 
and  (TOLOWER(serv_tag_name) LIKE '%scam seller%')
AND venture='ID'
;

```

- total ATO
   - 临时查询 - Jiangyi - black_sample
```sql

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
    b.ipparse_ipprovname,
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
            logindata_logintype,
            ipparse_ipprovname
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
    b.ipparse_ipprovname,
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

------------------------------------------------------------------------------------------------------
select * from lazada_biz_sec_dev.black_ato_login_sample;

select ipparse_ipisp, count(order_number) from lazada_biz_sec_dev.black_ato_login_sample group by ipparse_ipisp;
select ipparse_ipprovname, count(order_buyer_id) from lazada_biz_sec_dev.black_ato_login_sample group by ipparse_ipprovname;

select *
from lazada_biz_sec_dev.black_ato_login_sample;

```
## 1.3 Feature list
Abnormal environment level: 

| index | feature | remark |
| --- | --- | --- |
|  | buyer_id |  |
|  | login_date |  |
|  | labels (black/white) |  |
| 1 | id_new_ip3_4m | 
 |
| 2 | no_unique_umid_14d |  |
| 3 | no_unique_ip2_14d |  |

Order-info level:

| index | feature | remark |
| --- | --- | --- |
| 4 | id_ip3_same_seller_14d | Compared with the used ip3 within 4 months of previous 14d's sellers |
| 5 | avg_price_per_order_14d |  |
| 6 | std_price_per_order_14d |  |
| 7 | avg_dscnt_**rate**_per_order_14d |  |
| 8 | std_dscnt_**rate**_per_order_14d |  |
| 9 | avg_shpfee_per_order_14d |  |
| 10 | std_shpfee_per_order_14d |  |
| 11 | id_susp_paymethod_14d | indicator of suspicious payment method over past 14 days (VA/OTC) |

Login-cluster level:

| index | feature | remark |
| --- | --- | --- |
| 12 | no_acct_umid_14d | number of different accounts for the same umid (14d) |

Sellers level:

| index | feature | remark |
| --- | --- | --- |
| 13 | max_cancel_rate_14d | maximum of cancel rate (calculate within past 4 months) for sellers over past 14d |
| 14 | max_avg_price_seller_14d | maximum of average price (past 4 months) for sellers over past 14d  |
| 15 | max_avg_dscnt_rate_seller_14d | similar |
| 16 | max_avg_shpfee_seller_14d | similar |

### Code:
临时查询 - Jiangyi - feature_white_v2/feature_black_v2
```sql
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2 LIFECYCLE 30 as

select 
    a.user_id as buyer_id,
    a.login_date as current_login_time,
    a.umid as current_umid,
    concat(split_part(a.ip,'.',1), split_part(a.ip,'.',2), SPLIT_PART(a.ip,'.',3)) as current_ip3, 
    concat(split_part(a.ip,'.',1), split_part(a.ip,'.',2)) as current_ip2, 
    a.logindata_logintype as current_logintype
from lazada_biz_sec_dev.white_ato_login_sample_v2  a
;

select * from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2;
----------------------------------------------------------------------------------------------------------------------------------
-- environment features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_env_v2;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_env_v2 LIFECYCLE 60 as

WITH 
    tmp_4mon as
    (
        select 
            a.*,
            b.previous_login_time,
            b.previous_ip3
        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2   a
        left join
            (
                select
                    acctdata_userid,
                    FROM_UNIXTIME(receive_time/1000) as previous_login_time,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2), SPLIT_PART(envdata_ip,'.',3)) as previous_ip3
                from lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20211201' and SUBSTR(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'  
            )   b
        on a.buyer_id = b.acctdata_userid and a.current_login_time > b.previous_login_time and DATEDIFF(a.current_login_time, b.previous_login_time, 'mm') <= 4
    ),
    tmp_14d AS 
    (
        select 
            a.*,
            b.previous_login_time,
            b.previous_ip2,
            b.previous_umid
        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2   a
        left join
            (
                select
                    acctdata_userid,
                    FROM_UNIXTIME(receive_time/1000) as previous_login_time,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2)) as previous_ip2,
                    umid as previous_umid
                from lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20220201' and SUBSTR(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'  
            )   b
        on a.buyer_id = b.acctdata_userid and a.current_login_time > b.previous_login_time and DATEDIFF(a.current_login_time, b.previous_login_time, 'dd') <= 14
    )
SELECT 
    a.*,
    b.id_new_ip3_4m
FROM 
    (
        SELECT 
            buyer_id,
            current_login_time,
            current_umid,
            current_ip3,
            current_ip2,
            current_logintype,
            count(distinct previous_umid) as no_unique_umid_14d,
            count(distinct previous_ip2) as no_unique_ip2_14d
        FROM tmp_14d
        group by buyer_id, current_login_time, current_umid, current_ip3, current_ip2, current_logintype
    )   a
left JOIN 
    (
        SELECT
            buyer_id,
            current_login_time,
            current_umid,
            current_ip3,
            current_ip2,
            current_logintype,
            case when array_contains(COLLECT_LIST(previous_ip3), current_ip3) then 0
            else 1 end as id_new_ip3_4m
        FROM tmp_4mon
        group by buyer_id, current_login_time, current_umid, current_ip3, current_ip2, current_logintype
    )   b
on a.buyer_id = b.buyer_id and a.current_login_time = b.current_login_time
;
select * from lazada_biz_sec_dev.white_ato_login_sample_feature_env_v2;
----------------------------------------------------------------------------------------------------------------------------------
-- buyers corresponding previous sellers (14d) and their order records
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v2; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v2 LIFECYCLE 30 as


SELECT 
    a.*,
    b.sales_order_id,
    b.list_price as seller_list_price,
    b.unit_price as seller_unit_price,
    b.paid_price as seller_paid_price,
    b.shipping_amount_total as seller_shipping_amount_total,
    b.order_status as seller_order_status
from 
    (
        select
            a1.buyer_id,
            a1.current_login_time,
            a1.current_umid,
            a2.seller_id
        from 
            (
                select * from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2
            )   a1
        left join
            (
                select 
                    seller_id,
                    buyer_id,
                    dateadd(order_create_date, 1, 'hour') as order_create_date 
                from lazada_cdm.dwd_lzd_trd_core_create_di
                where ds >= '20220201' and ds <= '20220601'
                and venture = 'ID'
            )   a2
        on a1.buyer_id = a2.buyer_id and DATEDIFF(a1.current_login_time, a2.order_create_date, 'dd') <= 14 and a1.current_login_time > a2.order_create_date
    )   a
left JOIN 
    (
        SELECT 
            seller_id,
            sales_order_id,
            list_price,
            unit_price,
            paid_price,
            shipping_amount_total,
            dateadd(order_create_date, 1, 'hour') as order_create_date,
            CASE  WHEN item_status_ofc = 'lost_by_3pl' OR item_status_ofc = 'package_damaged' THEN '8.Lost_Damaged'
                WHEN ship_date IS NULL AND cancel_date IS NOT NULL AND is_final_state = 1 THEN '5.Cancellation'
                WHEN item_status_delivery = 'delivered' AND return_complete_date IS NULL THEN '4.Delivered' 
                WHEN item_status_delivery = 'delivered' AND return_complete_date IS NOT NULL THEN '6.Return_Refund'   
                WHEN item_status_last = 'order_create' THEN '0.Unpaid'
                WHEN ship_date IS NULl AND item_status_ofc = 'handled_by_seller' THEN '1.To_Pack'
                WHEN ship_date IS NULl AND item_status_ofc IN ('ready_to_ship','packed','transit_to_ship') THEN '2.To_Ship'
                WHEN ship_date IS NOT NULL AND delivery_date IS NULL AND cancel_date IS NULL AND item_status_ofc = 'shipped' AND item_status_last = 'shipped' THEN '3.Shipping'
                WHEN (ship_date IS NOT NULL AND delivery_date IS NULL  AND item_status_esm = 'rejected') OR item_status_ofc = 'deliver_failed' THEN '7.Failed_Delivered'
                ELSE 'Unknown'
            END AS order_status 
        from lazada_cdm.dwd_lzd_trd_core_create_di
        WHERE ds >= '20220101' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.seller_id = b.seller_id 
    and DATEDIFF(a.current_login_time, b.order_create_date, 'mm') <= 2 and a.current_login_time >= b.order_create_date
;

select * from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v2;
----------------------------------------------------------------------------------------------------------------------------------
-- seller sides features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v2; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v2 LIFECYCLE 60 as

select 
    a.*,
    b.max_avg_price_seller_14d,
    b.max_avg_dscnt_rate_seller_14d,
    b.max_avg_shpfee_seller_14d
from 
    (   
        SELECT 
            buyer_id,
            current_login_time,
            max(total_cancel_number/total_order_number) as max_cancel_rate_14d
        from
            (
                SELECT 
                    buyer_id,
                    seller_id,
                    current_login_time,
                    count(sales_order_id) as total_order_number,
                    sum(seller_order_status) as total_cancel_number
                FROM 
                    (
                        SELECT distinct
                            buyer_id,
                            seller_id,
                            current_login_time,
                            sales_order_id,
                            case when seller_order_status = '5.Cancellation' then '1' else '0' end as seller_order_status
                        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v2
                    )
                    group by buyer_id, seller_id, current_login_time
            )
            group by buyer_id, current_login_time
    )   a

left JOIN 
    (
        SELECT 
            buyer_id,
            current_login_time,
            max(avg_price_seller_14d) as max_avg_price_seller_14d,
            max(avg_dscnt_rate_seller_14d) as max_avg_dscnt_rate_seller_14d,
            max(avg_shpfee_seller_14d) as max_avg_shpfee_seller_14d
        FROM 
            (
                SELECT 
                    buyer_id,
                    seller_id,
                    current_login_time,
                    avg(seller_paid_price) as avg_price_seller_14d,
                    avg((seller_list_price-seller_paid_price)/seller_list_price) as avg_dscnt_rate_seller_14d,
                    avg(seller_shipping_amount_total) as avg_shpfee_seller_14d
                FROM 
                    (
                        SELECT distinct
                            buyer_id,
                            seller_id,
                            current_login_time,
                            seller_list_price,
                            seller_unit_price,
                            seller_paid_price,
                            seller_shipping_amount_total
                        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v2
                    )
                group by buyer_id, seller_id, current_login_time
            )
            group by buyer_id, current_login_time
    )   b
on a.buyer_id = b.buyer_id and a.current_login_time = b.current_login_time
;

select * from lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v2;
----------------------------------------------------------------------------------------------------------------------------------
-- Order info features

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_order_v2; -- feature_order
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_order_v2 LIFECYCLE 30 as

select 
    a1.*,
    CASE 
        when ARRAY_CONTAINS(a2.list_seller_ip3, a1.current_ip3) then '1'  else '0'
    end as id_ip3_same_seller_14d

from
    (
        SELECT 
            buyer_id,
            current_login_time,
            current_ip3,
            COLLECT_LIST(orderid) as list_sales_order_id_14d,
            avg(grosspay-vouchamt) as avg_price_per_order_14d,
            stddev(grosspay-vouchamt) as std_price_per_order_14d,
            avg(vouchamt/grosspay) as avg_dscnt_rate_per_order_14d,
            stddev(vouchamt/grosspay) as std_dscnt_rate_per_order_14d,
            avg(shpfee) as avg_shpfee_per_order_14d,
            stddev(shpfee) as std_shpfee_per_order_14d
        FROM 
            (
                select
                    a.buyer_id,
                    a.current_login_time,
                    a.current_ip3,
                    b.order_create_time,
                    b.orderid,
                    b.grosspay,
                    b.vouchamt,
                    b.shpfee
                from
                    (
                        SELECT 
                            buyer_id,
                            current_login_time,
                            current_ip3
                        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2
                    )   a
                left JOIN 
                    (
                        SELECT 
                            FROM_UNIXTIME(receive_time/1000) as order_create_time,
                            orderid,
                            byracctid,
                            grosspay,
                            vouchamt,
                            shpfee
                        from lzd_secods.odl_event_lazada_order_creation_risk_sg
                        where SUBSTR(ds, 1, 8) >= '20220201' and substr(ds, 1, 8) <= '20220601'
                    )   b
                on a.buyer_id = b.byracctid 
                    and datediff(a.current_login_time, b.order_create_time, 'dd') <= 14 and a.current_login_time >= b.order_create_time
            )            
        group by buyer_id, current_login_time, current_ip3
    )   a1

left JOIN 
    (
        SELECT 
            a.buyer_id,
            a.current_login_time,
            collect_list(distinct b.ip3) as list_seller_ip3
        from 
            (
                select distinct
                    buyer_id,
                    current_login_time,
                    seller_id
                from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v2
            )   a
        left join
            (
                SELECT
                    acctdata_userid,
                    FROM_UNIXTIME(receive_time/1000) as receive_time,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2), SPLIT_PART(envdata_ip,'.',3)) as ip3
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds, 1, 8) >= '20211201' and substr(ds, 1, 8) <= '20220601'
                and acctdata_bizrole <> 'byr'
                and otherdata_issucc = 'true'
            )   b
        on a.seller_id = b.acctdata_userid
            and DATEDIFF(a.current_login_time, b.receive_time, 'mm') <= 4 and a.current_login_time >= b.receive_time
        group by a.buyer_id, a.current_login_time
    )   a2
on a1.buyer_id = a2.buyer_id and a1.current_login_time = a2.current_login_time
;

select * from lazada_biz_sec_dev.white_ato_login_sample_feature_order_v2;
----------------------------------------------------------------------------------------------------------------------------------
-- login cluster
-- number of different accounts for the same umid

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v2; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v2 LIFECYCLE 30 as
SELECT 
    buyer_id,
    current_login_time,
    current_umid,
    count(distinct login_id) as no_acct_umid_14d
FROM 
    (
        SELECT 
            a.*,
            b.login_id
        FROM 
            (
                select
                    buyer_id,
                    current_login_time,
                    current_umid
                from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2
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
group by buyer_id, current_login_time, current_umid
;


select * from lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v2;

----------------------------------------------------------------------------------------------------------------------------------
-- Final features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_v2; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_v2 LIFECYCLE 60 as

SELECT 
    a.buyer_id,
    0 as label, -- white sample
    a.no_unique_umid_14d,
    a.no_unique_ip2_14d,
    a.id_new_ip3_4m,
    b.id_ip3_same_seller_14d,
    b.avg_price_per_order_14d,
    b.std_price_per_order_14d,
    b.avg_dscnt_rate_per_order_14d,
    b.std_dscnt_rate_per_order_14d,
    b.avg_shpfee_per_order_14d,
    b.std_shpfee_per_order_14d,
    f.is_susp_paymethod_14d as id_susp_paymethod_14d,
    c.no_acct_umid_14d,
    d.max_cancel_rate_14d,
    d.max_avg_price_seller_14d,
    d.max_avg_dscnt_rate_seller_14d,
    d.max_avg_shpfee_seller_14d
   --a.id_is_suspicious as id_susp_device

FROM 
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_env_v2
    )   a

left join
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_order_v2
    )   b
on a.buyer_id = b.buyer_id and a.current_login_time = b.current_login_time

left join 
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v2
    )   c
on a.buyer_id = c.buyer_id and a.current_login_time = c.current_login_time

left JOIN 
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v2
    )   d
on a.buyer_id = d.buyer_id and a.current_login_time = d.current_login_time
left JOIN 
    (
        select
            a1.buyer_id,
            a1.current_login_time,
            max(a2.is_susp_paymethod_flag) as is_susp_paymethod_14d
        from 
            (
                select
                    buyer_id,
                    current_login_time
                from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v2
            )   a1
        left join 
            (
                SELECT 
                    buyer_id,
                    case when (payment_method like '%VA%') or (payment_method like '%OTC%') then '1' else '0'
                    end as is_susp_paymethod_flag,
                    dateadd(order_create_date, 1, 'hour') as order_create_date
                from lazada_cdm.dwd_lzd_trd_core_create_di
                where ds >= '20220201' and ds <= '20220601'
                and venture = 'ID'
            )   a2
        on a1.buyer_id = a2.buyer_id 
            and DATEDIFF(a1.current_login_time, a2.order_create_date, 'dd') <= 14 and a1.current_login_time >= a2.order_create_date
        group by a1.buyer_id, a1.current_login_time
    )   f
on a.buyer_id = f.buyer_id and a.current_login_time = f.current_login_time
;

select * from lazada_biz_sec_dev.white_ato_login_sample_feature_v2;
---------------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_login_sample_feature_v2; 
create table if not exists lazada_biz_sec_dev.ato_login_sample_feature_v2 LIFECYCLE 30 as

SELECT 
    buyer_id,
    label,
    no_unique_umid_14d,
    no_unique_ip2_14d,
    cast(id_new_ip3_4m as bigint) as id_new_ip3_4m,
    cast(id_ip3_same_seller_14d as bigint) as id_ip3_same_seller_14d,
    avg_price_per_order_14d,
    std_price_per_order_14d,
    avg_dscnt_rate_per_order_14d,
    std_dscnt_rate_per_order_14d,
    avg_shpfee_per_order_14d,
    std_shpfee_per_order_14d,
    cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
    no_acct_umid_14d,
    max_cancel_rate_14d,
    max_avg_price_seller_14d,
    max_avg_dscnt_rate_seller_14d,
    max_avg_shpfee_seller_14d
from lazada_biz_sec_dev.white_ato_login_sample_feature_v2
union ALL 
    (
        select 
            buyer_id,
            label,
            no_unique_umid_14d,
            no_unique_ip2_14d,
            cast(id_new_ip3_4m as bigint) as id_new_ip3_4m,
            cast(id_ip3_same_seller_14d as bigint) as id_ip3_same_seller_14d,
            avg_price_per_order_14d,
            std_price_per_order_14d,
            avg_dscnt_rate_per_order_14d,
            std_dscnt_rate_per_order_14d,
            avg_shpfee_per_order_14d,
            std_shpfee_per_order_14d,
            cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
            no_acct_umid_14d,
            max_cancel_rate_14d,
            max_avg_price_seller_14d,
            max_avg_dscnt_rate_seller_14d,
            max_avg_shpfee_seller_14d
        from lazada_biz_sec_dev.black_ato_login_sample_feature_v2
    )
;

select * from lazada_biz_sec_dev.ato_login_sample_feature_v2;

---------------------------------------------------------------------------------

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.seller_scam_login_sample_feature_v2; 
create table if not exists lazada_biz_sec_dev.seller_scam_login_sample_feature_v2 LIFECYCLE 30 as

SELECT 
    buyer_id,
    label,
    no_unique_umid_14d,
    no_unique_ip2_14d,
    cast(id_new_ip3_4m as bigint) as id_new_ip3_4m,
    cast(id_ip3_same_seller_14d as bigint) as id_ip3_same_seller_14d,
    avg_price_per_order_14d,
    std_price_per_order_14d,
    avg_dscnt_rate_per_order_14d,
    std_dscnt_rate_per_order_14d,
    avg_shpfee_per_order_14d,
    std_shpfee_per_order_14d,
    cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
    no_acct_umid_14d,
    max_cancel_rate_14d,
    max_avg_price_seller_14d,
    max_avg_dscnt_rate_seller_14d,
    max_avg_shpfee_seller_14d
from lazada_biz_sec_dev.white_ato_login_sample_feature_v2
union ALL 
    (
        select 
            buyer_id,
            label,
            no_unique_umid_14d,
            no_unique_ip2_14d,
            cast(id_new_ip3_4m as bigint) as id_new_ip3_4m,
            cast(id_ip3_same_seller_14d as bigint) as id_ip3_same_seller_14d,
            avg_price_per_order_14d,
            std_price_per_order_14d,
            avg_dscnt_rate_per_order_14d,
            std_dscnt_rate_per_order_14d,
            avg_shpfee_per_order_14d,
            std_shpfee_per_order_14d,
            cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
            no_acct_umid_14d,
            max_cancel_rate_14d,
            max_avg_price_seller_14d,
            max_avg_dscnt_rate_seller_14d,
            max_avg_shpfee_seller_14d
        from lazada_biz_sec_dev.seller_scam_ato_login_sample_feature_v2
    )
;

select * from lazada_biz_sec_dev.seller_scam_login_sample_feature_v2;



```
## 1.4 Result

1. 524 black vs 1500 white		

[ato_v2_experiment2_0707.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659692087235-ca087c44-3d93-410c-94aa-9ed928c19e4b.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659692087235-ca087c44-3d93-410c-94aa-9ed928c19e4b.ipynb%22%2C%22name%22%3A%22ato_v2_experiment2_0707.ipynb%22%2C%22size%22%3A729857%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22u4e0f7a58-e9fb-4e9c-a4bd-5dbaee7ea49%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u9cbbf73d%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)

   - testing performance with RF

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657175849505-f5bd70b8-6f65-4ccb-b524-146f05af440e.png#clientId=ud7477239-d478-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=245&id=ub8047bfe&margin=%5Bobject%20Object%5D&name=image.png&originHeight=245&originWidth=352&originalType=binary&ratio=1&rotation=0&showTitle=false&size=22280&status=done&style=none&taskId=u009a960e-1fb2-4c82-af47-ad86ab5f526&title=&width=352)

   - testing performance wtih XGB

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657175880621-b0ecef4f-d090-4a37-a054-1237e5043c8d.png#clientId=ud7477239-d478-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=246&id=u6153fb16&margin=%5Bobject%20Object%5D&name=image.png&originHeight=246&originWidth=372&originalType=binary&ratio=1&rotation=0&showTitle=false&size=22606&status=done&style=none&taskId=ua2929239-e718-409f-ac7d-5feb1dc0601&title=&width=372)

2. 1155 black vs 1500 white

[ato_v2_experiment1.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659692094062-15dc0dac-6f29-4b97-87d7-2dc24e1321db.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659692094062-15dc0dac-6f29-4b97-87d7-2dc24e1321db.ipynb%22%2C%22name%22%3A%22ato_v2_experiment1.ipynb%22%2C%22size%22%3A773086%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22u8c0dfc03-a676-4bf3-8ffe-5818dcea9bf%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u06888bc2%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)

   - testing performance with RF

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657175997123-d73537cb-8efa-4842-9666-1fd3b87f5212.png#clientId=ud7477239-d478-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=246&id=u8ab3928a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=246&originWidth=379&originalType=binary&ratio=1&rotation=0&showTitle=false&size=22296&status=done&style=none&taskId=uba82ed06-9d43-4fb8-beba-c5f3ab5e03f&title=&width=379)

   - testing performance with XGB

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657176039240-e0d3b4d4-7d06-4671-a6c0-633b5165e41c.png#clientId=ud7477239-d478-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=249&id=u71de029e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=249&originWidth=412&originalType=binary&ratio=1&rotation=0&showTitle=false&size=23571&status=done&style=none&taskId=uf06f8aa4-8243-4d9a-8092-43e6d93fb79&title=&width=412)
# Experiment2
## 2.1 White samples

- ramdomly select 5000 white records and choose 3/4 who has previous order record, while others do not have;
### Code:
临时查询 - Jiangyi - white_sample_v3
```sql

-- two parts: (normal login part) + (abnormal login part)
-- both are based on case analysis selection

SET odps.instance.priority = 0;

drop table if exists lazada_biz_sec_dev.white_acct_list_v2;
create table if not exists lazada_biz_sec_dev.white_acct_list_v2 LIFECYCLE 60 as

SELECT 
    a.user_id,
    a.cnt_suspicious_pay,
    b.cnt_distinct_cust,
    b.cnt_distinct_shpadd
from
    (
        SELECT 
            a.user_id,
            sum(a.indicator_ATO) as cnt_suspicious_pay
        from 
            (
                select   
                    user_id,
                    case when (url like '%wallet%') or (url like '%bank-add%') or (url like '%bank-list%') or (url like '%info-change%') then '1'
                    else '0'
                    end as indicator_ATO -- 1 represents suspicious, 0 represents non-suspicious
                from alilog.dwd_lzd_log_ut_pv_di
                where ds >= '20220301' and ds <= '20220601'
                and venture = 'ID'
                and user_id > 0
                and url_type = 'other'
            ) a
        group by a.user_id
    )   a
left JOIN 
    (
        SELECT 
            buyer_id,
            count(distinct shipping_address) as cnt_distinct_shpadd,
            count(distinct shipping_customer_name) as cnt_distinct_cust
        from lazada_cdm.dwd_lzd_trd_core_create_di
        where ds >= '20220301' and ds <= '20220601'
        and venture = 'ID'
        group by buyer_id
    )   b
on a.user_id = b.buyer_id
; 

---------------------------------------------------------------------------------
select count(1) from lazada_biz_sec_dev.white_acct_list_v2
where cnt_suspicious_pay = 0
and cnt_distinct_cust = 1
and cnt_distinct_shpadd = 1
;

---------------------------------------------------------------------------------
set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base_v2;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base_v2 LIFECYCLE 60 as

select 
    a.user_id as user_id,
    b.umid,
    b.receive_time,
    b.envdata_useragent,
    b.envdata_ip,
    b.acsdata_entrance,
    b.logindata_logintype,
    b.ipparse_ipisp,
    b.previous_umid_list
from 
    (
        select 
            user_id
        from lazada_biz_sec_dev.white_acct_list_v2
        where cnt_suspicious_pay = 0
        and cnt_distinct_cust = 1
        and cnt_distinct_shpadd = 1
    )   a
left join
    (   
        SELECT 
            a1.*,
            collect_list(distinct a2.umid) as previous_umid_list
        FROM 
            (
                select 
                    acctdata_userid,
                    from_unixtime(receive_time/1000) as receive_time,
                    umid,
                    envdata_useragent,
                    logindata_logintype,
                    ipparse_ipisp,
                    envdata_ip,
                    acsdata_entrance
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds,1,8) >= '20220301' and substr(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'
            )   a1
        left join 
            (
                SELECT
                    acctdata_userid,
                    from_unixtime(receive_time/1000) as receive_time,
                    umid
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds,1,8) >= '20211201' and substr(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'
            )   a2
        on DATEDIFF(a1.receive_time, a2.receive_time, 'mm') <= 4 and a1.receive_time > a2.receive_time
            and a1.acctdata_userid = a2.acctdata_userid 
        group by a1.acctdata_userid, a1.receive_time, a1.umid, a1.envdata_useragent, a1.logindata_logintype, a1.ipparse_ipisp, a1.envdata_ip, a1.acsdata_entrance
    )   b
on a.user_id = b.acctdata_userid
;

---------------------------------------------------------------------------------
set odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_acct_logrec_base2_v2;
create table if not exists lazada_biz_sec_dev.white_acct_logrec_base2_v2 LIFECYCLE 60 as

SELECT 
    user_id,
    umid,
    receive_time,
    envdata_useragent,
    logindata_logintype,
    ipparse_ipisp,
    envdata_ip,
    acsdata_entrance,
    previous_umid_list
FROM 
    (
        select 
            user_id,
            umid,
            receive_time,
            envdata_useragent,
            logindata_logintype,
            ipparse_ipisp,
            envdata_ip,
            acsdata_entrance,
            case when ARRAY_CONTAINS(previous_umid_list, umid) then 0
            else 1 end as new_umid_flag,
            previous_umid_list
        from lazada_biz_sec_dev.white_acct_logrec_base_v2
        where size(previous_umid_list) <> 0
        and previous_umid_list is not Null
    )
where new_umid_flag = 1
;
---------------------------------------------------------------------------------
select * from lazada_biz_sec_dev.white_acct_logrec_base2_v2;
---------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_v2;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_v2 LIFECYCLE 30 as

select 
    user_id,
    umid, -- normal umid
    receive_time as login_date,
    envdata_ip as ip,
    envdata_useragent as useragent,
    acsdata_entrance,
    logindata_logintype
from lazada_biz_sec_dev.white_acct_logrec_base2_v2
where logindata_logintype <> 'auto'
order by RAND()
limit 1500
;
---------------------------------------------------------------------------------
select * from lazada_biz_sec_dev.white_ato_login_sample_v2;
---------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_v3_total;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_v3_total LIFECYCLE 30 as

select
    a.*,
    count(sales_order_id) as order_number
FROM 
    (
        select 
            user_id,
            umid, -- normal umid
            receive_time as login_date,
            envdata_ip as ip,
            envdata_useragent as useragent,
            acsdata_entrance,
            logindata_logintype
        from lazada_biz_sec_dev.white_acct_logrec_base2_v2
        where logindata_logintype <> 'auto'
    )   a
left JOIN 
    (
        select distinct
            buyer_id,
            sales_order_id,
            dateadd(order_create_date, 1, 'hour') as order_create_date
        from lazada_cdm.dwd_lzd_trd_core_create_di
        where ds >= '20220201' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.user_id = b.buyer_id
    and datediff(a.login_date, b.order_create_date, 'dd') <= 14 and a.login_date >= b.order_create_date 
group by a.user_id, a.umid, a.login_date, a.ip, a.useragent, a.acsdata_entrance, a.logindata_logintype
;
---------------------------------------------------------------------------------
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_v3;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_v3 LIFECYCLE 30 as

SELECT 
    *
from lazada_biz_sec_dev.white_ato_login_sample_v3_total
where order_number > 0 
order by RAND()
limit 4500
union ALL 
    (
        SELECT 
            *
        from lazada_biz_sec_dev.white_ato_login_sample_v3_total
        where order_number = 0 
        order by RAND()
        limit 1500
    )
;
---------------------------------------------------------------------------------
select * from lazada_biz_sec_dev.white_ato_login_sample_v3;

```
## 2.2 Black samples
**524** black records
### 2.2.1 White samples vs Black samples
From 0301 to 0601, there are: 

- 1155 ATO cases, among which 524 are labelled seller-scam cases;
- 965,339 white samples, in the sense that, 
   1. using the umid that hasn't been used in previous 3 months;
   1. umid is null;

To conclude, it is **965,339 white VS 524 black** if aim is to detect seller-scam ATO;
## 2.3 Feature list re-fine
Abnormal environment difference: 

| index | feature | remark |
| --- | --- | --- |
|  | buyer_id |  |
|  | login_date |  |
|  | labels (black/white) |  |
| 1 | new_ip2_3m | 
 |
| 2 | new_ip3_3m |  |
| 3 | count_unique_umid_14d |  |
| 4 | count_unique_ip2_14d |  |
| 5 | coun_login_14d |  |

Order info features:

| index | feature | remark |
| --- | --- | --- |
| 6 | 14dseller_same_ip | Compared with the used ip within 3 months of previous 14d's sellers |
| 7 | 14dseller_same_ip3ua | similar, replace ip with ip3+useragent |
| 8 | avg_price_per_order_usd_14d | **unit: usd** |
| 9 | std_price_per_order_usd_14d |  |
| 10 | avg_dscnt_**rate**_per_order_14d |  |
| 11 | std_dscnt_**rate**_per_order_14d |  |
| 12 | avg_shpfee_per_order_usd_14d |  |
| 13 | std_shpfee_per_order_usd_14d |  |
| 14 | susp_payment_method_14d | indicator of suspicious payment method over past 14 days (VA/OTC) |

Login cluster features:

| index | feature | remark |
| --- | --- | --- |
| 15 | count_acct_same_umid_3m | number of different accounts for the same umid (3m) |

Sellers' side features:

| index | feature | remark |
| --- | --- | --- |
| 16 | max_cancel_rate_14d | maximum of cancel rate (calculate within past 3 months) for sellers over past 14d |
| 17 | max_avg_price_seller_usd_14d | maximum of average price (past 3 months) for sellers over past 14d  |
| 18 | max_avg_dscnt_rate_seller_usd_14d | similar |
| 19 | max_avg_shpfee_seller_usd_14d | similar |

Note: time-window agreement: 

- long-term pattern: 3-month;
- otherwise: 14d;
### Code:
临时查询 - Jiangyi - feature_white_v3/feature_black_v3
```sql
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3 LIFECYCLE 30 as

select 
    a.user_id as buyer_id,
    a.login_date as current_login_time,
    a.umid as current_umid,
    concat(split_part(a.ip,'.',1), split_part(a.ip,'.',2), SPLIT_PART(a.ip,'.',3)) as current_ip3, 
    concat(split_part(a.ip,'.',1), split_part(a.ip,'.',2)) as current_ip2, 
    a.ip as current_ip,
    a.useragent as current_useragent,
    a.logindata_logintype as current_logintype
from lazada_biz_sec_dev.white_ato_login_sample_v3  a
;

select * from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3;
----------------------------------------------------------------------------------------------------------------------------------
-- environment features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_env_v3;
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_env_v3 LIFECYCLE 30 as

WITH 
    tmp_3mon as
    (
        select 
            a.*,
            b.previous_login_time,
            b.previous_ip3,
            b.previous_ip2
        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3   a
        left join
            (
                select
                    acctdata_userid,
                    FROM_UNIXTIME(receive_time/1000) as previous_login_time,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2), SPLIT_PART(envdata_ip,'.',3)) as previous_ip3,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2)) as previous_ip2
                from lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20220101' and SUBSTR(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'  
            )   b
        on a.buyer_id = b.acctdata_userid and a.current_login_time > b.previous_login_time and DATEDIFF(a.current_login_time, b.previous_login_time, 'mm') <= 3
    ),
    tmp_14d AS 
    (
        select 
            a.*,
            b.event_id,
            b.previous_login_time,
            b.previous_ip2,
            b.previous_umid
        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3   a
        left join
            (
                select
                    acctdata_userid,
                    event_id,
                    FROM_UNIXTIME(receive_time/1000) as previous_login_time,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2)) as previous_ip2,
                    umid as previous_umid
                from lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20220201' and SUBSTR(ds,1,8) <= '20220601'
                and acsdata_cntry = 'id'
                and otherdata_issucc = 'true'
                and acctdata_bizrole = 'byr'  
            )   b
        on a.buyer_id = b.acctdata_userid and a.current_login_time > b.previous_login_time and DATEDIFF(a.current_login_time, b.previous_login_time, 'dd') <= 14
    )
SELECT 
    a.*,
    b.id_new_ip3_3m,
    b.id_new_ip2_3m
FROM 
    (
        SELECT 
            buyer_id,
            current_login_time,
            current_umid,
            current_ip3,
            current_ip2,
            current_logintype,
            count(distinct previous_umid) as no_unique_umid_14d,
            count(distinct previous_ip2) as no_unique_ip2_14d,
            count(distinct event_id) as no_login_14d
        FROM tmp_14d
        group by buyer_id, current_login_time, current_umid, current_ip3, current_ip2, current_logintype
    )   a
left JOIN 
    (
        SELECT
            buyer_id,
            current_login_time,
            current_umid,
            current_ip3,
            current_ip2,
            current_logintype,
            case when array_contains(COLLECT_LIST(distinct previous_ip3), current_ip3) then 0
            else 1 end as id_new_ip3_3m,
            case when ARRAY_CONTAINS(collect_list(distinct previous_ip2), current_ip2) then 0
            else 1 end as id_new_ip2_3m
        FROM tmp_3mon
        group by buyer_id, current_login_time, current_umid, current_ip3, current_ip2, current_logintype
    )   b
on a.buyer_id = b.buyer_id and a.current_login_time = b.current_login_time
;
select * from lazada_biz_sec_dev.white_ato_login_sample_feature_env_v3;
----------------------------------------------------------------------------------------------------------------------------------
-- buyers corresponding previous sellers (14d) and their order records

-- next time can change for WITH!!!!!!
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v3; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v3 LIFECYCLE 30 as


SELECT 
    a.*,
    b.sales_order_id,
    b.list_price as seller_list_price,
    b.unit_price as seller_unit_price,
    b.paid_price as seller_paid_price,
    b.shipping_amount_total as seller_shipping_amount_total,
    b.order_status as seller_order_status
from 
    (
        select distinct
            a1.buyer_id,
            a1.current_login_time,
            a1.current_umid,
            a2.seller_id
        from 
            (
                select * from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3
            )   a1
        left join
            (
                select 
                    seller_id,
                    buyer_id,
                    dateadd(order_create_date, 1, 'hour') as order_create_date 
                from lazada_cdm.dwd_lzd_trd_core_create_di
                where ds >= '20220201' and ds <= '20220601'
                and venture = 'ID'
            )   a2
        on a1.buyer_id = a2.buyer_id and DATEDIFF(a1.current_login_time, a2.order_create_date, 'dd') <= 14 and a1.current_login_time >= a2.order_create_date
    )   a
left JOIN 
    (
        SELECT 
            seller_id,
            sales_order_id,
            list_price * exchange_rate as list_price,
            unit_price * exchange_rate as unit_price,
            paid_price * exchange_rate as paid_price,
            shipping_amount_total * exchange_rate as shipping_amount_total,
            dateadd(order_create_date, 1, 'hour') as order_create_date,
            CASE  WHEN item_status_ofc = 'lost_by_3pl' OR item_status_ofc = 'package_damaged' THEN '8.Lost_Damaged'
                WHEN ship_date IS NULL AND cancel_date IS NOT NULL AND is_final_state = 1 THEN '5.Cancellation'
                WHEN item_status_delivery = 'delivered' AND return_complete_date IS NULL THEN '4.Delivered' 
                WHEN item_status_delivery = 'delivered' AND return_complete_date IS NOT NULL THEN '6.Return_Refund'   
                WHEN item_status_last = 'order_create' THEN '0.Unpaid'
                WHEN ship_date IS NULl AND item_status_ofc = 'handled_by_seller' THEN '1.To_Pack'
                WHEN ship_date IS NULl AND item_status_ofc IN ('ready_to_ship','packed','transit_to_ship') THEN '2.To_Ship'
                WHEN ship_date IS NOT NULL AND delivery_date IS NULL AND cancel_date IS NULL AND item_status_ofc = 'shipped' AND item_status_last = 'shipped' THEN '3.Shipping'
                WHEN (ship_date IS NOT NULL AND delivery_date IS NULL  AND item_status_esm = 'rejected') OR item_status_ofc = 'deliver_failed' THEN '7.Failed_Delivered'
                ELSE 'Unknown'
            END AS order_status 
        from lazada_cdm.dwd_lzd_trd_core_create_di
        WHERE ds >= '20220101' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.seller_id = b.seller_id 
    and DATEDIFF(a.current_login_time, b.order_create_date, 'mm') <= 3 and a.current_login_time >= b.order_create_date
;

select * from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v3;
----------------------------------------------------------------------------------------------------------------------------------
-- seller sides features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v3; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v3 LIFECYCLE 60 as

select 
    a.*,
    b.max_avg_price_seller_usd_14d,
    b.max_avg_dscnt_rate_seller_14d,
    b.max_avg_shpfee_seller_usd_14d
from 
    (   
        SELECT 
            buyer_id,
            current_login_time,
            max(total_cancel_number/total_order_number) as max_cancel_rate_14d
        from
            (
                SELECT 
                    buyer_id,
                    seller_id,
                    current_login_time,
                    count(sales_order_id) as total_order_number,
                    sum(seller_order_status) as total_cancel_number
                FROM 
                    (
                        SELECT distinct
                            buyer_id,
                            seller_id,
                            current_login_time,
                            sales_order_id,
                            case when seller_order_status = '5.Cancellation' then '1' else '0' end as seller_order_status
                        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v3
                    )
                    group by buyer_id, seller_id, current_login_time
            )
            group by buyer_id, current_login_time
    )   a

left JOIN 
    (
        SELECT 
            buyer_id,
            current_login_time,
            max(avg_price_seller_14d) as max_avg_price_seller_usd_14d,
            max(avg_dscnt_rate_seller_14d) as max_avg_dscnt_rate_seller_14d,
            max(avg_shpfee_seller_14d) as max_avg_shpfee_seller_usd_14d
        FROM 
            (
                SELECT 
                    buyer_id,
                    seller_id,
                    current_login_time,
                    avg(seller_paid_price) as avg_price_seller_14d,
                    avg((seller_list_price-seller_paid_price)/seller_list_price) as avg_dscnt_rate_seller_14d,
                    avg(seller_shipping_amount_total) as avg_shpfee_seller_14d
                FROM 
                    (
                        SELECT distinct
                            buyer_id,
                            seller_id,
                            current_login_time,
                            seller_list_price,
                            seller_unit_price,
                            seller_paid_price,
                            seller_shipping_amount_total
                        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v3
                    )
                group by buyer_id, seller_id, current_login_time
            )
            group by buyer_id, current_login_time
    )   b
on a.buyer_id = b.buyer_id and a.current_login_time = b.current_login_time
;

select * from lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v3;
----------------------------------------------------------------------------------------------------------------------------------
-- Order info features

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_order_v3; -- feature_order
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_order_v3 LIFECYCLE 30 as

select 
    a1.*,
    CASE 
        when ARRAY_CONTAINS(a2.list_seller_ip, a1.current_ip) then '1'  else '0'
    end as id_ip_same_seller_14d,
    CASE 
        when array_contains(a2.list_seller_ip3ua, a1.current_ip3ua) then '1' else '0'
    end as id_ip3ua_same_seller_14d

from
    (
        SELECT 
            buyer_id,
            current_login_time,
            current_ip,
            current_ip3ua,
            COLLECT_LIST(sales_order_id) as list_sales_order_id_14d,
            avg(order_paid_price) as avg_price_per_order_usd_14d,
            stddev(order_paid_price) as std_price_per_order_usd_14d,
            avg((order_list_price - order_paid_price)/order_list_price) as avg_dscnt_rate_per_order_14d,
            stddev((order_list_price - order_paid_price)/order_list_price) as std_dscnt_rate_per_order_14d,
            avg(order_shipping_amount) as avg_shpfee_per_order_usd_14d,
            stddev(order_shipping_amount) as std_shpfee_per_order_usd_14d
        FROM 
            (
                select
                    a.buyer_id,
                    a.current_login_time,
                    a.current_ip,
                    a.current_ip3ua,
                    b.order_create_date,
                    b.sales_order_id,
                    b.order_list_price,
                    b.order_unit_price,
                    b.order_paid_price,
                    b.order_shipping_amount
                from
                    (
                        SELECT 
                            buyer_id,
                            current_login_time,
                            current_ip,
                            CONCAT(current_ip3, current_useragent) as current_ip3ua
                        from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3
                    )   a
                left JOIN 
                    (
                        SELECT 
                            dateadd(order_create_date, 1, 'hour') as order_create_date,
                            sales_order_id,
                            buyer_id,
                            sum(list_price * exchange_rate) as order_list_price,
                            sum(unit_price * exchange_rate) as order_unit_price,
                            sum(paid_price * exchange_rate) as order_paid_price,
                            sum(shipping_amount_total * exchange_rate)  as order_shipping_amount
                        from lazada_cdm.dwd_lzd_trd_core_create_di
                        where SUBSTR(ds, 1, 8) >= '20220201' and substr(ds, 1, 8) <= '20220601'
                        and venture = 'ID'
                        group by order_create_date, sales_order_id, buyer_id
                    )   b
                on a.buyer_id = b.buyer_id
                    and datediff(a.current_login_time, b.order_create_date, 'dd') <= 14 and a.current_login_time >= b.order_create_date
            )            
        group by buyer_id, current_login_time, current_ip, current_ip3ua
    )   a1

left JOIN 
    (
        SELECT 
            a.buyer_id,
            a.current_login_time,
            collect_list(distinct b.ip3ua) as list_seller_ip3ua,
            collect_list(distinct b.ip) as list_seller_ip
        from 
            (
                select distinct
                    buyer_id,
                    current_login_time,
                    seller_id
                from lazada_biz_sec_dev.white_ato_login_sample_basic_info_full_order_seller_v3
            )   a
        left join
            (
                SELECT
                    acctdata_userid,
                    FROM_UNIXTIME(receive_time/1000) as receive_time,
                    envdata_ip as ip,
                    concat(split_part(envdata_ip,'.',1), split_part(envdata_ip,'.',2), SPLIT_PART(envdata_ip,'.',3), envdata_useragent) as ip3ua
                from lzd_secods.odl_event_async_lazada_login_success
                where substr(ds, 1, 8) >= '20220101' and substr(ds, 1, 8) <= '20220601'
                and acctdata_bizrole <> 'byr'
                and otherdata_issucc = 'true'
            )   b
        on a.seller_id = b.acctdata_userid
            and DATEDIFF(a.current_login_time, b.receive_time, 'mm') <= 3 and a.current_login_time >= b.receive_time
        group by a.buyer_id, a.current_login_time
    )   a2
on a1.buyer_id = a2.buyer_id and a1.current_login_time = a2.current_login_time
;

select * from lazada_biz_sec_dev.white_ato_login_sample_feature_order_v3;
----------------------------------------------------------------------------------------------------------------------------------
-- login cluster
-- number of different accounts for the same umid

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v3; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v3 LIFECYCLE 30 as
SELECT 
    buyer_id,
    current_login_time,
    current_umid,
    count(distinct login_id) as no_acct_umid_3m
FROM 
    (
        SELECT 
            a.*,
            b.login_id
        FROM 
            (
                select
                    buyer_id,
                    current_login_time,
                    current_umid
                from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3
            )   a

        left join
            (
                select
                    acctdata_userid as login_id,
                    umid,
                    FROM_UNIXTIME(receive_time/1000) as login_time
                from lzd_secods.odl_event_async_lazada_login_success
                where SUBSTR(ds,1,8) >= '20220101' and SUBSTR(ds,1,8) <= '20220601'
                and otherdata_issucc = 'true'
            )   b
        on a.current_umid = b.umid and DATEDIFF(a.current_login_time, b.login_time, 'mm') <= 3 and a.current_login_time > b.login_time
    )
group by buyer_id, current_login_time, current_umid
;


select * from lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v3;

----------------------------------------------------------------------------------------------------------------------------------
-- Final features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_login_sample_feature_v3; 
create table if not exists lazada_biz_sec_dev.white_ato_login_sample_feature_v3 LIFECYCLE 60 as

SELECT 
    a.buyer_id,
    0 as label, -- white sample
    a.id_new_ip2_3m,
    a.id_new_ip3_3m,
    a.no_unique_umid_14d,
    a.no_unique_ip2_14d,
    a.no_login_14d,
    b.id_ip_same_seller_14d,
    b.id_ip3ua_same_seller_14d,
    b.avg_price_per_order_usd_14d,
    b.std_price_per_order_usd_14d,
    b.avg_dscnt_rate_per_order_14d,
    b.std_dscnt_rate_per_order_14d,
    b.avg_shpfee_per_order_usd_14d,
    b.std_shpfee_per_order_usd_14d,
    f.is_susp_paymethod_14d as id_susp_paymethod_14d,
    c.no_acct_umid_3m,
    d.max_cancel_rate_14d,
    d.max_avg_price_seller_usd_14d,
    d.max_avg_dscnt_rate_seller_14d,
    d.max_avg_shpfee_seller_usd_14d

FROM 
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_env_v3
    )   a

left join
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_order_v3
    )   b
on a.buyer_id = b.buyer_id and a.current_login_time = b.current_login_time

left join 
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_cluster_v3
    )   c
on a.buyer_id = c.buyer_id and a.current_login_time = c.current_login_time

left JOIN 
    (
        select * from lazada_biz_sec_dev.white_ato_login_sample_feature_seller_v3
    )   d
on a.buyer_id = d.buyer_id and a.current_login_time = d.current_login_time
left JOIN 
    (
        select
            a1.buyer_id,
            a1.current_login_time,
            max(a2.is_susp_paymethod_flag) as is_susp_paymethod_14d
        from 
            (
                select
                    buyer_id,
                    current_login_time
                from lazada_biz_sec_dev.white_ato_login_sample_basic_info_v3
            )   a1
        left join 
            (
                SELECT 
                    buyer_id,
                    case when (payment_method like '%VA%') or (payment_method like '%OTC%') then '1' else '0'
                    end as is_susp_paymethod_flag,
                    dateadd(order_create_date, 1, 'hour') as order_create_date
                from lazada_cdm.dwd_lzd_trd_core_create_di
                where ds >= '20220201' and ds <= '20220601'
                and venture = 'ID'
            )   a2
        on a1.buyer_id = a2.buyer_id 
            and DATEDIFF(a1.current_login_time, a2.order_create_date, 'dd') <= 14 and a1.current_login_time >= a2.order_create_date
        group by a1.buyer_id, a1.current_login_time
    )   f
on a.buyer_id = f.buyer_id and a.current_login_time = f.current_login_time
;

select * from lazada_biz_sec_dev.white_ato_login_sample_feature_v3;
---------------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_login_sample_feature_v3; 
create table if not exists lazada_biz_sec_dev.ato_login_sample_feature_v3 LIFECYCLE 30 as

SELECT 
    buyer_id,
    label,
    cast(id_new_ip2_3m as bigint) as id_new_ip2_3m,
    cast(id_new_ip3_3m as bigint) as id_new_ip3_3m,
    no_unique_umid_14d,
    no_unique_ip2_14d,
    no_login_14d,
    cast(id_ip_same_seller_14d as BIGINT ) as id_ip_same_seller_14d,
    cast(id_ip3ua_same_seller_14d as BIGINT ) as id_ip3ua_same_seller_14d,
    avg_price_per_order_usd_14d,
    std_price_per_order_usd_14d,
    avg_dscnt_rate_per_order_14d,
    std_dscnt_rate_per_order_14d,
    avg_shpfee_per_order_usd_14d,
    std_shpfee_per_order_usd_14d,
    cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
    no_acct_umid_3m,
    max_cancel_rate_14d,
    max_avg_price_seller_usd_14d,
    max_avg_dscnt_rate_seller_14d,
    max_avg_shpfee_seller_usd_14d
from lazada_biz_sec_dev.white_ato_login_sample_feature_v3
union ALL 
    (
        select 
            buyer_id,
            label,
            cast(id_new_ip2_3m as bigint) as id_new_ip2_3m,
            cast(id_new_ip3_3m as bigint) as id_new_ip3_3m,
            no_unique_umid_14d,
            no_unique_ip2_14d,
            no_login_14d,
            cast(id_ip_same_seller_14d as BIGINT ) as id_ip_same_seller_14d,
            cast(id_ip3ua_same_seller_14d as BIGINT ) as id_ip3ua_same_seller_14d,
            avg_price_per_order_usd_14d,
            std_price_per_order_usd_14d,
            avg_dscnt_rate_per_order_14d,
            std_dscnt_rate_per_order_14d,
            avg_shpfee_per_order_usd_14d,
            std_shpfee_per_order_usd_14d,
            cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
            no_acct_umid_3m,
            max_cancel_rate_14d,
            max_avg_price_seller_usd_14d,
            max_avg_dscnt_rate_seller_14d,
            max_avg_shpfee_seller_usd_14d
        from lazada_biz_sec_dev.black_ato_login_sample_feature_v3
    )
;

select * from lazada_biz_sec_dev.ato_login_sample_feature_v3;

---------------------------------------------------------------------------------

SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.seller_scam_login_sample_feature_v3; 
create table if not exists lazada_biz_sec_dev.seller_scam_login_sample_feature_v3 LIFECYCLE 30 as

SELECT 
    buyer_id,
    label,
    cast(id_new_ip2_3m as bigint) as id_new_ip2_3m,
    cast(id_new_ip3_3m as bigint) as id_new_ip3_3m,
    no_unique_umid_14d,
    no_unique_ip2_14d,
    no_login_14d,
    cast(id_ip_same_seller_14d as BIGINT ) as id_ip_same_seller_14d,
    cast(id_ip3ua_same_seller_14d as BIGINT ) as id_ip3ua_same_seller_14d,
    avg_price_per_order_usd_14d,
    std_price_per_order_usd_14d,
    avg_dscnt_rate_per_order_14d,
    std_dscnt_rate_per_order_14d,
    avg_shpfee_per_order_usd_14d,
    std_shpfee_per_order_usd_14d,
    cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
    no_acct_umid_3m,
    max_cancel_rate_14d,
    max_avg_price_seller_usd_14d,
    max_avg_dscnt_rate_seller_14d,
    max_avg_shpfee_seller_usd_14d
from lazada_biz_sec_dev.white_ato_login_sample_feature_v3
union ALL 
    (
        select 
            buyer_id,
            label,
            cast(id_new_ip2_3m as bigint) as id_new_ip2_3m,
            cast(id_new_ip3_3m as bigint) as id_new_ip3_3m,
            no_unique_umid_14d,
            no_unique_ip2_14d,
            no_login_14d,
            cast(id_ip_same_seller_14d as BIGINT ) as id_ip_same_seller_14d,
            cast(id_ip3ua_same_seller_14d as BIGINT ) as id_ip3ua_same_seller_14d,
            avg_price_per_order_usd_14d,
            std_price_per_order_usd_14d,
            avg_dscnt_rate_per_order_14d,
            std_dscnt_rate_per_order_14d,
            avg_shpfee_per_order_usd_14d,
            std_shpfee_per_order_usd_14d,
            cast(id_susp_paymethod_14d as bigint) as id_susp_paymethod_14d,
            no_acct_umid_3m,
            max_cancel_rate_14d,
            max_avg_price_seller_usd_14d,
            max_avg_dscnt_rate_seller_14d,
            max_avg_shpfee_seller_usd_14d
        from lazada_biz_sec_dev.seller_scam_ato_login_sample_feature_v3
    )
;

select * from lazada_biz_sec_dev.seller_scam_login_sample_feature_v3;

```
## 2.4 Model setting and result
[ato_v2_experiment3_0708.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659692344023-aa8d8ecb-ac73-4fad-8560-829524a604d4.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659692344023-aa8d8ecb-ac73-4fad-8560-829524a604d4.ipynb%22%2C%22name%22%3A%22ato_v2_experiment3_0708.ipynb%22%2C%22size%22%3A1174310%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22u05fddf03-c738-4fac-8b73-6a5f2d9ae19%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22uc1b9c3ea%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)
### 2.4.1 Model train setting

1. use K-folds to achieve all prediction for data;
1. 1500 white samples are achieved by no previous 14d order records; while other 4500 white samples do have previous 14d order records
### 2.4.2 Model result
Random forest Performance:
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657675971334-d6223595-87b7-41d1-b585-862039c73884.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=275&id=ud809dff3&margin=%5Bobject%20Object%5D&name=image.png&originHeight=550&originWidth=1200&originalType=binary&ratio=1&rotation=0&showTitle=false&size=68330&status=done&style=none&taskId=u88074c47-b37f-4283-8742-7158eabd086&title=&width=600)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1657676051316-4cdc2ca5-c0be-4993-ab64-b114acacacc3.png#clientId=ud32e1aba-6977-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=298&id=uc288e23e&margin=%5Bobject%20Object%5D&name=image.png&originHeight=596&originWidth=838&originalType=binary&ratio=1&rotation=0&showTitle=false&size=122256&status=done&style=none&taskId=ufe9ed726-e8a6-4fa7-8cce-63e3725a321&title=&width=419)
### 2.4.3 0621 Review result
#### Conclusion:

1. **black list (totally 8 black prediction):**

('410403081127','1590887','400114485127','400205907540','400215606377','400313742582','400325922966','779680')

2. **7/8 precision after self-review**
### 2.4.4 0621-0628 Review result (Totally 140k+ data)
#### Conclusion (_Precision: 39/48 = 81.25%_):

1. **black list (totally 48 black prediction):**

0621: (**Precision: 7/8**)
('410403081127','1590887','400114485127','400205907540','400215606377','400313742582','400325922966','779680')
0622:(**Precision: 4/5**)
('400025974429', '400041573305', '400150155337', '400660458471', '400688631010')
0623:(**Precision: 2/3**)
('400029218850', '400023270667', '400191294495')
0624:(**Precision: 6/8**)
('32330000', '400130166144', '400135527502', '400163868278', '400394001854', '400692138592', '400692795688', '410401053917')

- **from 0621 to 0624, the precision is 19/24 =0.79**

0625:
('11415590', '400163868278', '400385793232', '400033504401', '400218252999', '400375350199', '400247988635')
0626:
('400019440153', '400097976103', '400113501448', '400172994123', '400273209562', '400336824041', '400378602578', '410434335755', '11167527', '400325454905', '410476107903', '8000833', '400069686152', '400197453128')
0627:
()
0628:
('400314390195', '11167527', '400336824041')

- **from 0625 to 0628, the precision is 20/24 =0.83**
### Further Explore:
#### Rank
Based on the prediction score given by the random forest model, we give 10 ranks for total review samples from 0 to 9. For instance, score 0~0.1 corresponds to Rank 1, which is the most safe one.
The distribution of the 10 ranks is:

| rank | number | precision |
| --- | --- | --- |
| 0 | 137561 |  |
| 1 | 1853 |  |
| 2 | 876 |  |
| 3 | 356 |  |
| 4 | 191 |  |
| 5 | 86 |  |
| 6 | 68 |  |
| 7 | 44 |  |
| 8 | 49 |  |
| 9 | 39 | 92.31% |

# Deployment
### Model name code
Login Model V2: 005333a20666a3e8d1317ab67723ab73
### Offline indicators
#### 1. SQL file
create table: 手动任务 - jiangyi_ATO - ato_login_v2_offline_feature_table
insert table: 数据开发 - jiangyi - MaxCompute - 数据开发 - ato_login_v2_offline_feature_impute
#### 2. table and corresponding offline indicators
##### ato_login_v2_offline_tab_01 (need modification)
offline indicators: new_ip2_3m
```sql
WITH buyer_login_90d AS 
(
    select   cast(mbr_id as string)                                                   as mbr_id
            ,concat(split_part(client_ip,'.',1),'.', split_part(client_ip,'.',2))     as ip2
            ,venture                                                                  as venture
    from lzd_secdw.dwd_lzd_mbr_login_ent_di 
    where ds between '${bizdate_89d}' and '${bizdate}' 
    and mbr_type = 'byr'
    group by mbr_id
            ,ip2
            ,venture

    union
    
    select acctdata_userid                                                            as mbr_id
          ,concat(split_part(envdata_ip,'.',1),'.', split_part(envdata_ip,'.',2))     as ip2 
          ,TOUPPER(COALESCE(acsdata_cntry,'null'))                                    as venture
    from lzd_secods.odl_event_async_lazada_login_success 
    where substr(ds,1,8) = '${today}'  --取今天的数据
    and acctdata_bizrole = 'byr'
    and perf_test = 'false'
    group by mbr_id
            ,ip2
            ,venture
)

insert overwrite table ato_login_v2_offline_tab_01_new PARTITION(ds = '${today_hour}')

SELECT 
     mbr_id                         as buyer_id
    ,venture                        as venture
    ,COLLECT_LIST(distinct ip2)     as ip2_list

FROM buyer_login_90d
group BY 
     buyer_id
    ,venture
; 
```
##### ato_login_v2_offline_tab_02 (need modification)
offline indicator: new_ip3_3m
```sql

WITH buyer_login_90d AS 
(
    select   cast(mbr_id as string)                                                   as mbr_id
            ,concat(split_part(client_ip,'.',1),'.', split_part(client_ip,'.',2), split_part(client_ip, '.', 3)) 
                                                                                      as ip3 
            ,venture                                                                  as venture
    from lzd_secdw.dwd_lzd_mbr_login_ent_di 
    where ds between '${bizdate_89d}' and '${bizdate}' 
    and mbr_type = 'byr'
    group by mbr_id
            ,ip3
            ,venture


    union
    select acctdata_userid                                                            as mbr_id
          ,concat(split_part(envdata_ip,'.',1),'.', split_part(envdata_ip,'.',2), split_part(envdata_ip, '.', 3)) 
                                                                                      as ip3 
          ,TOUPPER(COALESCE(acsdata_cntry,'null'))                                    as venture

    from lzd_secods.odl_event_async_lazada_login_success 
    where substr(ds,1,8) = '${today}'  --取今天的数据
    and acctdata_bizrole = 'byr'
    and perf_test = 'false'
    group by mbr_id
            ,ip3
            ,venture

)

insert overwrite table ato_login_v2_offline_tab_02_new PARTITION(ds = '${today_hour}')

SELECT 
     mbr_id                         as buyer_id
    ,venture                        as venture
    ,COLLECT_LIST(distinct ip3)     as ip3_list
FROM buyer_login_90d
group BY 
     buyer_id
    ,venture
; 
```
##### ato_login_v2_offline_tab_03 (can use)
offline indicator: 1. count_unique_umid_14d; 2. count_unique_ip2_14d; 3. count_login_14d
```sql
WITH buyer_login_14d AS 
(
    select   cast(mbr_id as string)                                                   as mbr_id
            ,umid                                                                     as umid
            ,concat(split_part(client_ip,'.',1),'.', split_part(client_ip,'.',2))     as ip2
            ,venture                                                                  as venture
    from lzd_secdw.dwd_lzd_mbr_login_ent_di 
    where ds between '${bizdate_13d}' and '${bizdate}' 
    and mbr_type = 'byr'
 
    union all
    select acctdata_userid                                                            as mbr_id
          ,umid                                                                       as umid
          ,concat(split_part(envdata_ip,'.',1),'.', split_part(envdata_ip,'.',2)) 
                                                                                      as ip2 
          ,TOUPPER(COALESCE(acsdata_cntry,'null'))                                    as venture
    from lzd_secods.odl_event_async_lazada_login_success 
    where substr(ds,1,8) = '${today}'  --取今天的数据
    and acctdata_bizrole = 'byr'
    and perf_test = 'false'
  
)

insert overwrite table ato_login_v2_offline_tab_03 PARTITION(ds = '${today_hour}')

SELECT 
     mbr_id                     as buyer_id
    ,venture
    ,count(distinct umid)       as count_unique_umid_14d
    ,count(distinct ip2)        as count_unique_ip2_14d
    ,count(*)                   as count_login_14d
FROM buyer_login_14d
group BY 
     buyer_id
    ,venture
; 
```
##### ato_login_v2_offline_tab_04 (need modification)
offline indicators: 14dseller_same_ip
```sql

with buyer_14dorder_corresponding_sellers as 
  (--获取近14天订单购买过的买家
   select buyer_id                                      as buyer_id
         ,seller_id                                     as seller_id      
         ,venture                                       as venture

   from (select cast(byr_member_id as string )          as buyer_id     	  
               ,selllist                                as selllist
               ,venture                                 as venture
             from lzd_secdw.dwd_lzd_ord_crt_ent_di
             where ds between '${bizdate_13d}' and '${bizdate}'-----过去的数据
          union 
                select byracctid                        as buyer_id
                      ,selllist                         as selllist
                      ,toupper(lazadasite)              as venture 
                from lzd_secods.odl_event_lazada_order_creation_risk_sg
                where substr(ds,1,8) = '${today}'  --取今天的数据 20220708
       ) LATERAL VIEW explode(split(selllist ,','))  seller_id AS seller_id
    group by buyer_id     
            ,seller_id 
            ,venture
  ),

seller_90dlogin_info AS 
   (--关注sellser近3个月的登陆记录
        select cast(mbr_id as string)              as mbr_id
              ,client_ip                           as ip
              ,venture                             as venture
        from lzd_secdw.dwd_lzd_mbr_login_ent_di 
        where ds between '${bizdate_89d}' and '${bizdate}'   --89天到昨天
           and mbr_id is not null 
           and mbr_type <> 'byr'
        group by mbr_id  
                ,ip
                ,venture
      union 
      select acctdata_userid                            as mbr_id
            ,envdata_ip                                 as ip
            ,TOUPPER(COALESCE(acsdata_cntry,'null'))    AS venture
        from lzd_secods.odl_event_async_lazada_login_success 
       where substr(ds,1,8) = '${today}'  --取今天的数据 20220708
         and perf_test = 'false'
         and acctdata_bizrole <> 'byr'
         and acctdata_userid is not null 
       group by mbr_id
               ,ip
               ,venture
     )  

insert overwrite table ato_login_v2_offline_tab_04_new PARTITION(ds = '${today_hour}')

select  t1.buyer_id
       ,t1.venture
       ,COLLECT_LIST(distinct t2.ip)     as seller_ip_list
from buyer_14dorder_corresponding_sellers t1
left join seller_90dlogin_info t2 on t1.venture = t2.venture and t1.seller_id = t2.mbr_id
group by 
  t1.buyer_id
 ,t1.venture
;
```
##### ato_login_v2_offline_tab_05 (need modification)
offline indicator: 14dseller_same_ip3ua
```sql

with buyer_14dorder_corresponding_sellers as 
  (--获取近14天订单购买过的买家
   select buyer_id                                      as buyer_id
         ,seller_id                                     as seller_id      
         ,venture                                       as venture

   from (select cast(byr_member_id as string )          as buyer_id     	  
               ,selllist                                as selllist
               ,venture                                 as venture
             from lzd_secdw.dwd_lzd_ord_crt_ent_di
             where ds between '${bizdate_13d}' and '${bizdate}'-----过去的数据
          union 
                select byracctid                        as buyer_id
                      ,selllist                         as selllist
                      ,toupper(lazadasite)              as venture 
                from lzd_secods.odl_event_lazada_order_creation_risk_sg
                where substr(ds,1,8) = '${today}'  --取今天的数据 20220708
       ) LATERAL VIEW explode(split(selllist ,','))  seller_id AS seller_id
    group by buyer_id     
            ,seller_id 
            ,venture
  ),

seller_90dlogin_info AS 
   (--关注sellser近3个月的登陆记录
        select cast(mbr_id as string)                 as mbr_id
              ,concat(split_part(client_ip,'.',1),'.', split_part(client_ip,'.',2), split_part(client_ip,'.',3), useragent) 
                                                      as ip3ua
              ,venture                                as venture
        from lzd_secdw.dwd_lzd_mbr_login_ent_di  
        where ds between '${bizdate_89d}' and '${bizdate}'   --89天到昨天
           and mbr_id is not null 
           and mbr_type <> 'byr'
        group by mbr_id  
                ,ip3ua
                ,venture
      union 
      select acctdata_userid                            as mbr_id
            ,concat(split_part(envdata_ip,'.',1),'.', split_part(envdata_ip,'.',2), split_part(envdata_ip,'.',3), envdata_useragent) 
                                                        as ip3ua
            ,TOUPPER(COALESCE(acsdata_cntry,'null'))    AS venture
        from lzd_secods.odl_event_async_lazada_login_success 
       where substr(ds, 1, 8) = '${today}'  --取今天的数据 20220708
         and perf_test = 'false'
         and acctdata_bizrole <> 'byr'
         and acctdata_userid is not null 
       group by mbr_id
               ,ip3ua
               ,venture
     )  

insert overwrite table ato_login_v2_offline_tab_05_new PARTITION(ds = '${today_hour}')

select  t1.buyer_id
       ,t1.venture
       ,COLLECT_LIST(distinct t2.ip3ua)                  as seller_ip3ua_list
from buyer_14dorder_corresponding_sellers t1
left join seller_90dlogin_info t2 on t1.venture = t2.venture and t1.seller_id = t2.mbr_id
group by 
  t1.buyer_id
 ,t1.venture
;

```
##### ato_login_v2_offline_tab_06 (can use)
offline indicator: 1. avg_price_per_order_usd_14d; 2. std_price_per_order_usd_14d; 3. avg_dscnt_rate_per_order_usd_14d; 4. std_dscnt_rate_per_order_usd_14d; 5. avg_shpfee_per_order_usd_14d; 6. std_shpfee_per_order_usd_14d
```sql
insert overwrite table ato_login_v2_offline_tab_06 PARTITION(ds = '${today_hour}')

select 
     t1.buyer_id                    as buyer_id
    ,t1.venture                     as venture
    ,t1.avg_grosspay * t2.to_usd    as avg_price_per_order_usd_14d
    ,t1.std_grosspay * t2.to_usd    as std_price_per_order_usd_14d
    ,t1.avg_discount_rate           as avg_dscnt_rate_per_order_usd_14d
    ,t1.std_discount_rate           as std_dscnt_rate_per_order_usd_14d
    ,t1.avg_shpfee * t2.to_usd      as avg_shpfee_per_order_usd_14d
    ,t1.std_shpfee * t2.to_usd      as std_shpfee_per_order_usd_14d
from
    (
        SELECT 
             buyer_id                 as buyer_id 
            ,venture                  as venture
            ,avg(grosspay)            as avg_grosspay
            ,stddev(grosspay)         as std_grosspay
            ,avg(discount_rate)       as avg_discount_rate
            ,stddev(discount_rate)    as std_discount_rate
            ,avg(shpfee)              as avg_shpfee
            ,stddev(shpfee)           as std_shpfee
        from    (select  
                         cast(byr_member_id  as string)   as buyer_id     	  
                        ,gross_pay_amt                    as grosspay     
                        ,vouch_amt/gross_pay_amt          as discount_rate
                        ,shp_amt                          as shpfee
                        ,venture                          as venture
            from lzd_secdw.dwd_lzd_ord_crt_ent_di
            where ds between '${bizdate_13d}' and '${bizdate}' 
            union all 
                    select 
                         byracctid                       as buyer_id
                        ,cast(grosspay as double)        as grosspay 
                        ,vouchamt / grosspay             as discount_rate 
                        ,cast(shpfee as double)          as shpfee
                        ,toupper(lazadasite)             as venture 
                    from lzd_secods.odl_event_lazada_order_creation_risk_sg
                    where substr(ds,1,8) = '${today}'
                )
        group by buyer_id
                ,venture
    )   t1
left JOIN 
    (
        SELECT venture
              ,to_usd
        from lazada_cdm.dim_lzd_exchange_rate
        where ds = '${bizdate}' 
    )   t2
    on t1.venture = t2.venture
;
```
##### ato_login_v2_offline_tab_07 (can use)
offline indicators: susp_payment_method_14d
```sql
with payment_14d as 
(
        select   cast(buyer_id as string)                   as buyer_id
                ,max(case when payment_method like '%OTC%' or payment_method like '%VA%'  then 1 else 0 end) 
                                                            as id_susp_paymethod_14d
                ,venture                                    as venture
        from lazada_cdm.dwd_lzd_trd_core_create_di
        where ds >= '${bizdate_13d}' and ds <= '${bizdate}' 
        and is_test = 0
        and is_fulfilled = 1
        and b2b = 0
        group by buyer_id
                ,venture
        union all 
            SELECT 
                globlacct_havanauserid          as buyer_id
               ,max(case when globlpaydata_payselectedmethd like '%OTC%' or globlpaydata_payselectedmethd like '%VA%' then 1 else 0 end) 
                                                as id_susp_paymethod_14d
               ,TOUPPER(cntry)                  as venture
            from lzd_secods.odl_event_global_pay_now_sync
            where substr(ds,1,8) = '${today}'
            group by buyer_id
                    ,venture
)

insert overwrite table ato_login_v2_offline_tab_07 PARTITION(ds = '${today_hour}')

SELECT 
         buyer_id                       as buyer_id
        ,venture                        as venture
        ,max(id_susp_paymethod_14d)     as susp_payment_method_14d
from payment_14d
group BY buyer_id
        ,venture
;

```
##### ato_login_v2_offline_tab_08 (can use)
offline indicator: count_acct_same_umid_14d
```sql

with login_90d AS 
(
        select cast(mbr_id as string)           as mbr_id
              ,umid                             as umid
              ,venture                          as venture
        from lzd_secdw.dwd_lzd_mbr_login_ent_di  
        where ds between '${bizdate_89d}' and '${bizdate}' 
        group by mbr_id    
                ,umid
                ,venture
      union 
      select acctdata_userid                                                            as mbr_id
            ,umid                                                                       as umid
            ,TOUPPER(COALESCE(acsdata_cntry,'null'))                                    as venture
        from lzd_secods.odl_event_async_lazada_login_success 
       where substr(ds,1,8) = '${today}'  --取今天的数据
         and perf_test = 'false'
       group by  mbr_id    
                ,umid
                ,venture
)  

insert overwrite table ato_login_v2_offline_tab_08 PARTITION(ds = '${today_hour}')

SELECT      
         umid                               as umid
        ,venture                            as venture
        ,count(distinct mbr_id)             as count_acct_same_umid_14d
from login_90d
group by umid
        ,venture
;

```
##### ato_login_v2_offline_tab_09 (can use)
offline indicator: 1.max_cancel_rate_14d; 2. max_avg_price_seller_usd_14d; 3. max_avg_dscnt_rate_seller_usd_14d; 4. max_avg_shpfee_seller_usd_14d
```sql

with buyer_14dorder_corresponding_sellers as 
  (--获取近14天订单购买过的买家
   select buyer_id                                      as buyer_id
         ,seller_id                                     as seller_id      
         ,venture                                       as venture

   from (select cast(byr_member_id as string)           as buyer_id     	  
               ,selllist                                as selllist
               ,venture                                 as venture
             from lzd_secdw.dwd_lzd_ord_crt_ent_di
             where ds between '${bizdate_13d}' and '${bizdate}'-----过去的数据
          union 
                select byracctid                        as buyer_id
                      ,selllist                         as selllist
                      ,toupper(lazadasite)              as venture 
                from lzd_secods.odl_event_lazada_order_creation_risk_sg
                where substr(ds,1,8) = '${today}'  --取今天的数据 20220708
       ) LATERAL VIEW explode(split(selllist ,','))  seller_id AS seller_id
    group by buyer_id     
            ,seller_id 
            ,venture
  )

insert overwrite table ato_login_v2_offline_tab_09 PARTITION(ds = '${today_hour}')
--缺省值用-1填充
select t1.buyer_id                                as buyer_id
      ,max(nvl(orderinfo.cancel_rate        ,-1)) as max_cancel_rate_14d
      ,max(nvl(orderinfo.avg_item_paid_price,-1)) as max_avg_price_seller_usd_14d
      ,max(nvl(orderinfo.avg_item_dscnt_rate,-1)) as max_avg_dscnt_rate_seller_usd_14d
      ,max(nvl(orderinfo.avg_order_shpfee   ,-1)) as max_avg_shpfee_seller_usd_14d
      ,t1.venture                                 as venture
from buyer_14dorder_corresponding_sellers t1 
left join 
-- 如果order_creation_risk_sg中包含list_price，此处可替换成order_creation_risk_sg table
-- 此处统计信息不包含今天，卖家列表包含今天
(--订单的seller数据
   select seller_id                                                                 as seller_id
         ,COUNT(*)                                                                  as order_cnt
         ,sum(case when cancel_date is null then 0 else 1 end )                     as cancel_cnt 
         ,sum(case when cancel_date is null then 0 else 1 end ) / count(*)          as cancel_rate
         ,avg(paid_price * exchange_rate)                                           as avg_item_paid_price
         ,avg((list_price-paid_price)/paid_price)                                   as avg_item_dscnt_rate 
         ,sum(shipping_amount) / count(distinct order_id) * exchange_rate           as avg_order_shpfee
         ,venture                                                                   as venture
    from lazada_cdm.dwd_lzd_trd_core_create_di
   where ds between '${bizdate_89d}' and '${bizdate}'
     and is_test = 0
     and is_fulfilled = 1
     and b2b = 0
     group by seller_id
             ,venture
             ,exchange_rate
) orderinfo 
on t1.seller_id = orderinfo.seller_id and t1.venture = orderinfo.venture
group by t1.buyer_id
        ,t1.venture
;
```
##### ato_login_v2_offline_tab_10 (need modification)
offline indicator: new_umid_3m **[model trigger indicator]**
```sql

WITH buyer_login_90d AS 
(
    select   cast(mbr_id as string)              as mbr_id
            ,umid                                as umid
            ,venture                             as venture
    from lzd_secdw.dwd_lzd_mbr_login_ent_di 
    where ds between '${bizdate_89d}' and '${bizdate}' 
    and mbr_type = 'byr'
    group by mbr_id
            ,umid
            ,venture
 
    union
    select acctdata_userid                                                            as mbr_id
          ,umid                                                                       as umid
          ,TOUPPER(COALESCE(acsdata_cntry,'null'))                                    as venture
    from lzd_secods.odl_event_async_lazada_login_success 
    where substr(ds,1,8) = '${today}'  --取今据
    and acctdata_bizrole = 'byr'
    and perf_test = 'false'
    group by mbr_id
            ,umid
            ,venture

)

insert overwrite table ato_login_v2_offline_tab_10_new2 PARTITION(ds = '${today_hour}')

SELECT  
     mbr_id                         as buyer_id
    ,venture                        as venture
    ,COLLECT_LIST(umid)             as umid_list
FROM buyer_login_90d
group BY 
     buyer_id
    ,venture

; 
```
##### ato_login_v2_offline_tab_11 (can use)
offline indicator: count_login_3m **[model trigger indicator]**
```sql

WITH buyer_login_90d AS 
(
    select   cast(mbr_id as string)                 as mbr_id
            ,venture                                as venture
    from lzd_secdw.dwd_lzd_mbr_login_ent_di
    where ds between '${bizdate_89d}' and '${bizdate}' 
    and mbr_type = 'byr'
    
    union all
    select acctdata_userid                                                            as mbr_id
          ,TOUPPER(COALESCE(acsdata_cntry,'null'))                                    as venture
    from lzd_secods.odl_event_async_lazada_login_success 
    where substr(ds,1,8) = '${today}'  --取今天的数据
    and acctdata_bizrole = 'byr'
    and perf_test = 'false'
)

insert overwrite table ato_login_v2_offline_tab_11 PARTITION(ds = '${today_hour}')

SELECT 
     mbr_id                             as buyer_id
    ,venture                            as venture
    ,count(*)                           as count_login_3m
FROM buyer_login_90d
group BY 
     buyer_id
    ,venture
; 
```
#### 3. offline indicator and its corresponding code which can be used
**Features:**

1. max_cancel_rate_14d: LQRG
1. max_avg_discnt_rate_seller_usd_14d: LQRH
1. max_avg_shpfee_seller_usd_14d: LQRI
1. max_avg_price_seller_usd_14d: LQRF
1. count_acct_same_umid_14d: LQRE
1. susp_payment_method_14d: LQRD
1. avg_shpfee_per_order_usd_14d: LQRA
1. std_shpfee_per_order_usd_14d: LQRB
1. avg_price_per_order_usd_14d: LQRC
1. std_price_per_order_usd_14d: LQQX
1. avg_dscnt_rate_per_order_usd_14d: LQQY 
1. std_dscnt_rate_per_order_usd_14d: LQQZ
1. count_unique_ip2_14d: LQQU
1. count_unique_umid_14d: LQQS
1. count_login_14d: LQQT

**Trigger indicators:**

1. count_login_3m: LQRK
#### 4. offline indicators that required to be modified
**Features:**

1. new_ip2_3m
1. new_ip3_3m
1. 14dseller_same_ip3ua
1. 14dseller_same_ip

**Trigger indicators:**

1. new_umid_3m
