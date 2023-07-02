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

#ifndef __NULLAUDIODEVICE__
#define __NULLAUDIODEVICE__

#include <utils/TypedProperty.h>
#include <utils/point2D.h>

#include "IAudioSinkDevice.h"

namespace avatarflow {
namespace media {

class NullAudioGrabber;

class AvaFlow_API NullAudioSinkDevice : public IAudioSinkDevice {
  DECLARE_RTTI;

private:
public:
public:
  NullAudioSinkDevice(/* args */);
  virtual ~NullAudioSinkDevice();
  virtual void Close();

  virtual std::string BuildPipeline(const std::string &name, bool sync);
};

MAKE_AUDIOSINKDEVICE_FACTORY(NullAudioSinkDevice, "null")

} // namespace media
} // namespace avatarflow

#endif //__NULLAUDIODEVICE__