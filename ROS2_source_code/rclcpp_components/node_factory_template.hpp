// Copyright 2019 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef RCLCPP_COMPONENTS__NODE_FACTORY_TEMPLATE_HPP__
#define RCLCPP_COMPONENTS__NODE_FACTORY_TEMPLATE_HPP__

#include <chrono>
#include <functional>
#include <iostream>
#include <memory>

#include "rclcpp_components/node_factory.hpp"

namespace rclcpp_components
{

/// NodeFactoryTemplate is a convenience class for instantiating components.
/**
 * The NodeFactoryTemplate class can be used to provide the NodeFactory interface for
 * components that implement a single-argument constructor and `get_node_base_interface`.
 */
template<typename NodeT>
class NodeFactoryTemplate : public NodeFactory
{
public:
  NodeFactoryTemplate() = default;
  virtual ~NodeFactoryTemplate() = default;

  /// Create an instance of a component
  /**
   * \param[in] options Additional options used in the construction of the component.
   */
  NodeInstanceWrapper
  create_node_instance(const rclcpp::NodeOptions & options) override
  {
    auto node = std::make_shared<NodeT>(options);
auto now = std::chrono::system_clock::now();
auto time = std::chrono::system_clock::to_time_t(now);
auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(now.time_since_epoch()) -
          std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch());
          try
          {
            std::cout << "[TUM launched node cpp local UPDATE'" << node->get_name() << "'] " << std::put_time(std::localtime(&time), "%H:%M:%S.") << ns.count() << std::endl;
          }
          catch(const std::exception& e)
          {
            std::cout<<"node->getName() is missing"<<std::endl;
          }
          


    return NodeInstanceWrapper(
      node, std::bind(&NodeT::get_node_base_interface, node));
  }
};
}  // namespace rclcpp_components

#endif  // RCLCPP_COMPONENTS__NODE_FACTORY_TEMPLATE_HPP__
