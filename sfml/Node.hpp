#include "Vector.hpp"
#include <SFML/Graphics.hpp>
#include <iostream>
#pragma once

class Node : public sf::Drawable {
 public:
    double mass = 1;
    Vector p = {0, 0};
    Vector v = {0, 0};
    Vector f = {0, 0};
    double J = 1;
    double θ = 0;
    double ω = 0;
    double τ = 0;

    static constexpr double r = 5;

    explicit Node() {
        _shape.setRadius(r);
        _shape.setFillColor(sf::Color::Red);
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
        auto Integrate1 = [](double dt, const Vector& f, const Vector& x0) {
            // Based on Implicit Euler Method (?)
            // f(t, x) = dx/dt
            Vector x1 = x0 + dt * f;
            return x1;
        };
        
        auto Integrate2 = [](double dt, const double& f, const double& x0) {
            // Based on Implicit Euler Method (?)
            // f(t, x) = dx/dt
            double x1 = x0 + dt * f;
            return x1;
        };

        // Magically make simulation a bit more stable by decreasing speed
        // if acceleration is very high (high acceleration == stiff problem)
        double a_lim = 100;
        if (f.x / mass > +a_lim) v.x *= 0.85;
        if (f.x / mass < -a_lim) v.x *= 0.85;
        if (f.y / mass > +a_lim) v.y *= 0.85;
        if (f.y / mass < -a_lim) v.y *= 0.85;

        // Update states by integrating them
        // acc = force / mass = dvelocity/dt, f(t, velocity) = force/mass (a constant)
        v = Integrate(dt, f / mass, v);
        // dposition/dt = velocity = f(t, position) (a constant as well)
        p = Integrate(dt, v, p);
        // dω/dt  = τ/J, f(t, ω) = τ/J (τ constant)
        ω = Integrate2(dt, τ / J, ω);
        // dΘ/dt = ω, f(t, Θ) = ω (ω constant)
        θ = Integrate2(dt, ω, θ);
    }

    friend std::ostream& operator<<(std::ostream& os, const Node& node) {
        os << "m = " << node.mass << "\t"
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
        // states.transform *= getTransform();
        target.draw(_shape, states);
        
        // Draw a line indicating the force
        sf::Vertex line[] = {
            sf::Vertex(sf::Vector2f(p.x, p.y)),
            sf::Vertex(sf::Vector2f(p.x + f.x, p.y + f.y), sf::Color::Red)
        };
        target.draw(line, 2, sf::Lines);
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
    }
    
    virtual void Simulate(double dt, double t) override {
        f = f.dot(direction) * direction;
        if (b1.x > b2.x) {
            if (p.x > b1.x and f.x > 0) { f.x = 0; v.x = 0; p.x = b1.x; log(1);}
            if (p.x < b2.x and f.x < 0) { f.x = 0; v.x = 0; p.x = b2.x; log(2);}
        } else {
            if (p.x < b1.x and f.x < 0) { f.x = 0; v.x = 0; p.x = b1.x; log(3);}
            if (p.x > b2.x and f.x > 0) { f.x = 0; v.x = 0; p.x = b2.x; log(4);}
        }
        if (b1.y > b2.y) {
            if (p.y > b1.y and f.y > 0) { f.y = 0; v.y = 0; p.y = b1.y; log(5);}
            if (p.y < b2.y and f.y < 0) { f.y = 0; v.y = 0; p.y = b2.y; log(6);}
        } else {
            if (p.y < b1.y and f.y < 0) { f.y = 0; v.y = 0; p.y = b1.y; log(7);}
            if (p.y > b2.y and f.y > 0) { f.y = 0; v.y = 0; p.y = b2.y; log(8);}
        }

        std::cout << "p.x = " << p.x << std::endl;

        // Magically make simulation a bit more stable by decreasing speed
        // if acceleration is very high (high acceleration == stiff problem)
        double a_lim = 100;
        if (f.x / mass > +a_lim) v.x *= 0.85;
        if (f.x / mass < -a_lim) v.x *= 0.85;
        if (f.y / mass > +a_lim) v.y *= 0.85;
        if (f.y / mass < -a_lim) v.y *= 0.85;

        // Update states by integrating them
        // acc = force / mass = dvelocity/dt, f(t, velocity) = force/mass (a constant)
        v = Integrate(dt, f / mass, v);
        // dposition/dt = velocity = f(t, position) (a constant as well)
        p = Integrate(dt, v, p);
        // dω/dt  = τ/J, f(t, ω) = τ/J (τ constant)
        ω = Integrate(dt, τ / J, ω);
        // dΘ/dt = ω, f(t, Θ) = ω (ω constant)
        θ = Integrate(dt, ω, θ);
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

void log(int x) {std::cout << "cond " << x << std::endl;}
