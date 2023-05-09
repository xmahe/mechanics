#include "Vector.hpp"
#include "Node.hpp"
#include <SFML/Graphics.hpp>
#include <iostream>
#include <math.h>
#pragma once

class Constraint : public sf::Drawable {
 public:
    virtual void Apply() = 0;
};

class Spring : public Constraint {
 public:
    explicit Spring(Node* a_, Node* b_) : a(a_), b(b_) { 
        l0 = (a->p - b->p).length();
    }

    double k = 500;  // [N/m]  stiffness
    double ζ = 10;    // [Ns/m] damping
    double l0;        // [m]    nominal length

    virtual void Apply() override {
        Vector n_hat = (a->p - b->p).normalise();  //       spring normal
        double l = (a->p - b->p).length();         // [m]   spring length
        double v = (a->v - b->v).dot(n_hat);       // [m/s] spring expansion speed
        double f = k * (l - l0) + ζ * v;           // [N]   spring force
        a->ApplyForce(n_hat * (-f));
        b->ApplyForce(n_hat * (+f));
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        sf::Vertex line[] = {
            sf::Vertex(sf::Vector2f(a->p.x, a->p.y), {0, 0, 255}),
            sf::Vertex(sf::Vector2f(b->p.x, b->p.y), {0, 0, 255})
        };
        target.draw(line, 2, sf::Lines);
    }

 private:
    Node* const a;
    Node* const b;
};

class Gravity : public Constraint {
 public:
    Gravity(Node* node_) : node(node_) { }

    virtual void Apply() override {
        static constexpr double g = 9.82;
        node->ApplyForce(Vector(0, node->m*g));
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        // Intentional no-op
    }

 private:
    Node* const node;
};

class Drag : public Constraint {
 public:
    double k = 10;  // [Ns²/m²]  resulting drag coefficient, f = k∙v²

    explicit Drag(Node* node_, double Δt_) : node(node_), Δt(Δt_) { }
    
    virtual void Apply() override {
        double v2 = node->v.dot(node->v);
        if (abs(v2) > 0.1) {
            Vector v_hat = node->v.normalise();
            Vector f = -k*v2*v_hat;
            node->ApplyForce(f);
        } else {
            node->v *= (1 - 0.01*Δt);
        }
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        // Intentional no-op
    }

 private:
    Node* const node;
    double Δt;
};
