#ifndef PYCALLER_HPP
#define PYCALLER_HPP

#include <Python.h>
#include <iostream>
#include <list>

#include "PYListConverter.hpp"
#include "Position.hpp"

class PyCaller
{
private:

    // Position list
    std::list<Position> PosList;

    void Call_python_function(const char* pyModule, const char* function)
    {
	Py_Initialize();  // Initialize the Python interpreter

	// Set the path to the script (current directory in this case)
	PyObject* sysPath = PySys_GetObject("path");

	PyObject* path = PyUnicode_FromString(".");

	PyList_Append(sysPath, path);
	Py_DECREF(path);


	PyObject* pName = PyUnicode_DecodeFSDefault(pyModule);  // Name of the Python module
	PyObject* pModule = PyImport_Import(pName);
	Py_XDECREF(pName);

	if (pModule != nullptr) 
	{
	    PyObject* pFunc = PyObject_GetAttrString(pModule, function);

	    if (pFunc && PyCallable_Check(pFunc)) 
	    {
		PyObject* pValue = PyObject_CallObject(pFunc, nullptr);

		if (pValue != nullptr) 
		{
		    //converting pyObject to cpp position class
		    PosList = ListConverter::convertPyListToStdListPosition(pValue);

		    Py_XDECREF(pValue);
		} 
		else 
		{
		    PyErr_Print();
		    std::cerr << "Python function call failed" << std::endl;
		}
	    } 
	    else 
	    {
		PyErr_Print();
		std::cerr << "Cannot find function 'get_list'" << std::endl;
	    }

	    Py_XDECREF(pFunc);
	    Py_XDECREF(pModule);
	} 
	else 
	{
	    PyErr_Print();
	    std::cerr << "Failed to load module 'my_module'" << std::endl;
	}

	Py_Finalize();  // Finalize the Python interpreter

    }

public:

    std::list<Position> CallFunction(const char*  pyModule, const char* function)
    {
	Call_python_function(pyModule, function);

	return PosList;
    }
 
};

#endif //PYCALLER_HPP
