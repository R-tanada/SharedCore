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

#ifndef __UTILSCOMMONGUID__
#define __UTILSCOMMONGUID__

#include "GUID.h"
#include "avatarutils_config.h"

namespace utils {
class AvaUtils_API utilsCommonGUID {
public:
  static const utils::GUID SharedMemory;
  static const utils::GUID Media;
  static const utils::GUID Audio;
  static const utils::GUID Data;
  static const utils::GUID Video;
  static const utils::GUID Debug;
  static const utils::GUID SerialInterface;
  static const utils::GUID Thread;
  static const utils::GUID OS;
};
} // namespace utils

#endif //__UTILSCOMMONGUID__