#include <SFML/Graphics.hpp>

#include "Constraints.hpp"
#include "ControlSystem.hpp"
#include "Node.hpp"
#include "Text.hpp"
#include "Vector.hpp"
    
static std::vector<Node*> nodes;
static std::vector<Constraint*> constraints;

constexpr double fps = 100;
constexpr double Δt = 1/fps;

ControlSystem control_system;

class Target : public sf::Drawable {
 public:
    Vector p = {0, 0};

    Target() : Target(Vector(0, 0)) { }
    
    Target(Vector p_) : p(p_) {
        _shape.setRadius(r);
        _shape.setFillColor(sf::Color::Green);
        _shape.setOrigin(r, r);
    }

    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        _shape.setPosition(p.x, p.y);
        target.draw(_shape, states);
    }
 private:
    static constexpr double r = 0.03;
    mutable sf::CircleShape _shape; // Shape variable for drawing
};


int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Magnus Mechanical Solver");
    window.setFramerateLimit(fps);
    sf::View view;
    view.setSize(2.0f, 2.0f);
    view.setCenter(0.0f, 0.0f);

    Text time_text;
    Text position_text;
    time_text.p = {-0.8, -0.8};
    position_text.p = {-0.8, -0.7};

    Target target({0.1, 0.3});

    {
       // Add node which can only move on a line between two points, 
       //          which is also affected by drag and gravity
        auto node1 = new LineConstrainedNode({-0.3, -0.3}, {0.3, -0.3});
        auto gravity1 = new Gravity(node1);
        auto drag1 = new Drag(node1, Δt);
        nodes.push_back(node1);
        constraints.push_back(gravity1);
        constraints.push_back(drag1);
        
        // Add another node which is also affected by gravity and drag 
        //                  which is also linked to the first node with a spring
        auto node2 = new Node({0, 0.3});
        auto gravity2 = new Gravity(node2);
        auto drag2 = new Drag(node2, Δt);
        auto spring = new Spring(node1, node2);
        nodes.push_back(node2);
        constraints.push_back(gravity2);
        constraints.push_back(drag2);
        constraints.push_back(spring);
    }

    double t = -2;
    while (window.isOpen()) {
        // Handle events
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) window.close();
        }

        t += Δt;
        time_text.Set("t = " + std::to_string(t));
        position_text.Set("p.x = " + std::to_string(nodes[1]->p.x));

        // Reset all nodes and apply forces from constraints
        for (auto node : nodes)
            node->Reset();
        for (auto constraint : constraints)
            constraint->Apply();
        
        // Apply forces from control system
        double force = 0;
        if (t > 0) {
            force = control_system.Update(*nodes[0], *nodes[1]);
            if (force > +5) force = +5;
            if (force < -5) force = -5;

            nodes[0]->ApplyForce(Vector(force, 0));
        }

        // Simulate system
        for (auto node : nodes)
            node->Simulate(Δt, t);
        
        // Draw everything
        window.clear();
        window.draw(target);
        window.setView(view);
        for (auto node : nodes)
            window.draw(*node);
        for (auto constraint : constraints)
            window.draw(*constraint);
        window.draw(time_text);
        window.draw(position_text);
        DrawForce(window, *nodes[0], Vector(force, 0));


        window.display();
    }

    return 0;
}
