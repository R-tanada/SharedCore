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

#ifndef __PROFILER__
#define __PROFILER__

#include "flow/avatarflow_config.h"
#include <string>
#include <utils/atypes.h>

namespace utils {

/**
 * @brief Helper class to do profiling on data blocks to measure execution time
 *
 */
class ProfilerImpl;
class AvaFlow_API Profiler {
private:
  /* data */
  ProfilerImpl *_impl;

public:
  Profiler(const std::string &name);
  ~Profiler();

  /**
   * @brief Call at the beginning of the block to measure
   *
   */
  void Start();

  /**
   * @brief Call at the end of the block
   *
   */
  uint Stop();

  bool IsStarted();

  const std::string &GetName();
  ullong GetMin();
  ullong GetMax();
  ullong GetAverage();
  ullong GetTotalTime();
  uint GetTotalCalls();
};

class ProfilerBlock {
protected:
  Profiler *_p;

public:
  ProfilerBlock(Profiler &p) : _p(&p) { _p->Start(); }
  ~ProfilerBlock() { _p->Stop(); }
};

} // namespace utils

#endif //__PROFILER__