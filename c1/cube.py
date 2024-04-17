import numpy as np


class Cube:
    def __init__(self):
        self.nodes = np.zeros((0, 4))
        self.edges = []

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_edges(self, edges):
        self.edges = edges

    def translate(self, dx, dy, dz):
        translation_matrix = np.eye(4)
        translation_matrix[-1][:3] = dx, dy, dz
        self.nodes = self.nodes @ translation_matrix

    def rotate(self, radians, axis):
        sin = np.sin(radians)
        cos = np.cos(radians)
        rotation_matrix = np.eye(4)
        if axis == "x":
            rotation_matrix[1:3, 1:3] = np.array([cos, -sin, sin, cos]).reshape(2, 2)
        elif axis == "y":
            rotation_matrix[0, 0] = cos
            rotation_matrix[2, 0] = sin
            rotation_matrix[0, 2] = -sin
            rotation_matrix[2, 2] = cos
        elif axis == "z":
            rotation_matrix[0:2, 0:2] = np.array([cos, -sin, sin, cos]).reshape(2, 2)
        self.nodes = self.nodes @ rotation_matrix

    def get_2d_edges(self, focal):
        coordinates = self.get_nodes()
        points_2d = np.array(
            [node[:2] * focal / max(node[2], 0.001) for node in coordinates]
        )

        edges = []
        for edge in self.get_edges():
            idx1, idx2 = edge
            point1, point2 = coordinates[idx1], coordinates[idx2]

            if point1[2] > 0 and point2[2] > 0:
                edges.append(np.hstack((points_2d[idx1], points_2d[idx2])))
            elif point1[2] <= 0 and point2[2] <= 0:
                continue
            else:
                t = -point1[2] / (point2[2] - point1[2])
                x = point1[0] + t * (point2[0] - point1[0])
                y = point1[1] + t * (point2[1] - point1[1])
                z = 0.001
                interpolated_point = [x * focal / z, y * focal / z]
                visible_point = points_2d[idx2] if point1[2] <= 0 else points_2d[idx1]

                edges.append(np.hstack((interpolated_point, visible_point)))

        return np.array(edges)

    def read(file_name):
        with open(file_name, "r") as file:
            lines = file.readlines()

        nodes = np.empty((0, 4), dtype=float)
        edges = np.empty((0, 2), dtype=int)

        for line in lines:
            points = np.fromstring(line, sep=", ", dtype=float)
            start, end = points[:3], points[3:]

            for point in (start, end):
                point_with_one = np.append(point, 1)
                exists = np.all(nodes[:, :3] == point, axis=1).any()
                if not exists:
                    nodes = np.vstack((nodes, point_with_one))

            start_idx = np.where(np.all(nodes[:, :3] == start, axis=1))[0][0]
            end_idx = np.where(np.all(nodes[:, :3] == end, axis=1))[0][0]

            edges = np.vstack((edges, [start_idx, end_idx]))

        cube = Cube()
        cube.set_nodes(nodes)
        cube.set_edges(edges)
        return cube
