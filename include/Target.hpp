#pragma once

#include <math.h>
#include <string>
#include <SFML/Graphics.hpp>
#include "Node.hpp"
#include "Vector.hpp"


class Target : public sf::Drawable {
 public:
    Vector p = {0, 0};

    Target() : Target(Vector(0, 0), nullptr) { }

    Target(Vector p_, Node* node) : p(p_), _node(node) {
        _shape1.setRadius(r1);
        _shape1.setFillColor(sf::Color::Red);
        _shape1.setOrigin(r1, r1);
        _shape2.setRadius(r2);
        _shape2.setFillColor(sf::Color::White);
        _shape2.setOrigin(r2, r2);
        _shape3.setRadius(r3);
        _shape3.setFillColor(sf::Color::Red);
        _shape3.setOrigin(r3, r3);
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        _shape1.setPosition(p.x, p.y);
        _shape2.setPosition(p.x, p.y);
        _shape3.setPosition(p.x, p.y);
        target.draw(_shape3, states);
        target.draw(_shape2, states);
        target.draw(_shape1, states);
    }
    
    void Update(double Δt, double t) {
        double l = (_node->p - p).length();
        if (l < r1) {
            score += 1;
        } else if (l < r2) {
            score += 0.5;
        } else if (l < r3) {
            score += 0.25;
        }

        if (θ >  3*2*π and θ <  5*2*π) p.x += 0.1*Δt*sin(θ);
        if (θ >  7*2*π and θ <  9*2*π) p.x += 0.2*Δt*sin(θ);
        if (θ > 11*2*π and θ < 12*2*π) p.x -= 0.1*Δt;
        if (θ > 12*2*π and θ < 12.75*2*π) p.x += 0.1*Δt;
        if (θ > 14*2*π and θ < 17.2*2*π) p.y -= 0.1*Δt;
        if (θ > 22*2*π and θ < 26*2*π) p.x += 0.1*Δt*sin(θ);
        if (θ > 26*2*π) p.y -= 0.1;
        θ += 10*Δt/2/π;
    }

    std::string GetScoreString() const {
        return "Score = " + std::to_string(score);
    }

 private:
    double score = 0;
    static constexpr double r1 = 0.01;
    static constexpr double r2 = 0.02;
    static constexpr double r3 = 0.03;
    mutable sf::CircleShape _shape1; // Shape variable for drawing
    mutable sf::CircleShape _shape2; // Shape variable for drawing
    mutable sf::CircleShape _shape3; // Shape variable for drawing
    Node* const _node;
    double θ = 3.14/2;
    static constexpr double π = 3.141;
};
