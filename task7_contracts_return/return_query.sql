DROP TABLE IF EXISTS #Tmp;

SELECT mcc.ClientId, c.ContractID, c.StartDate, c.EndDate
INTO #Tmp
FROM
    [Contract] c
    INNER JOIN mapContractClient mcc ON mcc.ContractID = c.ContractID
WHERE
    c.ContractTypeID IN (1, 2)

UNION ALL

SELECT mcc.ClientId, c.ContractID, s.StartDate, s.EndDate
FROM
    [Contract] c
    INNER JOIN mapContractClient mcc ON mcc.ContractID = c.ContractID
    INNER JOIN mapContractService mcs ON mcs.ContractID = c.ContractID
    INNER JOIN Service s ON s.ServiceID = mcs.ServiceID
WHERE
    c.ContractTypeID IN (3, 4)
;


SELECT
    COUNT(DISTINCT cl.ClientID) count_return
    /*t.ContractId,
    cl.FullName,
    t.StartDate,
    t.EndDate,
    t2.ContractId,
    DATEDIFF(month,    t2.EndDate, t.StartDate) diff,
    t2.EndDate*/
FROM
    #Tmp t
    INNER JOIN Client cl ON cl.ClientID = t.ClientID
    INNER JOIN #Tmp t2 ON t2.ContractID = (
        SELECT TOP 1 t3.ContractID
        FROM #Tmp t3
        WHERE
            t3.ClientID = t.ClientID
            AND t3.ContractId <> t.ContractId
            AND t3.StartDate < t.EndDate
        ORDER BY
            t3.EndDate DESC
    )
WHERE
    DATEDIFF(month, t.StartDate, t2.EndDate) < 6
    AND t.StartDate > t2.EndDate

    -- Сейчас запрос выводит кол-во вернувшихся за все время.
    -- Можно добавить фильтр, чтобы отображались те, у кого сейчас действует договор.
    -- AND t.StartDate <= CAST(GETDATE() AS DATE)
    -- AND t.EndDate > CAST(GETDATE() AS DATE)
;
