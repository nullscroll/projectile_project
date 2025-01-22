# location of the Python header files
 
PYTHON_VERSION = 3.12
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
 
# location of the Boost Python include files and library
 
BOOST_INC = /usr/include
BOOST_LIB = /usr/lib
 
# compile mesh classes
TARGET = sim
 
$(TARGET).so: $(TARGET).o
	g++ -shared -std=c++11 -Wl,--export-dynamic $(TARGET).o -L$(BOOST_LIB) -lboost_python313 -L/usr/lib/python/config -lpython3 -o $(TARGET).so
 
$(TARGET).o: $(TARGET).C
	g++ -std=c++11 -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).C 
