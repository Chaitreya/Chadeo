#include <opencv2/opencv.hpp>
#include <grpcpp/grpcpp.h>
#include <thread>
#include <atomic>
#include "./rpc_gen/signaling.grpc.pb.h"

// ADD THESE LINES HERE:
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using signaling::MediaSignaling;
using signaling::CallRequest;
using signaling::CallResponse;

using namespace signaling;

class MediaSignalingImpl final : public MediaSignaling::Service {
    std::atomic<bool> keep_running{false};
    std::thread video_thread;

    // The actual Webcam Loop
    void run_webcam() {
        cv::VideoCapture cap(0);
        cv::Mat frame;
        if (!cap.isOpened()) return;

        while (keep_running) {
            cap >> frame;
            if (frame.empty()) break;
            cv::imshow("Chadeo Video Call", frame);
            if (cv::waitKey(30) >= 0) break; 
        }
        cap.release();
        cv::destroyAllWindows();
    }

    // Triggered by "Video Call" button
    grpc::Status InitiateCall(grpc::ServerContext* context, const CallRequest* request, CallResponse* reply) override {
        if (!keep_running) {
            keep_running = true;
            // Launch webcam in a background thread
            video_thread = std::thread(&MediaSignalingImpl::run_webcam, this);
            std::cout << "Webcam Started for: " << request->user_id() << std::endl;
        }
        reply->set_success(true);
        return grpc::Status::OK;
    }

    // Triggered by "End Call" button (You'll need this in your .proto)
    grpc::Status EndCall(grpc::ServerContext* context, const CallRequest* request, CallResponse* reply) override {
        std::cout << "End Call Received. Closing Camera..." << std::endl;
        keep_running = false;
        if (video_thread.joinable()) {
            video_thread.join(); // Wait for the camera thread to finish cleanly
        }
        reply->set_success(true);
        return grpc::Status::OK;
    }
};

// 2. Server Runner
void RunServer() {
    std::string server_address("0.0.0.0:50051");
    MediaSignalingImpl service;

    ServerBuilder builder;
    // Listen on port 50051 without SSL (Insecure) for local development
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "🚀 [C++] Media Worker is LIVE at " << server_address << std::endl;

    // This keeps the program running so it doesn't immediately close
    server->Wait();
}

int main(int argc, char** argv) {
    RunServer();
    return 0;
}