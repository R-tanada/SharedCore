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

#ifndef __flowCommonGUID__
#define __flowCommonGUID__

#include "avatarflow_config.h"
#include <utils/GUID.h>

namespace avatarflow {
class AvaFlow_API flowCommonGUID {
public:
  static const utils::GUID Services;
  static const utils::GUID GstPipeline;
  static const utils::GUID ServiceLoader;
  static const utils::GUID AvatarFlow;
  static const utils::GUID ServiceCoordinator;
  static const utils::GUID ServiceLauncher;
  static const utils::GUID CoreAPI;
  static const utils::GUID Devices;
  static const utils::GUID SharedMemory;
  static const utils::GUID Media;
  static const utils::GUID Audio;
  static const utils::GUID Data;
  static const utils::GUID GStreamer;
  static const utils::GUID Resources;
  static const utils::GUID RTP;
  static const utils::GUID Video;
  static const utils::GUID Shader;
  static const utils::GUID Plugin;
  static const utils::GUID cloudSDK;
  static const utils::GUID Debug;
  static const utils::GUID ServicesWiFi;
  static const utils::GUID ServicesLTE;
  static const utils::GUID SerialInterface;
  static const utils::GUID Thread;
  static const utils::GUID OS;
  static const utils::GUID NAPI;
  static const utils::GUID Python;
  static const utils::GUID Unity3D;
};
} // namespace avatarflow

#endif //__flowCommonGUID__