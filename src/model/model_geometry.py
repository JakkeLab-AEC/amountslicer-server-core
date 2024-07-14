import math
from typing import List
from abc import ABC, abstractmethod

class GeometryFundamental(ABC):
    @abstractmethod
    def to_string(self) -> str:
        pass

    def __init__(self):
        self.tolerance = 1.0e-3

class Point3d(GeometryFundamental):
    x: float
    y: float
    z: float

    # Constructor
    def __init__(self, x: float, y: float, z: float):
        """
        Initialize a new Point3d object.

        :param x: The x-coordinate of the point.
        :param y: The y-coordinate of the point.
        :param z: The z-coordinate of the point.
        """
        self.x = x
        self.y = y
        self.z = z

    # Methods
    def distance_to(self, point: 'Point3d') -> float:
        """
        Calculate the distance to another Point3d.

        :param point: The other Point3d object.
        :return: The distance to the other point.
        """
        return math.sqrt(
            (self.x - point.x) ** 2 +
            (self.y - point.y) ** 2 +
            (self.z - point.z) ** 2
        )

    def __eq__(self, other: 'Point3d') -> bool:
        """
        Check if this Point3d is equal to another Point3d within the tolerance.

        :param other: The other Point3d object.
        :return: True if the points are equal within the tolerance, False otherwise.
        """
        return (math.isclose(self.x, other.x, abs_tol=self.tolerance) and
                math.isclose(self.y, other.y, abs_tol=self.tolerance) and
                math.isclose(self.z, other.z, abs_tol=self.tolerance))

    # Operators
    def __add__(self, other: 'Vector3d') -> 'Point3d':
        """
        Add a Vector3d to this Point3d.

        :param other: The Vector3d to add.
        :return: A new Point3d object resulting from the addition.
        """
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Point3d') -> 'Vector3d':
        """
        Subtract another Point3d from this Point3d.

        :param other: The Point3d to subtract.
        :return: A new Vector3d object representing the difference.
        """
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    # Converters
    def to_vector3d(self) -> 'Vector3d':
        """
        Convert Point3d to Vector3d with the same coordinates.

        :return: A new Vector3d object with the same coordinates.
        """
        return Vector3d(self.x, self.y, self.z)

    def to_string(self) -> str:
        result = f"X : {self.x}, Y : {self.y}, Z : {self.z}"
        return result

    # Static values
    @classmethod
    def origin(cls) -> 'Point3d':
        """
        Origin Point of global coordinates.

        :return: Point3d object at the origin (0, 0, 0).
        """
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def invalid_point3d(cls) -> 'Point3d':
        """
        Invalid Point3d Object.

        :return: Point3d object with NaN coordinates.
        """
        return cls(math.nan, math.nan, math.nan)
class Vector3d(GeometryFundamental):
    x: float
    y: float
    z: float

    # Constructor
    def __init__(self, x: float, y: float, z: float):
        """
        Initialize a new Vector3d object.

        :param x: The x-coordinate of the vector.
        :param y: The y-coordinate of the vector.
        :param z: The z-coordinate of the vector.
        """
        self.x = x
        self.y = y
        self.z = z

    # Converter
    def to_point3d(self) -> 'Point3d':
        """
        Convert Vector3d to Point3d with the same coordinates.

        :return: A new Point3d object with the same coordinates.
        """
        return Point3d(self.x, self.y, self.z)

    def to_string(self) -> str:
        result = f"X : {self.x}, Y : {self.y}, Z : {self.z}"

    # Operators
    def __add__(self, other: 'Vector3d') -> 'Vector3d':
        """
        Add another Vector3d to this Vector3d.

        :param other: The Vector3d to add.
        :return: A new Vector3d object resulting from the addition.
        """
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3d') -> 'Vector3d':
        """
        Subtract another Vector3d from this Vector3d.

        :param other: The Vector3d to subtract.
        :return: A new Vector3d object resulting from the subtraction.
        """
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3d':
        """
        Multiply this Vector3d by a scalar.

        :param scalar: The scalar to multiply by.
        :return: A new Vector3d object resulting from the multiplication.
        """
        return Vector3d(self.x * scalar, self.y * scalar, self.z * scalar)

    # Methods
    def magnitude(self) -> float:
        """
        Calculate the magnitude (length) of the vector.

        :return: The magnitude of the vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> 'Vector3d':
        """
        Normalize the vector (convert it to a unit vector).

        :return: A new normalized Vector3d object.
        """
        mag = self.magnitude()
        return Vector3d(self.x / mag, self.y / mag, self.z / mag)

    def dot_product(self, other: 'Vector3d') -> float:
        """
        Calculate the dot product with another Vector3d.

        :param other: The other Vector3d object.
        :return: The dot product as a float.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other: 'Vector3d') -> 'Vector3d':
        """
        Calculate the cross product with another Vector3d.

        :param other: The other Vector3d object.
        :return: A new Vector3d object that is the cross product of this and the other vector.
        """
        return Vector3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    # Static values
    @classmethod
    def axis_x(cls) -> 'Vector3d':
        """
        Get the unit vector of the X-axis.

        :return: Vector3d object representing the X-axis unit vector.
        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def axis_y(cls) -> 'Vector3d':
        """
        Get the unit vector of the Y-axis.

        :return: Vector3d object representing the Y-axis unit vector.
        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def axis_z(cls) -> 'Vector3d':
        """
        Get the unit vector of the Z-axis.

        :return: Vector3d object representing the Z-axis unit vector.
        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def invalid_vector3d(cls) -> 'Vector3d':
        """
        Invalid Vector3d Object.

        :return: Vector3d object with NaN coordinates.
        """
        return cls(math.nan, math.nan, math.nan)
class Line(GeometryFundamental):
    """
    Represents a line in 3D space defined by two points.
    """

    def __init__(self, start: Point3d, end: Point3d):
        """
        Initialize a new Line object.

        :param start: The starting Point3d of the line.
        :param end: The ending Point3d of the line.
        """
        self.start = start
        self.end = end

    def length(self) -> float:
        """
        Calculate the length of the line.

        :return: The length of the line.
        """
        return self.start.distance_to(self.end)

    def direction(self) -> Vector3d:
        """
        Calculate the direction vector of the line.

        :return: A Vector3d representing the direction of the line.
        """
        return self.end - self.start

    def midpoint(self) -> Point3d:
        """
        Calculate the midpoint of the line.

        :return: A Point3d representing the midpoint of the line.
        """
        return Point3d(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2,
            (self.start.z + self.end.z) / 2
        )

    def to_string(self) -> str:
        result_start_pt = f"Start : X : {self.start.x}, Y : {self.start.y}, Z : {self.start.z}\n"
        result_end_pt = f"End : X : {self.end.x}, Y : {self.end.y}, Z : {self.end.z}"
        return result_start_pt + result_end_pt
class Polyline(GeometryFundamental):
    """
    Represents a polyline in 3D space defined by a sequence of points.
    """

    def __init__(self, points: List[Point3d]):
        """
        Initialize a new Polyline object.

        :param points: A list of Point3d objects defining the polyline.
        """
        self.points = points
        self.count = len(points)
        if(len(points) > 2 and points[0] == points[-1]):
            self.is_closed = True
        else:
            self.is_closed = False

    def length(self) -> float:
        """
        Calculate the total length of the polyline.

        :return: The total length of the polyline.
        """
        total_length = 0.0
        for i in range(len(self.points) - 1):
            total_length += self.points[i].distance_to(self.points[i + 1])
        return total_length

    def to_string(self) -> str:
        result = ""
        print(self.points)
        for i in range (0, len(self.points)):
            value = f"Point{i} : X : {self.points[i]}, Y : {self.points[i]}, Z : {self.points[i]}"
            result += value
            if i != len(self.points):
                result += '\n'
        return result

    def add_point(self, point: Point3d):
        """
        Add a point to the polyline.

        :param point: The Point3d object to add.
        """
        self.points.append(point)
        self.count += 1

    def point_count(self) -> int:
        """
        Get the number of points in the polyline.

        :return: The number of points in the polyline.
        """
        return len(self.points)
class Circle(GeometryFundamental):
    """
    Represents a circle in 3D space defined by a center point and a radius.
    """

    def __init__(self, center: Point3d, radius: float, normal: Vector3d):
        """
        Initialize a new Circle object.

        :param center: The center Point3d of the circle.
        :param radius: The radius of the circle.
        :param normal: The normal Vector3d defining the plane of the circle.
        """
        self.center = center
        self.radius = radius
        self.normal = normal.normalize()

    def circumference(self) -> float:
        """
        Calculate the circumference of the circle.

        :return: The circumference of the circle.
        """
        return 2 * math.pi * self.radius

    def area(self) -> float:
        """
        Calculate the area of the circle.

        :return: The area of the circle.
        """
        return math.pi * (self.radius ** 2)

    def is_point_on_circle(self, point: Point3d) -> bool:
        """
        Check if a given point lies on the circle.

        :param point: The Point3d object to check.
        :return: True if the point lies on the circle, False otherwise.
        """
        return math.isclose(self.center.distance_to(point), self.radius)
class Rectangle(GeometryFundamental):
    """
    Represents a rectangle in 3D space defined by a center point, width, height, and normal vector.
    """

    def __init__(self, center: Point3d, width: float, height: float, normal: Vector3d):
        """
        Initialize a new Rectangle object.

        :param center: The center Point3d of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.
        :param normal: The normal Vector3d defining the plane of the rectangle.
        """
        self.center = center
        self.width = width
        self.height = height
        self.normal = normal.normalize()

    def area(self) -> float:
        """
        Calculate the area of the rectangle.

        :return: The area of the rectangle.
        """
        return self.width * self.height

    def perimeter(self) -> float:
        """
        Calculate the perimeter of the rectangle.

        :return: The perimeter of the rectangle.
        """
        return 2 * (self.width + self.height)

    def vertices(self) -> list[Point3d]:
        """
        Calculate the vertices of the rectangle.

        :return: A list of Point3d objects representing the vertices of the rectangle.
        """
        half_width_vector = self.normal.cross_product(Vector3d(0, 0, 1)).normalize() * (self.width / 2)
        half_height_vector = self.normal.cross_product(half_width_vector).normalize() * (self.height / 2)

        return [
            self.center + half_width_vector + half_height_vector,
            self.center + half_width_vector - half_height_vector,
            self.center - half_width_vector - half_height_vector,
            self.center - half_width_vector + half_height_vector
        ]

    def to_string(self) -> str:
        result = \
        f"""
        Center - X : {self.center.x} Y : {self.center.y}
        """
        return result
class Arc(GeometryFundamental):
    """
    Represents an arc in 3D space defined by a center point, radius, start angle, end angle, and normal vector.
    """

    def __init__(self, center: Point3d, radius: float, start_angle: float, end_angle: float, normal: Vector3d):
        """
        Initialize a new Arc object.

        :param center: The center Point3d of the arc.
        :param radius: The radius of the arc.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.
        :param normal: The normal Vector3d defining the plane of the arc.
        """
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.normal = normal.normalize()

    def length(self) -> float:
        """
        Calculate the length of the arc.

        :return: The length of the arc.
        """
        return abs(self.end_angle - self.start_angle) * self.radius

    def start_point(self) -> Point3d:
        """
        Calculate the start point of the arc.

        :return: A Point3d object representing the start point of the arc.
        """
        return Point3d(
            self.center.x + self.radius * math.cos(self.start_angle),
            self.center.y + self.radius * math.sin(self.start_angle),
            self.center.z
        )

    def end_point(self) -> Point3d:
        """
        Calculate the end point of the arc.

        :return: A Point3d object representing the end point of the arc.
        """
        return Point3d(
            self.center.x + self.radius * math.cos(self.end_angle),
            self.center.y + self.radius * math.sin(self.end_angle),
            self.center.z
        )
class Ellipse(GeometryFundamental):
    """
    Represents an ellipse in 3D space defined by a center point, major axis, minor axis, and normal vector.
    """

    def __init__(self, center: Point3d, major_axis: float, minor_axis: float, normal: Vector3d):
        """
        Initialize a new Ellipse object.

        :param center: The center Point3d of the ellipse.
        :param major_axis: The length of the major axis of the ellipse.
        :param minor_axis: The length of the minor axis of the ellipse.
        :param normal: The normal Vector3d defining the plane of the ellipse.
        """
        self.center = center
        self.major_axis = major_axis
        self.minor_axis = minor_axis
        self.normal = normal.normalize()

    def area(self) -> float:
        """
        Calculate the area of the ellipse.

        :return: The area of the ellipse.
        """
        return math.pi * self.major_axis * self.minor_axis / 4

    def circumference(self) -> float:
        """
        Calculate the approximate circumference of the ellipse using Ramanujan's formula.

        :return: The approximate circumference of the ellipse.
        """
        a = self.major_axis / 2
        b = self.minor_axis / 2
        h = ((a - b)**2) / ((a + b)**2)
        return math.pi * (a + b) * (1 + (3*h) / (10 + math.sqrt(4 - 3*h)))

    def point_at_angle(self, angle: float) -> Point3d:
        """
        Calculate a point on the ellipse at a given angle.

        :param angle: The angle in radians from the major axis.
        :return: A Point3d object representing the point on the ellipse.
        """
        return Point3d(
            self.center.x + (self.major_axis / 2) * math.cos(angle),
            self.center.y + (self.minor_axis / 2) * math.sin(angle),
            self.center.z
        )
class BoundingBox(GeometryFundamental):
    """
    Represents a 3D bounding box defined by two points: minimum and maximum corners.
    """

    def __init__(self, min_point: Point3d, max_point: Point3d):
        """
        Initialize a new BoundingBox object.

        :param min_point: The minimum corner Point3d of the bounding box.
        :param max_point: The maximum corner Point3d of the bounding box.
        """
        self.min_point = min_point
        self.max_point = max_point

    def volume(self) -> float:
        """
        Calculate the volume of the bounding box.

        :return: The volume of the bounding box.
        """
        return (
            (self.max_point.x - self.min_point.x) *
            (self.max_point.y - self.min_point.y) *
            (self.max_point.z - self.min_point.z)
        )

    def contains(self, point: Point3d) -> bool:
        """
        Check if a given point is inside the bounding box.

        :param point: The Point3d object to check.
        :return: True if the point is inside the bounding box, False otherwise.
        """
        return (
            self.min_point.x <= point.x <= self.max_point.x and
            self.min_point.y <= point.y <= self.max_point.y and
            self.min_point.z <= point.z <= self.max_point.z
        )

    def center(self) -> Point3d:
        """
        Calculate the center point of the bounding box.

        :return: A Point3d object representing the center of the bounding box.
        """
        return Point3d(
            (self.min_point.x + self.max_point.x) / 2,
            (self.min_point.y + self.max_point.y) / 2,
            (self.min_point.z + self.max_point.z) / 2
        )
class Plane(GeometryFundamental):
    """
    Represents a plane in 3D space defined by a point and a normal vector.
    """

    def __init__(self, point: Point3d, normal: Vector3d):
        """
        Initialize a new Plane object.

        :param point: A Point3d object that lies on the plane.
        :param normal: A Vector3d object representing the normal vector of the plane.
        """
        self.point = point
        self.normal = normal.normalize()

    def distance_to(self, point: Point3d) -> float:
        """
        Calculate the shortest distance from a point to the plane.

        :param point: The Point3d object to calculate the distance to.
        :return: The shortest distance from the point to the plane.
        """
        vector_to_point = point - self.point
        return abs(vector_to_point.dot_product(self.normal))

    def project_point(self, point: Point3d) -> Point3d:
        """
        Project a point onto the plane.

        :param point: The Point3d object to project.
        :return: A Point3d object representing the projection of the point onto the plane.
        """
        vector_to_point = point - self.point
        distance = vector_to_point.dot_product(self.normal)
        projection_vector = self.normal * distance
        return point - projection_vector
class Triangle(GeometryFundamental):
    """
    Represents a triangle in 3D space defined by three points.
    """

    def __init__(self, p1: Point3d, p2: Point3d, p3: Point3d):
        """
        Initialize a new Triangle object.

        :param p1: The first vertex Point3d of the triangle.
        :param p2: The second vertex Point3d of the triangle.
        :param p3: The third vertex Point3d of the triangle.
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def area(self) -> float:
        """
        Calculate the area of the triangle.

        :return: The area of the triangle.
        """
        v1 = self.p2 - self.p1
        v2 = self.p3 - self.p1
        cross_product = v1.cross_product(v2)
        return 0.5 * cross_product.magnitude()

    def perimeter(self) -> float:
        """
        Calculate the perimeter of the triangle.

        :return: The perimeter of the triangle.
        """
        return (
            self.p1.distance_to(self.p2) +
            self.p2.distance_to(self.p3) +
            self.p3.distance_to(self.p1)
        )
class Polygon(GeometryFundamental):
    """
    Represents a polygon in 3D space defined by a sequence of points.
    """

    def __init__(self, points: list[Point3d]):
        """
        Initialize a new Polygon object.

        :param points: A list of Point3d objects defining the vertices of the polygon.
        """
        self.points = points

    def area(self) -> float:
        """
        Calculate the area of the polygon assuming it is planar.

        :return: The area of the polygon.
        """
        if len(self.points) < 3:
            return 0.0
        area = 0.0
        for i in range(len(self.points)):
            j = (i + 1) % len(self.points)
            area += self.points[i].x * self.points[j].y
            area -= self.points[j].x * self.points[i].y
        return abs(area) / 2.0

    def perimeter(self) -> float:
        """
        Calculate the perimeter of the polygon.

        :return: The perimeter of the polygon.
        """
        perimeter = 0.0
        for i in range(len(self.points)):
            j = (i + 1) % len(self.points)
            perimeter += self.points[i].distance_to(self.points[j])
        return perimeter
class Sphere(GeometryFundamental):
    """
    Represents a sphere in 3D space defined by a center point and a radius.
    """

    def __init__(self, center: Point3d, radius: float):
        """
        Initialize a new Sphere object.

        :param center: The center Point3d of the sphere.
        :param radius: The radius of the sphere.
        """
        self.center = center
        self.radius = radius

    def volume(self) -> float:
        """
        Calculate the volume of the sphere.

        :return: The volume of the sphere.
        """
        return (4/3) * math.pi * (self.radius ** 3)

    def surface_area(self) -> float:
        """
        Calculate the surface area of the sphere.

        :return: The surface area of the sphere.
        """
        return 4 * math.pi * (self.radius ** 2)

    def contains(self, point: Point3d) -> bool:
        """
        Check if a given point is inside the sphere.

        :param point: The Point3d object to check.
        :return: True if the point is inside the sphere, False otherwise.
        """
        return self.center.distance_to(point) <= self.radius