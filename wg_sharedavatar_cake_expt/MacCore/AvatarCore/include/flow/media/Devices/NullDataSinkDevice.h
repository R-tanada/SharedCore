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

#ifndef __NULLDATADEVICE__
#define __NULLDATADEVICE__

#include <utils/TypedProperty.h>
#include <utils/point2D.h>

#include "IDataSinkDevice.h"

namespace avatarflow {
namespace media {

class NullDataGrabber;

class AvaFlow_API NullDataSinkDevice : public IDataSinkDevice {
  DECLARE_RTTI;

private:
public:
public:
  NullDataSinkDevice(/* args */);
  virtual ~NullDataSinkDevice();
  virtual void Close();

  virtual std::string BuildPipeline(const std::string &name, bool sync);
};

MAKE_DATASINKDEVICE_FACTORY(NullDataSinkDevice, "null")

} // namespace media
} // namespace avatarflow

#endif //__NULLDATADEVICE__