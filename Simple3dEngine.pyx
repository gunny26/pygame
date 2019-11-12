#!/usr/bin/python3
# cython: language_level=3, boundscheck=False
"""
simple 3d engine written in pure python and pygame for graphics display

this attempt has educational focus, i fo not think it will be anywhere
near as fast as compiled optimized versions or GPU based versions.

the main goal is:
    how do 3D Engines work
    projection / shading / depth buffer (kind-of) / clipping
    what can be optimize algorithmically (matrices)
    what can be optimized with python (cython?, numpy?)

lets see how far we get

first version - projection, triangles
second version - shading, loading of obj files, refactoring
third version - refactoring, texture
"""
# non std

cdef extern from "math.h":
    double sin(double x)

cdef extern from "math.h":
    double cos(double x)

cdef extern from "math.h":
    double sqrt(double x)


cdef class Vec4d:

    cdef public double x
    cdef public double y
    cdef public double z
    cdef public double w
    cdef public double data[4]

    def __init__(self, double x, double y, double z, double w=0.0):
    # also store list of values):
        """
        vector in 3 dimensional space, additional w component
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        # also store list of values
        self.data = [self.x, self.y, self.z, self.w]

    def __add__(self, other):
        return Vec4d(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
            )

    def __sub__(self, other):
        return Vec4d(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w
            )

    def __getitem__(self, index):
        return self.data[index]

    def __div__(self, double factor):
        return Vec4d(self.x / factor, self.y / factor, self.z / factor, self.w / factor)

    cdef double length(self):
        """
        return length of verctor, including w part
        """
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)

    cpdef Vec4d cross(self, Vec4d other):
        """
        return the cross product of self and other as Vec4d
        :returns Vec4d:
        """
        cdef Vec4d ret
        ret = Vec4d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
            )
        return ret

    cpdef Vec4d normalize(self):
        """
        return normalized version of Vec4d
        :returns Vec4d:
        """
        length = self.length()
        return Vec4d(self.x / length, self.y / length, self.z / length, self.w / length)

    cpdef double dot(self, Vec4d other):
        """
        return dot product of self and ohter Vec4d
        TODO: what todo with this w component?
        :returns float:
        """
        return self.x * other.x + self.y * other.y + self.z * other.z


cdef class Triangle:

    cdef public Vec4d v1
    cdef public Vec4d v2
    cdef public Vec4d v3
    cdef public points

    def __init__(self, Vec4d v1, Vec4d v2, Vec4d v3):
        """
        :params v1 <Vec4d>: first vertex
        :params v2 <Vec4d>: second vertex
        :params v3 <Vec4d>: third vertex
        """
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.points = [v1, v2, v3]

    def __getitem__(self, index):
        return self.points[index]

    def __mul__(self, matrix):
        """
        multiply self with matrix, must be 4 x 4
        :params Matrix4x4:
        :return Triangle:
        """
        return Triangle(*[
            matrix * self.v1,
            matrix * self.v2,
            matrix * self.v3
        ])

    def __lt__(self, other):
        """
        compare self with other, use in painters algorithm
        """
        return self.avg_z() > other.avg_z()

    def __gt__(self, other):
        """
        compare self with other, use in painters algorithm
        """
        return self.avg_z() < other.avg_z()

    cpdef double avg_z(self):
        """
        return average z of triangle
        :returns double:
        """
        return (self.v1.z + self.v2.z + self.v3.z) / 3

    cpdef Vec4d normal(self):
        """
        return normal vector fr this triangle
        :returns Vec4d:
        """
        return ((self.v2 - self.v1).cross(self.v3 - self.v1)).normalize()

    cpdef Triangle translate(self, Vec4d vec4d):
        """
        translate this triangle
        :params vec4d:
        :returns Triangle:
        """
        return Triangle(*[
            self.v1 + vec4d,
            self.v2 + vec4d,
            self.v3 + vec4d
        ])


class Mesh:

    def __init__(self, triangles):
        self.triangles = triangles

    def __str__(self):
        return(f"mesh consists of {len(self.triangles)}")

    def __getitem__(self, index):
        return self.triangles[index]

    @staticmethod
    def from_file(filename):
        with open(filename, "rt") as infile:
            vertices = []
            triangles = []
            for line in infile:
                if not line or line[0] == "#":
                    continue
                parts = line.strip().split()
                if not parts:
                    continue
                if parts[0] == "v": # a vertex
                    # something like: v -1.000000 -1.000000 -1.000000
                    vertices.append(Vec4d(*[float(part) for part in parts[1:]]))
                if parts[0] == "f": # a face
                    # something like: f 2/1/1 3/2/1 4/3/1
                    t_vertices = [int(part.split("/")[0])-1 for part in parts[1:]]
                    triangles.append(Triangle(vertices[t_vertices[0]], vertices[t_vertices[1]], vertices[t_vertices[2]]))
            return Mesh(triangles)

cdef class Matrix4x4:
    """Helper class for matrix operations"""


    cdef public double vecs[4][4]

    def __init__(self, vecs):
        """
        :params vecs list of 4 Vec4d:
        """
        self.vecs = vecs

    def __str__(self):
        output = ""
        #for vec in self.vecs:
        #    output += "| " + " | ".join((f"{value:22}" for value in vec)) + " |\n"
        return output

    def __getitem__(self, index):
        return self.vecs[index]

    def __setitem__(self, index, value):
        print(index)

    def __mul__(self, vec3d):
        """
        multiply this matrix by vector 4D, and divide it by w component if w>0.0
        :params <Vec4d>: input vector to multiply with this matrix
        :returns <Vec4d>: new vector
        """
        vec4d = Vec4d(*[
            vec3d.x * self.vecs[0][0] + vec3d.y * self.vecs[1][0] + vec3d.z * self.vecs[2][0] + self.vecs[3][0], # x
            vec3d.x * self.vecs[0][1] + vec3d.y * self.vecs[1][1] + vec3d.z * self.vecs[2][1] + self.vecs[3][1], # y
            vec3d.x * self.vecs[0][2] + vec3d.y * self.vecs[1][2] + vec3d.z * self.vecs[2][2] + self.vecs[3][2], # z
            vec3d.x * self.vecs[0][3] + vec3d.y * self.vecs[1][3] + vec3d.z * self.vecs[2][3] + self.vecs[3][3]  # w
        ])
        if vec4d.w != 0.0:
            vec4d.x /= vec4d.w
            vec4d.y /= vec4d.w
            vec4d.z /= vec4d.w
        return vec4d

    def mul_matrix(self, other):
        """
        multiply self by Matrix4x4

        |a11 a12 a13 a14|   |b11 b12 b13 b14|   |(a11*b11+a12*b21+a13*b31+a14*b41) ...
        |a21 a22 a23 a24| * |b21 b22 b23 b24| =
        |a31 a32 a33 a34|   |b31 b32 b33 b34|
        |a41 a42 a43 a44|   |b41 b42 b43 b44|

        :params other <Matrix4x4>: Matrix B in A * B
        :returns <Matrix4x4>:
        """
        ret = Matrix4x4.get_zero() # get zero matrix
        for row in (0, 1, 2, 3):
            for col in (0, 1, 2, 3):
                for row2 in (0, 1, 2, 3):
                    ret[row][col] = ret[row][col] + self[row][row2] * other[row2][col]
        return ret

    @staticmethod
    def get_zero():
        """
        get zero matrix
        :returns <Matrix4x4>:
        """
        return Matrix4x4([
            [ 0, 0, 0, 0 ],
            [ 0, 0, 0, 0 ],
            [ 0, 0, 0, 0 ],
            [ 0, 0, 0, 0 ]
        ])

    @staticmethod
    def get_identity():
        """
        get identity matrix
        :returns <Matrix4x4>:
        """
        return Matrix4x4([
            [ 1, 0, 0, 0 ],
            [ 0, 1, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ 0, 0, 0, 1 ]
        ])

    @staticmethod
    def get_rot_x(double f_theta):
        """
        get rotation matrix around x
        :params f_theta <float>:
        :returns <Matrix4x4>:
        """
        return Matrix4x4([
            [ 1,                 0,                  0, 0 ],
            [ 0, cos(f_theta), -sin(f_theta), 0 ],
            [ 0, sin(f_theta),  cos(f_theta), 0 ],
            [ 0,                 0,                  0, 1 ]
        ])

    @staticmethod
    def get_rot_y(double f_theta):
        """
        get rotation matrix around y
        :params f_theta <float>:
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [  cos(f_theta), 0, sin(f_theta), 0 ],
            [                  0, 1,                 0, 0 ],
            [ -sin(f_theta), 0, cos(f_theta), 0 ],
            [                  0, 0,                 0, 1 ]
        ])

    @staticmethod
    def get_rot_z(double f_theta):
        """
        get rotation matrix around z
        :params f_theta <float>:
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [ cos(f_theta), -sin(f_theta), 0, 0 ],
            [ sin(f_theta),  cos(f_theta), 0, 0 ],
            [                 0,                  0, 1, 0 ],
            [                 0,                  0, 0, 1 ]
        ])

    @staticmethod
    def get_translate(vec):
        """
        get translation matrix from given Vec4d, w must be 1
        TODO: not sure if this correct
        :params f_theta <float>:
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [ 1, 0, 0, 0 ],
            [ 0, 1, 0, 0 ],
            [ 0, 0, 1, 0 ],
            [ vec[0], vec[1], vec[2], 1 ]
        ])

    @staticmethod
    def get_projection(double aspect, double fov, double q, double z_near=0.1):
        """
        return projection matrix
        :params aspect <float>: aspect ratiion height/width
        :params fov <float>: field of view 1 / tan(theta/2))
        :params q <float>: z_far / (z_far - z_near)
        :params znear <float>: z_near value, defaults 0.1
        :returns <Matrix4x4:
        """
        return Matrix4x4([
            [ aspect * fov, 0  , 0          , 0],
            [ 0           , fov, 0          , 0],
            [ 0           , 0  , q          , 1],
            [ 0           , 0  , -z_near * q, 0]
        ])
