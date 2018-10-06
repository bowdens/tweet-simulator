class Graph(object):
    def __init__(self):
        self.__size = 0
        self.__matrix = []
        self.__verticies = []

    @property
    def verticies(self):
        return self.__verticies

    @property
    def matrix(self):
        return self.__matrix

    @property
    def size(self):
        return self.__size

    def add_vertex(self,vertex):
        if self.is_vertex(vertex):
            raise ValueError("Vertex already in graph")
        self.__verticies.append(vertex)
        for m in self.__matrix:
            m.append(0)
        self.__matrix.append([])
        self.__size += 1
        for i in range(0, self.__size):
            self.__matrix[self.__size-1].append(0)

    def is_vertex(self,vertex):
        return vertex in self.__verticies

    def vertex_index(self,vertex):
        if not self.is_vertex(vertex):
            raise ValueError("Vertex not in graph")
        return self.__verticies.index(vertex)

    def set_edge(self,v1, v2, edge):
        self.__matrix[self.vertex_index(v1)][self.vertex_index(v2)] = edge

    def get_edge(self,v1, v2):
        return self.__matrix[self.vertex_index(v1)][self.vertex_index(v2)]

    def increment_edge(self, v1, v2):
        self.set_edge(v1, v2, self.get_edge(v1, v2) + 1)

    def __str__(self):
        rstr = ""
        count = 0
        for vertex in self.__verticies:
            rstr += "{}: {}\n".format(count, vertex)
            count += 1

        i = 0
        for m in self.__matrix:
            rstr += "{}: {}".format(self.__verticies[i],str(m))
            if m is not self.__matrix[-1:][0]:
                rstr += "\n"
            i+=1

        return rstr


