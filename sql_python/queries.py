# Диапозон дат таблицы installs
def installs_dates():
    q = """
    select 
    min(toDate(InstallationDate)) as min_date
    ,max(toDate(InstallationDate)) as max_date
    from default.installs 
    """
    return q

# Диапозон дат таблицы events
def events_dates():
    q = """
    select 
    min(toDate(EventDate)) as min_date
    ,max(toDate(EventDate)) as max_date
    from default.events 
    """
    return q

# Диапозон дат таблицы checks
def checks_dates():
    q = """
    select 
    min(toDate(BuyDate)) as min_date
    ,max(toDate(BuyDate)) as max_date
    from default.checks 
    """
    return q    

# 1. Количество установок приложения по платформам
def count_installs_by_platform():
    q= '''
    select 
    Platform
    ,uniq(DeviceID) as cnt
    from default.installs
    group by Platform
    order by cnt
    '''
    return q

# 2.Пришедшие пользователи с какого источника (Source) совершили больше всего покупок
def total_bought_by_source():
    q = '''
    with subquery as (
    select distinct
    checks.Rub as rub
    ,installs.Source as source
    ,devices.DeviceID as device_id
    from checks
    inner join devices
        using(UserID) 
    inner join installs
        on devices.DeviceID = installs.DeviceID
    where checks.Rub > 0
    order by source
    )
    select 
    source
    ,sum(rub) as total_sum
    from subquery
    where source is not null
    group by source
    '''
    return q

# 3. А теперь посмотрим наиболее популярные источники установки, вангую это 27. Но будут ли соотв. источники 9 и 14 покупкам?
def installs_by_source():
    q = """
    select 
    uniq(DeviceID) as installs
    ,Source
    from default.installs
    group by Source
    order by installs desc
    limit 10
    """
    return q

# 4. Повторные покупки пользователей с каких источников делали чаще
def repeat_bought_by_source():
    q = '''
    with subquery as (
    select distinct
    toDate(checks.BuyDate) as buy_date
    ,installs.Source as source
    ,devices.UserID as user_id
    ,row_number() over(partition by user_id
                       order by toDate(checks.BuyDate)) as row_num
    from checks
    inner join devices
        using(UserID) 
    inner join installs
        on devices.DeviceID = installs.DeviceID
    where 1=1
        and checks.Rub > 0
        and installs.Source is not null
    order by user_id, buy_date
    )
    select 
    source
    ,uniq(user_id) as repeat_bought
    from subquery
    where row_num > 1
    group by source
    '''
    return q


# 5. суммы покупок по месяцам в разбивке по ios и android
def purchases_by_monthly():
    q = '''
    select 
    toMonth(toDate(BuyDate)) as buy_monthly
    ,installs.Platform as platform
    ,sum(Rub) as sum_rub
    from default.checks
    left join default.devices
        using(UserID)
    left join default.installs
        on installs.DeviceID = devices.DeviceID
    where installs.Platform in ('iOS', 'android')
    group by buy_monthly, platform
    order by buy_monthly
    '''
    return q


# 6. посмотрим динамику установок приложения по 'ios' и 'android'
def installs_by_monthly():
    q = '''
    select 
    toMonth(toDate(InstallationDate)) as install_date
    ,Platform
    ,uniq(DeviceID) as installs
    from default.installs
    where Platform in ('iOS', 'android')
    group by install_date, Platform
    order by install_date, Platform
    '''
    return q


# 7. Теперь посмотрим сколько пользователей совершило конверсию из установок в просмотры
def conv_by_platform():
    q = '''
    select 
    installs.Platform as platform
    ,count(distinct events.DeviceID) / count(distinct installs.DeviceID) as conv
    from installs 
    left join events
        using(DeviceID)
    group by platform
    '''
    return q
