cmake_minimum_required(VERSION 3.10)
project(ChadeoMediaWorker)

# 1. Use C++17 (standard for modern SDE roles)
set(CMAKE_CXX_STANDARD 17)

# 2. Find gRPC and Protobuf (vcpkg handles the paths!)
find_package(gRPC CONFIG REQUIRED)
find_package(Protobuf CONFIG REQUIRED)

# 3. Tell CMake where your generated headers are
include_directories(rpc_gen)

# 4. Define the executable and its source files
add_executable(media_worker 
    main.cpp 
    rpc_gen/signaling.pb.cc 
    rpc_gen/signaling.grpc.pb.cc
)

# 5. Updated "Link" section for vcpkg gRPC
target_link_libraries(media_worker PRIVATE 
    gRPC::grpc++ 
    gRPC::grpc 
    gRPC::gpr 
    protobuf::libprotobuf
)