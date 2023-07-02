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

#ifndef __PROFILERMANAGER__
#define __PROFILERMANAGER__

#include "flow/avatarflow_config.h"
#include <utils/ISingleton.h>

namespace utils {
class ProfilerManagerImpl;
class Profiler;

class AvaFlow_API ProfilerManager : public ISingleton<ProfilerManager> {
private:
  ProfilerManagerImpl *_impl;

public:
  ProfilerManager(/* args */);
  ~ProfilerManager();

  void PushProfiler(Profiler *p);
  void PopProfiler(Profiler *p);

  // to be called at the beginning of a frame to reset the profilers
  void Reset();

  void PrintStatistics();
};

#define gProfilerManager utils::ProfilerManager::getInstance()

} // namespace utils

#endif //__PROFILERMANAGER__