import DivideProblem

# Nie mam pojecia, dlaczego nie chce to normalnie dzialac.
# Ten sposob dziala.

mes = DivideProblem.CreateFromDocument(open('DivideProblem.xml').read())

mes.ProblemType="TSP"
mes.Id = 12

s = "Tekst"

mes.Data = s.encode("ascii")
mes.ComputationalNodes = 16
mes.NodeId = 7

mes.toxml('utf-8')
