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

#ifndef __BitrateMonitorELEMENT__
#define __BitrateMonitorELEMENT__

#include <string>

#include "flow/avatarflow_config.h"
#include "flow/media/GStreamer/GstMyListener.h"

namespace avatarflow {
namespace media {

class BitrateMonitorElementImpl;
class GstPipeline;
/**
 * @brief This class will interrupt a media pipeline so you can manipulate
 * an image frame when new buffers reaches it
 *
 */
class AvaFlow_API BitrateMonitorElement {
private:
  BitrateMonitorElementImpl *_impl;

public:
  BitrateMonitorElement(/* args */);
  virtual ~BitrateMonitorElement();

  std::string BuildPipeline(const std::string &prefix);

  virtual void LinkWithPipeline(GstPipeline *pipeline);

  GstMyListener *GetListener();

  unsigned int GetBitrate();
};

} // namespace media

} // namespace avatarflow

#endif //__BitrateMonitorELEMENT__