#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <thread>
#include <chrono>
#include <vector>
#include <curl/curl.h>  // Include libcurl for HTTP requests

using namespace std;

struct CPUStats {
    long user, nice, system, idle, iowait, irq, softirq, steal;
};

CPUStats getCpuStats() {
    ifstream file("/proc/stat");
    string line;
    CPUStats stats = { 0 };

    if (getline(file, line)) {
        istringstream iss(line);
        string cpu;
        iss >> cpu >> stats.user >> stats.nice >> stats.system >> stats.idle
            >> stats.iowait >> stats.irq >> stats.softirq >> stats.steal;
    }
    return stats;
}

double calculateCpuUsage(CPUStats prev, CPUStats curr) {
    long prevIdle = prev.idle + prev.iowait;
    long currIdle = curr.idle + curr.iowait;
    long prevTotal = prev.user + prev.nice + prev.system + prevIdle +
        prev.irq + prev.softirq + prev.steal;
    long currTotal = curr.user + curr.nice + curr.system + currIdle +
        curr.irq + curr.softirq + curr.steal;

    double totalDiff = currTotal - prevTotal;
    double idleDiff = currIdle - prevIdle;

    return 100.0 * (1.0 - (idleDiff / totalDiff));
}

long getMemoryUsage() {
    ifstream file("/proc/meminfo");
    string line;
    long totalMem = 0, availableMem = 0;

    while (getline(file, line)) {
        istringstream iss(line);
        string key;
        long value;
        string unit;
        iss >> key >> value >> unit;

        if (key == "MemTotal:")
            totalMem = value;
        else if (key == "MemAvailable:")
            availableMem = value;
    }
    return totalMem - availableMem;
}

long getTotalMemory() {
    ifstream file("/proc/meminfo");
    string line;
    long totalMem = 0;

    while (getline(file, line)) {
        istringstream iss(line);
        string key;
        long value;
        string unit;
        iss >> key >> value >> unit;

        if (key == "MemTotal:")
            totalMem = value;
    }
    return totalMem;
}

void sendDataToBackend(double cpuUsage, long usedMemory, long totalMemory) {
    CURL* curl;
    CURLcode res;
    curl = curl_easy_init();

    if (curl) {
        string jsonPayload = "{ \"cpu_usage\": " + to_string(cpuUsage) +
            ", \"memory_used\": " + to_string(usedMemory / 1024) +
            ", \"memory_total\": " + to_string(totalMemory / 1024) + " }";

        curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:8000/monitor/"); // Change to your backend URL
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonPayload.c_str());

        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            cerr << "Failed to send data: " << curl_easy_strerror(res) << endl;
        }

        curl_easy_cleanup(curl);
    }
}

int main() {
    CPUStats prevCpuStats = getCpuStats();
    this_thread::sleep_for(chrono::seconds(1));

    while (true) {
        CPUStats currCpuStats = getCpuStats();
        double cpuUsage = calculateCpuUsage(prevCpuStats, currCpuStats);
        prevCpuStats = currCpuStats;

        long usedMemory = getMemoryUsage();
        long totalMemory = getTotalMemory();

        sendDataToBackend(cpuUsage, usedMemory, totalMemory);

        this_thread::sleep_for(chrono::seconds(5));  // Send data every 5 seconds
    }

    return 0;
}