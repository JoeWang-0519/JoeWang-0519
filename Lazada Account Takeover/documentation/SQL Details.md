## 1. SQL for selecting black samples
### Total ATO samples (including seller-scam and other MOs):
#### Logic part:

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
- match with 'lzd_secods.odl_event_async_lazada_login_success' table for all umids from 0201 to 0601 to find the frequent umid; 
   - **218/1637: only 1 used umid (there must be no abnormal login for these cases);**
   - 1419/1637: >= 2 used umids (potential ATO)
      - 7/1419: have >= 10 different umids (**_too many different umids seem to be suspicious account_**)
      - 1412/1419:  2 <= different umids < 10 
         - **Define frequqent umid: **
            - max(login times) >=4 and the corresponding umid	(_can modify_)
            - Next generation: explode cleverer ways for determine frequent umids
               - One idea: use percentage of all login number, select some thresholds, then we may have multiple frequent umids (if use max, we can just have one).
         - 42/1412 : max(login times) <= 3, inactive customers, kick out
         - 1370/1412:  max(login times) >= 4, our interest
            - 9/1370: multiple maximum, kick out
            - 1361/1370: one max login times record, treat as frequent umid! (**_totally 1361_**)
- match with 'lzd_secods.odl_event_async_lazada_login_success' table, **find the login records that, 1. not frequent umid; 2. logintype != 'auto'; 3. the nearest two (before and after). Moreover, we require that, cnt_umid_login <= 10 (to select those accounts which are not so abnormal);**
   - **_totally 1361 records_**
      - **_before: 340_**
      - **_after:  1092_**
- choose the record that satisfies **_either of these 3 scenarios:_** 
   - 1. umid_before = '\N' but umid_after exists; 
   - 2. umid_before exists but umid_after = '\N'; 
   - 3. umid_before and umid_after both exists and umid_before = umid_after;
   - **totally 1155 records (which is our black samples)**

With this procedure, there are **1155** black samples;
#### SQL codes with notes: 

- table: **lazada_biz_sec_dev.black_ato_login_sample;**
```sql
SET odps.instance.priority = 0;

-- Description: Make the hit_flag (trigger second verification), diff_id (difference between CC_create userid and order_create userid)
-- for the earliest CC case
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
-- Aim: Find the Abnormal Login Time
-- 1. find the frequent devices

-- base1 Description: 
-- find CC_create_time, order_create_time, whether CC_buyer_id corresponds with order_buyer_id, whether trigger second verification
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
-- base2 Description:
-- select earliest records with respect to each buyer id

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

-- base2.5 Description:
-- For each order, select the latest ato (CC) records;

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
-- Description:
-- for each order_buyer_id, find different login counts with respect to different umid

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
-- Description:
-- find those buyers who satisfy: 
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
-- Description:
-- find the frequent umid with respect to each buyer, and left join with the CC records

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
-- Description:
-- Find the ALL abnormal login records with respect to each buyer, and left join with the CC records
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
-- Description: 
-- Find all abnormal login records before the ATO (CC) create

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
-- Description: 
-- Find abnormal login counts before the ATO (CC) create

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
-- Description: 
-- Find all abnormal login records after the ATO (CC) create

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
-- Description: 
-- Find abnormal login counts after the ATO (CC) create

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
-- Description:
-- Use logic to determine those relatively reliable ATO abnormal login records

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
-- Description: 
-- Determine the abnormal login umid for each ATO CC case;

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

-- Description:
-- ATO CC case left join the total login records with abnormal umid;

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

-- Description:
-- Find the first Abnormal login ATO records

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
```
### seller-scam ATO samples (aim for Login ATO Model)
#### SQL codes (focus on 'serv_tag_name' in CC ticket table):

- table: **lazada_biz_sec_dev.black_ato_scam_seller_v2**;
```sql
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
### direct ATO samples (aim for Order-create ATO Model)
#### Logic part:
Find those records which satisfy:

- not appear in seller-scam ATO samples;
- earliest abnormal login time is **earlier** than order create time;
#### SQL codes:

- table: **lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base1**
```sql
select 
    order_buyer_id,
    abnormal_umid,
    earliest_abnormal_login
FROM 
    (
        SELECT 
            order_buyer_id,
            abnormal_umid,
            earliest_abnormal_login,
            case when order_buyer_id in (SELECT distinct buyer_id from lazada_biz_sec_dev.black_ato_scam_seller_v2) then '0'
                else '1' end as direct_ato_flag
        from lazada_biz_sec_dev.black_ato_login_sample
        where acsdata_entrance = 'native'
        and order_create_date > earliest_abnormal_login
    )
where direct_ato_flag = 1
;
```
## 2. SQL for selecting white samples
### White samples for  Login Model:

- recent version: ATO login v2;
#### Logic part:

1. select those accounts which satisfy:
   - click path does not include 'wallet', 'bank-add', 'bank-list', 'info-change';
   - unique shipping address;
   - unique shipping customer name;
2. among those accounts satisfy condition (1), select those login records which satisfy (trigger condition for model):
   - logintype is not 'auto';
   - is new umid over the past 3 months;
   - not the first login record over the past 3 months;
3. select 1500 white samples that do not have previous 14d's order records and 4500 that have previous 14d's order records (totally 6000 white samples); **[for ATO login v2 experiment 2]**
#### SQL codes with notes:

- table:** lazada_biz_sec_dev.white_ato_login_sample_v3**;
```sql
-- Description:
-- Find the click-path, shipping address, shipping customer counts
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
-- Description:
-- Construct trigger condition (is_new_umid and not_first_login) for those not suspicious accounts
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
-- Description:
-- Select those login records for not suspicious accounts and triggered by our model
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
-- Description:
-- Total Table for white login sample
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
-- Description:
-- White samples after randomly sampling (1500 no order records + 4500 have order records)
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
```
## 3. Login Model Features Pipeline

- recent version: ATO login v2;
### Feature list:
Abnormal environment difference: 

| index | feature | remark |
| --- | --- | --- |
|  | buyer_id |  |
|  | login_date |  |
|  | labels (black/white) |  |
| 1 | ip2_3m | indicator |
| 2 | ip3_3m | indicator |
| 3 | count_unique_umid_14d |  |
| 4 | count_unique_ip2_14d |  |
| 5 | count_login_14d |  |

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

### SQL codes with notes:

- table: **lazada_biz_sec_dev.seller_scam_login_sample_feature_v3**;
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

```
## 4. Order-create Model Features Pipeline

- recent version: ATO order-create v1 (experiment 2);
### Feature list:
Click-info level:

| index | feature | remark |
| --- | --- | --- |
|  | buyer_id |  |
|  | order_create_date |  |
|  | labels (black/white) |  |
| 1 | click_path_embedding | 512 dimension vector (embedding) |
| 2 | freq_myacct |  |
| 3 | freq_searchlist |  |
| 4 | freq_pdp |  |
| 5 | freq_acctinfo |  |
| 6 | avg_stay_time_pdp	 |  |
| 7 | total_stay_time_pdp |  |
| 8 | avg_stay_time |  |
| 9 | total_stay_time |  |
| 10 | click_path_length |  |

Order-info level:

| index | feature | remark |
| --- | --- | --- |
| 11 | id_susp_payment (paynow event) | here, suspicous payment method means: a) paylater; b) account money c) credit card (存疑, **currently just use a) and b)**) |
| 12 | id_category_dg (order creation risk sg) | check if the order includes digital goods |
| 13 | no_acct_same_umid_3m | number of different accounts that are logined with this umid (this time is included) |
| 14 | no_login_same_umid_3m | number of different login times (for this account) that are logined with this umid (this time is included) |

### SQL codes with notes:

- table: **lazada_biz_sec_dev.ato_order_create_v1_exp2_feature**;
```sql
-- Description:
-- for each black order-create records, find the closest login records with same device (umid)
select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_fst_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_fst_null LIFECYCLE 30 as

SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as avg_stay_time,
    sum(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as total_stay_time_pdp,
    avg(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as avg_stay_time_pdp,
    count(b.visit_time) as click_path_length,
    count(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end)/count(b.visit_time) as freq_pdp,
    count(case when tolower(b.url) = 'member_myaccount' then b.page_stay_time end)/count(b.visit_time) as freq_myacct,
    count(case when tolower(b.url) = 'page_searchlist' then b.page_stay_time end)/count(b.visit_time) as freq_searchlist,
    count(case when tolower(b.url) = 'account_info' then b.page_stay_time end)/count(b.visit_time) as freq_acctinfo
from 
    (
        select *
        from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4
        where envdata_utdid is NULL 
        and SUBSTR(order_create_time,1,10) < '2022-04-01' 
        and order_buyer_id is not Null
    )   a
left join 
    (
        SELECT 
            local_time,
            url,
            visit_time,
            user_id,
            split_part(spm_id, '.', 2) as spam,
            utdid,
            page_stay_time
        from alilog.dwd_lzd_log_ut_pv_di
        where ds >= '20220201' and ds <= '20220401'
        and venture = 'ID'
    )   b
on a.order_create_time >= b.local_time and a.login_time <= b.local_time and a.order_buyer_id = b.user_id
group by a.order_buyer_id, a.orderid, a.order_create_time
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_fst_null;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_not_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_not_null LIFECYCLE 30 as

SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as avg_stay_time,
    sum(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as total_stay_time_pdp,
    avg(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as avg_stay_time_pdp,
    count(b.visit_time) as click_path_length,
    count(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end)/count(b.visit_time) as freq_pdp,
    count(case when tolower(b.url) = 'member_myaccount' then b.page_stay_time end)/count(b.visit_time) as freq_myacct,
    count(case when tolower(b.url) = 'page_searchlist' then b.page_stay_time end)/count(b.visit_time) as freq_searchlist,
    count(case when tolower(b.url) = 'account_info' then b.page_stay_time end)/count(b.visit_time) as freq_acctinfo
from 
    (
        select *
        from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4
        where envdata_utdid is not NULL 
        and SUBSTR(order_create_time,1,10) <= '2022-06-01' and SUBSTR(order_create_time,1,10) >= '2022-04-01'
        and order_buyer_id is not Null
    )   a
left join 
    (
        SELECT 
            local_time,
            url,
            visit_time,
            user_id,
            split_part(spm_id, '.', 2) as spam,
            utdid,
            page_stay_time
        from alilog.dwd_lzd_log_ut_pv_di
        where ds >= '20220401' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.order_create_time >= b.local_time and a.login_time <= b.local_time and a.order_buyer_id = b.user_id and a.envdata_utdid = b.utdid
group by a.order_buyer_id, a.orderid, a.order_create_time
;

--select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_not_null;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_null LIFECYCLE 30 as

SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as avg_stay_time,
    sum(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as total_stay_time_pdp,
    avg(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as avg_stay_time_pdp,
    count(b.visit_time) as click_path_length,
    count(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end)/count(b.visit_time) as freq_pdp,
    count(case when tolower(b.url) = 'member_myaccount' then b.page_stay_time end)/count(b.visit_time) as freq_myacct,
    count(case when tolower(b.url) = 'page_searchlist' then b.page_stay_time end)/count(b.visit_time) as freq_searchlist,
    count(case when tolower(b.url) = 'account_info' then b.page_stay_time end)/count(b.visit_time) as freq_acctinfo
from 
    (
        select *
        from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4
        where envdata_utdid is NULL 
        and SUBSTR(order_create_time,1,10) <= '2022-06-01' and SUBSTR(order_create_time,1,10) >= '2022-04-01'
        and order_buyer_id is not Null
    )   a
left join 
    (
        SELECT 
            local_time,
            url,
            visit_time,
            user_id,
            split_part(spm_id, '.', 2) as spam,
            utdid,
            page_stay_time
        from alilog.dwd_lzd_log_ut_pv_di
        where ds >= '20220401' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.order_create_time >= b.local_time and a.login_time <= b.local_time and a.order_buyer_id = b.user_id
group by a.order_buyer_id, a.orderid, a.order_create_time
;

--select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_null;

------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_click; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp2_click LIFECYCLE 30 as

select *
from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_fst_null
union ALL 
    (
        select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_null
    )
union all
    (
        select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_base5_scd_not_null
    )
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_click
limit 100;
-- WHITE
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_order_create_v1_exp2_click; 
create table if not exists lazada_biz_sec_dev.white_ato_order_create_v1_exp2_click LIFECYCLE 30 as
SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as avg_stay_time,
    sum(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as total_stay_time_pdp,
    avg(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end) as avg_stay_time_pdp,
    count(b.visit_time) as click_path_length,
    count(case when tolower(b.url) = 'page_pdp' then b.page_stay_time end)/count(b.visit_time) as freq_pdp,
    count(case when tolower(b.url) = 'member_myaccount' then b.page_stay_time end)/count(b.visit_time) as freq_myacct,
    count(case when tolower(b.url) = 'page_searchlist' then b.page_stay_time end)/count(b.visit_time) as freq_searchlist,
    count(case when tolower(b.url) = 'account_info' then b.page_stay_time end)/count(b.visit_time) as freq_acctinfo
from
    (
        select *
        from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base3
        where order_buyer_id is not Null
    )   a
left join 
    (
        SELECT 
            local_time,
            url,
            visit_time,
            user_id,
            split_part(spm_id, '.', 2) as spam,
            utdid,
            page_stay_time
        from alilog.dwd_lzd_log_ut_pv_di
        where ds >= '20220401' and ds <= '20220602'
        and venture = 'ID'
    )   b
on a.order_create_time >= b.local_time and a.login_time <= b.local_time and a.order_buyer_id = b.user_id
group by a.order_buyer_id, a.orderid, a.order_create_time
;

select * from lazada_biz_sec_dev.white_ato_order_create_v1_exp2_click
limit 10
;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_order_create_v1_exp2_click; 
create table if not exists lazada_biz_sec_dev.ato_order_create_v1_exp2_click LIFECYCLE 30 as

select 
    1 as label,
    TO_CHAR(order_buyer_id) as order_buyer_id,
    orderid,
    order_create_time,
    features,
    spam_list,
    freq_myacct,
    freq_searchlist,
    freq_pdp,
    freq_acctinfo,
    avg_stay_time_pdp,
    total_stay_time_pdp,
    avg_stay_time,
    total_stay_time,
    click_path_length
from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_click
union ALL 
    (
        select 
            0 as label,
            order_buyer_id,
            orderid,
            order_create_time,
            features,
            spam_list,
            freq_myacct,
            freq_searchlist,
            freq_pdp,
            freq_acctinfo,
            avg_stay_time_pdp,
            total_stay_time_pdp,
            avg_stay_time,
            total_stay_time,
            click_path_length
        from lazada_biz_sec_dev.white_ato_order_create_v1_exp2_click
        where features is not null
    )
;

select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_click
limit 1500;

select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_click
where label = 1;
------------------------------------------------------------------------
-- Order-info level
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part1; 
create table if not exists lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part1 LIFECYCLE 30 as

SELECT 
    a.*,
    max(case when b.payment_method in ("PAYMENT_ACCOUNT", "PAY_LATER") then 1 else 0 end) as id_susp_payment,
    max(b.is_digital) as id_category_dg
FROM 
    (
        select 
            order_buyer_id,
            orderid,
            order_create_time
        from lazada_biz_sec_dev.ato_order_create_v1_exp2_click
    )   a
left join 
    (
        SELECT 
            buyer_id,
            sales_order_id,
            payment_method,
            is_digital
        from lazada_cdm.dwd_lzd_trd_core_create_di
        where ds >= '20220201' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.order_buyer_id = b.buyer_id and a.orderid = b.sales_order_id
group by a.order_buyer_id, a.order_create_time, a.orderid
;

select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part1;
------------------------------------------------------------------------
------------------------------------------------------------------------
--BLACK
-- achieve corresponding umid for each trade record
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_base1; 
create table if not exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_base1 LIFECYCLE 30 as

select 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    b.abnormal_umid as umid 
FROM 
    (
        select
            *
        from lazada_biz_sec_dev.black_ato_order_create_v1_exp2_click
    )   a
left JOIN 
    (
        SELECT 
            *
        from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4
    )   b
on a.order_buyer_id = b.order_buyer_id and a.orderid = b.orderid
;

select * from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_base1;

------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_acct; 
create table if not exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_acct LIFECYCLE 30 as
SELECT 
    a.*,
    count(distinct b.acctdata_userid) as no_acct_same_umid_3m
FROM 
    (
        select * from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_base1
    )   a
left join 
    (
        select 
            acctdata_userid,
            umid,
            from_unixtime(receive_time/1000) as login_time
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20211101' and substr(ds,1,8) <= '20220601'
    )   b
on a.umid = b.umid and a.order_create_time > b.login_time and datediff(a.order_create_time, b.login_time, 'month') <= 3
group by a.order_buyer_id, a.orderid, a.order_create_time, a.umid
;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_login; 
create table if not exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_login LIFECYCLE 30 as

SELECT 
    a.*,
    count(1) as no_login_same_umid_3m
FROM 
    (
        select * from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_base1
    )   a
left join 
    (
        select 
            acctdata_userid,
            umid,
            from_unixtime(receive_time/1000) as login_time
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20211101' and substr(ds,1,8) <= '20220601'
    )   b
on a.umid = b.umid and a.order_buyer_id = b.acctdata_userid and a.order_create_time > b.login_time and datediff(a.order_create_time, b.login_time, 'month') <= 3
group by a.order_buyer_id, a.orderid, a.order_create_time, a.umid
;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2; 
create table if not exists lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2 LIFECYCLE 30 as

select
    a.*,
    b.no_login_same_umid_3m
from 
    (
        select * from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_acct
    )   a 
left join
    (
        SELECT * from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2_login
    )   b
on a.order_buyer_id = b.order_buyer_id and a.orderid = b.orderid and a.umid = b.umid
;

select * from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2;
------------------------------------------------------------------------
------------------------------------------------------------------------
--WHITE
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_base1; 
create table if not exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_base1 LIFECYCLE 30 as

select 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    b.umid as umid 
FROM 
    (
        select
            *
        from lazada_biz_sec_dev.white_ato_order_create_v1_exp2_click
        where features is not Null
    )   a
left JOIN 
    (
        SELECT 
            event_id,
            orderid,
            from_unixtime(receive_time/1000) as order_create_time,
            byracctid,
            umid
        from lzd_secods.odl_event_lazada_order_creation_risk_sg
        where substr(ds,1,8) >= '20220401' and substr(ds,1,8) <= '20220601'
    )   b
on a.order_buyer_id = b.byracctid and a.orderid = b.orderid and a.order_create_time = b.order_create_time
;

select * from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_base1;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_acct; 
create table if not exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_acct LIFECYCLE 30 as
SELECT 
    a.*,
    count(distinct b.acctdata_userid) as no_acct_same_umid_3m
FROM 
    (
        select * from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_base1
    )   a
left join 
    (
        select 
            acctdata_userid,
            umid,
            from_unixtime(receive_time/1000) as login_time
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220101' and substr(ds,1,8) <= '20220601'
    )   b
on a.umid = b.umid and a.order_create_time > b.login_time and datediff(a.order_create_time, b.login_time, 'month') <= 3
group by a.order_buyer_id, a.orderid, a.order_create_time, a.umid
;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_login; 
create table if not exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_login LIFECYCLE 30 as

SELECT 
    a.*,
    count(1) as no_login_same_umid_3m
FROM 
    (
        select * from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_base1
    )   a
left join 
    (
        select 
            acctdata_userid,
            umid,
            from_unixtime(receive_time/1000) as login_time
        from lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220101' and substr(ds,1,8) <= '20220601'
    )   b
on a.umid = b.umid and a.order_buyer_id = b.acctdata_userid and a.order_create_time > b.login_time and datediff(a.order_create_time, b.login_time, 'month') <= 3
group by a.order_buyer_id, a.orderid, a.order_create_time, a.umid
;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2; 
create table if not exists lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2 LIFECYCLE 30 as

select
    a.*,
    b.no_login_same_umid_3m
from 
    (
        select * from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_acct
    )   a 
left join
    (
        SELECT * from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2_login
    )   b
on a.order_buyer_id = b.order_buyer_id and a.orderid = b.orderid and a.umid = b.umid
;

select * from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part2; 
create table if not exists lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part2 LIFECYCLE 30 as

SELECT
    *
from lazada_biz_sec_dev.white_order_create_v1_exp2_order_part2
union ALL 
    (
        SELECT 
            to_char(order_buyer_id) as order_buyer_id,
            orderid,
            order_create_time,
            umid,
            no_acct_same_umid_3m,
            no_login_same_umid_3m
        from lazada_biz_sec_dev.black_order_create_v1_exp2_order_part2
    )
;

select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part2;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_order_create_v1_exp2_feature; 
create table if not exists lazada_biz_sec_dev.ato_order_create_v1_exp2_feature LIFECYCLE 30 as

select
    a.*,
    b.id_susp_payment,
    b.id_category_dg,
    c.no_acct_same_umid_3m,
    c.no_login_same_umid_3m
from 
    (
        select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_click 
    )   a
left join 
    (
        select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part1
    )   b
on a.order_buyer_id = b.order_buyer_id and a.orderid = b.orderid and a.order_create_time = b.order_create_time
left JOIN 
    (
        select * from lazada_biz_sec_dev.ato_order_create_v1_exp2_order_part2
    )   c
on a.order_buyer_id = c.order_buyer_id and a.orderid = c.orderid and a.order_create_time = c.order_create_time
;
```
 
### 



