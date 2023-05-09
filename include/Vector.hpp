#include <math.h>
#pragma once

struct Vector {
    double x;
    double y;

    class TooShort : public std::exception {
    public:
        const char* what() const noexcept override {
            return "Vector is too short.";
        }
    };

    Vector() : x(0), y(0) {}

    Vector(double x, double y) : x(x), y(y) {}

    Vector(const Vector& other) : x(other.x), y(other.y) {}

    Vector operator+(const Vector& other) const {
        return Vector(x + other.x, y + other.y);
    }
    
    Vector& operator+=(const Vector& other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    Vector operator-(const Vector& other) const {
        return Vector(x - other.x, y - other.y);
    }

    Vector scale(double factor) const {
        return Vector(x * factor, y * factor);
    }

    double length() const {
        return std::sqrt(x * x + y * y);
    }

    Vector normalise() const {
        double l = length();
        if (l < 1e-5) {
            throw TooShort();
        }
        return scale(1 / l);
    }

    std::string toString() const {
        return "(" + std::to_string(x) + ", " + std::to_string(y) + ")";
    }

    double dot(const Vector& other) const {
        return x * other.x + y * other.y;
    }

    double cross(const Vector& other) const {
        return x * other.y - y * other.x;
    }

    Vector rotate90CCW() const {
        return Vector(-y, x);
    }

    Vector rotate90CW() const {
        return Vector(y, -x);
    }

    Vector rotate(double theta) const {
        double c = std::cos(theta);
        double s = std::sin(theta);
        return Vector(x * c - y * s, x * s + y * c);
    }

    Vector operator*(double factor) const {
        return Vector(x * factor, y * factor);
    }

    friend Vector operator*(double factor, const Vector& vec) {
        return Vector(vec.x * factor, vec.y * factor);
    }
    
    Vector& operator*=(double factor) {
        x *= factor;
        y *= factor;
        return *this;
    }

    Vector operator/(double factor) const {
        return Vector(x / factor, y / factor);
    }

    friend std::ostream& operator<<(std::ostream& os, const Vector& vec) {
        os << "(" << vec.x << ", " << vec.y << ")";
        return os;
    }
};

