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

#ifndef __RESOURCEPLAYER__
#define __RESOURCEPLAYER__

#include "flow/avatarflow_config.h"
#include <string>

namespace avatarflow {
namespace media {

class ResourcePlayerImpl;

class AvaFlow_API ResourcePlayer {
private:
  ResourcePlayerImpl *_impl;

public:
  ResourcePlayer(/* args */);
  ~ResourcePlayer();

  void Start(const std::string &recordingPath);
  void Stop();
};

} // namespace media
} // namespace avatarflow

#endif //__RESOURCEPLAYER__