#include <SFML/Graphics.hpp>

#include "Vector.hpp"
#include "Node.hpp"
#include "Constraints.hpp"
    
std::vector<Node*> nodes;
std::vector<Constraint*> constraints;

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Example");

    // Set up System
    Vector b1 = {300, 300};
    Vector b2 = {400, 400};
    LineConstrainedNode node(b1, b2);
    node.p.x = 350;
    node.p.y = 350;
    nodes.push_back(&node);
    Gravity gravity(&node);
    Drag drag(&node);
    constraints.push_back(&gravity);
    constraints.push_back(&drag);

    double time = 0;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) window.close();
        }

        for (auto node : nodes) node->Reset();
        
        for (auto constraint : constraints) constraint->Apply();
        
        node.Simulate(0.1, time);
        
        window.clear();
        window.draw(node);
        window.display();
    }

    return 0;
}
