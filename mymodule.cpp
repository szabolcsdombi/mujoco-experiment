#include <Python.h>
#include <mujoco.h>

float state[23 * 3];

mjModel * model;
mjData * data;

PyObject * meth_init(PyObject * self) {
    char errstr[256] = {};
    model = mj_loadXML("data/rope.xml", NULL, errstr, 256);
    if (!model) {
        PyErr_Format(PyExc_Exception, "%s", errstr);
        return NULL;
    }
    data = mj_makeData(model);
    if (!data) {
        PyErr_Format(PyExc_Exception, "cannot make data");
        return NULL;
    }
    Py_RETURN_NONE;
}

PyObject * meth_update(PyObject * self) {
    // printf("%d\n", model->nbody);
    for (int i = 0; i < 5; ++i) {
        mj_step(model, data);
    }
    float * ptr = state;
    for (int i = 0; i < model->nbody; ++i) {
        *ptr++ = data->xpos[i * 3 + 0];
        *ptr++ = data->xpos[i * 3 + 1];
        *ptr++ = data->xpos[i * 3 + 2];
    }
    Py_RETURN_NONE;
}

PyMethodDef module_methods[] = {
    {"init", (PyCFunction)meth_init, METH_NOARGS, NULL},
    {"update", (PyCFunction)meth_update, METH_NOARGS, NULL},
    {},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "mymodule", NULL, -1, module_methods};

extern "C" PyObject * PyInit_mymodule() {
    PyObject * module = PyModule_Create(&module_def);
    PyObject * mem = PyMemoryView_FromMemory((char *)state, sizeof(state), PyBUF_READ);
    PyModule_AddObject(module, "state", mem);
    return module;
}
