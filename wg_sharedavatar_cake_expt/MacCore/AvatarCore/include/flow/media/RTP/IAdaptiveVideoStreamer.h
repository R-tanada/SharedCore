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

#ifndef __IADAPTIVEVIDEOSTREAMER__
#define __IADAPTIVEVIDEOSTREAMER__

#include "flow/avatarflow_config.h"
#include <utils/GUID.h>
#include <utils/JSONUtils.h>

namespace avatarflow {
namespace media {
class QOSFeedback;

class IAdaptiveVideoStreamer {
private:
  /* data */
protected:
  bool _enabled;
  utils::GUID _type;

public:
  IAdaptiveVideoStreamer(const utils::GUID &t) : _enabled(false), _type(t) {}
  virtual ~IAdaptiveVideoStreamer() {}

  const utils::GUID &GetType() const { return _type; }

  virtual void SetEnabled(bool e) { _enabled = e; }
  bool IsEnabled() { return _enabled; }

  virtual bool OnQoS(const QOSFeedback &qos) = 0;

  virtual void Reset() = 0;
  virtual void Update(float dt) = 0;

  virtual float GetCurrQuality() = 0;
  virtual int GetBitrate() = 0;
  virtual int GetWidth(int currWidth) = 0;
  virtual int GetHeight(int currHeight) = 0;

  virtual bool Parse(const JSONObject &stream) {
    if (stream.contains("Enabled"))
      _enabled = utils::JSONUtils::GetBoolValue(stream["Enabled"], false);
    return true;
  }
};

} // namespace media
} // namespace avatarflow

#endif //__IADAPTIVEVIDEOSTREAMER__