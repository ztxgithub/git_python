cmake_minimum_required(VERSION 3.6)
project(test_python)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        main.cpp)
set(PYTHON_FILES
        main_test.py)

add_executable(test_python
                ${SOURCE_FILES}
                ${PYTHON_FILES})

target_link_libraries(test_python
                        ${PYTHON_LIBRARIES})