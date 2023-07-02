

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

#ifndef __AVATARFLOW__
#define __AVATARFLOW__

#include "flow/avatarflow_config.h"
#include "utils/BlackboardSharedMemory.h"
#include "utils/ISingleton.h"

namespace avatarflow {
namespace engine {

class AvatarFlowImpl;

class AvaFlow_API AvatarFlow : public utils::ISingleton<AvatarFlow> {
private:
  AvatarFlowImpl *_impl;

public:
  AvatarFlow(const std::string &name = "", const std::string &appPath = "",
             const std::string &logPath = ".");
  ~AvatarFlow();

  bool Initialize(bool master, int coordPort = 40933,
                  bool multithreaded = true);
  void Process();
  void Shutdown();

  utils::BlackboardSharedMemory *GetBlackboard();

  const std::string &GetLogPath();
};
#define gAvatarflow avatarflow::engine::AvatarFlow::getInstance()

} // namespace engine
} // namespace avatarflow

#endif //__AVATARFLOW__