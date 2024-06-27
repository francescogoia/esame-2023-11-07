from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllBrands():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct Product_brand 
            from go_products gp
            order by Product_brand asc
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["Product_brand"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(brand):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select Product_number 
            from go_products gp 
            where Product_brand = %s
        """
        cursor.execute(query, (brand,))
        result = []
        for row in cursor:
            result.append(row["Product_number"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(u, v, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select gds1.Product_number as p1, gds2.Product_number as p2, count(distinct gds1.Retailer_code) as numRivenditori
                from go_daily_sales gds1, go_daily_sales gds2
                where gds1.Product_number = %s and gds2.Product_number = %s
                    and gds1.`Date` = gds2.`Date` and gds1.Retailer_code = gds2.Retailer_code
                    and year(gds1.`Date`) = year(gds2.`Date`) and year(gds1.`Date`) = %s
                """
        try:
            cursor.execute(query, (u, v, anno,))

        except Exception as e:
            print(e)
            cursor.close()
            conn.close()
            return []
        result = []
        for row in cursor:
            result.append((row["p1"], row["p2"], row["numRivenditori"]))
        cursor.close()
        conn.close()
        return result
