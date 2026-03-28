cmake_minimum_required(VERSION 3.10)
project(ChadeoMediaWorker)

set(CMAKE_CXX_STANDARD 17)

# 1. Find gRPC and Protobuf
find_package(gRPC CONFIG REQUIRED)
find_package(Protobuf CONFIG REQUIRED)

# 2. NEW: Find OpenCV (Specify modules to keep it lightweight)
set(OpenCV_DIR "C:/opencv/build/x64/vc16/lib")
find_package(OpenCV REQUIRED)

# 3. NEW: Find Threading support
find_package(Threads REQUIRED)

include_directories(rpc_gen)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(media_worker 
    main.cpp 
    rpc_gen/signaling.pb.cc 
    rpc_gen/signaling.grpc.pb.cc
)

# 4. Updated Link section
target_link_libraries(media_worker PRIVATE 
    gRPC::grpc++ 
    gRPC::grpc 
    gRPC::gpr 
    protobuf::libprotobuf
    ${OpenCV_LIBS}               # Link OpenCV
    Threads::Threads             # Link Threading
)