#include "Vector.hpp"
#include "Node.hpp"
#include <SFML/Graphics.hpp>
#include <iostream>
#pragma once

class Constraint : public sf::Drawable {
 public:
    virtual void Apply() = 0;
};

class Spring : public Constraint {
 public:
    explicit Spring(Node* a_, Node* b_) : a(a_), b(b_) { }
    double k = 1000;  // [N/m]  stiffness
    double ζ = 30;    // [Ns/m] damping
    double l0 = 1;    // [m]    nominal length

    virtual void Apply() {
        Vector n_hat = (a->p - b->p).normalise();  //       spring normal
        double l = (a->p - b->p).length();         // [m]   spring length
        double v = (a->v - b->v).dot(n_hat);       // [m/s] spring expansion speed
        double f = k * (l - l0) + ζ * v;           // [N]   spring force
        a->ApplyForce(n_hat * (-f));
        b->ApplyForce(n_hat * (+f));
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        // Intentional no-op
    }

 private:
    Node* const a;
    Node* const b;
};

class Gravity : public Constraint {
 public:
    Gravity(Node* node_) : node(node_) { }

    virtual void Apply() {
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
    double k = 0.1;  // [Ns²/m²]  resulting drag coefficient, f = k∙v²

    Drag(Node* node_) : node(node_) { }
    
    virtual void Apply() {
        double v2 = node->v.dot(node->v);
        if (v2 < 0.1)
            return;
        Vector v_hat = node->v.normalise();
        Vector f = -k*v2*v_hat;
        node->ApplyForce(f);
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        // Intentional no-op
    }

 private:
    Node* const node;
};
