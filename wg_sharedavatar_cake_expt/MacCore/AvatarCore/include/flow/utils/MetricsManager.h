/************************************************************************
 *                                                                      *
 * Copyright 2020 AvatarIn Inc. Tokyo, Japan. All Rights Reserved       *
 *                                                                      *
 *       _____               __               .___                      *
 *      /  _  \___  ______ _/  |______ _______|   | ____                *
 *     /  /_\  \  \/ |__  \\   __\__  \\_  __ \   |/    \               *
 *    /    |    \   / / __ \|  |  / __ \|  | \/   |   |  \              *
 *    \____|__  /\_/ (____  /__| (____  /__|  |___|___|  /              *
 *            \/          \/          \/               \/               *
 *                                                                      *
 * Developed by: Yamen Saraiji                                          *
 ************************************************************************/

#ifndef __METRICSMANAGER__
#define __METRICSMANAGER__

#include "flow/avatarflow_config.h"
#include <unordered_map>
#include <utils/ISingleton.h>
#include <vector>

namespace utils {

class MetricsManagerImpl;
class AvaFlow_API MetricsManager : public ISingleton<MetricsManager> {
private:
  /* data */
  MetricsManagerImpl *_impl;

public:
  MetricsManager(/* args */);
  ~MetricsManager();

  void AddMetric(const std::string &source, const std::string &name,
                 const std::string &value);

  std::string GetMetric(const std::string &source, const std::string &name,
                        const std::string &defaultValue);
  std::unordered_map<std::string, std::string>
  GetMetrics(const std::string &source);

  std::vector<std::string> GetSources();

  bool IsMetricExist(const std::string &source, const std::string &name);

  void RemoveMetric(const std::string &source, const std::string &name);
  void RemoveMetrics(const std::string &source);

  void CleanMetrics();

  void PrintMetrics();
};

#define gMetricsManager utils::MetricsManager::getInstance()

} // namespace utils

#endif //__METRICSMANAGER__