#include "Vector.hpp"
#include <SFML/Graphics.hpp>
#include <iostream>
#pragma once

class Node : public sf::Drawable {
 public:
    double m = 1;
    Vector p = {0, 0};
    Vector v = {0, 0};
    Vector f = {0, 0};
    double J = 1;
    double θ = 0;
    double ω = 0;
    double τ = 0;

    static constexpr double r = 0.01;

    Node() : Node(Vector(0, 0)) { }
    
    Node(Vector p_) : p(p_) {
        _shape.setRadius(r);
        _shape.setFillColor(sf::Color::Blue);
        _shape.setOrigin(r, r);
    }

    void Reset() {
        f = Vector(0, 0);
        τ = 0;
    }

    void ApplyForce(const Vector& f_) {
        f += f_;
    }

    void ApplyTorque(double τ_) {
        τ += τ_;
    }

    virtual void ApplyForceAt(const Vector& f_, const Vector& r_world) {
        ApplyForce(f_);
        Vector r = r_world - p;
        ApplyTorque(r.cross(f_));
    }

    virtual void Simulate(double dt, double t) {
        // Magically make simulation a bit more stable by decreasing speed
        // if acceleration is very high (high acceleration == stiff problem)
        double a_lim = 100;
        if (f.x / m > +a_lim) v.x *= 0.85;
        if (f.x / m < -a_lim) v.x *= 0.85;
        if (f.y / m > +a_lim) v.y *= 0.85;
        if (f.y / m < -a_lim) v.y *= 0.85;

        // Update states by integrating them
        // acc = force / m = dvelocity/dt, f(t, velocity) = force/m (a constant)
        v = Integrate(dt, f / m, v);
        // dposition/dt = velocity = f(t, position) (a constant as well)
        p = Integrate(dt, v, p);
        // dω/dt  = τ/J, f(t, ω) = τ/J (τ constant)
        ω = Integrate(dt, τ / J, ω);
        // dΘ/dt = ω, f(t, Θ) = ω (ω constant)
        θ = Integrate(dt, ω, θ);
    }

    friend std::ostream& operator<<(std::ostream& os, const Node& node) {
        os << "m = " << node.m << "\t"
           << "p = " << node.p << "\t"
           << "v = " << node.v << "\t"
           << "F = " << node.f << "\t"
           << "J = " << node.J << "\t"
           << "θ = " << node.θ << "\t"
           << "ω = " << node.ω << "\t"
           << "τ = " << node.τ;
        return os;
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        _shape.setPosition(p.x, p.y);
        target.draw(_shape, states);
    }
 
    
 protected:
    mutable sf::CircleShape _shape; // Shape variable for drawing

    template <typename T>
    T Integrate(double dt, const T& f, const T& x0) {
        // Based on Implicit Euler Method (?)
        // f(t, x) = dx/dt
        T x1 = x0 + dt * f;
        return x1;
    };
};

class LineConstrainedNode : public Node {
 public:
    explicit LineConstrainedNode(Vector b1_, Vector b2_) { 
        b1.x = b1_.x;
        b1.y = b1_.y;
        b2.x = b2_.x;
        b2.y = b2_.y;
        direction = b1-b2;
        direction = direction / direction.length();

        p.x = (b1.x + b2.x) / 2;
        p.y = (b1.y + b2.y) / 2;
    }
    
    virtual void Simulate(double dt, double t) override {
        // Limit forces to line direction
        f = f.dot(direction) * direction;

        if (b1.x > b2.x) {
            if (p.x > b1.x) {
                p.x = b1.x;
                if (f.x > 0) {
                    f.x = 0;
                    v.x = 0;
                }
            }
            if (p.x < b2.x) {
                p.x = b2.x;
                if (f.x < 0) {
                    f.x = 0;
                    v.x = 0;
                }
            }
        } else {
            if (p.x < b1.x) {
                p.x = b1.x;
                if (f.x < 0) { 
                    f.x = 0;
                    v.x = 0;
                }
            }
            if (p.x > b2.x) {
                p.x = b2.x;
                if (f.x > 0) {
                    f.x = 0;
                    v.x = 0;
                }
            }
        }
        if (b1.y > b2.y) {
            if (p.y > b1.y) {
                p.y = b1.y;
                if (f.y > 0) {
                    f.y = 0;
                    v.y = 0;
                }
            }
            if (p.y < b2.y) {
                p.y = b2.y;
                if (f.y < 0) {
                    f.y = 0;
                    v.y = 0;
                }
            }
        } else {
            if (p.y < b1.y) {
                p.y = b1.y;
                if (f.y < 0) {
                    f.y = 0;
                    v.y = 0;
                }
            }
            if (p.y > b2.y) {
                p.y = b2.y;
                if (f.y > 0) {
                    f.y = 0;
                    v.y = 0;
                }
            }
        }

        Node::Simulate(dt, t);
    }
    
    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        // Draw a line indicating the constraint
        sf::Vertex line[] = {
            sf::Vertex(sf::Vector2f(b1.x, b1.y), {100,100,100}),
            sf::Vertex(sf::Vector2f(b2.x, b2.y), {100,100,100})
        };
        target.draw(line, 2, sf::Lines);
        
        Node::draw(target, states);
    }

 private:
    Vector b1;
    Vector b2;
    Vector direction;
};

void DrawForce(sf::RenderTarget& target, Node node, Vector f) {
    double k = 0.2;
    sf::Vertex line[] = {
        sf::Vertex(sf::Vector2f(node.p.x, node.p.y)),
        sf::Vertex(sf::Vector2f(node.p.x + k*f.x, node.p.y + k*f.y), sf::Color::Red)
    };
    target.draw(line, 2, sf::Lines);
}

