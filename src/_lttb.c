#include <Python.h>
#include "py_defines.h"
#include <math.h>


static PyObject* downsample(PyObject* self, PyObject *args);

static PyObject* downsample(PyObject* self, PyObject *args)
{

    PyObject* data;
    PyObject* dataSeq;
    long threshold;
    Py_ssize_t dataLen;
    PyObject* result; 


    Py_ssize_t avgRangeStart,avgRangeEnd,rangeOffs,rangeTo;
    Py_ssize_t a = 0;
    Py_ssize_t aNext=0;
    double   every;

    if (!PyArg_ParseTuple(args, "Ol", &data, &threshold)) {
        dataSeq = PySequence_Fast(data, "expected a sequence");
        Py_DECREF(dataSeq);
        return NULL;
    }


   dataLen = PySequence_Size(data);

    if(dataLen<=threshold || dataLen <=2){
        return data;
    }

    result = PyList_New(0);
    
    every = (dataLen - 2.0)/(threshold - 2.0);

    PyList_Append(result, PySequence_Fast_GET_ITEM(data, 0));

    for(Py_ssize_t i = 0; i<threshold-2; i++){
        PyObject* maxAreaPoint;
        double avgRangeLength, pointAX, pointAY;
        double avgX = 0.0;
        double avgY = 0.0;
        avgRangeStart = (Py_ssize_t) (floor((i+1.0)*every) + 1.0);
        avgRangeEnd = (Py_ssize_t) (floor((i+2.0)*every) + 1.0);
        if(avgRangeEnd > dataLen) avgRangeEnd = dataLen;
        avgRangeLength = avgRangeEnd - avgRangeStart;

        while (avgRangeStart < avgRangeEnd){
            avgX += PyFloat_AsDouble( PySequence_Fast_GET_ITEM(PySequence_Fast_GET_ITEM(data, avgRangeStart), 0));
            avgY += PyFloat_AsDouble(  PySequence_Fast_GET_ITEM(PySequence_Fast_GET_ITEM(data, avgRangeStart), 1));
            avgRangeStart++;
        }

        avgX = avgX / avgRangeLength;
        avgY = avgY / avgRangeLength;

        rangeOffs =(Py_ssize_t) (floor((i+0.0)*every) + 1.0);
        rangeTo = (Py_ssize_t) (floor((i+1.0)*every) + 1.0);

        pointAX =  PyFloat_AsDouble( PySequence_Fast_GET_ITEM(PySequence_Fast_GET_ITEM(data, a), 0));
        pointAY =  PyFloat_AsDouble( PySequence_Fast_GET_ITEM(PySequence_Fast_GET_ITEM(data, a), 1));

        double maxArea = -1.0;

        while(rangeOffs < rangeTo){
            double area = fabs(
                (pointAX - avgX) * (PyFloat_AsDouble( PySequence_Fast_GET_ITEM(PySequence_Fast_GET_ITEM(data, rangeOffs), 1)) - pointAY) -
                (avgY - pointAY) * (pointAX - PyFloat_AsDouble(  PySequence_Fast_GET_ITEM(PySequence_Fast_GET_ITEM(data, rangeOffs), 0)) )) * 0.5;


            if(area > maxArea){
                maxArea = area;
                maxAreaPoint =  PySequence_Fast_GET_ITEM(data, rangeOffs);
                aNext = rangeOffs;
            }

            rangeOffs++;

        }

        PyList_Append(result, maxAreaPoint);
        a = aNext;

    }
  PyList_Append(result, PySequence_Fast_GET_ITEM(data, dataLen - 1));
  
  return (PyObject*) result;
}

static char downsample_docs[] =
    "downsample( ): Any message you want to put here!!\n";

static PyMethodDef lttb_funcs[] = {
    {"downsample", (PyCFunction)downsample,
        METH_VARARGS, downsample_docs},
        { NULL, NULL, 0, NULL }
};


#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_lttb",
  0,              /* m_doc */
  -1,             /* m_size */
  lttb_funcs,   /* m_methods */
  NULL,           /* m_reload */
  NULL,           /* m_traverse */
  NULL,           /* m_clear */
  NULL            /* m_free */
};

#define PYMODINITFUNC       PyObject *PyInit__lttb(void)
#define PYMODULE_CREATE()   PyModule_Create(&moduledef)
#define MODINITERROR        return NULL

#else

#define PYMODINITFUNC       PyMODINIT_FUNC init_lttb(void)
#define PYMODULE_CREATE()   Py_InitModule("_lttb", lttb_funcs)
#define MODINITERROR        return

#endif

PYMODINITFUNC
{
    PyObject *module;
    
    module = PYMODULE_CREATE();
    
   if (module == NULL)
   {
       MODINITERROR;
    }
    
    #if PY_MAJOR_VERSION >= 3
        return module;
    #else
        Py_InitModule3("_lttb", lttb_funcs,
                       "ulttb downsampling C implementation");
    
    #endif
}
