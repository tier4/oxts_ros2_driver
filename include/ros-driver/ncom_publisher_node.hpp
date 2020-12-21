/**
 * \file ncom_publisher_node.hpp
 * Defines node to take NCom data and publish it in ROS messages.
 */

#ifndef NCOM_PUBLISHER_NODE_HPP
#define NCOM_PUBLISHER_NODE_HPP

#include <chrono>
#include <functional>
#include <memory>
#include <string>
#include <cmath>

// ROS includes
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"
#include "sensor_msgs/msg/imu.hpp"
// Boost includes
#include <boost/asio.hpp>

// gad-sdk includes
#include "nav/NComRxC.h"
#include "ros-driver/nav_const.hpp"
#include "ros-driver/ros_ncom_wrapper.hpp"


/* 
 * This class creates a subclass of Node designed to take NCom data from the 
 * NCom decoder and publish it to pre-configured ROS topics.
 */

class NComPublisherNode : public rclcpp::Node
{
public:
  NComPublisherNode()
  : Node("ncom_publisher"), count_(0)
  {
    // Initialise the publisher with the string message type, topic name 
    // "topic", and queue size limit
    pubString_    = this->create_publisher<std_msgs::msg::String>      ("ncom_pub/std_msgs/msg/string", 10); 
    pubOdometry_  = this->create_publisher<nav_msgs::msg::Odometry>    ("ncom_pub/nav_msgs/msg/odometry", 10); 
    pubNavSatFix_ = this->create_publisher<sensor_msgs::msg::NavSatFix>("ncom_pub/sensor_msgs/msg/nav_sat_fix", 10); 
    pubImu_       = this->create_publisher<sensor_msgs::msg::Imu>      ("ncom_pub/sensor_msgs/msg/imu", 10); 

  }
  int ncom_callback(const NComRxC* nrx);

private:

  /* 
   * @TODO: Config
   */
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr       pubString_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr     pubOdometry_;
  rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr pubNavSatFix_;
  rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr pubImu_;
  /* 
   * @TODO: Restructure with different publishers for different messages
   */
  int count_;
};






#endif //NCOM_PUBLISHER_NODE_HPP