
#include <Python.h>
#include <iostream>
#include <list>
#include <ctime>

#include "PYCaller.hpp"
#include "Position.hpp"

int main()
{
    //python function details
    const char* pyModule = "Tomatoe_Detection_Camera";    
    const char* function = "start";    
    
    //Python caller
    PyCaller caller;
    std::list<Position> tomatoPositions = caller.CallFunction(pyModule, function);

    for(auto pos : tomatoPositions)
    {
	std::cout << "PosX = " << pos.PosX << "  PosY = " << pos.PosY << std::endl; 
    }
    
    return 0;
}
