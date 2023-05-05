#include <SFML/Graphics.hpp>

#include "Vector.hpp"
#include "Node.hpp"



int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Example");

    Vector b1 = {300, 300};
    Vector b2 = {400, 400};

    LineConstrainedNode node(b1, b2);
    node.p.x = 350;
    node.p.y = 350;

    double time = 0;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) window.close();
        }

        node.Reset();
        node.ApplyForce({0.01,0});
        node.Simulate(0.1, time);
        window.clear();
        window.draw(node);
        window.display();
    }

    return 0;
}
