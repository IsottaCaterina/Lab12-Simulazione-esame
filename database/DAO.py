from database.DB_connect import DBConnect
from model.actor import Actor
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllVoti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = '''select  distinct r.avg_rating as voto
                        from ratings r 
                        order by r.avg_rating '''

        cursor.execute(query)

        for row in cursor:
            results.append(row['voto'])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(voto1, voto2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = '''select n.*
                    from ratings r , movie m , role_mapping rm , names n 
                    where r.movie_id =m.id and m.id =rm.movie_id and rm.name_id =n.id and n.date_of_birth is not null 
                    and r.avg_rating between %s and %s
                    group by n.id 
                    order by n.name '''

        cursor.execute(query, (voto1, voto2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(voto1, voto2, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = '''select rm1.name_id as Actor1, rm2.name_id as Actor2, sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as Peso
                    from movie m, role_mapping rm1, role_mapping rm2, ratings r, names n1, names n2
                    where m.id = rm1.movie_id
                    and m.id = rm2.movie_id
                    and m.id = r.movie_id
                    and rm1.name_id = n1.id
                    and rm2.name_id = n2.id
                    and n1.date_of_birth IS NOT NULL
                    and n2.date_of_birth IS NOT NULL
                    and rm1.name_id < rm2.name_id
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and m.worlwide_gross_income is not null
                    and m.worlwide_gross_income like '$%'
                    group by rm1.name_id, rm2.name_id'''

        cursor.execute(query,(voto1, voto2))

        for row in cursor:
            results.append(Arco(idMap[row['Actor1']],idMap[row['Actor2']],row['Peso']))

        cursor.close()
        conn.close()
        return results



