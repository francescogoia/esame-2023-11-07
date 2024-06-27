from database.DB_connect import DBConnect
from model.squadra import Squadra


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select distinct `year` 
            from appearances a 
            where `year` >= 1980
            order by `year` desc
                """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllTeams(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select t.teamCode, t.ID , t.name  , sum(s.salary) as salarioSquadra
            from salaries s, teams t, appearances a 
            where t.`year` = %s and s.`year` = t.`year`
                and a.`year` = t.`year`
                and t.ID = a.teamID 
                and a.playerID = s.playerID 
            group by t.teamCode, t.name
        """
        cursor.execute(query, (anno, ))
        result = []
        for row in cursor:
            result.append(Squadra(**row))
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
