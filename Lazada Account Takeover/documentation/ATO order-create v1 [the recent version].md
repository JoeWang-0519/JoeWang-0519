# Experiment 1 (for native)
## Idea:
Here, we mainly focus on those direct ATO cases. That is mainly because, there are great differences between seller-scam ATO and direct ATO, in the sense that the former has the incentive to refund, while the latter only directly makes money by creating orders. 
Therefore, a natural way to solve this problem is to, build different models for different senarios. Firstly, we handle the direct ATO cases by building models on order-create step. Then, we detect the seller-scam ATO cases by building models on order-cancel step.
Our model is to detect those suspicious order after login.
## Black samples (0201-0601):

- Assumption: our earliest abnormal login time is approximately accurate.
### Pipeline with codes:

1. For each account, fix the abnormal umid corresponding to the earliest abnormal login record;
1. Select all the order-creation time with the same abnormal umid (**end time**);
1. For each order, select the closest abnormal login time with the same umid (**start time**), with the same time, record the abnormal envdata_utdid;
1. Between the **start time** and **end time**, select the click path with the same abnormal envdata_utdid;
```sql
---- PIPLINE FOR ORDER-CREATE MODEL (ONLY FOCUS ON DIRECT-ATO)
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base1; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base1 LIFECYCLE 30 as

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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base1;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base2; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base2 LIFECYCLE 30 as

SELECT 
a.*,
b.orderid,
b.order_create_time
FROM lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base1 a
left join
(
  SELECT 
  event_id,
  orderid,
  from_unixtime(receive_time/1000) as order_create_time,
  byracctid,
  umid
  from lzd_secods.odl_event_lazada_order_creation_risk_sg
  where substr(ds,1,8) >= '20220201' and substr(ds,1,8) <= '20220620'
)   b
on a.order_buyer_id = b.byracctid and a.abnormal_umid = b.umid
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base2;
-- 10 records do not have corresponding order
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base3; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base3 LIFECYCLE 30 as

SELECT 
a.*,
b.event_id,
b.login_time,
b.envdata_utdid,
datediff(a.order_create_time, b.login_time, 'ss') as date_diff
from 
(
  select 
  order_buyer_id,
  abnormal_umid,
  earliest_abnormal_login,
  orderid,
  max(order_create_time) as order_create_time -- exist case that same orderid has several create time
  from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base2
  where order_create_time >= '2022-01-01 00:00:00'
  group by order_buyer_id, orderid, abnormal_umid, earliest_abnormal_login
)   a
left join 
(
  SELECT distinct
  event_id,
  acctdata_userid,
  umid,
  envdata_utdid,
  from_unixtime(receive_time/1000) as login_time
  FROM lzd_secods.odl_event_async_lazada_login_success
  where substr(ds,1,8) >= '20220201' and substr(ds,1,8) <= '20220620'
)   b
on a.order_buyer_id = b.acctdata_userid and a.abnormal_umid = b.umid
and DATEDIFF(a.order_create_time, b.login_time, 'mi') > 0
and DATEDIFF(a.order_create_time, b.login_time, 'dd') < 5
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base3;

------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4 LIFECYCLE 30 as

SELECT 
b.*
from
(
  select 
  order_buyer_id,
  orderid,
  min(date_diff) as min_date_diff
  from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base3
  group by order_buyer_id, orderid
)   a
left JOIN 
(
  SELECT 
  *
  from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base3
)   b
on a.order_buyer_id = b.order_buyer_id and a.orderid = b.orderid and a.min_date_diff = b.date_diff
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base4;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null LIFECYCLE 30 as

SELECT 
a.order_buyer_id,
a.orderid,
a.order_create_time,
wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
sum(b.page_stay_time) as total_stay_time,
avg(b.page_stay_time) as average_stay_time
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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null LIFECYCLE 30 as

SELECT 
a.order_buyer_id,
a.orderid,
a.order_create_time,
wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
sum(b.page_stay_time) as total_stay_time,
avg(b.page_stay_time) as average_stay_time
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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null LIFECYCLE 30 as

SELECT 
a.order_buyer_id,
a.orderid,
a.order_create_time,
wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
sum(b.page_stay_time) as total_stay_time,
avg(b.page_stay_time) as average_stay_time
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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null;

------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click LIFECYCLE 30 as

select *
from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null
union ALL 
(
  select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null
)
union all
(
  select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null
)
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click;



```

- Totally **_1086_** login records (1 user may correspond to multiple records)
## White samples (0401-0601):
### Pipeline with codes:

1. Find the white samples list;
1. Choose one order record (one way is to choose latest order record);
1. Find the closest login time which is before the order-creation time;
1. Start time: login time; End time: order-creation time;
```
-- WHITE
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base1; 
create table if not exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base1 LIFECYCLE 30 as

select
    a.user_id as order_buyer_id,
    b.orderid,
    b.order_create_time
from
    (
        select *
        from lazada_biz_sec_dev.white_ato_login_sample_v3
        where acsdata_entrance = 'native'
        and umid is not NULL
    )   a
left join
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
on a.user_id = b.byracctid
;
select * from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base1;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base2; 
create table if not exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base2 LIFECYCLE 30 as

select
    a.*,
    b.event_id,
    b.login_time,
    DATEDIFF(a.order_create_time, b.login_time, 'ss') as date_diff
from 
    (
        select * from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base1
    )   a
left join 
    (
        SELECT distinct
            event_id,
            acctdata_userid,
            umid,
            envdata_utdid,
            from_unixtime(receive_time/1000) as login_time
        FROM lzd_secods.odl_event_async_lazada_login_success
        where substr(ds,1,8) >= '20220401' and substr(ds,1,8) <= '20220601'
    )   b
on a.order_buyer_id = b.acctdata_userid
    and DATEDIFF(a.order_create_time, b.login_time, 'mi') > 0
    and DATEDIFF(a.order_create_time, b.login_time, 'dd') < 5
;

select * from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base2;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base3; 
create table if not exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base3 LIFECYCLE 30 as

SELECT 
    b.*
from 
    (
        select 
            order_buyer_id,
            orderid,
            min(date_diff) as min_date_diff
        from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base2
        where event_id is not null
        group by order_buyer_id, orderid
    )   a
left join 
    (
        SELECT 
            *
        from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base2
    )   b
on a.order_buyer_id = b.order_buyer_id and a.orderid = b.orderid and a.min_date_diff = b.date_diff
;

select * from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_base3;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_click; 
create table if not exists lazada_biz_sec_dev.white_ato_order_create_v1_exp1_click LIFECYCLE 30 as
SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as average_stay_time
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

------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.ato_order_create_v1_exp1_click; 
create table if not exists lazada_biz_sec_dev.ato_order_create_v1_exp1_click LIFECYCLE 30 as

select 
    1 as label,
    TO_CHAR(order_buyer_id) as order_buyer_id,
    orderid,
    order_create_time,
    features,
    spam_list,
    total_stay_time,
    average_stay_time
from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click
union ALL 
    (
        select 
            0 as label,
            *
        from lazada_biz_sec_dev.white_ato_order_create_v1_exp1_click
        where features is not null
    )
;

select * from lazada_biz_sec_dev.ato_order_create_v1_exp1_click
limit 1500;

```

- Totally **_10905_** login records;
## Feature:
### Feature list:

- click path embedding;
### Code: [for generating click path]
临时查询 - Jiangyi - order_feature_v1_exp1
```sql
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null LIFECYCLE 30 as

SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as average_stay_time
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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null LIFECYCLE 30 as

SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as average_stay_time
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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null;
------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null LIFECYCLE 30 as

SELECT 
    a.order_buyer_id,
    a.orderid,
    a.order_create_time,
    wm_CONCAT(',',b.spam) within group(order by b.visit_time, b.local_time) as features,
    collect_list(b.spam) within group(order by b.visit_time, b.local_time) as spam_list,
    sum(b.page_stay_time) as total_stay_time,
    avg(b.page_stay_time) as average_stay_time
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

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null;

------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click; 
create table if not exists lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click LIFECYCLE 30 as

select *
from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_fst_null
union ALL 
    (
        select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_null
    )
union all
    (
        select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_base5_scd_not_null
    )
;

select * from lazada_biz_sec_dev.black_ato_order_create_v1_exp1_click;
```
## Experiment result:
[ato_order_create_v1_experiment1.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659691266429-43e307b4-a0c7-4ca3-aac4-6d5e56487adc.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659691266429-43e307b4-a0c7-4ca3-aac4-6d5e56487adc.ipynb%22%2C%22name%22%3A%22ato_order_create_v1_experiment1.ipynb%22%2C%22size%22%3A5083163%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22u5c481e9e-7a36-4b9c-b8c8-5d4ea1f0f3c%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22u9210c5a0%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)
### Setting recall:

1. 10905 white v.s. 1086 black
1. only click path, from closest login time to order create time;
### Performance Metric:
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658212692185-65278d6e-48b8-43c9-bbbd-a7c12b5da592.png#clientId=u24736d55-876e-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=228&id=ue7c8bc0d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=201&originWidth=516&originalType=binary&ratio=1&rotation=0&showTitle=false&size=18326&status=done&style=none&taskId=u7cd6663f-2168-429b-b948-d864e9209e1&title=&width=586)
### Word Embedding PCA:
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658213033454-1f84518c-7c7c-4b42-8eee-7e1e031309ee.png#clientId=u24736d55-876e-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=375&id=u430ca5dc&margin=%5Bobject%20Object%5D&name=image.png&originHeight=750&originWidth=970&originalType=binary&ratio=1&rotation=0&showTitle=false&size=272464&status=done&style=none&taskId=u7bfbab7b-e611-46b9-9de9-766a3161ba2&title=&width=485)
[these 12 principal components constitue 71% of all information (refer to click-path embeddings)]

# Experiment 2 (for native)
## Black and white samples:
The same setting as experiment 1;
## Features:
### Outline:

1. Click-info level (from recent login time to order create time);
- sequence embeddings
   - 512-dimension dense vectors
- statistics features (something like fequency of 'my_account', which is a frequent url in black samples but a realtivley rare url in white samples)
   - develop more **direct** patterns for ATO
      - average time in 'pdp' page, click path length, frequency for 'my_account' page etc;
2. Login-step level;
- time used for second verifcation etc;
3. Order-step level;
- number of different accounts that is logined with the same umid as the order-create one;
- order payment method;
- order product category etc;
4. Info-change level;
- number of info-change over the past 3 days;
- number of reset-password over the past 3 days;
### Feature list:
Click-info level:

| index | feature | remark |
| --- | --- | --- |
|  | buyer_id |  |
|  | order_create_date |  |
|  | labels (black/white) |  |
| 1 | click_path_embedding | 512 dimension vector |
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

Info-change level:

| index | feature | remark |
| --- | --- | --- |
| 15 | no_info_change_3d_same_umid | number of info-change over the past 3 days with the same umid |
| 16 | no_reset_psw_3d_same_umid | similar |

Login-step level:

| index | feature | remark |
| --- | --- | --- |
| 17 | second_verify_time | the time between a) trigger the second verification & b) successful login  |

In this experiment 2, we will take a) click-info level and b) order-info level features into consderation since data issues for the last 2 feature types.
### Code: [combining with generating other statistical features]
临时查询 - Jiangyi - order_feature_v1_exp2
```sql
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
```
## Model result:
[ato_order_create_v1_experiment2.ipynb](https://yuque.antfin.com/attachments/lark/0/2022/ipynb/59656497/1659691415225-449f0dc5-bd72-4ffc-b262-1c9377a65bd4.ipynb?_lake_card=%7B%22src%22%3A%22https%3A%2F%2Fyuque.antfin.com%2Fattachments%2Flark%2F0%2F2022%2Fipynb%2F59656497%2F1659691415225-449f0dc5-bd72-4ffc-b262-1c9377a65bd4.ipynb%22%2C%22name%22%3A%22ato_order_create_v1_experiment2.ipynb%22%2C%22size%22%3A498805%2C%22type%22%3A%22%22%2C%22ext%22%3A%22ipynb%22%2C%22source%22%3A%22%22%2C%22status%22%3A%22done%22%2C%22mode%22%3A%22title%22%2C%22download%22%3Atrue%2C%22taskId%22%3A%22udc753bd7-6e14-4792-a7d9-3c03f1c19a2%22%2C%22taskType%22%3A%22upload%22%2C%22__spacing%22%3A%22both%22%2C%22id%22%3A%22uaaa53459%22%2C%22margin%22%3A%7B%22top%22%3Atrue%2C%22bottom%22%3Atrue%7D%2C%22card%22%3A%22file%22%7D)
### 1) only statistical features (feature 2-14)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658806087391-09a43f1d-06cd-49ea-958a-008f1a40276a.png#clientId=ud053323d-fef8-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=398&id=uf1618ada&margin=%5Bobject%20Object%5D&name=image.png&originHeight=398&originWidth=1030&originalType=binary&ratio=1&rotation=0&showTitle=false&size=44561&status=done&style=none&taskId=u96212ccb-5054-429c-8d16-175674f9a5d&title=&width=1030)
### 2) click embedding + statistical features (feature 1-14)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1658806125771-95420ff5-b28c-41bc-8146-b4d4f81e735d.png#clientId=ud053323d-fef8-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=434&id=ud647c6b1&margin=%5Bobject%20Object%5D&name=image.png&originHeight=434&originWidth=1092&originalType=binary&ratio=1&rotation=0&showTitle=false&size=45620&status=done&style=none&taskId=u5d27a62b-c315-424a-bbba-4aaa585a679&title=&width=1092)
