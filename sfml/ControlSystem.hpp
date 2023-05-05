#pragma once

#include "Vector.hpp"
#include <iostream>

class ControlSystem {
 public:
    double Update(Node a, Node b) {
        double error = b.p.x - _r.x;
        const double kaP = 10;
        const double kbD = 2;
        const double kv  = -3;
        double v_rel_error = b.v.x - a.v.x;
        return -kaP * error - kbD * b.v.x - kv*v_rel_error;
    }

    void SetReference(Vector r) {
        _r = r;
    }

 private:
    Vector _r = {0.1, 0};  // reference position
};

