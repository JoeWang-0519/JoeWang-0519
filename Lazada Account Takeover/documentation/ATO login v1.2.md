In this version, we apply the black and white samples as before. We re-fine the feature list.
# 1. Feature Setting
## a. Feature List
Abnormal environment difference: 

| index | feature | remark | chinese |
| --- | --- | --- | --- |
|  | buyer_id |  |  |
|  | login_date |  |  |
|  | labels (black/white) |  |  |
| 1 | no_unique_umid_14d |  | 过去14天登陆不同umid个数 |
| 2 | no_unique_ip2_14d |  | 过去14天登陆不同ip2个数 |
| 3 | no_unique_ipisp_14d |  | 类似 |
| 4 | id_new_umid_14d | indicator of new umid (14d) | 相比过去14天的登陆记录，此次登陆是否是新umid |
| 5 | id_new_ip2_14d |  | 类似 |
| 6 | id_new_ipisp_14d |  | 类似 |
| 7 | id_is_auto | logintype | 此次登陆方式为自动登录 |

Order info features:

| index | feature | remark |  |
| --- | --- | --- | --- |
| 8 | id_umid_same_seller_14d | indicator of same device with some ordered sellers | 在过去14天订单对应的卖家列表中，检查umid是否与此次登陆umid有重合 |
| 9 | id_ip2_same_seller_14d |  | 类似 |
| 10 | avg_price_per_order_14d |  | 过去14天订单平均价格 |
| 11 | std_price_per_order_14d |  | 标准差 |
| 12 | avg_dscnt_**rate**_per_order_14d |  | 过去14天订单平均折扣率 |
| 13 | std_dscnt_**rate**_per_order_14d |  | 标准差 |
| 14 | avg_shpfee_per_order_14d |  | 过去14天订单平均运费价格 |
| 15 | std_shpfee_per_order_14d |  | 标准差 |
| 16 | id_susp_paymethod_14d | indicator of suspicious payment method over past 14 days (VA/OTC) | 过去14天订单是否存在可疑（可获利）支付方式（VA/OTC） |

Login cluster features:

| index | feature | remark |  |
| --- | --- | --- | --- |
| 17 | no_acct_umid_14d | number of different accounts for the same umid (14d) | 此次登陆umid在过去14天中，登录不同账号个数 |

Sellers' side features:

| index | feature | remark |  |
| --- | --- | --- | --- |
| 18 | max_cancel_rate_14d | maximum of cancel rate for sellers over past 14d | 过去14天订单对应卖家的最高订单取消率 |
| 19 | max_avg_price_seller_14d | maximum of average price (from 0201 to 0601) for sellers over past 14d  | 过去14天订单对应卖家的最高订单平均价格 |
| 20 | max_avg_dscnt_rate_seller_14d |  | 类似 |
| 21 | max_avg_shpfee_seller_14d |  | 类似 |

Device indicators: 

| index | feature | remark |
| --- | --- | --- |
| 22 | id_susp_device | 此次登陆为可疑设备登陆 |

## b. Pipline
```
----------------------------------------------------------------------------------------------------------------------------------
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_v1;
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_v1 LIFECYCLE 30 as

select 
    a.order_buyer_id as buyer_id,
    a.earliest_abnormal_login as current_login_time,
    a.abnormal_umid as current_umid,
    concat(split_part(a.ip,'.',1), split_part(a.ip,'.',2)) as current_ip2, --可以调整成ip1字段和ip2字段
    a.ipparse_ipisp as current_ipisp,
    a.ipparse_ipprovname as current_ipprovname,
    a.logindata_logintype as current_logintype,
    b.is_suspicious
from lazada_biz_sec_dev.black_ato_login_sample  a
left join
    (
        select distinct
            acctdata_userid,
            FROM_UNIXTIME(receive_time/1000) as previous_login_time,
            case
                when (wuadecrydata_bit1reserve4 = '1'  or wuadecrydata_pkguncrypted = '1' or substr(wuadecrydata_wuauadecryptionstr, locate('stgyroot', wuadecrydata_wuauadecryptionstr) + 10, 1) = '1') = true
                then 1 else 0 
            end as is_suspicious
        from lzd_secods.odl_event_async_lazada_login_success
        where SUBSTR(ds,1,8) >= '20220101' and SUBSTR(ds,1,8) <= '20220601'
        and acsdata_cntry = 'id'
        and otherdata_issucc = 'true'
        and acctdata_bizrole = 'byr'  
    )   b
on a.order_buyer_id = b.acctdata_userid and a.earliest_abnormal_login = b.previous_login_time
;

----------------------------------------------------------------------------------------------------------------------------------

-- Combine with previsou 14 days login records
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_v1; -- basic_info_full_login
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_v1 LIFECYCLE 60 as

select 
    a.*,
    b.previous_login_time,
    b.previous_umid,
    b.previous_ip2,
    b.previous_ipisp,
    b.previous_ipprovname
from lazada_biz_sec_dev.black_ato_login_sample_basic_info_v1   a
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
on a.buyer_id = b.acctdata_userid and a.current_login_time > b.previous_login_time and DATEDIFF(a.current_login_time, b.previous_login_time, 'dd') <= 14
;


----------------------------------------------------------------------------------------------------------------------------------
-- environment features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_env_v1;
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_env_v1 LIFECYCLE 60 as

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
    end as id_new_ipisp_14d,
    case
        when current_logintype = 'auto' then '1' else '0'
    end as id_is_auto,
    is_suspicious as id_is_suspicious
FROM 
    (
        select 
            buyer_id, 
            current_login_time, 
            current_umid, current_ip2, 
            current_ipisp, 
            current_ipprovname,
            current_logintype,
            is_suspicious,
            count(distinct previous_umid) as no_unique_umid_14d,
            count(distinct previous_ip2) as no_unique_ip2_14d,
            count(distinct previous_ipisp) as no_unique_ipisp_14d,
            COLLECT_LIST(distinct previous_umid) as list_previous_umid_14d,
            COLLECT_LIST(distinct previous_ip2) as list_previous_ip2_14d,
            COLLECT_LIST(distinct previous_ipisp) as list_previous_ipisp_14d

        from lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_v1
        group by buyer_id, current_login_time, current_umid, current_ip2, current_ipisp, current_ipprovname, current_logintype, is_suspicious
    )
;


----------------------------------------------------------------------------------------------------------------------------------
-- buyers corresponding previous sellers (14d) and their order records
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order_seller_v1; 
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order_seller_v1 LIFECYCLE 60 as


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
        select DISTINCT 
            buyer_id,
            current_login_time,
            current_umid,
            current_ip2,
            current_ipisp,
            current_ipprovname,
            seller_id
        from lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order 
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
        WHERE ds >= '20220201' and ds <= '20220601'
        and venture = 'ID'
    )   b
on a.seller_id = b.seller_id
;

----------------------------------------------------------------------------------------------------------------------------------
-- seller sides features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_seller_v1; 
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_seller_v1 LIFECYCLE 60 as

select 
    a.*,
    b.max_avg_price_seller_14d,
    b.max_avg_dscnt_rate_seller_14d,
    b.max_avg_shpfee_seller_14d
from 
    (   
        SELECT 
            buyer_id,
            max(total_cancel_number/total_order_number) as max_cancel_rate_14d
        from
            (
                SELECT 
                    buyer_id,
                    seller_id,
                    count(sales_order_id) as total_order_number,
                    sum(seller_order_status) as total_cancel_number
                FROM 
                    (
                        SELECT distinct
                            buyer_id,
                            seller_id,
                            sales_order_id,
                            case when seller_order_status = '5.Cancellation' then '1' else '0' end as seller_order_status
                        from lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order_seller_v1
                    )
                    group by buyer_id, seller_id
            )
            group by buyer_id
    )   a

left JOIN 
    (
        SELECT 
            buyer_id,
            max(avg_price_seller_14d) as max_avg_price_seller_14d,
            max(avg_dscnt_rate_seller_14d) as max_avg_dscnt_rate_seller_14d,
            max(avg_shpfee_seller_14d) as max_avg_shpfee_seller_14d
        FROM 
            (
                SELECT 
                    buyer_id,
                    seller_id,
                    avg(seller_paid_price) as avg_price_seller_14d,
                    avg((seller_list_price-seller_paid_price)/seller_list_price) as avg_dscnt_rate_seller_14d,
                    avg(seller_shipping_amount_total) as avg_shpfee_seller_14d
                FROM 
                    (
                        SELECT distinct
                            buyer_id,
                            seller_id,
                            seller_list_price,
                            seller_unit_price,
                            seller_paid_price,
                            seller_shipping_amount_total
                        from lazada_biz_sec_dev.black_ato_login_sample_basic_info_full_order_seller_v1
                    )
                group by buyer_id, seller_id
            )
            group by buyer_id
    )   b
on a.buyer_id = b.buyer_id
;


----------------------------------------------------------------------------------------------------------------------------------
-- Order info features
SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_order_v1; -- feature_order
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_order_v1 LIFECYCLE 60 as

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
            avg((list_price_order - paid_price_order)/list_price_order) as avg_dscnt_rate_per_order_14d,
            stddev((list_price_order - paid_price_order)/list_price_order) as std_dscnt_rate_per_order_14d,
            avg(shipping_fee_order) as avg_shpfee_per_order_14d,
            stddev(shipping_fee_order) as std_shpfee_per_order_14d,
            max(is_susp_paymethod_flag) as is_susp_paymethod_14d
        FROM 
            (
                select
                    *,
                    case when (payment_method like '%VA%') or (payment_method like '%OTC%') then '1' else '0'
                    end as is_susp_paymethod_flag
                from lazada_biz_sec_dev.black_ato_login_sample_basic_info_order
            )
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

----------------------------------------------------------------------------------------------------------------------------------
-- Final features


SET odps.instance.priority = 0;
drop table if exists lazada_biz_sec_dev.black_ato_login_sample_feature_v1; 
create table if not exists lazada_biz_sec_dev.black_ato_login_sample_feature_v1 LIFECYCLE 60 as

SELECT 
    to_char(a.buyer_id) as buyer_id,
    1 as label, -- black sample
    a.no_unique_umid_14d,
    a.no_unique_ip2_14d,
    a.no_unique_ipisp_14d,
    a.id_new_umid_14d,
    a.id_new_ip2_14d,
    a.id_new_ipisp_14d,
    a.id_is_auto,
    b.id_umid_same_seller_14d,
    b.id_ip2_same_seller_14d,
    b.avg_price_per_order_14d,
    b.std_price_per_order_14d,
    b.avg_dscnt_rate_per_order_14d,
    b.std_dscnt_rate_per_order_14d,
    b.avg_shpfee_per_order_14d,
    b.std_shpfee_per_order_14d,
    b.is_susp_paymethod_14d as id_susp_paymethod_14d,
    c.no_acct_umid_14d,
    d.max_cancel_rate_14d,
    d.max_avg_price_seller_14d,
    d.max_avg_dscnt_rate_seller_14d,
    d.max_avg_shpfee_seller_14d,
    a.id_is_suspicious as id_susp_device

FROM 
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_env_v1
    )   a

left join
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_order_v1
    )   b
on a.buyer_id = b.buyer_id

left join 
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_cluster 
    )   c
on a.buyer_id = c.buyer_id

left JOIN 
    (
        select * from lazada_biz_sec_dev.black_ato_login_sample_feature_seller_v1
    )   d
on a.buyer_id = d.buyer_id
;



```
# 2. Model
_**-XGBoost**_

- The best parameter is：
   - best estimator: { colsample_bytree : 0.8 gamma : 0.5 max_depth : 3 min_child_weight : 1 random_state : 0 subsample : 1.0 use_label_encoder : False verbosity : 0 }
- Performance Metric:

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655951600237-149a3708-f6a6-4eb1-a7d0-4020cb01bc06.png#clientId=u7bf9a6f0-aa75-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=255&id=ua4c29a5f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=510&originWidth=750&originalType=binary&ratio=1&rotation=0&showTitle=false&size=133205&status=done&style=none&taskId=uc6a3d590-0d45-4baa-a259-06d898ca18c&title=&width=375)
![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655951612069-0061c139-1ccd-4570-878b-a0003c1afa38.png#clientId=u7bf9a6f0-aa75-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=247&id=u64552c8a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=494&originWidth=812&originalType=binary&ratio=1&rotation=0&showTitle=false&size=132848&status=done&style=none&taskId=u1e2a488b-14c2-41b3-b7c0-14882767d5f&title=&width=406)

- Feature importance

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655952315136-d66f5d96-2b8f-47ce-8f68-8e948c8eb7d0.png#clientId=u7bf9a6f0-aa75-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=400&id=u5070e768&margin=%5Bobject%20Object%5D&name=image.png&originHeight=800&originWidth=862&originalType=binary&ratio=1&rotation=0&showTitle=false&size=323299&status=done&style=none&taskId=ub0818c3d-417e-4813-8b02-bf70dff07f4&title=&width=431)

- Shapley Value

![image.png](https://intranetproxy.alipay.com/skylark/lark/0/2022/png/59656497/1655952411786-eff1a77e-6e9f-416a-b326-d774afa6572d.png#clientId=u7bf9a6f0-aa75-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=306&id=u369ec947&margin=%5Bobject%20Object%5D&name=image.png&originHeight=611&originWidth=755&originalType=binary&ratio=1&rotation=0&showTitle=false&size=69661&status=done&style=none&taskId=u78b567dd-9c32-47de-ab3f-11eeebb71a7&title=&width=377.5)

In our first step (login step), what we want to do is to block those "very black" abnormal login. Therefore, our aim is to extremely high precision and an acceptable recall.

   - If our aim is maximum f1-score, the optimal threshold is 0.59;
   - If our aim is nearly 1 precision rate and a good recall rate, the optimal threshold should be **_0.84_**. In this case, we can achieve 0.99 precision rate and 0.94 recall rate.
# [*]. Notation
New temp tables compared with previous version (v0):

1. white_ato_login_sample_basic_info: abnormal/normal login information tablel (**along with suspicious device information**);
1. white_ato_login_sample_feature_env: environment features (**include suspicious device indicator and auto login indicator**);
1. white_ato_login_sample_basic_info_full_order_seller: previous 14d seller and their corresponding order records from 0201-0601 table (product-level);
1. white_ato_login_sample_feature_seller: seller side features;
1. white_ato_login_sample_feature_order: order features (**include suspicious payment method indicator**);

