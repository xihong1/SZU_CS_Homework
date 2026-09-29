
const nodeTypeExplainMap = {
    "Sort": "Sort Node: Sort the record set based on the specified sort key",
    "Unique" : "Deduplication node: De-duplicate the sorted tuples returned from the lower-level nodes",
    "Nested Loop": "Nested Loop: Scan each row of the outer table (m rows), and then connect it with all the records (n rows) in the inner table. The time complexity is: m * n",
    "Hash" : "Generate a hash table from the input record set. The hash is used by Hash Join",
    "Hash Join" : "Connect two record sets by hashing one of the record sets (using hash scan)",
    "Merge Join" : "Merge two record sets by first sorting them on the join key",
    "Aggregate" : "Group records together based on GROUP BY or aggregate functions (such as sum())",
    "HashAggregate" : "Hash Aggregation: Partition the input data into different groups based on a hash algorithm, and then compute the aggregate result for each group. This is suitable for tables with unordered data",
    "Group Aggregate" : "Performs grouping by sorting the data, and then calculates the aggregate results for each group. This method is suitable for tables with ordered data",
    "Seq Scan" : "Continuously scan all data in the actual data access order (often used in the case of no index). When reading from a table, \"Sequential Scan\" (different from \"Index Scan\") performs a single read operation (only reading the table)",
    "Index Scan" : "Scan the index based on the query conditions. Index Scan performs two read operations: first, it reads the index (as the index is ordered, it uses binary search to quickly find the matching index data), and then it reads the actual values from the table",
    "Index Only Scan" : "Also known as Covering Index Scan, it allows obtaining the tuple directly from the index. Covering Index Scan requires that all the data needed by the query can be obtained from the index pages of the same index of the table, without needing to read from the corresponding table",
    "Bitmap Index Scan" : "Use a bitmap index (each page using 1 bit of the index) to locate all relevant pages. The result of this node will be provided to the Bitmap Heap Scan",
    "Bitmap Heap Scan" : "Searches for relevant rows within the pages returned by the Bitmap Index Scan",
    "CTE Scan" : "Sequential Scan of Common Table Expression (CTE) Query Results. Note that the results of the CTE are materialized (computed and temporarily stored, as in the WITH clause)",
    "Subquery Scan" : "Performs a tuple scan on another query plan tree (the subplan) as the object of the scan, and the scanning process is ultimately converted to the execution of the subplan",
    "Limit" : "Returns a specified number of rows from the result set",
    "Parallel Seq Scan" : "Finds relevant records by sequentially scanning the input record set. When reading from the table, the \"sequential scan\" (as opposed to an \"index scan\") performs a single read operation (reading only the table)",
    "Function Scan" : "Executes a function to generate the query result set",
    "Foreign Scan" : "Performs a scanning operation on an external data source (an external data wrapper or a Foreign Data Wrapper (FDW) or dblink) to read and process external data",
    // 其他情况的处理
    "default" : ""
};

/**
 * 返回nodeType对应的中文释义
 * @param nodeType
 * @returns {*|string}
 */
function nodeTypeExplain(nodeType) {
    return nodeTypeExplainMap[nodeType] || nodeTypeExplainMap["default"];
}