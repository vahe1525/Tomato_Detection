#ifndef PYLISTCONVERTER_HPP
#define PYLISTCONVERTER_HPP

#include <Python.h>
#include <iostream>
#include <list>

#include "Position.hpp"


// This class converts python list to cpp std::list
class ListConverter
{
public:

    static std::list<Position> convertPyListToStdListPosition(PyObject* pyList) 
    {
	std::list<Position> cppList;

	if (PyList_Check(pyList)) 
	{
	    Py_ssize_t size = PyList_Size(pyList);
	    for (Py_ssize_t i = 0; i < size; ++i) 
	    {
		PyObject* item = PyList_GetItem(pyList, i);

		if (PyObject_HasAttrString(item, "PosX") && PyObject_HasAttrString(item, "PosY")) 
		{
		    PyObject* pyPosX = PyObject_GetAttrString(item, "PosX");
		    PyObject* pyPosY = PyObject_GetAttrString(item, "PosY");


		    if (PyLong_Check(pyPosX) && PyLong_Check(pyPosY)) 
		    {
			long posX = PyLong_AsLong(pyPosX);
			long posY = PyLong_AsLong(pyPosY);

			Position pos;
			pos.PosX = static_cast<unsigned int>(posX);
			pos.PosY = static_cast<unsigned int>(posY);
			cppList.push_back(pos);
		    } 
		    else 
		    {
			std::cerr << "Position attributes are not integers." << std::endl;
		    }

		    Py_DECREF(pyPosX);
		    Py_DECREF(pyPosY);
		} 
		else 
		{
		    std::cerr << "Item in list does not have 'PosX' and 'PosY' attributes." << std::endl;
		}
	    }
	} 
	else 
	{
	    std::cerr << "Provided object is not a Python list." << std::endl;
	}

	return cppList;
    }	

};

#endif //PYLISTCONVERTER_HPP
