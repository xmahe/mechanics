#pragma once

#include <string>
#include "Vector.hpp"

class Text : public sf::Drawable {
 public:
    Vector p = {0, 0};
    Text() {
        font.loadFromFile("../resources/Inconsolata-Medium.ttf");
        text.setFont(font);
        text.setString("text");
        text.setCharacterSize(24);
        text.setFillColor(sf::Color::White);
        text.setScale(0.002, 0.002);
    }

    void Set(std::string str) {
        text.setString(str);
    }
    
    void draw(sf::RenderTarget& target, sf::RenderStates states) const override {
        text.setPosition(p.x, p.y);
        target.draw(text, states);
    }

 private:
    mutable sf::Text text;
    sf::Font font;
};

