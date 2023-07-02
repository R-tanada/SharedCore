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

#ifndef __RESOURCERECORDERCOMMON__
#define __RESOURCERECORDERCOMMON__

#include "CoreResource.h"
#include <utils/atypes.h>

namespace avatarflow {
namespace media {

class ResourceFrameIndexHeader {
public:
  media::CoreResourceType type;
  utils::ullong timestamp;
  utils::ullong dataOffset;
  utils::ullong dataSize;
  char resourceName[64];
  char channelName[64];
};

template <class T> class ResourceDataObject {
public:
  ResourceDataObject() : object(0) {}
  T *object;
  utils::ullong timestamp;
  std::string resource;
  std::string channel;
};
} // namespace media
} // namespace avatarflow

#endif //__RESOURCERECORDERCOMMON__