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

#ifndef __NULLVIDEODEVICE__
#define __NULLVIDEODEVICE__

#include <utils/TypedProperty.h>
#include <utils/point2D.h>

#include "IVideoSinkDevice.h"

namespace avatarflow {
namespace media {

class NullVideoGrabber;

class AvaFlow_API NullVideoSinkDevice : public IVideoSinkDevice {
  DECLARE_RTTI;

private:
public:
public:
  NullVideoSinkDevice(/* args */);
  virtual ~NullVideoSinkDevice();
  virtual void Close();

  virtual std::string BuildPipeline(const std::string &name, bool sync);
};

MAKE_VIDEOSINKDEVICE_FACTORY(NullVideoSinkDevice, "null")

} // namespace media
} // namespace avatarflow

#endif //__NULLVIDEODEVICE__